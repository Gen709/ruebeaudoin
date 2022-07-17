from django.db import models
from canadiannutrientfile.models import FoodName, ConversionFactor, NutrientAmount
# Create your models here.

class Recipy(models.Model):
    Recipe_source = models.CharField(max_length=300, blank=True, null=True)
    recipy_url = models.URLField(max_length=250, blank=True, null=True, unique=True)
    lang = models.CharField(max_length=10, blank=True, null=True)
    recipy_title = models.CharField(max_length=100, blank=True, null=True) 
    recipy_yield_str = models.CharField(max_length=100, blank=True, null=True)
    recipy_yield_int = models.IntegerField(blank=True, null=True)
    prep_time = models.CharField(max_length=100, blank=True, null=True)
    cook_time = models.CharField(max_length=100, blank=True, null=True)
    total_time = models.CharField(max_length=100, blank=True, null=True)
    # image_list = models.CharField(max_length=500, blank=True, null=True)
    
    def get_absolute_url(self):
        return "recipy/%i/" % self.id
    
    def get_nutritional_info(self, param=None): # self
        macro_nutrient_name_list = ['carbohydrate, total (by difference)', 'fat (total lipids)', 'protein']
        simple_sugar_name_list = ['sucrose', 'glucose', 'fructose']
        ingredient_queryset = self.ingredients_set.all()
        nutrient_dict = {}
        # need the conversion factor here
        for ingredient in ingredient_queryset:
            for nutrient in ingredient.get_nutrient_profile():
                if nutrient.nutrient_name.nutrient_name.lower() in nutrient_dict.keys():
                    nutrient_dict[nutrient.nutrient_name.nutrient_name.lower()]['qty'] += nutrient.nutrient_value
                else:
                    nutrient_dict[nutrient.nutrient_name.nutrient_name.lower()] = {'qty': nutrient.nutrient_value,
                                                                                   'unit' : "test"}
                     
                
        if param == 'macro_nutrients':
            l = macro_nutrient_name_list
        elif param == 'simple_sugar':
            l = simple_sugar_name_list
        else:
            return nutrient_dict
            
        return {k:v['qty'] for k,v in nutrient_dict.items() if k in l}
    
    
    
class Ingredients(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    food_name = models.ForeignKey(FoodName, on_delete=models.CASCADE, blank=True, null=True)
    ingredient_str = models.CharField(max_length=100, blank=True, null=True) 
    qty = models.CharField(max_length=100, blank=True) 
    unit =  models.CharField(max_length=100, blank=True) 
    detail = models.CharField(max_length=100, blank=True, null=True)
    conversion_factor = models.ForeignKey(ConversionFactor, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipy', 'ingredient_str'], name='unique Ingredient')
            ]
        
    def get_conversion_factors(self):
        conversion_factor_queryset = ConversionFactor.objects.filter(food_name = self.food_name)  
        return conversion_factor_queryset
    
    def get_nutrient_profile(self):
        nutrient_amount_queryset = NutrientAmount.objects.filter(food_name = self.food_name)
        return nutrient_amount_queryset
    
class Steps(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    step = models.TextField(max_length=500) 
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['recipy', 'step'], name='unique Step')
    #         ]
         
class Images(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    image = models.CharField(max_length=250, unique=True)
    