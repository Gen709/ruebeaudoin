from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


# from .models import GroceryStore
from .forms import GroceryStoreModelForm, GroceryItemsForm
from .models import GroceryStore, GroceryItems, GroceryItemHistory
from canadiannutrientfile.models import FoodName
from datetime import date
# Create your views here.

def index(request):
    context={}
    return render(request, 'grocerylist/index.html', context)

def grocery_store_list_view(request):
    queryset = GroceryStore.objects.all()
    context={'queryset':queryset}
    return render(request, 'grocerylist/grocery_store_list.html', context)

def grocery_store_create_view(request):
    context={}
    if request.method == 'POST':
        form = GroceryStoreModelForm(request.POST)
        if form.is_valid():
            created, objects = GroceryStore.objects.get_or_create(name=form.cleaned_data['name'])
            return redirect('grocery-store-create')
        else:
            # form = GroceryStoreModelForm(request.POST)
            context['grocery_store_form'] = form
            # return render(request, 'grocerylist/grocery_store_create.html', context)   
    else:
        form = GroceryStoreModelForm()
        context['grocery_store_form'] = form
        context['stores'] = GroceryStore.objects.all()
    return render(request, 'grocerylist/grocery_store_create.html', context)

def grocery_store_delete_view(request, pk):
    gs = GroceryStore.objects.get(id=pk)
    gs.delete()
    return redirect('grocery-store-create')

def grocery_list_view(request):
    context={}
    if request.method == "POST":
        form = GroceryItemsForm(request.POST)
        context['store'] = GroceryStore.objects.get(id=request.POST.get('grocerystore_id'))
        context['food_name'] = FoodName.objects.get(food_id=request.POST.get('food_name_id'))
        context['price'] = request.POST.get('price')
        context['qty'] = request.POST.get('qty')
        try:
            gi = GroceryItems.objects.create(store=context['store'],
                                             food_name=context['food_name'],
                                             price=context['price'],
                                             qty=context['qty'])
            try:
                GroceryItemHistory.objects.create(item=gi,
                                                 status="wished for",
                                                 date=date())
                
            except:
                gi.objects.delete() 
        except:
            pass
        
        if form.is_valid():
            pass
        else:
            context['grocery_item_form'] = form
    else:
        pass
    
    context['groceryitems_queryset'] = GroceryItems.objects.filter(status=1) # this needs to be filtered on the status wish for as of now
    context['food_name_categories_queryset'] = GroceryItems.objects.values('food_name__food_group__food_group_name_f').distinct()
    context['grocerystore_queryset'] = GroceryStore.objects.all()
    context['grocery_item_form'] = GroceryItemsForm()
    
    return render(request, 'grocerylist/grocery_wish_list3.html', context)

def groceryitem_delete_view(request, pk):
    gi = GroceryItems.objects.get(id=pk)
    gi.delete()
    
    return redirect('wishlist')
    
def groceryitem_buy_view(request):
    if request.method == 'POST':
        context = {'post': request.POST }
    else:
        context = {'post': "Failed"}
        return render(request, 'grocerylist/test.html', {})