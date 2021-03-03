# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 00:36:22 2020

@author: Nathan Nickelson
"""

import requests
from bs4 import BeautifulSoup
import VideoGameEntry as vge
import re

class Barcode:
    def __init__(self):
        
        self.game_list = []
        self.game_data = vge.VideoGameEntry("stupid", None, None, None, None, None)
        self.base_URL = 'https://www.pricecharting.com/search-products?type=videogames&q='
        self.variant_URL = 'https://www.pricecharting.com'

    def barcode_data(self, barcode, gameVariants, variant):
        
        try:
            gameVariants.clear()
            if ('/game/' in barcode):
                URL = self.variant_URL + barcode
            else:
                URL = self.base_URL + barcode
            
            resp = requests.get(URL)
            #print(URL)
            soup = BeautifulSoup(resp.text, 'html.parser')
            #print(soup)
            stuff = soup.find_all("meta", {'itemprop':'name'})
            #print(stuff)
            variants = soup.find_all('a', class_='variant')
            #print(variants)
            standardSoup = soup.find_all('a', text=re.compile(r'Standard'))
            #print(variants)
            #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            #print(standardSoup)
            if ( standardSoup is not None and len(standardSoup) > 0):
                print('soupy soupy')
                variants.extend(standardSoup)
                #variants.append(standardSoup)
            #print(standardSoup)
            #print(variants)
            for i in variants:
                gameVariants[i.string] = i['href']
                print(gameVariants)
            
            #print(str(stuff).find('<script'))
            y = str(stuff).find('<script')
            x = (str(stuff)[:y])[1:]

            soup2 = BeautifulSoup(x, 'html.parser')
            name_tag = soup2.find('meta',{'itemprop':'name'})
            category_tag = soup2.find('meta',{'itemprop':'applicationCategory'})
            platform_tag = soup2.find('meta',{'itemprop':'gamePlatform'})
            
            
            pricing = [p1 for p1 in ( p4.findAll('td') for p4 in (p2.find('tr') for p2 
                    in (p3.find('tbody') for p3 in soup.findAll('table', {'class':'info_box'})))) if p1]
                
            soup3 = BeautifulSoup(str(pricing[0]), 'html.parser')
        
            used_price = str((soup3.find('td', {'id':'used_price'})).contents[1].contents[0]).strip()
            complete_price = str((soup3.find('td', {'id':'complete_price'})).contents[1].contents[0]).strip()
            new_price = str((soup3.find('td', {'id':'new_price'})).contents[1].contents[0]).strip()
            graded_price = str((soup3.find('td', {'id':'graded_price'})).contents[1].contents[0]).strip()
            box_price = str((soup3.find('td', {'id':'box_only_price'})).contents[1].contents[0]).strip()
            manual_price = str((soup3.find('td', {'id':'manual_only_price'})).contents[1].contents[0]).strip()

            used_price = used_price.replace(',','')
            complete_price = complete_price.replace(',','')
            new_price = new_price.replace(',','')
            graded_price = graded_price.replace(',','')
            box_price = box_price.replace(',','')
            manual_price = manual_price.replace(',','')
            
            name = name_tag['content']
            category = category_tag['content']
            platform = platform_tag['content']
            
            price_list = [used_price, complete_price, new_price, graded_price, box_price, manual_price]
            game_data = vge.VideoGameEntry(name, platform, category, price_list, barcode, variant)
            return game_data, gameVariants
        except:
            print('******************soup error***********************************')

    def variantDict(self, variants, variantsURL):
        pass
    