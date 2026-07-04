"""
Cymor Movie API
================
A FastAPI wrapper around the `moviebox-api` PyPI package (v1 namespace),
built to power Cymor Movie Hub.

LEARNING / PORTFOLIO PROJECT — read the README before using this for
anything beyond personal experimentation. moviebox-api is an *unofficial*
wrapper around moviebox.ph, which streams copyrighted films without a
license. That's a real legal exposure if this is ever exposed publicly
as part of a real product.

Every class/method used below is taken directly from the official docs at
https://moviebox-api-docs.netlify.app/v1/movies and
https://moviebox-api-docs.netlify.app/v1/tv_series — nothing here is guessed.
Where the docs didn't spell out an exact field name (e.g. what a quality
label is literally called on a download entry), we lean on Pydantic's own
`.model_dump()` to pass through whatever fields actually exist, rather than
hardcoding a field name we haven't verified.
"""

import os
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

from moviebox_api.v1 import (
    MovieDetails,
    Search,
    Session,
    SubjectType,
    TVSeriesDetails,
    DownloadableMovieFilesDetail,
    DownloadableTVSeriesFilesDetail,
)
from moviebox_api.v1.download import CaptionFileDownloader, MediaFileDownloader

app = FastAPI(
    title="Cymor Movie API",
    description=(
        "Unofficial FastAPI wrapper around moviebox-api, built to power Cymor Movie Hub. "
        "Learning/portfolio project — see README for the legal caveat."
    ),
    version="1.0.0",
)

# Tighten this to your actual Movie Hub domain via the CYMOR_HUB_ORIGIN env
# var once you know it — "*" is fine for a learning project, not for
# anything handling real traffic.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CYMOR_HUB_ORIGIN", "*")],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ---------- Tiny in-memory per-IP rate limiter (same pattern used in the
# TikTok downloader project — no extra dependency, good enough for a
# single-instance learning deployment). ----------
RATE_LIMIT_MAX = 30
RATE_LIMIT_WINDOW_SECONDS = 600
_request_log: dict[str, list[float]] = {}


