from django.urls import path
from .views import DepensesCreateView, DepenseStatusCreateView


urlpatterns = [
    path('create/depenses/', DepensesCreateView.as_view(template_name="depense_create.html"), name="depense-create-view"), 
    
    path('create/depensestatus/', DepenseStatusCreateView.as_view(template_name="depensestatus_create.html"), name="depensestatus-create-view"),
    path('depensestatus/<int:pk>/', DepenseStatusCreateView.as_view(template_name="depensestatus_create.html"), name="depensestatus-detail-view"),
 
    ]