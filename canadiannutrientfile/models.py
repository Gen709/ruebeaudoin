from django.db import models
from django.urls import reverse

# Create your models here.

class MesureName(models.Model):
    mesure_id = models.IntegerField(primary_key=True)
    mesure_name = models.CharField(max_length=200)
    mesure_name_f = models.CharField(max_length=200)
    
    class Meta:
        unique_together = ('mesure_name', 'mesure_name_f',)
        
        
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
    rank = models.IntegerField(default=0)
    
    
class NutrientName(models.Model):
    nutrient_id = models.IntegerField(primary_key=True)
    nutrient_code = models.IntegerField(unique=True)
    nutrient_symbole = models.CharField(max_length=10)
    unit = models.CharField(max_length=8)
    nutrient_name = models.CharField(max_length=200)
    nutrient_name_f = models.CharField(max_length=200)
    tag_name = models.CharField(max_length=20)
    nutrient_decimal = models.IntegerField()
    
    def get_absolute_url(self):
        return reverse('nutrientname_detail', kwargs={'pk':self.pk})
    
 
class NutrientSource(models.Model):
    nutrient_source_id = models.IntegerField(primary_key=True)
    nutrient_source_code = models.IntegerField()
    nutrient_source_description = models.CharField(max_length=200)
    nutrient_source_description_f = models.CharField(max_length=200)
    

     
class NutrientAmount(models.Model):
    # nutrient_amount_id = models.IntegerField(primary_key=True)
    food_name = models.ForeignKey(FoodName, on_delete=models.CASCADE)
    nutrient_name = models.ForeignKey(NutrientName, on_delete=models.CASCADE)
    nutrient_value = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    standard_error = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    number_of_observations = models.IntegerField(null=True, blank=True)
    nutrient_source = models.ForeignKey(NutrientSource, on_delete=models.CASCADE)
    nutrient_date_of_entry = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together = ('food_name', 'nutrient_name', 'nutrient_value',)
        
    def get_absolute_url(self):
        return reverse('nutrientamount_detail', kwargs={'pk':self.pk})
    
class ConversionFactor(models.Model):
    # conversion_factor_id = models.IntegerField(primary_key=True)
    food_name = models.ForeignKey(FoodName, on_delete=models.CASCADE)
    mesure_name = models.ForeignKey(MesureName, on_delete=models.CASCADE)
    conversion_factor_value = models.DecimalField(max_digits=12, decimal_places=8)
    conversion_date_of_entry = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together = ('food_name', 'mesure_name',)