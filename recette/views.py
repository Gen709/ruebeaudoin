
from django.shortcuts import render, redirect



from .forms import UrlForm

from .models import Recipy, Ingredients, Steps, Images
from canadiannutrientfile.models import FoodName, ConversionFactor

from .common import comm_class
from .common.comm_class import WebSite



# Create your views here.

def get_recipy_from_url(request):
    # this is the form view to enter the recioy URL
    
    # we receive a post from our form
    if request.method == "POST":
        
        data = UrlForm(request.POST) # the data is placed in the UrlForm class data.url_name
        if data.is_valid(): # <- how do we add to validation (by field i guess)
            # on split le URL
            url = data.cleaned_data["url_name"]
            
            r = comm_class.WebSite(url)
            
            request.session['recepy_url'] = url
            r.scrape_data()
            try:
                recipy_already_there = Recipy.objects.get(recipy_url=r.get_url())
                return redirect(recipy_already_there)
            except:
                context = {}
                
                context['Recipe_title'] = r.get_scraping_factory().get_title()
                context['Recipe_source'] = r.get_url_object().netloc
                context['lang'] = r.get_scraping_factory().get_language()
                context['Recipe_url'] = r.get_url()
                context['prep_time'] = r.get_scraping_factory().get_preperation_time()
                context['cook_time'] = r.get_scraping_factory().get_cooking_time()
                context['total_time'] = r.get_scraping_factory().get_total_time()
                context['yield'] = r.get_scraping_factory().get_yield()
                context['total_time'] = r.get_scraping_factory().get_total_time()
                context['ingredient_list'] = r.get_scraping_factory().get_ingredient_list_formated_str()
                context['ingredient_dict'] = r.get_scraping_factory().get_ingredient_list_of_dict_itemized()
                context['step_list'] = r.get_scraping_factory().get_steps_list_raw()
                context['image_list'] = r.get_scraping_factory().get_image_list()
                context['ingrdient_list_dict_zip'] = zip(r.get_scraping_factory().get_ingredient_list_formated_str(), 
                                                         r.get_scraping_factory().get_ingredient_list_of_dict_itemized())
            
                return render(request, 'select_food_name.html', context) # this is the url 
            
    else: # the form hasn't been seen yet by the user, generate empty form
        form = UrlForm() # Intsantiate a form instance
        return render(request, 'form_get_url.html', {'form':form})


