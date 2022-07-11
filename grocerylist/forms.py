from .models import GroceryStore, GroceryItems

from django.forms import ModelForm 


class GroceryStoreModelForm(ModelForm):
    class Meta:
        model=GroceryStore
        fields='__all__' 
        
class GroceryItemsForm(ModelForm):
    class Meta:
        model=GroceryItems
        fields='__all__'