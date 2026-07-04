"""
app/api/series.py

TV Series API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/series/{series_id}
GET /api/v1/series/{series_id}/metadata
GET /api/v1/series/{series_id}/seasons
GET /api/v1/series/{series_id}/episodes
GET /api/v1/series/{series_id}/episodes/{season}/{episode}
GET /api/v1/series/{series_id}/watch
GET /api/v1/series/{series_id}/downloads
GET /api/v1/series/{series_id}/subtitles
GET /api/v1/series/{series_id}/cast
GET /api/v1/series/{series_id}/similar
GET /api/v1/series/{series_id}/recommendations
GET /api/v1/series/{series_id}/complete

Author: Cymor
"""

from fastapi import APIRouter, Path, Query

from app.services.moviebox import series as series_service

router = APIRouter(
    prefix="/series",
    tags=["TV Series"],
)


# ==========================================================
# Series Details
# ==========================================================

@router.get("/{series_id}")
async def series_details(
    series_id: str = Path(..., description="Series ID"),
):
    """
    Get TV series details.
    """

    return {
        "success": True,
        "data": await series_service.get_series(series_id),
    }


# ==========================================================
# Metadata
# ==========================================================

@router.get("/{series_id}/metadata")
async def metadata(
    series_id: str,
):
    """
    Get series metadata.
    """

    return {
        "success": True,
        "data": await series_service.get_metadata(series_id),
    }


# ==========================================================
# Seasons
# ==========================================================

@router.get("/{series_id}/seasons")
async def seasons(
    series_id: str,
):
    """
    Get all seasons.
    """

    return {
        "success": True,
        "data": await series_service.get_seasons(series_id),
    }


# ==========================================================
# Episodes
# ==========================================================

@router.get("/{series_id}/episodes")
async def episodes(
    series_id: str,
    season: int | None = Query(
        default=None,
        ge=1,
        description="Season number",
    ),
):
    """
    Get all episodes or a specific season.
    """

    return {
        "success": True,
        "data": await series_service.get_episodes(
            series_id,
            season,
        ),
    }


# ==========================================================
# Single Episode
# ==========================================================

@router.get("/{series_id}/episodes/{season}/{episode}")
async def episode(
    series_id: str,
    season: int = Path(..., ge=1),
    episode: int = Path(..., ge=1),
):
    """
    Get a single episode.
    """

    return {
        "success": True,
        "data": await series_service.get_episode(
            series_id,
            season,
            episode,
        ),
    }


# ==========================================================
# Watch Sources
# ==========================================================

@router.get("/{series_id}/watch")
async def watch(
    series_id: str,
):
    """
    Get streaming sources.
    """

    return {
        "success": True,
        "data": await series_service.get_watch_sources(series_id),
    }


# ==========================================================
# Downloads
# ==========================================================

@router.get("/{series_id}/downloads")
async def downloads(
    series_id: str,
):
    """
    Get download links.
    """

    return {
        "success": True,
        "data": await series_service.get_downloads(series_id),
    }


# ==========================================================
# Subtitles
# ==========================================================

@router.get("/{series_id}/subtitles")
async def subtitles(
    series_id: str,
):
    """
    Get subtitles.
    """

    return {
        "success": True,
        "data": await series_service.get_subtitles(series_id),
    }


# ==========================================================
# Cast
# ==========================================================

@router.get("/{series_id}/cast")
async def cast(
    series_id: str,
):
    """
    Get cast information.
    """

    return {
        "success": True,
        "data": await series_service.get_cast(series_id),
    }


# ==========================================================
# Similar Series
# ==========================================================

@router.get("/{series_id}/similar")
async def similar(
    series_id: str,
):
    """
    Get similar TV series.
    """

    return {
        "success": True,
        "data": await series_service.get_similar(series_id),
    }


# ==========================================================
# Recommendations
# ==========================================================

@router.get("/{series_id}/recommendations")
async def recommendations(
    series_id: str,
):
    """
    Get recommended TV series.
    """

    return {
        "success": True,
        "data": await series_service.get_recommendations(series_id),
    }


# ==========================================================
# Complete Payload
# ==========================================================

@router.get("/{series_id}/complete")
async def complete(
    series_id: str,
):
    """
    Get complete TV series payload.
    """

    return {
        "success": True,
        "data": await series_service.get_complete_series(series_id),
  }
