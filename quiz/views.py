import json
import os
from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from quiz.models import Flags, Language, Country, Continent, Game, Results
from bs4 import BeautifulSoup
import requests
import re
import base64
import time
import pyautogui
import random
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from selenium import webdriver

URL = "https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata"
content = requests.get(URL).content
pattern = re.compile(r'\w\/\w{2}\/[\w\-\d\%]*.svg')


def country_scraping(language):
    # This function scraps from the Wikipedia the translation of country names and save them to db
    soup = BeautifulSoup(content, 'lxml')
    all_countries = soup.find(class_='wikitable').find_all('tr')
    for country in all_countries[1:]:
        country_site_src = country.find('a')['href']
        description = country.find('a')['title']
        country_site_full_src = f"https://pl.wikipedia.org/{country_site_src}"
        country_site_content = requests.get(country_site_full_src).content
        country_soup = BeautifulSoup(country_site_content, 'lxml')
        name = country_soup.find('a', attrs={'lang': language})['title']
        cleared_name = re.sub(r"(\s\(\w+\))?(\s[\-\–]\s\w+)?", '', name)
        name_language = Language.objects.get(pk=language)
        flag = Flags.objects.get(description=description)
        entry = Country(name=cleared_name, flag=flag, name_language=name_language)
        entry.save()


def flags_scraping():
    # This function scraps from the Wikipedia the country flag in svg format and save them to db
    soup = BeautifulSoup(content, 'lxml')
    all_countries = soup.find(class_='wikitable').find_all('tr')
    for country in all_countries[1:]:
        country_site_src = country.find('a')['href']
        description = country.find('a')['title']
        country_site_full_src = f"https://pl.wikipedia.org/{country_site_src}"
        country_site_content = requests.get(country_site_full_src).content
        country_soup = BeautifulSoup(country_site_content, 'lxml')
        flag_src_to_convert = country_soup.find('img', attrs={'alt': 'Flaga'})['src']
        flag_src_converted = pattern.findall(flag_src_to_convert)[0]
        flag_full_src = f"https://upload.wikimedia.org/wikipedia/commons/{flag_src_converted}"
        flag_svg = requests.get(flag_full_src).text
        flag_base64 = base64.b64encode(bytes(flag_svg, 'utf-8'))
        entry = Flags(description=description, flag_base64=flag_base64)
        entry.save()


def audio_scraping(request):
    # This experimental function save mp3 files generated in Chrome browser as video object
    countries = Flags.objects.all().order_by('description')
    print(countries)
    for country in countries[16:]:
        name = country.description
        print(name)
        driver = webdriver.Chrome()
        driver.get(
            f'https://audio2.pronouncekiwi.com/pronouncekiwiAudioFunctionAPIGateway?language=plNEW1&word={name}&serviceType=pronunciation')
        pyautogui.hotkey('ctrl', 's')
        time.sleep(5)
        pyautogui.click(x=2771, y=384)
        time.sleep(5)
        audio_file_patch = '/home/bear/Downloads/pronouncekiwiAudioFunctionAPIGateway.mp3'
        os.rename(audio_file_patch, f'static/{name}.mp3')


class MemoryView(View):
    # If GET request contains parameters "result" the function check parameter "user".
    # If it is not an empty string the result is saved to db.
    # Otherwise, function returns Json object with 8 random flags.

    def get(self, request):
        if request.GET.get('result'):
            if request.GET.get('user') != '':
                user = User.objects.get(username=request.GET.get('user'))
                result = request.GET.get('result')
                game = Game.objects.get(name='Memory')
                entry = Results.objects.create(user=user, result=result, game=game)
                entry.save()
                best_result = Results.objects.filter(user=user)[0]
                return JsonResponse({'best_result': f'{best_result}'})
            else:
                return JsonResponse({})
        else:
            random_flags_pk = random.sample(range(1, Flags.objects.all().count()), 8)
            list_of_flags = Flags.objects.filter(pk__in=random_flags_pk)
            json_data = []
            for item in list_of_flags:
                json_entry = {"description": item.description,
                              "image": "data:image/svg+xml;base64," + (bytes(item.flag_base64)).decode('utf-8')}
                json_data.append(json_entry)
            response = JsonResponse(json_data, safe=False)
            return response


class QuizView(View):
    # If request contains parameter "result" the result is saved to db.
    # Otherwise, function returns Json object with 8 random flags.
    def get(self, request):
        if request.GET.get('result'):
            user = User.objects.get(username=request.GET.get('user'))
            result = request.GET.get('result')
            game = Game.objects.get(name='Memory')
            entry = Results.objects.create(user=user, result=result, game=game)
            entry.save()
            best_result = Results.objects.filter(user=user)[0]
            return JsonResponse({'best_result': f'{best_result}'})
        elif request.GET.get('lang'):
            language = request.GET.get('lang')
            random_flags_pk = random.sample(range(1, Flags.objects.all().count()), 4)
            list_of_flags = Flags.objects.filter(pk__in=random_flags_pk)
            item = list_of_flags[0]
            country = Country.objects.filter(flag=item).get(name_language=language)
            json_data = [{"description": country.name,
                          "image": "data:image/svg+xml;base64," + (bytes(item.flag_base64)).decode('utf-8')}]
            for item in list_of_flags[1:4]:
                country = Country.objects.filter(flag=item).get(name_language=language)
                json_entry = {"description": country.name}
                json_data.append(json_entry)
            response = JsonResponse(json_data, safe=False)
            return response
        else:
            return HttpResponseBadRequest(request)



def sign_out(request):
    logout(request)
    return JsonResponse({'logged': 'false'})


class SignInView(View):
    # Following the GET request, JSON object with csrf token is generated.
    # Sending POST request with required data allows to log in.
    def get(self, request):
        token = get_token(request)
        response = JsonResponse({'csrfToken': token})
        return response

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
    # Following the GET request, JSON object with csrf token is generated.
    # Sending POST request with required data allows to create new account.
    def get(self, request):
        token = get_token(request)
        return JsonResponse({'csrfToken': token})

    def post(self, request):
        request_data = json.loads(request.body)
        try:
            username = request_data['username']
            password = request_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({"account_status": "created"})
        except:
            return JsonResponse({"account_status": "error"})


class FlagCourseView(View):
    # This function returns 42 random images
    def get(self, request):
        random_flags_pk = random.sample(range(1, Flags.objects.all().count()), 42)
        list_of_flags = Flags.objects.filter(pk__in=random_flags_pk)
        json_data = []
        for item in list_of_flags:
            json_entry = {"description": item.description,
                          "image": "data:image/svg+xml;base64," + (bytes(item.flag_base64)).decode('utf-8')}
            json_data.append(json_entry)
        response = JsonResponse(json_data, safe=False)
        return response

class ExtraFeautureView(View):
    # Logged in users can add additional language to the Quiz
    def get(self, request):
        if request.GET.get('user'):
            user = request.GET.get('user')
            try:
                username = User.objects.get(username=user)
                if username.is_authenticated:
                    language_list = list(Language.objects.values())
                    return JsonResponse([language_list, {'logged': 'true'}], safe=False)
            except:
                return JsonResponse({'logged': 'false'})
        elif request.GET.get('newlang'):
            language = request.GET.get('newlang')
            country_scraping(language)
            return JsonResponse({'request_status': 'in_progress'})
