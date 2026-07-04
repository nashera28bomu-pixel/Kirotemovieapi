"""
app/api/genres.py

Genre API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/genres
GET /api/v1/genres/{genre}
GET /api/v1/genres/{genre}/movies
GET /api/v1/genres/{genre}/series

Author: Cymor
"""

from fastapi import APIRouter, Path

from app.services.moviebox import search as search_service

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


# ==========================================================
# Available Genres
# ==========================================================

@router.get("")
async def genres():
    """
    Return supported genres.

    This list can later be populated dynamically from MovieBox
    if the provider exposes a genres endpoint.
    """

    return {
        "success": True,
        "data": {
            "genres": [
                "Action",
                "Adventure",
                "Animation",
                "Anime",
                "Biography",
                "Comedy",
                "Crime",
                "Documentary",
                "Drama",
                "Family",
                "Fantasy",
                "History",
                "Horror",
                "Music",
                "Mystery",
                "Romance",
                "Sci-Fi",
                "Sport",
                "Thriller",
                "War",
                "Western",
            ]
        },
    }


# ==========================================================
# Genre Search
# ==========================================================

@router.get("/{genre}")
async def genre(
    genre: str = Path(..., description="Genre name"),
):
    """
    Search content by genre.
    """

    return {
        "success": True,
        "data": await search_service.search(
            query=genre,
            page=1,
        ),
    }


# ==========================================================
# Movies By Genre
# ==========================================================

@router.get("/{genre}/movies")
async def genre_movies(
    genre: str,
):
    """
    Search movies by genre.
    """

    return {
        "success": True,
        "data": await search_service.search_movies(
            genre,
        ),
    }


# ==========================================================
# TV Series By Genre
# ==========================================================

@router.get("/{genre}/series")
async def genre_series(
    genre: str,
):
    """
    Search TV series by genre.
    """

    return {
        "success": True,
        "data": await search_service.search_series(
            genre,
        ),
    }