def create_recepy_from_url_view(request, pk=None):
    
    
    def get_user_input(request):
        exlusion_list = ['csrfmiddlewaretoken', 'yield_int']
        # index_list = [k,v for k,v in request.POST.items() if k not in exlusion_list]
        qty_list = []
        unit_list =[]
        ingredient_id_list = []
        convertion_factor_list = []
        
        for k, v in request.POST.items():
            if 'Qty_' in k:
                qty_list.append(v)
            if 'Unit_' in k:
                unit_list.append(v)
            if 'Ingredient_id_' in k:
                ingredient_id_list.append(v)
            if 'convertion_factor_' in k:
                convertion_factor_list.append(v)
        
        
        return {'qty_list': qty_list,
                'unit_list': unit_list,
                'ingredient_id_list' : ingredient_id_list,
                'convertion_factor_list' : convertion_factor_list
                }
     
             
    def create_parent(recipy_obj, request):
        isinstance(recipy_obj, WebSite)
        
        recipy, created = Recipy.objects.get_or_create(  Recipe_source = recipy_obj.get_url_object().netloc,
                                                         recipy_url = recipy_obj.get_url(),
                                                         lang = recipy_obj.get_scraping_factory().get_language(),
                                                         recipy_title = recipy_obj.get_scraping_factory().get_title(),
                                                         recipy_yield_str = recipy_obj.get_scraping_factory().get_yield(),
                                                         recipy_yield_int = request.POST.get('yield_int', None),
                                                         prep_time = recipy_obj.get_scraping_factory().get_preperation_time(),
                                                         cook_time = recipy_obj.get_scraping_factory().get_cooking_time(),
                                                         total_time = recipy_obj.get_scraping_factory().get_total_time()
                                                         )
        
        return recipy
    
        
    def get_ingredients_obj_list(recipy_obj, parent, user_input_dict):
        # create the ingredients_objects and store them in a list
        # create empty list to store created objects
        ingredients_obj_list = []
        # get the user input
        # user_input_dict = get_user_input(request)
        # get the ingredient string 
        ingredient_strings_list = recipy_obj.get_scraping_factory().get_ingredient_list_formated_str()
        # get the list of dict
        items_ingredient_list_of_dict = recipy_obj.get_scraping_factory().get_ingredient_list_of_dict_itemized()
        # generate the object
        # try:
        for ingredient_str, qty, unit, food_name_id, ingredient_dict, conversion_factor_id in zip(ingredient_strings_list, 
                                                                                                  user_input_dict['qty_list'], 
                                                                                                  user_input_dict['unit_list'],
                                                                                                  user_input_dict['ingredient_id_list'], 
                                                                                                  items_ingredient_list_of_dict,
                                                                                                  user_input_dict['convertion_factor_list']
                                                                                                  ):
            i, created = Ingredients.objects.get_or_create(  recipy = parent, 
                                                    food_name = FoodName.objects.get(food_id=food_name_id), # on_delete=models.CASCADE, blank=True, null=True)
                                                    ingredient_str = ingredient_str, # models.CharField(max_length=100, blank=True, null=True)
                                                    qty = qty, # models.CharField(max_length=100, blank=True)
                                                    unit = unit, # .CharField(max_length=100, blank=True)
                                                    detail = ingredient_dict.get('Detail_str', None), # models.CharField(max_length=100, blank=True, null=True
                                                    conversion_factor = ConversionFactor.objects.get(id=conversion_factor_id)
                                                    )
            # add the objects to the list
            ingredients_obj_list.append(i)
               
        return ingredients_obj_list
            

    def get_steps_obj_list(recipy_obj, parent):
        # create the ingredients_objects and store them in a list
        # create empty list to store the created objects
        step_obj_list = []
        # generate the object
        # try:
        for step in recipy_obj.get_scraping_factory().get_steps_list_raw():
            s, created = Steps.objects.get_or_create(recipy = parent,
                                            step = step.strip())
        
            # add the objects to the list
            step_obj_list.append(s)

        return step_obj_list
    
    
    def get_images_obj_list(recipy_obj, parent):
        # create the ingredients_objects and store them in a list
        # create empty list to store the created objects
        images_obj_list = []
        # generate the object
        # try:
        for image in recipy_obj.get_scraping_factory().get_image_list():
            im, created = Images.objects.get_or_create(recipy = parent,
                                                       image = image)
        
            # add the objects to the list
            images_obj_list.append(im)
                # return the list
        # except Exception as e:
        #     images_obj_list.append('Something went wrong in the get_step_obj_list' + str(e))
            
        return images_obj_list
            
                    
    def generate_relationships(recipy_obj, parent, request):
        isinstance(recipy_obj, WebSite)
        isinstance(parent, Recipy)
        # list that will be a concatenation of the 3 list
        
        ingredients_obj_list = get_ingredients_obj_list(recipy_obj, parent, request)
        steps_obj_list = get_steps_obj_list(recipy_obj, parent)
        images_obj = get_images_obj_list(recipy_obj, parent)
        
        return ingredients_obj_list + steps_obj_list + images_obj
    
        # there are 2 list, data from the databse and data from the form
        # is there data in the database
        # is it different from the one from the form     
                     
    if request.method == "POST": # and no primary key which would indicate 
        # retrieve url from previous page                   
        url = request.session['recepy_url'] # this is not re-submited yet from 
        # instantiate recepy
        recipy_obj = comm_class.WebSite(url)
        # scrape data -- could be made more efficient if not doing all the steps
        recipy_obj.scrape_data()
        # data generated from the URL        
        user_input_dict = get_user_input(request)
        parent = create_parent(recipy_obj, request)
        ingredients_obj_list = get_ingredients_obj_list(recipy_obj, parent, user_input_dict)
        steps_obj_list = get_steps_obj_list(recipy_obj, parent)
        images_obj_list = get_images_obj_list(recipy_obj, parent)
        
        # recipy_form = RecipyModelForm(instance=parent)

        parent_creation_msg = ""
        ingredient_parent_list=""
        ingredient_creation_message=""
        steps_creation_message=""
        images_creation_message=""
        context = {'parent':parent,
                   # 'recipy_form': recipy_form,
                   'parent_creation_msg': parent_creation_msg,
                   # 'user_input_dict': user_input_dict, 
                   # 'post':request.POST, 
                   'ingredients_obj_list' : ingredients_obj_list,
                   'ingredients_parent_list': ingredient_parent_list,
                   'ingredient_creation_message': ingredient_creation_message,
                   'steps_obj_list': steps_obj_list,
                   'steps_creation_message': steps_creation_message,
                   'images_obj_list': images_obj_list,
                   'images_creation_message': images_creation_message
                   }
        # if fails
        # return render(request, 'create_recipy_errorpage.html', context)
        return render(request, 'create_recipy_errorpage.html', context)
 
 
from django.views.generic import DetailView, DeleteView, ListView, UpdateView   
from django.urls import reverse_lazy


class RecipyDetailView(DetailView):
    model = Recipy
    context_object_name = 'recipy'
    
    
class RecipyDeleteView(DeleteView):
    model = Recipy
    success_url = reverse_lazy('recipy_list')
    

class RecipyListView(ListView):
    model = Recipy
    context_object_name = 'recipy'
    
    
class RecipyUpdateView(UpdateView):
    model = Recipy
    fields='__all__'