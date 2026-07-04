"""
app/api/download.py

Download API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/download/{item_id}
GET /api/v1/download/{item_id}/best
GET /api/v1/download/{item_id}/lowest
GET /api/v1/download/{item_id}/quality/{quality}
GET /api/v1/download/{item_id}/qualities
GET /api/v1/download/{item_id}/info

Author: Cymor
"""

from fastapi import APIRouter, Path

from app.services.moviebox import downloads as download_service

router = APIRouter(
    prefix="/download",
    tags=["Download"],
)


# ==========================================================
# All Downloads
# ==========================================================

@router.get("/{item_id}")
async def downloads(
    item_id: str = Path(..., description="Movie or Series ID"),
):
    """
    Get all available download links.
    """

    return {
        "success": True,
        "data": await download_service.get_downloads(item_id),
    }


# ==========================================================
# Best Quality
# ==========================================================

@router.get("/{item_id}/best")
async def best_quality(
    item_id: str,
):
    """
    Get the highest available download quality.
    """

    return {
        "success": True,
        "data": await download_service.get_best_quality(item_id),
    }


# ==========================================================
# Lowest Quality
# ==========================================================

@router.get("/{item_id}/lowest")
async def lowest_quality(
    item_id: str,
):
    """
    Get the lowest available download quality.
    """

    return {
        "success": True,
        "data": await download_service.get_lowest_quality(item_id),
    }


# ==========================================================
# Specific Quality
# ==========================================================

@router.get("/{item_id}/quality/{quality}")
async def quality(
    item_id: str,
    quality: str,
):
    """
    Get download link for a specific quality.
    """

    return {
        "success": True,
        "data": await download_service.get_quality(
            item_id,
            quality,
        ),
    }


# ==========================================================
# Available Qualities
# ==========================================================

@router.get("/{item_id}/qualities")
async def qualities(
    item_id: str,
):
    """
    Get all available download qualities.
    """

    return {
        "success": True,
        "data": await download_service.get_qualities(item_id),
    }


# ==========================================================
# Download Information
# ==========================================================

@router.get("/{item_id}/info")
async def info(
    item_id: str,
):
    """
    Get complete download information.
    """

    return {
        "success": True,
        "data": await download_service.get_download_info(item_id),
    }
