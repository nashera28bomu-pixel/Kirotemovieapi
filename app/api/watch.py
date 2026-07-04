"""
app/api/watch.py

Watch API routes for Cymor Movie API.

Endpoints
---------
GET /api/v1/watch/{item_id}
GET /api/v1/watch/{item_id}/best
GET /api/v1/watch/{item_id}/lowest
GET /api/v1/watch/{item_id}/quality/{quality}
GET /api/v1/watch/{item_id}/hls
GET /api/v1/watch/{item_id}/mp4
GET /api/v1/watch/{item_id}/dubbed
GET /api/v1/watch/{item_id}/qualities
GET /api/v1/watch/{item_id}/info

Author: Cymor
"""

from fastapi import APIRouter, Path

from app.services.moviebox import watch as watch_service

router = APIRouter(
    prefix="/watch",
    tags=["Watch"],
)


# ==========================================================
# All Watch Sources
# ==========================================================

@router.get("/{item_id}")
async def watch_sources(
    item_id: str = Path(..., description="Movie or Series ID"),
):
    """
    Get all available streaming sources.
    """

    return {
        "success": True,
        "data": await watch_service.get_watch_sources(item_id),
    }


# ==========================================================
# Best Stream
# ==========================================================

@router.get("/{item_id}/best")
async def best_stream(
    item_id: str,
):
    """
    Get the highest quality stream.
    """

    return {
        "success": True,
        "data": await watch_service.get_best_stream(item_id),
    }


# ==========================================================
# Lowest Stream
# ==========================================================

@router.get("/{item_id}/lowest")
async def lowest_stream(
    item_id: str,
):
    """
    Get the lowest quality stream.
    """

    return {
        "success": True,
        "data": await watch_service.get_lowest_stream(item_id),
    }


# ==========================================================
# Specific Quality
# ==========================================================

@router.get("/{item_id}/quality/{quality}")
async def quality_stream(
    item_id: str,
    quality: str,
):
    """
    Get a stream for a specific quality.
    """

    return {
        "success": True,
        "data": await watch_service.get_quality_stream(
            item_id,
            quality,
        ),
    }


# ==========================================================
# HLS Streams
# ==========================================================

@router.get("/{item_id}/hls")
async def hls_streams(
    item_id: str,
):
    """
    Get HLS (.m3u8) streams.
    """

    return {
        "success": True,
        "data": await watch_service.get_hls_streams(item_id),
    }


# ==========================================================
# MP4 Streams
# ==========================================================

@router.get("/{item_id}/mp4")
async def mp4_streams(
    item_id: str,
):
    """
    Get MP4 streams.
    """

    return {
        "success": True,
        "data": await watch_service.get_mp4_streams(item_id),
    }


# ==========================================================
# Dubbed Streams
# ==========================================================

@router.get("/{item_id}/dubbed")
async def dubbed_streams(
    item_id: str,
):
    """
    Get dubbed streams.
    """

    return {
        "success": True,
        "data": await watch_service.get_dubbed_streams(item_id),
    }


# ==========================================================
# Available Qualities
# ==========================================================

@router.get("/{item_id}/qualities")
async def qualities(
    item_id: str,
):
    """
    Get all available stream qualities.
    """

    return {
        "success": True,
        "data": await watch_service.get_stream_qualities(item_id),
    }


# ==========================================================
# Complete Watch Information
# ==========================================================

@router.get("/{item_id}/info")
async def watch_info(
    item_id: str,
):
    """
    Get complete watch information.
    """

    return {
        "success": True,
        "data": await watch_service.get_watch_info(item_id),
  }
