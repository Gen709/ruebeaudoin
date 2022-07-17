from abc import ABC, abstractmethod, abstractproperty
from bs4 import BeautifulSoup as bs
from contextlib import closing
import pickle

import os
from os.path import isfile, join
from os import listdir

import sys

import requests
from urllib.parse import urlparse
import urllib

import json

# import nltk #import the natural language toolkit library
# # from nltk.stem.snowball import FrenchStemmer #import the French stemming library
# from nltk.corpus import stopwords #import stopwords from nltk corpus
# from nltk.tokenize import word_tokenize
import string
# import re #import the regular expressions library; will be used to strip punctuation
# from collections import Counter #allows for counting the number of occurences in a list
###################################################################################
# Web Site
################################################################################### 

class WebSite(object):
    path = 'html/'
    
    def __init__(self, url_str):
        
        # This is the WebSite Attribute
        self._url_str = url_str
        self._url_object = urlparse(self._url_str)
        self._url = None
        self._host_name = None
        self._file_dir = None
        self._file_name = None
        self._file_path = None
        self._bs4_object = None
        self._scraping_factory = None
        
    def get_url_object(self):
        return self._url_object
    
    
    def set_host_name(self):
        self._host_name = self._url_object.scheme+"://"+self._url_object.netloc
        
    def get_host_name(self):
        if self._host_name is not None:
            return self._host_name
        else:
            print("instantiating host name")
            self.set_host_name()
            return self.get_host_name()
    
    
    def set_file_dir(self):
        self._file_dir = os.path.join(self.path, self._url_object.netloc)
        
    def get_file_dir(self):
        if self._file_dir is not None:
            return self._file_dir
        else:
            print("Instantiating file path")
            self.set_file_dir()
            return self.get_file_dir()
    
    
    def set_file_name(self):
        self._file_name = urllib.parse.quote(self._url_object.path, " ")+'.pickle'
        
    def get_file_name(self):
        if self._file_name is not None:
            return self._file_name
        else:
            self.set_file_name()
            return self.get_file_name()
    
    
    def set_file_path(self):
        self._file_path = os.path.join(self.get_file_dir(),self.get_file_name())
        
    def get_file_path(self):
        if self._file_path is not None:
            return self._file_path
        else:
            self.set_file_path()
            return self.get_file_path()
    
    
    def set_url(self):
        self._url = self.get_host_name()+self._url_object.path
            
    def get_url(self):
        if self._url is not None:
            return self._url
        else:
            self.set_url()
            return self.get_url()
    
    
    def file_already_exists(self):
        """
        check if website directory exist, if not creates it and recals itself, 
        check if file has been saved
        returns 
        returns 
        """
        if not os.path.exists(self.get_file_dir()):
            # directory does not exist, create the directory 
            os.makedirs(self.get_file_dir())
            print("Directory ", self.get_file_dir(), "as been created, receipy does not exist")
            # call the function again
            self.file_already_exists()
        else:
            # the folder already exists but not the file
            if not os.path.exists(self.get_file_path()):
                # get the file
                # print("the folder already exists but not the file, GET THE FILE")
                return False
            else: # the file exist 
                # print("the receipy exists on file")
                return True
            # os.makedis(path_to_main_folder)
            # print('Folder ', path_to_main_folder, ' had to be created')
        
    def get_html(self):
        """
        Makes a GET request to the specified URL
        
        Returns:
            
            True, requests.content if successful
            
            False, error_message if un-successfull
            
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15', 
                   'Host': self._url_object.netloc,
                   'Origin': self.get_host_name(),
                   'Referer': self.get_host_name()
                  }
        try:
            with closing(requests.get(self.get_url(), headers=headers, verify=False)) as page_request:
                return True, page_request.content
        except requests.exceptions.RequestException as e:
            error_message = "Could not open " + self.get_url() + "error " + e
            return False, error_message
     
    
    def save_file(self, data):
        """
        Function simply save data as a pickle file. 
        It will handle recursion_limit error up to 10 0000
        If the operation fails, the method will print the data
        The path to the file is constructed based on the URL's domain and query or path
        depending on the get_file_path() method implemented for that particular domain.

        Paramaters:
        
            data : 

        Returns:

            True if the operation is successful  
            
            print the data otherwise

        """
        with open(self.get_file_path(), 'wb') as handle:
            try:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

            except RecursionError:
                sys.setrecursionlimit(100000)
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

            finally:
                print(self.get_file_path(), 'as been saved')
                sys.setrecursionlimit(1000)
                print("System recursions limits has been re-set at 1000")

                return True            
        
     
    def acquire_data(self):
        """ 
        Check if the html data has been downlaoded to disk.
            if the file isn't there, the method will call the other method get_html()
                then if the acquisition is successful -- the get_html() returns True --
        The data will be saved to disk and will return true
        
        If the file isn't already on file and the acquisition has not been successful the 
        function will return False
        
        Returns: 
        
            True if the file is there or can be acquired
            
            False if the file isn't there and could not be acquired via the get_html() method
            
        """
        
        if self.file_already_exists():
            print("File is already on disk")
            return True
        else: # get the html data
            data_acquired, data = self.get_html()
            if data_acquired: 
                print("Data succeffuly acquired, saving on file")
                # save the data on disk
                self.save_file(data)
                print('The file has been saved on disk')
                return True
            else:
                print("Unable to acquire html file thru the get_html function" + data)
                return False
    
    def set_bs4_object(self):
        """
            Use the get_file_path() method, if the path exist using 
            receipy_already_exist() method, opens it and reads it in a bs4 objects


            Parameters:

                None


            Return:

                return the tuple True, _bs4_object if the operation is successfull or
                return the tuple False, and the message from the method recepy_already_exist()
        """
        
        if self.file_already_exists():
            file =  self.get_file_path()

            with open(file, "rb") as f:
                soup_obj = bs(pickle.load(f), "html.parser")
            self._bs4_object = soup_obj
        else:
            self.acquire_data()
            
    def get_bs4_object(self):
        if self._bs4_object is not None:
            return self._bs4_object
        else:
            self.set_bs4_object()
            return self.get_bs4_object()
               
    def set_scraping_factory(self):
        if self._bs4_object is not None:
            if self._url_object.netloc == "www.ricardocuisine.com":
                self._scraping_factory = RicardoRecipyWebSite(self)
            elif self._url_object.netloc == "cooking.nytimes.com":
                self._scraping_factory = NytcReceipyWebSite(self)
        else:
            self.set_bs4_object()
            return self.set_scraping_factory()
        
    def get_scraping_factory(self):
        if self._scraping_factory is not None:
            return self._scraping_factory
        else:
            self.set_scraping_factory()
            return self.get_scraping_factory()
        
    def scrape_data(self):
        if self.get_scraping_factory() is not None:
            self.get_scraping_factory().scrape_data()
        else:
            self.set_scraping_factory()
            return self.scrape_data()
    
    def __str__(self):
        return self.get_url()

###################################################################################
# Nutritional abstract class
################################################################################### 

class HumanNutritionalNeedsWebSite(ABC):
    def __init__(self):
        self._language = None
        
###################################################################################
# Britanica abstract class
################################################################################### 
class Britanica(HumanNutritionalNeedsWebSite):
    def __init__(self):
        super().__init__()

###################################################################################
# Recipe abstract class
################################################################################### 

class ReceipyWebSite(ABC): 
    def __init__(self):
        self._language = None
        self._ingredient_list_raw = []
        self._ingredient_list_formated_str = []
        self._ingredient_list_of_dict_itemized = []
        # self._ingredient_list_of_usefull_words = []
        self._steps_list_raw = []
        self._image_set = set()
        self._yield = None
        self._title = None
        self._preperation_time = None
        self._cooking_time = None
        self._total_time = None
        self._json_object = None
        self._raw_stop_word_list = None
        # this will (could) be used as vector for graph and other calculation
        # probably would be better in the django model
        self.qty_list=[]
        self.unit_mesure_list = []
        self.ingredient_list = []
        self.detail_list = []
        
    @abstractmethod 
    def set_language(self):pass
            
    def get_language(self):
        if self._language is not None:
            return self._language
        else:
            self.set_language()
            return self._language
        
    def set_raw_stopword_list(self): 
        if self.get_language() is not None:
            if self.get_language() == "en":
                self._raw_stop_word_list = stopwords.words('english')
            elif self.get_language() == "fr":
                self._raw_stop_word_list = stopwords.words('french')
            else:
                self._raw_stop_word_list = "N/A"
        else:
            self.set_language()
            return self.set_raw_stopword_list()
        
    def get_raw_stopword_list(self):
        if self._raw_stop_word_list is not None:
            return self._raw_stop_word_list
        else:
            self.set_raw_stopword_list()
            return self.get_raw_stopword_list()
    
    @abstractmethod   
    def set_ingredient_list_raw(self):
        """
        Return the ingredient as it was scraped from the web site
        """
        pass
    def get_ingredient_list_raw(self):
        return self._ingredient_list_raw
        
    @abstractmethod
    def set_steps_list_raw(self):pass      
    def get_steps_list_raw(self):
        return self._steps_list_raw
    
    @abstractmethod
    def set_ingredient_list_of_dict_itemized(self):pass
    def get_ingredient_list_of_dict_itemized(self):
        if self._ingredient_list_of_dict_itemized is not None:
            return self._ingredient_list_of_dict_itemized
        else:
            return self.get_ingredient_list_of_dict_itemized()
        
    @abstractmethod
    def set_ingredient_list_formated_str(self):pass
    def get_ingredient_list_formated_str(self):
        if self._ingredient_list_formated_str is not None:
            return self._ingredient_list_formated_str
        else:
            return self.get_ingredient_list_formated_str()
    
    @abstractmethod
    def set_yield(self):pass
    def get_yield(self):
        return self._yield
    
    @abstractmethod
    def set_title(self):pass
    def get_title(self):
        return self._title
    
    @abstractmethod
    def set_preperation_time(self):pass
    def get_preperation_time(self):
        if self._preperation_time is not None:
            return self._preperation_time
        else:
            self.set_preperation_time()
            return self.get_preperation_time()
        
    @abstractmethod
    def set_cooking_time(self):pass
    def get_cooking_time(self):
        if self._cooking_time is not None:
            return self._cooking_time
        else:
            self.set_cooking_time()
            return self.get_cooking_time()
            # print('probleme')
            
    @abstractmethod
    def set_total_time(self):pass
    def get_total_time(self):
        if self._total_time is not None:
            return self._total_time
        else:
            self.set_total_time()
            return self.get_total_time()
            # print('probleme')
        
    @abstractmethod
    def set_json_object(self):pass
    def get_json_object(self):
        if self._json_object is not None:
            return self._json_object
        else:
            self.set_json_object()
            return self.get_json_object()
        
    @abstractmethod
    def set_image_set(self):pass
    def get_image_list(self):
        """
        a set is used to prevent duplocating image links, and a list is used for it's indexing capabilities
        """
        if len(self._image_set) > 0:
            return list(self._image_set)
        else:
            self.set_image_set()
            return self.get_image_list()
    
    
    def scrape_data(self):
        """
        This is a concrete application of an abstract method from the website class
        """
        self.set_ingredient_list_raw()
        self.set_steps_list_raw()
        self.set_yield()
        self.set_title()
        self.set_ingredient_list_of_dict_itemized()
        self.set_ingredient_list_formated_str()
        self.set_json_object()
        self.set_preperation_time()
        self.set_cooking_time()
        self.set_image_set()
    
    def is_a_number(self, _str:str):
        """
        This function checks if the fist element of the ingredient split string is 
            a fraction, 
            an Integer 
            a float
            
        Used to check if the first element.
        What is the string?

        Returns:

             True, the number
             or
             False, None

        """
        if "/" in _str:
            try:
                num = float(_str.split('/')[0])
                denum = float(_str.split('/')[1])
                qty = True, num / denum
            except:
                qty = False, None
        else:
            try:
                int(_str)
                qty = True, int(_str)
            except ValueError:   
                try:
                    float(_str)
                    qty = True, float(_str)
                except ValueError:
                    qty = False, None
        return qty
    
    def get_ingredient_details(self, str_list:list):
        """
        Looks for the strings "(" and ")" in the list, and store their position in a list.
        if the strings can be found in 2 positions in the list, removes all intermediary position and joins
        them together and retruns the str

        Return: 

            str: The ingredient details

        """
        # check if parenthesis
        # position = [i if ("(" in s or ")" in s) else None for i, s in enumerate(str_list)]
        # parenthese_range = [i for i, s in enumerate(str_list) if ("(" in s or ")" in s)]
        parenthese_range = [i for i, s in enumerate(str_list) if ("(" == s or ")" == s)]
        if len(parenthese_range) == 2:
            individual_detail_list = []
            correction = 0 # the correction is because the index changes at every pop operation
            for elem_index in range(parenthese_range[0], parenthese_range[1]+1):
                individual_detail_list.append(str_list.pop(elem_index - correction))
                correction += 1
            return " ".join(individual_detail_list)
        elif len(parenthese_range) == 1:
            return str_list.pop(parenthese_range[0])
        else:
            return None
        
##########################################################
# NYTC concrete implemantation or Recepy abs class
##########################################################
class NytcReceipyWebSite(ReceipyWebSite):
    """
    The class is a concrete implementation of the method from the ReceipyInterface
        - set_ingredient_list_raw
        - set_steps_list_raw
        - set_yield
        - set_title
        - set_ingredient_list_formated
        
    
    Parameters:
        bas4_object: bs4 
        
    """
    def __init__(self, WebPage):
        super().__init__() 
        self._bs4_object = WebPage.get_bs4_object()
        self._url_object = WebPage.get_url_object()
        
    def set_language(self):
        self._language = "en"
        
    def get_bs4_object(self):
        return self._bs4_object
    
    def set_ingredient_list_raw(self):
        # th jason object could be used for all set functions
        # j = json.loads(self.get_bs4_object().find('script', type="application/ld+json").text.strip())
        # self._ingredient_list_raw = j["recipeIngredient"]
        self._ingredient_list_raw = self.get_json_object()["recipeIngredient"]
        # for ingredient in self.get_bs4_object().find('ul',  class_ ="recipe-ingredients").findAll("li"):
        #     ingredient_tuple = (ingredient.find("span", class_="quantity").text.strip(),
        #                         ingredient.find("span", class_="ingredient-name").text.strip()
        #                        )
            # self._ingredient_list_raw.append(ingredient_tuple) ### this for sure is not good
    
    def set_ingredient_list_formated_str(self):
        if self._ingredient_list_raw is not None:
            self._ingredient_list_formated_str = self._ingredient_list_raw
        else:
            self.set_ingredient_list_raw
            return self.set_ingredient_list_formated_str()
            
    def set_steps_list_raw(self):
        for step in self.get_bs4_object().find("ol", class_="recipe-steps").findAll("li"):
            self._steps_list_raw.append(step.text)
            
    def set_yield(self):
        self._yield = self.get_json_object()['recipeYield']
        
    def set_title(self):
        self._title = self.get_bs4_object().find("h1",class_="recipe-title title name").text.strip()
        
    def set_ingredient_list_of_dict_itemized(self):
        ###############################################
        # Pu bon après avoir changer la liste des ingredient raw qui n'est plus une liste de tuple (qty, ingredient)
        ############################################
        qty_list=[]
        unit_mesure_list = []
        ingredient_list = []
        detail_list = []

        for ingredient_line in self.get_ingredient_list_raw():
            ingredient_line_split_str_list = ingredient_line.split()
            detail = self.get_ingredient_details(ingredient_line_split_str_list)

            self.detail_list.append(detail)
            is_number, number = self.is_a_number(ingredient_line_split_str_list[0])
            if is_number: # si le premier element de la liste est un nombre, le deuxieme est probablement une mesure
                self.qty_list.append(number)
                self.unit_mesure_list.append(ingredient_line_split_str_list[1])
                # after the unit mesure c est l'ingredient
                self.ingredient_list.append(", ".join([x for x in ingredient_line_split_str_list[2:] if x !='']))
            else: # si ce n'est pas un nombre, on ne sait rien, on fou tout dans la str
                self.qty_list.append(None)
                # unit_mesure_list.append(ingredient_line_split_str_list[0])
                self.unit_mesure_list.append(None)
                self.ingredient_list.append(", ".join([x for x in ingredient_line_split_str_list if x !='']))
        
        
        
        # for ingredient_line in self.get_ingredient_list_raw():
        #     # ingredient_line_split_str_list = ingredient_line[1].split()
        #     ingredient_line_split_str_list = [x for x in word_tokenize(ingredient_line, language='english') 
        #                                       if x not in self.get_raw_stopword_list()]
        #     detail_list.append(self.get_ingredient_details(ingredient_line_split_str_list)) # self.
        #     ingredient_line_split_str_list = [x for x in ingredient_line_split_str_list 
        #                                                       if x not in string.punctuation]
        #     qty_list.append(ingredient_line[0])
        #     if ingredient_line[0] !='':
        #         unit_mesure_list.append(ingredient_line_split_str_list[0])
        #         ingredient_list.append(ingredient_line_split_str_list[1:])
        #     else:
        #         unit_mesure_list.append(None)
        #         ingredient_list.append(ingredient_line_split_str_list)

        self._ingredient_list_of_dict_itemized = [ {"Qty":e[0], "Unit":e[1], "Ingredient_str":e[2], "Detail_str":e[3]} for e in zip(self.qty_list, 
                                                                                                                                    self.unit_mesure_list, 
                                                                                                                                    self.ingredient_list, 
                                                                                                                                    self.detail_list)]
        
    def set_cooking_time(self):
        # 'cookTime'
        try:
            self._cooking_time = self.get_json_object()['cookTime']
        except:
            self._cooking_time = 'N/A'
        pass
    def set_preperation_time(self):
        # 'prepTime'
        try:
            self._preperation_time = self.get_json_object()['prepTime']
        except:
            self._preperation_time = 'N/A'
            
    def set_total_time(self):
        try:
            self._total_time = self.get_json_object()['totalTime']
        except:
            # add prep time and cook time
            self._total_time =  "N/A"
            
    def set_json_object(self):
        self._json_object = json.loads(self.get_bs4_object().find("script", type="application/ld+json").text)
        
    def set_image_set(self):
        try:
            im = self.get_json_object()['image']
            if type(im) == str:
                self._image_set.add(im)
            elif type(im) == list:
                self._image_set = set(im)
                
        except:
            self._image_list = "N/A"

        
#######################################################
# Ricardo concrete implemantation or Recepy abs class
#######################################################

class RicardoRecipyWebSite(ReceipyWebSite):
    """
    The class is a concrete implementation of the method from the ReceipyInterface
        - set_ingredient_list_raw
        - set_steps_list_raw
        - set_yield
        - set_title
        - set_ingredient_list_formated
        
    
    Parameters:
        bas4_object: bs4 
        
    """
    def __init__(self, WebPage):
        super().__init__() 
        self._bs4_object = WebPage.get_bs4_object()
        self._url_object = WebPage.get_url_object()
    
    def set_language(self):
        # this should be access by get_url_object, but mthod already in WebSite and also not in NYTC 
        if self._url_object.path[1:3] == "en":
            self._language = "en"
        else:
            self._language = "fr"
        
    def get_bs4_object(self):
        return self._bs4_object
        
    def set_ingredient_list_raw(self):
        self._ingredient_list_raw = self.get_json_object()["recipeIngredient"]
        # for ingredient in self.get_bs4_object().find("section", class_="ingredients").find("ul").findAll("li"):
        #     self._ingredient_list_raw.append(ingredient.find("label").text)
    
    def set_ingredient_list_formated_str(self):
        if self._ingredient_list_raw is not None:
            # enlever le caractère \t
            self._ingredient_list_formated_str = [x.replace('\t', ' ').replace('  ', ' ') for x in self._ingredient_list_raw]
        else:
            self.set_ingredient_list_raw
            return self.set_ingredient_list_formated_str()
            
    def set_steps_list_raw(self):
        for steps in self.get_bs4_object().find("section", class_="preparation").find("ol").findAll("li"):
            self._steps_list_raw.append(steps.find("span").text)

    def set_yield(self):
        # la position sur la page n'est pas fixe. Elle depend des autres informations qui sont présrntées
        self._yield = self.get_json_object()['recipeYield']
        
    def set_title(self):
        self._title = self.get_bs4_object().find("title").text.split("|")[0].strip()
        
    # This needs to be conditiones on langage (en / fr) 
    def set_ingredient_list_of_dict_itemized(self):

        def get_position_de(str_list:list) -> int:
            """
            this will be replace by NLTK
            
            Looks for the string 'de' or 'd'' and retruns the position or None
            De or d' precesds the ingredient but not necessarly  

            Returns:

                Position:int
            """
            try:
                position = str_list.index('de')
                position_of_first = position
                return position_of_first
            except:
                try:
                    position = [i for i, s in enumerate(str_list) if "d’" in s]
                    position_of_first = position[0]
                    return position_of_first
                except:
                    return None

        qty_list=[]
        unit_mesure_list = []
        ingredient_list = []
        detail_list = []
        #############################
        # Not working for english page
        ##########################
        # this is for the french page
        if self._language == "fr":
            
            for ingredient_line in self.get_ingredient_list_raw():
                ingredient_line_split_str_list = ingredient_line.split()
                # ingredient_line_split_str_list = [x for x in word_tokenize(ingredient_line, language='french') 
                #                                               if x not in self.get_raw_stopword_list()]
                # ingredient_line_tokenized = word_tokenize(ingredient_line, language='french')
                ingredient_line_split_str_list[0] = ingredient_line_split_str_list[0].replace(",", ".")
                detail_list.append(self.get_ingredient_details(ingredient_line_split_str_list))
                ingredient_line_split_str_list = [x for x in ingredient_line_split_str_list 
                                                              if x not in string.punctuation]
                # get first element
                is_number, number = self.is_a_number(ingredient_line_split_str_list[0])
                if is_number: # si le premier element de la liste est un nombre, le deuxieme est probablement une mesure
                    qty_list.append(number)
                    unit_mesure_list.append(ingredient_line_split_str_list[1])
                    # after the unit mesure c est l'ingredient
                    ingredient_list.append(", ".join([x for x in ingredient_line_split_str_list[2:] if x !='']))
                else: # si ce n'est pas un nombre, on ne sait rien, on fou tout dans la str
                    qty_list.append(None)
                    # unit_mesure_list.append(ingredient_line_split_str_list[0])
                    unit_mesure_list.append(None)
                    ingredient_list.append(", ".join([x for x in ingredient_line_split_str_list if x !='']))
        elif self._language == "en":
            for ingredient_line in self.get_ingredient_list_raw():
                qty_list.append(None)
                unit_mesure_list.append(None)
                ingredient_list.append(None)
                detail_list.append(None)
        elif self._language is None:
            self.set_language()
            return self.set_ingredient_list_of_dict_itemized()

        ingredient_list_of_dict = [ {"Qty":e[0], "Unit":e[1], "Ingredient_str":e[2], "Detail_str":e[3]} for e in zip(qty_list, unit_mesure_list, ingredient_list, detail_list)]
        # this is for the english page
        # get all of the the mesuring units in a list including abreviations
        # find the postion on the mesuring unit
        # the quanty
        
        
        #both needs to return ingredeint list
        self._ingredient_list_of_dict_itemized = ingredient_list_of_dict
        
        
         
    def set_cooking_time(self):
        # 'cookTime'
        try:
            self._cooking_time = self.get_json_object()['cookTime']
        except:
            self._cooking_time = 'N/A'
        pass
    def set_preperation_time(self):
        # 'prepTime'
        try:
            self._preperation_time = self.get_json_object()['prepTime']
        except:
            self._preperation_time = 'N/A'
            
    def set_total_time(self):
        try:
            self._total_time = self.get_json_object()['totalTime']
        except:
            # add prep time and cook time
            self._total_time =  "N/A"
            
    def set_json_object(self):
        self._json_object = json.loads(self.get_bs4_object().find("script", type="application/ld+json").text)
        
    def set_image_set(self):
        try:
            im = self.get_json_object()['image']
            if type(im) == str:
                self._image_set.add(im)
            elif type(im) == list:
                self._image_set = set(im)
                
        except:
            self._image_list = "N/A"






