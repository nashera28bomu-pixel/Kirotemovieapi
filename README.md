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

## Known issue: 403 Forbidden on `/api/files` (download resolution)

**Status: confirmed.** After redeploying with the fixed dependency install
(see Dockerfile), `/api/files` and `/api/download` still return the same
403 from `h5.aoneroom.com`. That rules out the dependency theory — this is
almost certainly IP-based blocking of Render's server IP ranges by
Cloudflare (or similar), not a code bug. Multiple independent "Moviebox
API" wrapper projects specifically advertise "Cloudflare bypass" as a
feature for this exact endpoint, which is a strong tell.

Try these in order — cheapest/lowest-risk first:

### Tier 1 — switch mirrors (free, try this first)

`MOVIEBOX_API_HOST` is a supported env var. Per the maintainer's own
[issue #27](https://github.com/Simatwa/moviebox-api/issues/27), known
alternates include: `moviebox.ph`, `moviebox.ke`, `moviebox.pk`,
`moviebox.id`, `movieboxapp.in`, `netnaija.video`, `netnaija.com`,
`sflix.film`, `moviebox.ng`.

In Render's dashboard, set an environment variable:
```
MOVIEBOX_API_HOST=moviebox.ph
```
(or try a couple of the others — no code change, no redeploy needed beyond
the env var, just restart the service.) If a different mirror isn't behind
the same Cloudflare rule, this alone fixes it for free.

### Tier 2 — route through a proxy (costs money, only if Tier 1 fails)

`httpx` (used internally by this library) honours `HTTP_PROXY`/
`HTTPS_PROXY` environment variables **by default**, unless the library
explicitly disabled that — I couldn't find evidence either way in the
public docs, so this isn't guaranteed, but it's worth trying since it needs
no code change either:

```
HTTP_PROXY=http://username:password@proxy-host:port
HTTPS_PROXY=http://username:password@proxy-host:port
```

**Important:** this needs a real **residential** proxy, not a free public
proxy list — Cloudflare's whole point is blocking datacenter IPs, and free
public proxies are almost always datacenter IPs too (often already
blocklisted themselves). Residential proxy providers (Webshare, IPRoyal,
Smartproxy, Bright Data, and others) are the category to look at — check
current pricing yourself since it changes, but expect this to be the first
part of this whole project that isn't free, unlike the rest of your stack.

### If neither works

That would mean the block is specifically fingerprinting the request
itself (TLS/JA3 fingerprint, missing JS challenge solve) rather than just
IP reputation — at that point, a proxy alone won't help either, and the
realistic path is a library built specifically to solve that (the
"Cloudflare bypass" wrapper projects mentioned above take a fundamentally
different technical approach, not just a proxy). That's a bigger rewrite,
not a config change — happy to look into it if Tier 1 and 2 both fail.

## Render free-tier considerations

Worth knowing before you build on top of this:

- **Cold starts.** Free instances spin down after ~15 min idle. First
  request after that can take 30-60s while it wakes back up — build that
  into your Movie Hub's loading state, same as the TikTok downloader.
- **512MB RAM.** Fine for search/details/files (small JSON responses). Full
  movie downloads via `/api/download` load the whole file before responding
  — for anything multi-GB, that risks hitting the memory ceiling or being
  killed mid-request. This is the actual reason the README suggests linking
  directly to the raw media URL instead of proxying large files through
  this server.
- **No persistent disk on the free plan.** Downloaded files exist only
  during that request's lifetime (which is exactly what the cleanup logic
  in `main.py` assumes) — don't rely on anything being cached between
  requests.
- **Possible IP-range blocking**, per the 403 section above — free-tier
  Render IPs are shared/well-known, which may make this worse than a paid
  instance with a dedicated IP (though no guarantee a paid plan avoids it
  either, if it's genuine datacenter-range blocking rather than
  free-tier-specific).

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
