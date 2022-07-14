from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import DepenseStatus, Depenses, Categorie

# Create your views here.

class DepensesCreateView(CreateView):
    model=Depenses
    fields = "__all__"
    exclude = ('status',)
    
class DepensesListView(ListView):
    model=Depenses
    fields="__all__"
    context_object_name = 'depense_list'
    
class DepensesDetailView(DetailView):
    model=Depenses
    context_object_name = 'depense'
class DepenseStatusCreateView(CreateView):
    model=DepenseStatus
    fields="__all__"
    
class DepenseStatusDetailView(DetailView):
    model=DepenseStatus
    fields="__all__"
    
class CategorieDepenseCreateView(CreateView):
    model=Categorie
    fields="__all__"
class CategorieDepenseDetailView(DetailView):
    model=Categorie
    fields="__all__"