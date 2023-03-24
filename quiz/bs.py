from bs4 import BeautifulSoup
from django.views import View
import requests
from django.http import JsonResponse
import shutil
import re
# from quiz.models import Flags


URL = "https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata"
content = requests.get(URL).content
pattern = re.compile(r'\w\/\w{2}\/[\w\-\d\%]*.svg')


def get_data_to_populate_db():
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find(class_='wikitable').find_all('tr')
    for country in table[110:112]:
        # country_name = country.contents[1].get_text().rstrip('\n')
        # print(country_name)
        flag = country.find('a')['href']
        flag2 = country.find('a')['title']
        print(flag2, flag)
        link = f"https://pl.wikipedia.org/{flag}"
        print(link)
        content2 = requests.get(link).content
        soup2 = BeautifulSoup(content2, 'lxml')
        x = soup2.find('a', attrs={'lang': 'en'})['lang']
        y = soup2.find('a', attrs={'lang': 'en'})['title']
        xx = soup2.find('a', attrs={'lang': 'de'})['lang']
        yy = soup2.find('a', attrs={'lang': 'de'})['title']
        z = soup2.find('img', attrs={'alt': 'Flaga'})['src']
        flag_re = pattern.findall(z)[0]
        link = f"https://upload.wikimedia.org/wikipedia/commons/{flag_re}"
        print(link)
        print(x, y, xx, yy)

        flag_img = requests.get(link).text
        print(flag_img)
        # with open(f"flag2/{y}.svg", 'w') as f:
        #     f.write(flag_img)
