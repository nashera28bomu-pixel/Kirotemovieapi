"""
app/api/movies.py

Movie API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/movies/{movie_id}
GET /api/v1/movies/{movie_id}/metadata
GET /api/v1/movies/{movie_id}/watch
GET /api/v1/movies/{movie_id}/downloads
GET /api/v1/movies/{movie_id}/subtitles
GET /api/v1/movies/{movie_id}/cast
GET /api/v1/movies/{movie_id}/crew
GET /api/v1/movies/{movie_id}/similar
GET /api/v1/movies/{movie_id}/recommendations
GET /api/v1/movies/{movie_id}/complete

Author: Cymor
"""

from fastapi import APIRouter, Path

from app.services.moviebox import movies as movie_service

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


# ==========================================================
# Movie Details
# ==========================================================

@router.get("/{movie_id}")
async def movie_details(
    movie_id: str = Path(..., description="Movie ID"),
):
    """
    Get movie details.
    """

    return {
        "success": True,
        "data": await movie_service.get_movie(movie_id),
    }


# ==========================================================
# Metadata
# ==========================================================

@router.get("/{movie_id}/metadata")
async def metadata(
    movie_id: str,
):
    """
    Get movie metadata.
    """

    return {
        "success": True,
        "data": await movie_service.get_metadata(movie_id),
    }


# ==========================================================
# Watch Sources
# ==========================================================

@router.get("/{movie_id}/watch")
async def watch_sources(
    movie_id: str,
):
    """
    Get streaming sources.
    """

    return {
        "success": True,
        "data": await movie_service.get_watch_sources(movie_id),
    }


# ==========================================================
# Download Sources
# ==========================================================

@router.get("/{movie_id}/downloads")
async def downloads(
    movie_id: str,
):
    """
    Get download links.
    """

    return {
        "success": True,
        "data": await movie_service.get_downloads(movie_id),
    }


# ==========================================================
# Subtitles
# ==========================================================

@router.get("/{movie_id}/subtitles")
async def subtitles(
    movie_id: str,
):
    """
    Get subtitles.
    """

    return {
        "success": True,
        "data": await movie_service.get_subtitles(movie_id),
    }


# ==========================================================
# Cast
# ==========================================================

@router.get("/{movie_id}/cast")
async def cast(
    movie_id: str,
):
    """
    Get movie cast.
    """

    return {
        "success": True,
        "data": await movie_service.get_cast(movie_id),
    }


# ==========================================================
# Crew
# ==========================================================

@router.get("/{movie_id}/crew")
async def crew(
    movie_id: str,
):
    """
    Get movie crew.
    """

    return {
        "success": True,
        "data": await movie_service.get_crew(movie_id),
    }


# ==========================================================
# Similar Movies
# ==========================================================

@router.get("/{movie_id}/similar")
async def similar(
    movie_id: str,
):
    """
    Get similar movies.
    """

    return {
        "success": True,
        "data": await movie_service.get_similar(movie_id),
    }


# ==========================================================
# Recommendations
# ==========================================================

@router.get("/{movie_id}/recommendations")
async def recommendations(
    movie_id: str,
):
    """
    Get recommended movies.
    """

    return {
        "success": True,
        "data": await movie_service.get_recommendations(movie_id),
    }


# ==========================================================
# Complete Movie Payload
# ==========================================================

@router.get("/{movie_id}/complete")
async def complete(
    movie_id: str,
):
    """
    Get complete movie information.
    """

    return {
        "success": True,
        "data": await movie_service.get_complete_movie(movie_id),
    }
