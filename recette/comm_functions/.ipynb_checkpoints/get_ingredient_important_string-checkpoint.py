
from django.db.models import Q, CharField
from django.db.models.functions import Lower

import nltk #import the natural language toolkit library
from nltk.stem.snowball import FrenchStemmer #import the French stemming library
from nltk.corpus import stopwords #import stopwords from nltk corpus
import re #import the regular expressions library; will be used to strip punctuation
from collections import Counter #allows for counting the number of occurences in a list


CharField.register_lookup(Lower, "lower")

def get_results(term_str, result):
    
        if type(term_str) == str:
            str_split = term_str.split(',')
        else:
            str_split = term_str
            
        if len(str_split) > 0:
            search_term = str_split.pop()
            result = result.filter(Q(food_description__lower__contains=search_term))
            return get_results(str_split, result)
        else:
            print()
            return result

