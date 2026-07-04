"""
app/api/home.py

Homepage API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/home
GET /api/v1/home/featured
GET /api/v1/home/trending
GET /api/v1/home/latest
GET /api/v1/home/movies
GET /api/v1/home/series
GET /api/v1/home/anime

Author: Cymor
"""

from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.services.moviebox import home

router = APIRouter(prefix="/home", tags=["Home"])


# ==========================================================
# Homepage
# ==========================================================

@router.get("")
async def homepage():
    """
    Complete homepage payload.
    """

    try:

        data = await home.get_homepage()

        return {
            "success": True,
            "data": data,
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==========================================================
# Featured
# ==========================================================

@router.get("/featured")
async def featured():

    try:

        return {
            "success": True,
            "data": await home.get_featured(),
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==========================================================
# Trending
# ==========================================================

@router.get("/trending")
async def trending():

    try:

        return {
            "success": True,
            "data": await home.get_trending(),
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==========================================================
# Latest Releases
# ==========================================================

@router.get("/latest")
async def latest():

    try:

        return {
            "success": True,
            "data": await home.get_latest(),
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==========================================================
# Movies
# ==========================================================

@router.get("/movies")
async def movies():

    try:

        return {
            "success": True,
            "data": await home.get_movies(),
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==========================================================
# TV Series
# ==========================================================

@router.get("/series")
async def series():

    try:

        return {
            "success": True,
            "data": await home.get_series(),
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==========================================================
# Anime
# ==========================================================

@router.get("/anime")
async def anime():

    try:

        return {
            "success": True,
            "data": await home.get_anime(),
        }

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
