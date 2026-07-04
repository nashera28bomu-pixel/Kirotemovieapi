"""
app/services/moviebox/__init__.py

MovieBox service package.

This module exposes all MovieBox services through a single import,
making them easy to use throughout the Cymor Movie API.

Example
-------
from app.services.moviebox import (
    moviebox,
    get_homepage,
    get_movie,
    get_series,
)

Author: Cymor
"""

# Shared client
from .client import moviebox

# Homepage
from .home import (
    get_homepage,
    get_featured,
    get_trending,
    get_latest,
    get_movies,
    get_series as get_home_series,
    get_anime,
)

# Search
from .search import (
    search,
    search_movies,
    search_series,
    suggestions,
    trending,
)

# Movies
from .movies import (
    get_movie,
    get_metadata,
    get_cast,
    get_crew,
    get_similar,
    get_recommendations,
    get_complete_movie,
)

# TV Series
from .series import (
    get_series,
    get_seasons,
    get_episodes,
    get_episode,
    get_complete_series,
)

# Watch
from .watch import (
    get_watch_sources,
    get_best_stream,
    get_lowest_stream,
    get_quality_stream,
    get_hls_streams,
    get_mp4_streams,
    get_dubbed_streams,
    get_stream_qualities,
    get_watch_info,
)

# Downloads
from .downloads import (
    get_downloads,
    get_best_quality,
    get_lowest_quality,
    get_quality,
    get_qualities,
    get_download_info,
)

# Subtitles
from .subtitles import (
    get_subtitles,
    get_default_subtitle,
    get_subtitle,
    get_languages,
    has_language,
    get_download_url,
    get_subtitle_info,
)

__all__ = [
    # Client
    "moviebox",

    # Home
    "get_homepage",
    "get_featured",
    "get_trending",
    "get_latest",
    "get_movies",
    "get_home_series",
    "get_anime",

    # Search
    "search",
    "search_movies",
    "search_series",
    "suggestions",
    "trending",

    # Movies
    "get_movie",
    "get_metadata",
    "get_cast",
    "get_crew",
    "get_similar",
    "get_recommendations",
    "get_complete_movie",

    # Series
    "get_series",
    "get_seasons",
    "get_episodes",
    "get_episode",
    "get_complete_series",

    # Watch
    "get_watch_sources",
    "get_best_stream",
    "get_lowest_stream",
    "get_quality_stream",
    "get_hls_streams",
    "get_mp4_streams",
    "get_dubbed_streams",
    "get_stream_qualities",
    "get_watch_info",

    # Downloads
    "get_downloads",
    "get_best_quality",
    "get_lowest_quality",
    "get_quality",
    "get_qualities",
    "get_download_info",

    # Subtitles
    "get_subtitles",
    "get_default_subtitle",
    "get_subtitle",
    "get_languages",
    "has_language",
    "get_download_url",
    "get_subtitle_info",
]
