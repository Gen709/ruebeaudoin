from django.urls import path
from .views import DepensesCreateView, DepenseStatusCreateView, DepensesDetailView, DepensesListView, CategorieDepenseCreateView, CategorieDepenseDetailView


urlpatterns = [
    path('depenses/create/', DepensesCreateView.as_view(template_name="depense_create.html"), name="depense-create-view"),
    path('depenses/list/', DepensesListView.as_view(template_name="depense_list.html"), name="depense-list-view"),
    path('depenses/<int:pk>', DepensesDetailView.as_view(template_name="depense_detail.html"), name="depense-detail-view"), 
    
    path('create/depensestatus/', DepenseStatusCreateView.as_view(template_name="depensestatus_create.html"), name="depensestatus-create-view"),
    path('depensestatus/<int:pk>/', DepenseStatusCreateView.as_view(template_name="depensestatus_create.html"), name="depensestatus-detail-view"),
    
    path('categoriedepense/create/', CategorieDepenseCreateView.as_view(template_name="categoriedepense_create.html"), name="categoriedepense-create-view"),
    path('categoriedepense/<int:pk>/', CategorieDepenseDetailView.as_view(template_name="categoriedepense_detail.html"), name="categoriedepense-detail-view"),
 
    ]