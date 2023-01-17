from django.db import models
from canadiannutrientfile.models import FoodName 
# Create your models here.

class TimeStampMixin(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class GroceryStore(models.Model):
    name = NameField(max_length=100, unique=True)
    def __str__(self) -> str:
        return self.name
    
    
class GroceryItemStatus(models.Model):
    # Grocery history, 1) planned because needed or on special, 2) put on that week's list, 3) purchased, item closed
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class GroceryItems(TimeStampMixin):
    store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE)
    food_name = models.ForeignKey(FoodName, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    qty = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=25, blank=True, null=True, default=None)
    status=models.ForeignKey(GroceryItemStatus, on_delete=models.CASCADE, default=1)
    
    class Meta:
        unique_together = ('created_at', 'store', 'food_name')


class GroceryItemHistory(models.Model):
    item = models.ForeignKey(GroceryItems, on_delete=models.CASCADE)
    status = models.ForeignKey(GroceryItemStatus, on_delete=models.CASCADE)
    date = models.DateField()