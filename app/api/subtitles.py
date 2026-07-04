"""
app/api/subtitles.py

Subtitle API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/subtitles/{item_id}
GET /api/v1/subtitles/{item_id}/default
GET /api/v1/subtitles/{item_id}/languages
GET /api/v1/subtitles/{item_id}/language/{language}
GET /api/v1/subtitles/{item_id}/download
GET /api/v1/subtitles/{item_id}/download/{language}
GET /api/v1/subtitles/{item_id}/check/{language}
GET /api/v1/subtitles/{item_id}/info

Author: Cymor
"""

from fastapi import APIRouter, Path

from app.services.moviebox import subtitles as subtitle_service

router = APIRouter(
    prefix="/subtitles",
    tags=["Subtitles"],
)


# ==========================================================
# All Subtitles
# ==========================================================

@router.get("/{item_id}")
async def subtitles(
    item_id: str = Path(..., description="Movie or Series ID"),
):
    """
    Get all available subtitles.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_subtitles(item_id),
    }


# ==========================================================
# Default Subtitle
# ==========================================================

@router.get("/{item_id}/default")
async def default_subtitle(
    item_id: str,
):
    """
    Get the default subtitle.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_default_subtitle(item_id),
    }


# ==========================================================
# Available Languages
# ==========================================================

@router.get("/{item_id}/languages")
async def languages(
    item_id: str,
):
    """
    Get all available subtitle languages.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_languages(item_id),
    }


# ==========================================================
# Subtitle By Language
# ==========================================================

@router.get("/{item_id}/language/{language}")
async def subtitle_by_language(
    item_id: str,
    language: str,
):
    """
    Get subtitle by language.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_subtitle(
            item_id,
            language,
        ),
    }


# ==========================================================
# Default Download URL
# ==========================================================

@router.get("/{item_id}/download")
async def default_download(
    item_id: str,
):
    """
    Get the default subtitle download URL.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_download_url(item_id),
    }


# ==========================================================
# Download URL By Language
# ==========================================================

@router.get("/{item_id}/download/{language}")
async def download_language(
    item_id: str,
    language: str,
):
    """
    Get subtitle download URL for a specific language.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_download_url(
            item_id,
            language,
        ),
    }


# ==========================================================
# Check Language Availability
# ==========================================================

@router.get("/{item_id}/check/{language}")
async def check_language(
    item_id: str,
    language: str,
):
    """
    Check whether a subtitle language exists.
    """

    return {
        "success": True,
        "data": await subtitle_service.has_language(
            item_id,
            language,
        ),
    }


# ==========================================================
# Complete Subtitle Information
# ==========================================================

@router.get("/{item_id}/info")
async def subtitle_info(
    item_id: str,
):
    """
    Get complete subtitle information.
    """

    return {
        "success": True,
        "data": await subtitle_service.get_subtitle_info(item_id),
    }
