"""
views.py
Member A adds: fetch_movie_from_tmdb(), fetch_actors_from_tvmaze()
Member C will add: transform_data()
Member B will add: MovieActorSummaryView
"""

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# !! Replace with your real free TMDB API key !!
# Get one at: https://www.themoviedb.org/settings/api
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TVMAZE_BASE_URL = "https://api.tvmaze.com"


def fetch_movie_from_tmdb(title: str) -> dict | None:
    """
    Calls the TMDB API to search for a movie by title.
    Returns full movie details dict, or None if not found.
    """
    search_url = f"{TMDB_BASE_URL}/search/movie"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US",
        "page": 1,
    }
    search_response = requests.get(search_url, params=search_params, timeout=10)
    search_response.raise_for_status()
    search_data = search_response.json()

    if not search_data.get("results"):
        return None

    first_result = search_data["results"][0]
    detail_url = f"{TMDB_BASE_URL}/movie/{first_result['id']}"
    detail_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    detail_response = requests.get(detail_url, params=detail_params, timeout=10)
    detail_response.raise_for_status()
    return detail_response.json()


def fetch_actors_from_tvmaze(movie_title: str) -> list:
    """
    Calls the TVmaze API to search for actors by movie title.
    No API key required — TVmaze is completely free.
    """
    url = f"{TVMAZE_BASE_URL}/search/people"
    params = {"q": movie_title}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
