"""
api/tests.py — Automated Tests
Member C adds this file.
Run with: python manage.py test api
"""

from unittest.mock import patch
from django.test import TestCase

MOCK_TMDB_DETAIL_RESPONSE = {
    "id": 27205,
    "title": "Inception",
    "tagline": "Your mind is the scene of the crime.",
    "overview": "Cobb is a skilled thief who steals secrets from dreams.",
    "release_date": "2010-07-16",
    "runtime": 148,
    "budget": 160000000,
    "vote_average": 8.364,
    "vote_count": 35000,
    "popularity": 125.5,
    "original_language": "en",
    "genres": [
        {"id": 28, "name": "Action"},
        {"id": 878, "name": "Science Fiction"},
    ],
}

MOCK_TVMAZE_RESPONSE = [
    {
        "score": 100,
        "person": {
            "id": 1,
            "name": "Leonardo DiCaprio",
            "birthday": "1974-11-11",
            "gender": "Male",
            "country": {"name": "United States", "code": "US"},
            "image": {"medium": "https://example.com/leo.jpg"},
        }
    }
]


class MovieActorSummaryViewTests(TestCase):

    def setUp(self):
        self.url = '/api/v1/movie-summary/'

    @patch('api.views.fetch_actors_from_tvmaze')
    @patch('api.views.fetch_movie_from_tmdb')
    def test_successful_response(self, mock_tmdb, mock_tvmaze):
        mock_tmdb.return_value = MOCK_TMDB_DETAIL_RESPONSE
        mock_tvmaze.return_value = MOCK_TVMAZE_RESPONSE
        response = self.client.get(self.url, {'title': 'Inception'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('meta', data)
        self.assertIn('movie', data)
        self.assertIn('related_actors', data)
        self.assertIn('quick_facts', data)
        self.assertEqual(data['movie']['title'], 'Inception')
        self.assertEqual(data['movie']['popularity_label'], 'Blockbuster')
        self.assertEqual(data['movie']['budget'], '$160,000,000')
        self.assertEqual(data['movie']['runtime'], '2h 28m')
        print("✅ Test 1 passed: Successful response")

    def test_missing_title_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Bad Request')
        print("✅ Test 2 passed: Missing title returns 400")

    def test_empty_title_returns_400(self):
        response = self.client.get(self.url, {'title': ''})
        self.assertEqual(response.status_code, 400)
        print("✅ Test 3 passed: Empty title returns 400")

    @patch('api.views.fetch_movie_from_tmdb')
    def test_movie_not_found_returns_404(self, mock_tmdb):
        mock_tmdb.return_value = None
        response = self.client.get(self.url, {'title': 'xyznonexistentmovie999'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Not Found')
        print("✅ Test 4 passed: Non-existent movie returns 404")

    @patch('api.views.fetch_movie_from_tmdb')
    def test_external_api_failure_returns_502(self, mock_tmdb):
        import requests as req
        mock_tmdb.side_effect = req.exceptions.ConnectionError("Connection refused")
        response = self.client.get(self.url, {'title': 'Inception'})
        self.assertEqual(response.status_code, 502)
        print("✅ Test 5 passed: External API failure returns 502")

    @patch('api.views.fetch_actors_from_tvmaze')
    @patch('api.views.fetch_movie_from_tmdb')
    def test_popularity_label_transformation(self, mock_tmdb, mock_tvmaze):
        low_pop_movie = MOCK_TMDB_DETAIL_RESPONSE.copy()
        low_pop_movie['popularity'] = 5.0
        mock_tmdb.return_value = low_pop_movie
        mock_tvmaze.return_value = []
        response = self.client.get(self.url, {'title': 'Inception'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['movie']['popularity_label'], 'Niche / Classic')
        print("✅ Test 6 passed: Popularity label transformation correct")