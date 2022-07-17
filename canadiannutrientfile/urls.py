
from django.urls import path
from .views import index, search_food_name, search_conversion_factor

urlpatterns = [
    path('', index, name='index'),
    path('search/foodname/', search_food_name, name='search-foodname'),
    path('search/conversionfactors/', search_conversion_factor, name='search-conversionfactors'),
    ]