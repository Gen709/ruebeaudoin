from django.shortcuts import render
from .models import FoodName
from urllib.parse import unquote
from django.http.response import JsonResponse, HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'canadiannutrientfile/index.html', context)


def search_food_name(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # input_str = request.GET.get('term', '')
        input_str = unquote(request.GET['term'])
        lang = request.GET['lang']
        # result = FoodName.objects.all()
        if lang == "fr":
            # data_list = [{x.food_id: {'description':x.food_description_f}} for x in get_results(input_str, result)]
            data_list = [{x.food_id: {'description':x.food_description_f}} for x in FoodName.objects.filter(food_description_f__icontains=input_str).order_by('-rank', 'food_description_f')]
        else:
            data_list = [{x.food_id: {'description':x.food_description}} for x in FoodName.objects.filter(food_description__icontains=input_str).order_by('-rank', 'food_description')]
            
        # data_list = [{x.food_id: {'description':x.food_description}} for x in get_results(input_str, result)]
        data = JsonResponse(data_list, safe=False)
        
        mimetype = 'application/json'
        if len(data_list) > 0 and input_str != '':
            return HttpResponse(data, mimetype)
        else:
            return HttpResponse('', mimetype)
    else:
        return render(request, 'canadian_nutrient_file/search_form.html')
    


def search_conversion_factor(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        food_name_id = unquote(request.GET['foodnameid'])
        lang = request.GET['lang']
        if lang == "fr":
            data_list = [{conv_factor.id: {'description':conv_factor.mesure_name.mesure_name_f, 
                                           'cf_value': conv_factor.conversion_factor_value} } for conv_factor in FoodName.objects.get(food_id=food_name_id).conversionfactor_set.all()]
        if lang == "en":
            data_list = [{conv_factor.id: {'description':conv_factor.mesure_name.mesure_name, 
                                           'cf_value': conv_factor.conversion_factor_value} } for conv_factor in FoodName.objects.get(food_id=food_name_id).conversionfactor_set.all()]
        data = JsonResponse(data_list, safe=False)
       
    else:
        data_list = [{1:{'description':"Failed"}}]
        data = JsonResponse(data_list, safe=False)
        
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)