
from django.urls import path
from .views import index, search_food_name

urlpatterns = [
    path('', index, name='index'),
    path('search/foodname/', search_food_name, name='search-foodname'),
    ]