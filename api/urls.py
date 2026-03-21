from django.urls import path
from .views import MovieActorSummaryView, FrontendView

urlpatterns = [
    # Front-facing UI  →  http://localhost:8000/
    path('', FrontendView.as_view(), name='frontend'),

    # Main API endpoint  →  http://localhost:8000/api/v1/movie-summary/?title=Inception
    path('movie-summary/', MovieActorSummaryView.as_view(), name='movie-actor-summary'),
]
