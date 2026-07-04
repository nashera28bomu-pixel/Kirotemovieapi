"""
app/api/__init__.py

API package for Cymor Movie API.

Exports all API routers so they can be imported from a
single location.

Example
-------
from app.api import (
    health,
    home,
    search,
    movies,
    series,
    watch,
    download,
    subtitles,
    genres,
)

Author: Cymor
"""

from . import (
    health,
    home,
    search,
    movies,
    series,
    watch,
    download,
    subtitles,
    genres,
)

__all__ = [
    "health",
    "home",
    "search",
    "movies",
    "series",
    "watch",
    "download",
    "subtitles",
    "genres",
]
