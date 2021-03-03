import sys 
from PySide6.QtWidgets import *


class TableView(QTableWidget):
    def __init__(self): 
        super().__init__() 

        self.setColumnCount(9)
        #self.setRowCount(0)
        self.rowDict = dict()

        self.headerLabels = ['Barcode','Game Name', 'Platform', 'Category','Loose Price', 'Complete Price', 'New Price', 'Owned Condition', 'Owned Purchase Price', 'Variant']
        self.setHorizontalHeaderLabels(self.headerLabels)
        
        #Table will fit the screen horizontally 
        self.horizontalHeader().setStretchLastSection(True) 
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.setRowDict(self.headerLabels)

    def addRow(self, gameData, condition, price, barcode):
        if gameData == None: 
            return

        gameData.print_game_data()
        
        row = self.rowCount()
        self.setRowCount(row + 1)
        
        
        print('row = {}'.format(row))
        self.setItem(row, self.rowDict['Barcode'], QTableWidgetItem(barcode))
        self.setItem(row, self.rowDict['Game Name'], QTableWidgetItem(gameData.name))
        self.setItem(row, self.rowDict['Platform'], QTableWidgetItem(gameData.platform))
        self.setItem(row, self.rowDict['Category'], QTableWidgetItem(gameData.category))
        self.setItem(row, self.rowDict['Loose Price'], QTableWidgetItem(gameData.prices.get('Loose')))
        self.setItem(row, self.rowDict['Complete Price'], QTableWidgetItem(gameData.prices.get('Complete')))
        self.setItem(row, self.rowDict['New Price'], QTableWidgetItem(gameData.prices.get('New')))
        self.setItem(row, self.rowDict['Owned Condition'], QTableWidgetItem(condition))
        self.setItem(row, self.rowDict['Owned Purchase Price'], QTableWidgetItem(price))
        
    def setRowDict(self, headers):
        col = 0
        for i in headers:
            self.rowDict[i] = col
            col += 1


        
    
        