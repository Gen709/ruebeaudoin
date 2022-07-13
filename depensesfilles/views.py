from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import DepenseStatus, Depenses

# Create your views here.

class DepensesCreateView(CreateView):
    model=Depenses
    fields = "__all__"
    exclude = ('status',)
    
class DepenseStatusCreateView(CreateView):
    model=DepenseStatus
    fields="__all__"
    
class DepenseStatusDetailView(DetailView):
    model=DepenseStatus
    fields="__all__"