"""
app/services/moviebox/movies.py

Movie service for Cymor Movie API.

Handles all movie-specific operations.

Responsibilities
----------------
✓ Movie details
✓ Movie metadata
✓ Watch sources
✓ Download sources
✓ Similar movies
✓ Recommendations

All provider communication is centralized through the shared
MovieBox client.

Author: Cymor
"""

from __future__ import annotations

from app.core.cache import cache
from app.core.exceptions import (
    NotFoundError,
    ValidationError,
)
from app.core.logger import logger

from app.services.moviebox.client import moviebox


# ==========================================================
# Helpers
# ==========================================================

def _validate(movie_id: str) -> str:
    """
    Validate movie id.
    """

    movie_id = (movie_id or "").strip()

    if not movie_id:
        raise ValidationError("Movie id is required.")

    return movie_id


# ==========================================================
# Movie Details
# ==========================================================

async def get_movie(movie_id: str):
    """
    Return movie details.
    """

    movie_id = _validate(movie_id)

    cache_key = cache.build_key(
        "movie",
        movie_id,
    )

    async def fetch():

        logger.info(
            f"Fetching movie {movie_id}"
        )

        movie = await moviebox.details(
            movie_id
        )

        if not movie:
            raise NotFoundError(
                "Movie not found."
            )

        return movie

    return await cache.remember(
        cache_key,
        fetch,
    )


# ==========================================================
# Metadata
# ==========================================================

async def get_metadata(movie_id: str):
    """
    Return only metadata.
    """

    movie = await get_movie(movie_id)

    return {
        "id": movie.get("id"),
        "title": (
            movie.get("title")
            or movie.get("name")
        ),
        "year": movie.get("year"),
        "runtime": movie.get("runtime"),
        "country": movie.get("country"),
        "language": movie.get("language"),
        "genres": movie.get("genres"),
        "rating": movie.get("rating"),
        "votes": movie.get("votes"),
        "overview": (
            movie.get("overview")
            or movie.get("description")
        ),
        "poster": movie.get("poster"),
        "backdrop": movie.get("backdrop"),
    }


# ==========================================================
# Watch Sources
# ==========================================================

async def get_watch_sources(
    movie_id: str,
):
    """
    Return available streaming sources.
    """

    movie = await get_movie(movie_id)

    return {
        "id": movie_id,
        "sources": (
            movie.get("watch")
            or movie.get("watch_sources")
            or []
        ),
    }


# ==========================================================
# Download Sources
# ==========================================================

async def get_downloads(
    movie_id: str,
):
    """
    Return downloadable files.
    """

    movie = await get_movie(movie_id)

    return {
        "id": movie_id,
        "downloads": (
            movie.get("downloads")
            or movie.get("download")
            or []
        ),
    }


# ==========================================================
# Subtitles
# ==========================================================

async def get_subtitles(
    movie_id: str,
):
    """
    Return subtitle list.
    """

    movie = await get_movie(movie_id)

    return {
        "id": movie_id,
        "subtitles": (
            movie.get("subtitles")
            or []
        ),
    }


# ==========================================================
# Cast
# ==========================================================

async def get_cast(
    movie_id: str,
):
    """
    Return cast.
    """

    movie = await get_movie(movie_id)

    return {
        "id": movie_id,
        "cast": (
            movie.get("cast")
            or []
        ),
    }


# ==========================================================
# Crew
# ==========================================================

async def get_crew(
    movie_id: str,
):
    """
    Return crew.
    """

    movie = await get_movie(movie_id)

    return {
        "id": movie_id,
        "crew": (
            movie.get("crew")
            or []
        ),
    }


# ==========================================================
# Recommendations
# ==========================================================

async def get_recommendations(
    movie_id: str,
):
    """
    Return recommended movies.
    """

    movie = await get_movie(movie_id)

    recommendations = (
        movie.get("recommendations")
        or movie.get("similar")
        or []
    )

    return {
        "id": movie_id,
        "count": len(recommendations),
        "results": recommendations,
    }


# ==========================================================
# Similar Movies
# ==========================================================

async def get_similar(
    movie_id: str,
):
    """
    Return similar movies.
    """

    movie = await get_movie(movie_id)

    similar = (
        movie.get("similar")
        or movie.get("recommendations")
        or []
    )

    return {
        "id": movie_id,
        "count": len(similar),
        "results": similar,
    }


# ==========================================================
# Complete Payload
# ==========================================================

async def get_complete_movie(
    movie_id: str,
):
    """
    Complete movie response.

    This is the endpoint your frontend
    will typically consume.
    """

    return {
        "details": await get_movie(movie_id),
        "watch": await get_watch_sources(movie_id),
        "downloads": await get_downloads(movie_id),
        "subtitles": await get_subtitles(movie_id),
        "recommendations": await get_recommendations(movie_id),
    }