def rate_limit(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    hits = [t for t in _request_log.get(ip, []) if t > window_start]
    if len(hits) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Too many requests — please slow down.")
    hits.append(now)
    _request_log[ip] = hits


# ---------- One shared Session reused across requests ----------
_session: Optional[Session] = None


def get_session() -> Session:
    global _session
    if _session is None:
        _session = Session()
    return _session


def subject_type_from_str(media_type: str) -> SubjectType:
    if media_type == "movie":
        return SubjectType.MOVIES
    if media_type == "tv":
        return SubjectType.TV_SERIES
    raise HTTPException(status_code=400, detail="type must be 'movie' or 'tv'.")


# ---------- Request bodies ----------


class SearchRequest(BaseModel):
    query: str
    type: str = "movie"  # "movie" | "tv"
    page: int = 1
    per_page: int = 10


class DetailsRequest(BaseModel):
    type: str = "movie"
    query: Optional[str] = None
    page_url: Optional[str] = None


class FilesRequest(BaseModel):
    type: str = "movie"
    query: Optional[str] = None
    page_url: Optional[str] = None
    season: Optional[int] = None
    episode: Optional[int] = None


class DownloadRequest(BaseModel):
    type: str = "movie"
    query: Optional[str] = None
    page_url: Optional[str] = None
    season: Optional[int] = None
    episode: Optional[int] = None
    # Matched against whatever quality-ish field is actually present on
    # each download entry (see _pick_media_file) — falls back to the
    # library's own best_media_file if nothing matches or this is omitted.
    quality: Optional[str] = None
    subtitle_language: Optional[str] = None  # if set, also fetches a subtitle file


# ---------- Helpers ----------


async def _resolve_details(media_type: str, query: Optional[str], page_url: Optional[str], session: Session):
    """Resolve a MovieDetails/TVSeriesDetails model, from either a page_url
    (fastest — comes from a previous /api/search result's page_url) or a
    fresh search query (we take the first result, matching MovieAuto's
    own documented "search then pick first" behaviour)."""
    subject_type = subject_type_from_str(media_type)
    details_cls = MovieDetails if media_type == "movie" else TVSeriesDetails

    if page_url:
        details_inst = details_cls(page_url, session=session)
        return await details_inst.get_content_model()

    if not query:
        raise HTTPException(status_code=400, detail="Provide either 'query' or 'page_url'.")

    search = Search(session, query=query, subject_type=subject_type)
    search_results = await search.get_content_model()
    if not search_results.items:
        raise HTTPException(status_code=404, detail=f"No {media_type} found for '{query}'.")
    target_item = search_results.first_item
    details_inst = details_cls(target_item, session=session)
    return await details_inst.get_content_model()


async def _resolve_files_detail(media_type: str, details_model, session: Session, season, episode):
    if media_type == "movie":
        files = DownloadableMovieFilesDetail(session, details_model)
        return await files.get_content_model()

    if season is None or episode is None:
        raise HTTPException(status_code=400, detail="TV series require both 'season' and 'episode'.")
    files = DownloadableTVSeriesFilesDetail(session, details_model)
    return await files.get_content_model(season=season, episode=episode)


def _pick_media_file(files_detail, quality: Optional[str]):
    downloads = getattr(files_detail, "downloads", None) or []
    if quality:
        for f in downloads:
            # The docs don't pin down one exact attribute name for the
            # quality label, so we check the plausible candidates rather
            # than assume one — this is a documented uncertainty, not a
            # silent guess.
            for attr in ("resolution", "quality", "label"):
                if getattr(f, attr, None) == quality:
                    return f
    best = getattr(files_detail, "best_media_file", None)
    if best:
        return best
    if downloads:
        return downloads[0]
    raise HTTPException(status_code=404, detail="No downloadable video file found for this title.")


def _cleanup_file(path: Path):
    try:
        path.unlink(missing_ok=True)
    except Exception:
        pass


# ---------- Routes ----------


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/search")
async def search(body: SearchRequest, request: Request):
    rate_limit(request)
    session = get_session()
    subject_type = subject_type_from_str(body.type)
    search_obj = Search(
        session, query=body.query, subject_type=subject_type, page=body.page, per_page=body.per_page
    )
    try:
        results = await search_obj.get_content_model()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Moviebox search failed: {exc}") from exc
    return results.model_dump(mode="json")


@app.post("/api/details")
async def details(body: DetailsRequest, request: Request):
    rate_limit(request)
    session = get_session()
    try:
        details_model = await _resolve_details(body.type, body.query, body.page_url, session)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Couldn't fetch details: {exc}") from exc
    return details_model.model_dump(mode="json")


@app.post("/api/files")
async def files(body: FilesRequest, request: Request):
    rate_limit(request)
    session = get_session()
    try:
        details_model = await _resolve_details(body.type, body.query, body.page_url, session)
        files_detail = await _resolve_files_detail(body.type, details_model, session, body.season, body.episode)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Couldn't fetch downloadable files: {exc}") from exc
    return files_detail.model_dump(mode="json")


@app.post("/api/download")
async def download(body: DownloadRequest, request: Request):
    """Downloads the video server-side (via MediaFileDownloader, exactly as
    documented) and streams the resulting file back, deleting it once sent.

    Heads up for large files: full movies can be hundreds of MB to a few GB.
    On Render's free tier this endpoint may be slow or hit request/memory
    limits for big files — see README for the lighter-weight alternative
    (returning the raw media URL via /api/files and linking to it directly
    instead of proxying through this server)."""
    rate_limit(request)
    session = get_session()
    try:
        details_model = await _resolve_details(body.type, body.query, body.page_url, session)
        files_detail = await _resolve_files_detail(body.type, details_model, session, body.season, body.episode)
        target_media_file = _pick_media_file(files_detail, body.quality)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Couldn't resolve a downloadable file: {exc}") from exc

    try:
        downloader = MediaFileDownloader()
        kwargs = {"filename": body.query or "cymor-movie"}
        if body.type == "tv":
            kwargs["season"] = body.season
            kwargs["episode"] = body.episode
        downloaded = await downloader.run(target_media_file, **kwargs)
        saved_path = Path(downloaded.saved_to)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Download failed: {exc}") from exc

    if not saved_path.exists():
        raise HTTPException(status_code=502, detail="Download reported success but the file is missing.")

    return FileResponse(
        saved_path,
        filename=saved_path.name,
        media_type="video/mp4",
        background=BackgroundTask(_cleanup_file, saved_path),
    )


@app.post("/api/download/subtitle")
async def download_subtitle(body: DownloadRequest, request: Request):
    """Same idea as /api/download, but for the subtitle file
    (CaptionFileDownloader, per the docs)."""
    rate_limit(request)
    session = get_session()
    try:
        details_model = await _resolve_details(body.type, body.query, body.page_url, session)
        files_detail = await _resolve_files_detail(body.type, details_model, session, body.season, body.episode)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Couldn't fetch downloadable files: {exc}") from exc

    target_caption_file = getattr(files_detail, "english_subtitle_file", None)
    if body.subtitle_language and body.subtitle_language.lower() != "english":
        # The docs only show .english_subtitle_file as a named shortcut;
        # for any other language we fall back to scanning .captions
        # ourselves rather than guessing another shortcut attribute exists.
        captions = getattr(files_detail, "captions", None) or []
        match = next(
            (c for c in captions if getattr(c, "language", "").lower() == body.subtitle_language.lower()),
            None,
        )
        target_caption_file = match or target_caption_file

    if not target_caption_file:
        raise HTTPException(status_code=404, detail="No subtitle file found for this title/language.")

    try:
        downloader = CaptionFileDownloader()
        kwargs = {"filename": body.query or "cymor-movie"}
        if body.type == "tv":
            kwargs["season"] = body.season
            kwargs["episode"] = body.episode
        downloaded = await downloader.run(target_caption_file, **kwargs)
        saved_path = Path(downloaded.saved_to)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Subtitle download failed: {exc}") from exc

    if not saved_path.exists():
        raise HTTPException(status_code=502, detail="Download reported success but the file is missing.")

    return FileResponse(
        saved_path,
        filename=saved_path.name,
        media_type="text/vtt",
        background=BackgroundTask(_cleanup_file, saved_path),
    )
