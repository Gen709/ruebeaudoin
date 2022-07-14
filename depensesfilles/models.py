from django.db import models
from django.urls import reverse


# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class DepenseStatus(models.Model):
    desc = models.CharField(max_length=200, unique=True)
    
    def get_absolute_url(self):
        return reverse('depensestatus-detail-view', kwargs={'pk' : self.pk})
    
    def __str__(self):
        return self.desc
        
class Categorie(models.Model):
    desc = models.CharField(max_length=200, unique=True)
    
    def get_absolute_url(self):
        return reverse('categoriedepense-detail-view', kwargs={'pk' : self.pk})
    
    def __str__(self):
        return self.desc
    
class Depenses(TimeStampMixin):
    date = models.DateField()
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.ForeignKey(DepenseStatus, on_delete=models.SET_NULL, null=True)
    ref = models.ImageField(upload_to='bills')
    
    def get_absolute_url(self):
        return reverse('depense-detail-view', kwargs={'pk' : self.pk})