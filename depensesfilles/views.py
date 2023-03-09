from django.shortcuts import render, redirect

from django.db.models import Sum

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import DepenseStatus, Depenses, Categorie
from .forms import DepensesModelForm

from datetime import datetime as dt

# Create your views here.

class DepensesCreateView(CreateView):
    model=Depenses
    form_class = DepensesModelForm

def depenses_create(request):
    if request.method == 'POST':
        form = DepensesModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('depense-list-view')
        else:
            return render(request, 'depensesfilles/depense_create.html', {'form': form})
    elif request.method == 'GET':
        default_data_dict = {'date': dt.strftime(dt.today(), '%Y-%m-%d'),
                             'categorie': Categorie.objects.get(desc='Autre'),
                             'status': DepenseStatus.objects.get(desc='Non remboursée')}
        form = DepensesModelForm(default_data_dict)
        return render(request, 'depensesfilles/depense_create.html', {'form': form})
    
class DepensesListView(ListView):
    model=Depenses
    fields="__all__"
    context_object_name = 'depense_list'

    def get_context_data(self,**kwargs):
        context = super(DepensesListView,self).get_context_data(**kwargs)
        context['total_unpaid'] = Depenses.objects.filter(status=1).aggregate(total_unpaid=Sum('amount'))
        return context
    
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