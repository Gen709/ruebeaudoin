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
            data_list = [{x.food_id: {'description':x.food_description_f}} for x in FoodName.objects.all().filter(food_description_f__icontains=input_str)]
        else:
            data_list = [{x.food_id: {'description':x.food_description}} for x in FoodName.objects.all().filter(food_description__icontains=input_str)]
            
        # data_list = [{x.food_id: {'description':x.food_description}} for x in get_results(input_str, result)]
        data = JsonResponse(data_list, safe=False)
        
        mimetype = 'application/json'
        if len(data_list) > 0 and input_str != '':
            return HttpResponse(data, mimetype)
        else:
            return HttpResponse('', mimetype)
    else:
        return render(request, 'canadian_nutrient_file/search_form.html')