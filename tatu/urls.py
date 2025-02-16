from django.urls import path
from .views2 import search_answer
from .views import search_answe

urlpatterns = [
    path("test/v2/848796050", search_answe, name="search_answe"),
    path('api/search/',search_answer, name='search_answer'),
]


