"""
app/api/search.py

Search API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/search
GET /api/v1/search/movies
GET /api/v1/search/series
GET /api/v1/search/suggestions
GET /api/v1/search/trending

Author: Cymor
"""

from fastapi import APIRouter, Query

from app.services.moviebox import search as search_service

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


# ==========================================================
# Global Search
# ==========================================================

@router.get("")
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
):
    """
    Search movies and TV series.
    """

    return {
        "success": True,
        "data": await search_service.search(
            query=q,
            page=page,
        ),
    }


# ==========================================================
# Movie Search
# ==========================================================

@router.get("/movies")
async def search_movies(
    q: str = Query(..., min_length=1),
):
    """
    Search movies only.
    """

    return {
        "success": True,
        "data": await search_service.search_movies(q),
    }


# ==========================================================
# TV Series Search
# ==========================================================

@router.get("/series")
async def search_series(
    q: str = Query(..., min_length=1),
):
    """
    Search TV series only.
    """

    return {
        "success": True,
        "data": await search_service.search_series(q),
    }


# ==========================================================
# Search Suggestions
# ==========================================================

@router.get("/suggestions")
async def suggestions(
    q: str = Query(..., min_length=1),
):
    """
    Return search suggestions.
    """

    return {
        "success": True,
        "data": await search_service.suggestions(q),
    }


# ==========================================================
# Trending Searches
# ==========================================================

@router.get("/trending")
async def trending():
    """
    Return trending homepage search content.
    """

    return {
        "success": True,
        "data": await search_service.trending(),
    }
