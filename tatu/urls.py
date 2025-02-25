from django.urls import path
from .views import search_answer

urlpatterns = [
    path('api/search/',search_answer, name='search_answer'),
]


