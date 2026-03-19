from django.urls import path
from .views import MovieActorSummaryView

urlpatterns = [
    # Main endpoint: GET /api/v1/movie-summary/?title=Inception
    path('movie-summary/', MovieActorSummaryView.as_view(), name='movie-actor-summary'),
]
