from django.urls import path

from .views import get_recipy_from_url, create_recepy_from_url_view, RecipyDetailView, RecipyDeleteView, RecipyListView

urlpatterns = [
    path('recipy/get_from_url', get_recipy_from_url, name='get_url'),
    path('insert', create_recepy_from_url_view, name='recipy_insert'),
    path('recipy/<int:pk>/', RecipyDetailView.as_view(), name='recipy_detail'),
    path('recipy/delete/<int:pk>/', RecipyDeleteView.as_view(), name='recipy_delete'),
    path('recipy/list', RecipyListView.as_view(), name='recipy_list'),
    
    
]