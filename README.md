# 🎬 Cymor Movie API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![MovieBox](https://img.shields.io/badge/Powered%20By-MovieBox-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### A modern, production-ready Movie & TV Series REST API built with FastAPI.

Search movies, TV series and anime, fetch detailed metadata, stream sources, download links, subtitles and much more through a clean REST API.

Designed for **Cymor Movie Hub**.

</div>

---

# Features

- Production-ready FastAPI architecture
- Lightning-fast async endpoints
- MovieBox powered content
- Movie search
- TV Series search
- Anime support
- Homepage discovery
- Trending content
- Featured content
- Movie details
- Series details
- Seasons & Episodes
- Streaming links
- Download links
- Subtitle support
- Multiple subtitle languages
- Smart caching
- Rate limiting
- Automatic error handling
- OpenAPI documentation
- ReDoc documentation
- Render deployment ready

---

# Technology Stack

- FastAPI
- Python 3.12
- moviebox-api
- HTTPX
- CacheTools
- Pydantic v2
- SlowAPI
- Uvicorn

---

# Project Structure

```
cymor-movie-api/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── home.py
│   │   ├── search.py
│   │   ├── movies.py
│   │   ├── series.py
│   │   ├── watch.py
│   │   ├── download.py
│   │   ├── subtitles.py
│   │   └── genres.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logger.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   └── rate_limit.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   │
│   │   └── moviebox/
│   │       ├── __init__.py
│   │       ├── client.py
│   │       ├── home.py
│   │       ├── search.py
│   │       ├── movies.py
│   │       ├── series.py
│   │       ├── watch.py
│   │       ├── downloads.py
│   │       └── subtitles.py
│   │
│   └── __init__.py
│
├── requirements.txt
├── render.yaml
├── .env.example
├── README.md
└── .gitignore
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cymor-movie-api.git
```

Enter the project

```bash
cd cymor-movie-api
```

Create virtual environment

```bash
python -m venv .venv
```

Activate it

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running

```bash
uvicorn app.main:app --reload
```

Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# Environment Variables

Example

```
APP_NAME=Cymor Movie API

VERSION=1.0.0

ENVIRONMENT=production

CACHE_ENABLED=true

CACHE_TTL=600

CACHE_MAXSIZE=1000

REQUEST_TIMEOUT=30

RATE_LIMIT=120/minute
```

---

# API Documentation

Swagger

```
/docs
```

ReDoc

```
/redoc
```

OpenAPI JSON

```
/openapi.json
```

---

# API Endpoints

## Health

```
GET /
GET /api
GET /health
```

---

## Homepage

```
GET /api/v1/home

GET /api/v1/home/featured

GET /api/v1/home/trending

GET /api/v1/home/latest

GET /api/v1/home/movies

GET /api/v1/home/series

GET /api/v1/home/anime
```

---

## Search

```
GET /api/v1/search?q=avatar

GET /api/v1/search/movies?q=avatar

GET /api/v1/search/series?q=breaking

GET /api/v1/search/suggestions?q=mar

GET /api/v1/search/trending
```

---

## Movies

```
GET /api/v1/movies/{id}

GET /api/v1/movies/{id}/metadata

GET /api/v1/movies/{id}/watch

GET /api/v1/movies/{id}/downloads

GET /api/v1/movies/{id}/subtitles

GET /api/v1/movies/{id}/cast

GET /api/v1/movies/{id}/crew

GET /api/v1/movies/{id}/similar

GET /api/v1/movies/{id}/recommendations

GET /api/v1/movies/{id}/complete
```

---

## TV Series

```
GET /api/v1/series/{id}

GET /api/v1/series/{id}/metadata

GET /api/v1/series/{id}/seasons

GET /api/v1/series/{id}/episodes

GET /api/v1/series/{id}/episodes/{season}/{episode}

GET /api/v1/series/{id}/watch

GET /api/v1/series/{id}/downloads

GET /api/v1/series/{id}/subtitles

GET /api/v1/series/{id}/cast

GET /api/v1/series/{id}/similar

GET /api/v1/series/{id}/recommendations

GET /api/v1/series/{id}/complete
```

---

## Watch

```
GET /api/v1/watch/{id}

GET /api/v1/watch/{id}/best

GET /api/v1/watch/{id}/lowest

GET /api/v1/watch/{id}/quality/{quality}

GET /api/v1/watch/{id}/hls

GET /api/v1/watch/{id}/mp4

GET /api/v1/watch/{id}/dubbed

GET /api/v1/watch/{id}/qualities

GET /api/v1/watch/{id}/info
```

---

## Downloads

```
GET /api/v1/download/{id}

GET /api/v1/download/{id}/best

GET /api/v1/download/{id}/lowest

GET /api/v1/download/{id}/quality/{quality}

GET /api/v1/download/{id}/qualities

GET /api/v1/download/{id}/info
```

---

## Subtitles

```
GET /api/v1/subtitles/{id}

GET /api/v1/subtitles/{id}/default

GET /api/v1/subtitles/{id}/languages

GET /api/v1/subtitles/{id}/language/{language}

GET /api/v1/subtitles/{id}/download

GET /api/v1/subtitles/{id}/download/{language}

GET /api/v1/subtitles/{id}/check/{language}

GET /api/v1/subtitles/{id}/info
```

---

## Genres

```
GET /api/v1/genres

GET /api/v1/genres/{genre}

GET /api/v1/genres/{genre}/movies

GET /api/v1/genres/{genre}/series
```

---

# Caching

The API includes a built-in in-memory cache.

Features

- Automatic expiration
- Configurable TTL
- Thread-safe
- Configurable size
- Cache statistics
- Cache helpers

---

# Error Handling

Every endpoint returns a consistent JSON response.

Example

```json
{
  "success": false,
  "message": "Movie not found"
}
```

---

# Rate Limiting

Built-in protection against abuse.

Default

```
120 requests/minute
```

---

# Deployment

Render

The repository already contains a production-ready

```
render.yaml
```

Simply:

- Push to GitHub
- Create a new Render Web Service
- Connect the repository
- Deploy

---

# Powered By

- FastAPI
- MovieBox
- Python
- Uvicorn

---

# Disclaimer

This project is an unofficial API wrapper built on top of publicly available MovieBox resources.

The project does **not** host, upload, store, or redistribute movies, TV series, subtitles, or any copyrighted media. All media remains the property of its respective owners. This API only retrieves metadata and publicly accessible links from third-party sources.

Use responsibly and comply with the laws and regulations applicable in your jurisdiction.

---

# Cymor

Built with ❤️ by **Cymor**

Making entertainment APIs beautiful.
