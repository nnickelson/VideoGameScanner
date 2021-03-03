# -*- coding: utf-8 -*-

class VideoGameEntry():
    def __init__(self, name, platform, category, prices, barcode, variant):
        self.name = name
        self.platform = platform
        self.category = category
        self.barcode = barcode
        self.variant = variant
        self.prices = self.set_prices(prices)

    #def returnEmptyGameData   
        
    def set_prices(self, prices):
        if (prices is None): 
            return None
        pricing = dict([])
        price_categories = ['Loose','Complete','New','Graded','Box','Manual' ]
        for (p,c) in zip (prices,price_categories):
            pricing[c] = p
        return pricing

    def print_game_data(self):
        print('*****', self.name, self.platform, self.category, self.barcode, self.prices)
