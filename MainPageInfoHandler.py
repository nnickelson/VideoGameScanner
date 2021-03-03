import VideoGameEntry as veg
import BarcodeInfo as bc
import GamePriceTableView as pt
import re
from PySide6.QtGui import ( QPalette,  QColor)
from PySide6.QtWidgets import (QTableWidgetItem, QPushButton)
from copy import deepcopy

def readBarcodesFromMain(self, barcode, standardBarcode):

    if (len(barcode) > 12 and '/game/' not in barcode):
        self.barcodeScannerInput.clear()
        return
    
    barcodeObj = bc.Barcode()
    self.videoGameInfo, self.gameVariantDict = barcodeObj.barcode_data(barcode, self.gameVariantDict, self.variant)

    if (barcode != standardBarcode):
        self.videoGameInfo.barcode = standardBarcode

    addVariantButtons(self, self.gameVariantDict)

    if (self.videoGameInfo is None):
        print('No data')
        return
    else:
        self.videoGameInfo.print_game_data()

    self.gameNameBox.setText(self.videoGameInfo.name)
    self.gameSystemBox.setText(self.videoGameInfo.platform)
    self.gameUsedPrice.setText(self.videoGameInfo.prices.get('Loose'))
    self.gameCompletePrice.setText(self.videoGameInfo.prices.get('Complete'))
    self.gameNewPrice.setText(self.videoGameInfo.prices.get('New'))


def putGameInfoInTable(self, btnText, table, barcode):
    
    if (self.videoGameInfo is None):
        print('No data --------------------------------------------------------------------------------------------------------------------')
        return
    else:
        self.videoGameInfo.print_game_data()

    price = None
    if (btnText == 'Loose Price'):
        price =  self.gameUsedPrice.text()
    if (btnText == 'Complete Price'):
        price =  self.gameCompletePrice.text()
    if (btnText == 'New Price'):
        price =  self.gameNewPrice.text()

    if (len(self.singleAltPrice.text()) > 0):
        try:
            price = convertDecimalToDollars(self.singleAltPrice.text())
        except:
            #set some error
            return
    
    table.addRow(self.videoGameInfo, btnText, price, barcode)
    if (len(self.bulkPrice.text())> 0):
        convertToBulkpricing(self, table)
    tablePriceSum(self, table)
    
    clearBoxes(self)

def readBarcodeFromFrame(self, frame):
    if (frame is not None):
            self.newBarcode = self.barcode.read_barcodes(frame)
            if (len(self.newBarcode) == 12 and self.newBarcode != self.oldBarcode):
                self.gameDataLineEdit.setText(self.newBarcode)
                self.oldBarcode = self.newBarcode

def clearBoxes(self):
    self.gameNameBox.clear()
    self.gameSystemBox.clear()
    self.gameUsedPrice.clear()
    self.gameCompletePrice.clear()
    self.gameNewPrice.clear()
    self.singleAltPrice.clear()
    self.barcodeScannerInput.clear()

    items = (self.variantButtons.gameVariantLayout.itemAt(i) for i in range(self.variantButtons.gameVariantLayout.count()))
    for btn in items:
        btn.widget().deleteLater()

    self.videoGameInfoList.append(deepcopy(self.videoGameInfo))
    self.videoGameInfo = None
    self.variant = 'Standard'
    print(len(self.videoGameInfoList))


def tablePriceSum(self, gameTable):
    total = 0
    col = gameTable.rowDict['Owned Purchase Price']
    #print(col)
    model = gameTable.model()
    #print(gameTable.rowCount())
    for row in range(model.rowCount()):
        index = model.index(row, col)
        price = str(model.data(index))
        print(price)
        total = total + convertPriceToDecimal(price)
    self.totalPriceLabel.setText(convertDecimalToDollars(total))


def convertPriceToDecimal(dollars):
    priceString = dollars.strip('$').strip(',')
    try:
        price = float(priceString)
    except:
        return 0.0
    return price

def convertDecimalToDollars(numDec):
    if(isinstance(numDec, str)):
        numDec = convertPriceToDecimal(numDec)
    if (str(numDec) != '$'):
        return '${:.2f}'.format(numDec)
    else:
        return numDec


def convertToBulkpricing(self, gameTable):
    #needs editing
    print('%^&%^&%^&%^&%^&')
    print(self.bulkPrice.text())
    bulkPrice =  convertPriceToDecimal(self.bulkPrice.text())
    totalPrice = standardTotalPricing(self, gameTable)
    print('bulk price = ' + str(bulkPrice))
    print('total price = ' + str(totalPrice))
    print('factor change = ' + str(bulkPrice/totalPrice))
    total = 0
    col = gameTable.rowDict['Owned Purchase Price']
    for i in range(gameTable.rowCount()):
        condition = (gameTable.item(i, gameTable.rowDict['Owned Condition'])).text()
        stdPrice = (gameTable.item(i, gameTable.rowDict[condition])).text()
        price = convertPriceToDecimal(stdPrice)
        newPrice = QTableWidgetItem(str(round((price * bulkPrice/totalPrice), 2)))
        gameTable.setItem(i, col, newPrice)

def standardTotalPricing(self, gameTable):
    total = 0
    for i in range(gameTable.rowCount()):
        priceType = gameTable.item(i, gameTable.rowDict['Owned Condition'])
        print('************************************()()()()()()()()')
        print(priceType.text())
        print(gameTable.rowDict.keys())
        print(gameTable.rowDict.values())
        col = gameTable.rowDict[priceType.text()]
        price = convertPriceToDecimal((gameTable.item(i, col)).text())
        total = total + price
    print(total)
    return total

def addVariantButtons(self, variantDict):
    for v in variantDict:
        btn = QPushButton(v.string)
        btn.clicked.connect(self.variantClicked)
        self.variantButtonList.append(btn)
        self.variantButtons.gameVariantLayout.addWidget(btn)




