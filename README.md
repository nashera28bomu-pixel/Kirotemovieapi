# Cymor Movie API

A FastAPI wrapper around [`moviebox-api`](https://pypi.org/project/moviebox-api)
(the `v1` namespace specifically), built to power Cymor Movie Hub.

## ⚠️ Read this first

This is a **learning / portfolio project**, not something to put real business
weight behind. `moviebox-api` is an *unofficial* wrapper around `moviebox.ph`,
which itself streams copyrighted films without a license — its own disclaimer
says as much. That's fine for personal experimentation and for showing off
FastAPI/async skills in a portfolio. It is **not** something to expose as a
public product with your name on it — that's real copyright exposure, not a
hypothetical one.

Every endpoint here is built strictly from the documented `v1` classes at
https://moviebox-api-docs.netlify.app/v1/movies and `.../v1/tv_series` —
`v2`/`v3` are still marked "Coming Soon" in the docs as of writing, so this
deliberately stays on `v1`.

**I haven't been able to test this end-to-end** — I have no network access in
my environment to actually install `moviebox-api` and hit the real Moviebox
service. The code faithfully follows the documented API surface, but you
should run it locally and check the responses before relying on it.

## Endpoints

All are documented interactively at `/docs` once running (FastAPI's built-in
Swagger UI) — genuinely useful for exploring exact response shapes live.

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check (used by Render) |
| POST | `/api/search` | Search movies or TV series |
| POST | `/api/details` | Get full details for one title |
| POST | `/api/files` | Get downloadable file metadata (video + subtitle URLs, quality options) |
| POST | `/api/download` | Download the video server-side and stream it back |
| POST | `/api/download/subtitle` | Same, for the subtitle file |

### Example: search

```bash
curl -X POST https://your-app.onrender.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "avatar", "type": "movie"}'
```

### Example: get files, then download

```bash
# 1. Search or get details first to obtain a page_url (or just pass query directly)
curl -X POST https://your-app.onrender.com/api/files \
  -H "Content-Type: application/json" \
  -d '{"query": "avatar", "type": "movie"}'

# 2. Download
curl -X POST https://your-app.onrender.com/api/download \
  -H "Content-Type: application/json" \
  -d '{"query": "avatar", "type": "movie"}' \
  --output avatar.mp4
```

### TV series

Same shape, plus `season` and `episode`:

```json
{ "query": "Merlin", "type": "tv", "season": 1, "episode": 1 }
```

## Why responses aren't hand-mapped to fixed fields

The docs don't spell out every field name on the underlying Pydantic models
(e.g. exactly what a quality label is called on a download entry). Rather
than guess and risk silently returning wrong/missing data, every endpoint
returns the full model via Pydantic's `.model_dump()` — so you get every
real field that exists, and can inspect the actual shape via `/docs` or a
test request rather than trusting a guess from me.

## A note on `/api/download` and file size

Full movies can be hundreds of MB to a few GB. This endpoint downloads the
file server-side via `MediaFileDownloader` (exactly as documented) and
streams it back, deleting it once sent. **On Render's free tier, this may be
slow or hit memory/timeout limits for large files.**

A lighter alternative: call `/api/files` and read the raw media URL out of
the response directly (it's in there — `.model_dump()` includes it), and
have your Movie Hub frontend link/stream directly from that URL instead of
proxying the whole file through this server. Less robust against
hotlink-protection possibly needing specific headers, but far lighter on
your Render instance.

## If the default mirror gets blocked

The library reads a `MOVIEBOX_API_HOST` environment variable to switch
mirrors (documented on PyPI). If requests start failing, set it in Render's
environment variables. Discover alternatives by running (locally, with the
`[cli]` extra installed) `moviebox v1 mirror-hosts`.

## If moviebox-api itself gets unstable

The maintainer's own README lists these as alternatives for a similar
approach: [`fzmovies-api`](https://github.com/Simatwa/fzmovies-api) (movies)
and [`fzseries-api`](https://github.com/Simatwa/fzseries-api) (TV series).

## Running locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Deploying to Render

This needs Docker (moviebox-api requires Python ≥3.12, which Render's default
buildpack may not match) — `render.yaml` and the `Dockerfile` handle this.
Push the whole repo, connect it to Render, make sure it's set up as a
**Docker** web service (should auto-detect from `render.yaml`).
