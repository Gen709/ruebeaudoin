from django.db import models


# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class DepenseStatus(models.Model):
    desc = models.CharField(max_length=200)
    
class Depenses(TimeStampMixin):
    date = models.DateField()
    categorie = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.ForeignKey(DepenseStatus, on_delete=models.SET_NULL, null=True)
    ref = models.ImageField(upload_to='bills')