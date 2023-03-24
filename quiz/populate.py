from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pyautogui

import requests
import re
import base64
from quiz.models import Flags, Translations
import urllib.request

# URL = "https://audio2.pronouncekiwi.com/pronouncekiwiAudioFunctionAPIGateway?language=Ewa&word=Polska&serviceType=pronunciation"
# content = requests.get(URL).content
# print(content)

# driver = webdriver.Chrome()
# driver.get("https://audio2.pronouncekiwi.com/pronouncekiwiAudioFunctionAPIGateway?language=Ewa&word=Polska&serviceType=pronunciation")
# pyautogui.hotkey('ctrl','s')
# time.sleep(3)
# print(pyautogui.position())
# pyautogui.click(x=2768, y=384)
# time.sleep(3)



def download_audio_description():
    options = webdriver.ChromeOptions();
    prefs = {"download.default_directory": "quiz/flag2"};
    options.add_experimental_option("prefs", prefs);
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options);
    try:
        driver.get('https://www.browserstack.com/test-on-the-right-mobile-devices');
        gotit = driver.find_element_by_id('accept-cookie-notification');
        gotit.click();
        downloadcsv = driver.find_element_by_css_selector('.icon-csv');
        downloadcsv.click();
        time.sleep(5)
        driver.close()
    except:
        print("Invalid URL")



def flags_scraping():
    URL = "https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata"
    content = requests.get(URL).content
    pattern = re.compile(r'\w\/\w{2}\/[\w\-\d\%]*.svg')

    soup = BeautifulSoup(content, 'lxml')
    all_countries = soup.find(class_='wikitable').find_all('tr')
    for country in all_countries[70:90]:
        country_site_src = country.find('a')['href']
        pl_name = country.find('a')['title']
        country_site_full_src = f"https://pl.wikipedia.org/{country_site_src}"
        country_site_content = requests.get(country_site_full_src).content
        country_soup = BeautifulSoup(country_site_content, 'lxml')
        en = country_soup.find('a', attrs={'lang': 'en'})['title']
        de = country_soup.find('a', attrs={'lang': 'de'})['title']
        es = country_soup.find('a', attrs={'lang': 'es'})['title']
        en_name = en.split(' – ')[0]
        de_name = de.split(' – ')[0]
        es_name = es.split(' – ')[0]
        flag_src_to_convert = country_soup.find('img', attrs={'alt': 'Flaga'})['src']
        flag_src_converted = pattern.findall(flag_src_to_convert)[0]
        flag_full_src = f"https://upload.wikimedia.org/wikipedia/commons/{flag_src_converted}"
        flag_svg = requests.get(flag_full_src).text
        flag_base64 = base64.b64encode(bytes(flag_svg, 'utf-8'))
        myobject = Flags(name=pl_name, flag_base64=flag_base64)
        myobject.save()
        myobject2 = Translations(name=myobject, en_name=en_name, de_name=de_name, es_name=es_name)
        myobject2.save()

        # with open(f"flag2/{y}.svg", 'w') as f:
        #     f.write(flag_img)


