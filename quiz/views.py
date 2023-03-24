import json
import os

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from quiz.models import Flags, Translations, Language
import requests
from bs4 import BeautifulSoup
import requests
import re
import base64
from quiz.populate import flags_scraping
import time
import pyautogui
import random
from django.core import serializers
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from selenium import webdriver

# def get_audio():
#     x = requests.get('https://audio2.pronouncekiwi.com/pronouncekiwiAudioFunctionAPIGateway?language=Ewa&word=Polska&serviceType=pronunciation')
#     with open('myfile.mp3', 'wb') as f:
#         f.write(x.content)

file = "/home/bear/Desktop/praca_zaliczeniowa/games_platform/static/Angola.svg"
# class QuizView(View):
#
#     def get(self, request):
#         pass
        # x = Flags.objects.all()
        # svg = x[0].svg
        # return HttpResponse(svg)

        # file_content = open(file, "r").read()
        # myobject = Flags(svg=file_content)
        # myobject.save()
        # return HttpResponse(myobject.svg)






URL = "https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata"
content = requests.get(URL).content
pattern = re.compile(r'\w\/\w{2}\/[\w\-\d\%]*.svg')


def flags_scraping():
    i = 1
    soup = BeautifulSoup(content, 'lxml')
    all_countries = soup.find(class_='wikitable').find_all('tr')
    for country in all_countries[71:90]:
        country_site_src = country.find('a')['href']
        pl_name = country.find('a')['title']
        continent = country.find_all('td')[3].text
        country_site_full_src = f"https://pl.wikipedia.org/{country_site_src}"
        country_site_content = requests.get(country_site_full_src).content
        country_soup = BeautifulSoup(country_site_content, 'lxml')
        en = country_soup.find('a', attrs={'lang': 'en'})['title']
        de = country_soup.find('a', attrs={'lang': 'de'})['title']
        es = country_soup.find('a', attrs={'lang': 'es'})['title']
        en_name = re.sub(r"(\s\(\w+\))?(\s[\-\–]\s\w+)?", '', en)
        print(en_name)
        de_name = re.sub(r"(\s\(\w+\))?(\s[\-\–]\s\w+)?", '', de)
        es_name = re.sub(r"(\s\(\w+\))?(\s[\-\–]\s\w+)?", '', es)
        flag_src_to_convert = country_soup.find('img', attrs={'alt': 'Flaga'})['src']
        flag_src_converted = pattern.findall(flag_src_to_convert)[0]
        flag_full_src = f"https://upload.wikimedia.org/wikipedia/commons/{flag_src_converted}"
        flag_svg = requests.get(flag_full_src).text
        flag_base64 = base64.b64encode(bytes(flag_svg, 'utf-8'))
        language = Language.objects.get(pk='en')
        myobject = Flags(pk=i, description=pl_name, flag_base64=flag_base64, continent=continent)
        myobject.save()
        myobject2 = Translations(country_name=myobject, translated_country_name=en_name, language=language)
        myobject2.save()
        i += 1
        # with open(f"flag2/{y}.svg", 'w') as f:
        #     f.write(flag_img)




class QuizView(View):

    def get(self, request):
        random_flags_pk = random.sample(range(1,20), 4)
        list_of_flags = Flags.objects.filter(pk__in=random_flags_pk)
        item = list_of_flags[0]
        json_data = [{"description" : item.description, "image" : "data:image/svg+xml;base64," + (bytes(item.flag_base64)).decode('utf-8')}]
        for item in list_of_flags[1:4]:
            json_entry = {"description" : item.description}
            json_data.append(json_entry)
        response = JsonResponse(json_data, safe=False)
        return response


class MemoryView(View):

    def get(self, request):
        random_flags_pk = random.sample(range(1,12), 8)
        list_of_flags = Flags.objects.filter(pk__in=random_flags_pk)
        json_data = []
        for item in list_of_flags:
            json_entry = {"description" : item.description, "image" : "data:image/svg+xml;base64," + (bytes(item.flag_base64)).decode('utf-8')}
            json_data.append(json_entry)
        response = JsonResponse(json_data, safe=False)
        return response


    def post(self, request):
        pass


def csrf(request):
    countries = Flags.objects.filter(pk=2)
    print(countries)
    for country in countries:
        name = country.description
        print(name)
        driver = webdriver.Chrome()
        driver.get(f'https://audio2.pronouncekiwi.com/pronouncekiwiAudioFunctionAPIGateway?language=plNEW1&word={name}&serviceType=pronunciation')
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        pyautogui.click(x=2771, y=384)
        time.sleep(1)
        audio_file_patch = '/home/bear/Downloads/pronouncekiwiAudioFunctionAPIGateway.mp3'
        os.rename(audio_file_patch, f'static/{name}.mp3')
    return HttpResponse('ok')



# @login_required
def ping(request):
    logout(request)
    print(request.user.is_authenticated)
    return JsonResponse({'result': 'OK'})

class SignInView(View):
    def get(self, request):
        token = get_token(request)
        response = JsonResponse({'csrfToken': token, 'ok_get':'ok_get_v'})
        return response

        # if 'csrfToken' in json.loads(response.content).keys():
        #     print('ok')


    def post(self, request):
        request_data = json.loads(request.body)
        username = request_data['username']
        password = request_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                response = JsonResponse({"logged": "true"}, safe=False)
                return response
        else:
            response = JsonResponse({"logged": "false"}, safe=False)
            return response


class SignUpView(View):
    def get(self, request):
        token = get_token(request)
        return JsonResponse({'csrfToken': token})

    def post(self, request):
        request_data = json.loads(request.body)
        # username = request_data['username']
        # password = request_data['password']
        # user = User.objects.create_user(username=username, password=password)
        # user.save()
        print('ok')
        response = JsonResponse({"ok":"ok"}, safe=False)
        print(response)
        return response


