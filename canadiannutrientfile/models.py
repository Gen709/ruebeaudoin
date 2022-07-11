from django.db import models
from django.urls import reverse

# Create your models here.
class FoodGroup(models.Model):
    food_group_id = models.IntegerField(primary_key=True)
    food_group_code = models.IntegerField(unique=True)
    food_group_name = models.CharField(max_length=255)
    food_group_name_f = models.CharField(max_length=255)
    
    # def get_absolute_url(self):
    #     return reverse('foodgroup_detail', kwargs={'pk':self.pk})

class FoodSource(models.Model):
    food_source_id = models.IntegerField(primary_key=True)
    food_source_code = models.IntegerField()
    food_source_name = models.CharField(max_length=255)
    food_source_name_f = models.CharField(max_length=255)
    
    # def get_absolute_url(self):
    #     return reverse('foodsource_detail', kwargs={'pk':self.pk})

class FoodName(models.Model):
    food_id = models.IntegerField(primary_key=True)
    food_code = models.IntegerField()
    food_group = models.ForeignKey(FoodGroup, on_delete=models.CASCADE)
    food_source = models.ForeignKey(FoodSource, on_delete=models.CASCADE)
    food_description = models.CharField(max_length=255)
    food_description_f = models.CharField(max_length=255)
    country_code = models.IntegerField()
    food_date_of_entry = models.DateField(blank=True, null=True)
    food_date_of_publication = models.DateField(blank=True, null=True)
    scientific_name = models.CharField(max_length=255)