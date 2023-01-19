from django.urls import path
from .views import cal_view

urlpatterns = [
    path('', cal_view, name='calendar'),
    ]