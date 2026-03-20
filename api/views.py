"""
views.py — FULL FILE (Member C adds transform_data)
Member A added : fetch_movie_from_tmdb(), fetch_actors_from_tvmaze()
Member C adds  : transform_data()
Member B added : MovieActorSummaryView
"""

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


TMDB_API_KEY = "fd1f7f208c259d51a736f10da715e460"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TVMAZE_BASE_URL = "https://api.tvmaze.com"




def fetch_movie_from_tmdb(title: str) -> dict | None:
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
    url = f"{TVMAZE_BASE_URL}/search/people"
    params = {"q": movie_title}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()




def transform_data(movie: dict, actors: list) -> dict:
    """
    Merges and transforms raw data from both APIs into one clean unified response.

    Transformations:
      - popularity_label : raw float  →  human-readable label
      - budget           : int        →  "$160,000,000"
      - runtime          : minutes    →  "2h 28m"
      - genres           : objects    →  name strings only
      - related_actors   : cleaned, top 5 only
      - quick_facts      : newly generated summary sentence
    """
    raw_popularity = movie.get("popularity", 0)
    if raw_popularity >= 100:
        popularity_label = "Blockbuster"
    elif raw_popularity >= 50:
        popularity_label = "Highly Popular"
    elif raw_popularity >= 20:
        popularity_label = "Moderately Popular"
    else:
        popularity_label = "Niche / Classic"

    budget = movie.get("budget", 0)
    budget_display = f"${budget:,}" if budget > 0 else "Not disclosed"

    runtime_minutes = movie.get("runtime") or 0
    runtime_hours   = runtime_minutes // 60
    runtime_mins    = runtime_minutes % 60
    runtime_display = f"{runtime_hours}h {runtime_mins}m" if runtime_minutes else "Unknown"

    genres = [g["name"] for g in movie.get("genres", [])]

    cleaned_actors = []
    for item in actors[:5]:
        person  = item.get("person", {})
        country = person.get("country") or {}
        cleaned_actors.append({
            "name":          person.get("name", "Unknown"),
            "birthday":      person.get("birthday", "N/A"),
            "country":       country.get("name", "N/A"),
            "gender":        person.get("gender", "N/A"),
            "profile_image": (person.get("image") or {}).get("medium", None),
        })

    return {
        "meta": {
            "api_version": "v1",
            "sources": ["TMDB Movie API", "TVmaze People API"],
        },
        "movie": {
            "title":             movie.get("title"),
            "tagline":           movie.get("tagline") or "N/A",
            "release_date":      movie.get("release_date"),
            "genres":            genres,
            "overview":          movie.get("overview"),
            "runtime":           runtime_display,
            "budget":            budget_display,
            "vote_average":      round(movie.get("vote_average", 0), 1),
            "vote_count":        movie.get("vote_count"),
            "popularity_score":  round(raw_popularity, 2),
            "popularity_label":  popularity_label,
            "original_language": movie.get("original_language", "N/A").upper(),
            "tmdb_id":           movie.get("id"),
        },
        "related_actors": cleaned_actors,
        "quick_facts": (
            f"'{movie.get('title')}' is a "
            f"{', '.join(genres) if genres else 'film'} "
            f"released on {movie.get('release_date', 'N/A')} "
            f"with a rating of {round(movie.get('vote_average', 0), 1)}/10 "
            f"and is classified as '{popularity_label}'."
        ),
    }




class MovieActorSummaryView(APIView):
    """GET /api/v1/movie-summary/?title=<movie_title>"""

    @swagger_auto_schema(
        operation_summary="Get Movie + Actor Summary",
        operation_description=(
            "Retrieves movie details from TMDB and related actor info from TVmaze, "
            "then merges and transforms them into a single unified response.\n\n"
            "**Example:** `/api/v1/movie-summary/?title=Inception`"
        ),
        manual_parameters=[
            openapi.Parameter(
                name='title',
                in_=openapi.IN_QUERY,
                description='Movie title to search for (e.g. Inception, Avengers)',
                type=openapi.TYPE_STRING,
                required=True,
                example='Inception',
            )
        ],
        responses={
            200: openapi.Response(description="Successful unified response"),
            400: openapi.Response(description="Missing or invalid title parameter"),
            404: openapi.Response(description="Movie not found"),
            502: openapi.Response(description="TMDB external API failure"),
            503: openapi.Response(description="TMDB API timeout"),
        }
    )
    def get(self, request):
        title = request.query_params.get("title", "").strip()

        if not title:
            return Response(
                {
                    "error": "Bad Request",
                    "message": "The 'title' query parameter is required.",
                    "example_usage": "/api/v1/movie-summary/?title=Inception",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(title) < 2:
            return Response(
                {
                    "error": "Bad Request",
                    "message": "Title must be at least 2 characters long.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            movie_data = fetch_movie_from_tmdb(title)
        except requests.exceptions.Timeout:
            return Response(
                {
                    "error": "External API Timeout",
                    "message": "TMDB API did not respond in time. Please try again.",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {
                    "error": "External API Failure",
                    "message": f"Could not reach TMDB API: {str(e)}",
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if not movie_data:
            return Response(
                {
                    "error": "Not Found",
                    "message": f"No movie found matching '{title}'. Try a different title.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            actor_data = fetch_actors_from_tvmaze(title)
        except requests.exceptions.RequestException:
            actor_data = []

        unified_response = transform_data(movie_data, actor_data)
        return Response(unified_response, status=status.HTTP_200_OK)
