import pyodbc
import copy
from datetime import date
from MainPageInfoHandler import convertPriceToDecimal as cpd
from DatabaseCreation import CreateSQLTables as cst
from DatabaseCreation import CreateSQLStoredProcs as cssp
from DatabaseCreation import MySQLConnection as msc 
from DatabaseCreation import SQLConnection as sqlc

class SqlHandler():
    def __init__(self):

        self.CONNECTION_STRING = msc.connectionString()
        #self.CONNECTION_STRING = sqlc.connectionString()

        self.conn = pyodbc.connect(self.CONNECTION_STRING)
        self.conn.autocommit = True
        
        self.cursor = self.conn.cursor()
        self.tablesAndProcsInit()

    def insertCollectedGamesProc(self, barcode, gameTitle, gamePlatform, gameVariant):
        storedProc = "Exec [dbo].[insertCollectedGames] ?, ?, ?, ?"
        params = (barcode, gameTitle, gamePlatform, gameVariant)
        self.cursor.execute(storedProc, params)

    def insertDefaultPricingOnDatesProc(self, barcode, gameVariant, pricingDate, loosePrice, completePrice, newPrice, gradedPrice, boxPrice, manualPrice):
        storedProc = "Exec [dbo].[insertDefaultPricingOnDates] ?,?,?,?,?,?,?,?,?" 
        params = (barcode, gameVariant, pricingDate, loosePrice, completePrice, newPrice, gradedPrice, boxPrice, manualPrice)
        self.cursor.execute(storedProc, params)
    
    def insertPurchaseTransactionProc(self, barcode, purchaseDate, gameVariant, gameCondition, standardPrice, purchasePrice):
        storedProc = "Exec [dbo].[insertPurchaseTransactions] ?,?,?,?,?,?"
        params = (barcode, purchaseDate, gameVariant, gameCondition, standardPrice, purchasePrice)
        self.cursor.execute(storedProc, params)

    def processMainWindowTable(self, videoGameList, table):
        condition = ''
        for i in range(len(table.headerLabels)):
            if table.headerLabels[i] == 'Owned Condition':
                condition = table.item(0,i).text()
        
        for videoGameInfo in videoGameList:
            print(videoGameInfo.barcode +'**barcode') 
            print(videoGameInfo.name +'**Game Name') 
            print(videoGameInfo.platform + '**Game Platform')
            
            self.insertCollectedGamesProc(videoGameInfo.barcode, videoGameInfo.name, videoGameInfo.platform, videoGameInfo.variant)
            self.insertDefaultPricingOnDatesProc(videoGameInfo.barcode, videoGameInfo.variant, str(date.today()), cpd(videoGameInfo.prices['Loose']), cpd(videoGameInfo.prices['Complete']), 
                cpd( videoGameInfo.prices['New']), cpd(videoGameInfo.prices['Graded']), cpd(videoGameInfo.prices['Box']), cpd(videoGameInfo.prices['Manual']))

            condCol = table.rowDict['Owned Condition']
            condition = table.item(0, condCol).text()
            self.insertPurchaseTransactionProc(videoGameInfo.barcode, date.today(), videoGameInfo.variant, condition, 
                cpd(table.item(0, table.rowDict[condition]).text()), cpd(table.item(0, table.rowDict['Owned Purchase Price']).text()))
                    
            table.removeRow(0)
            
        videoGameList.clear()
        

    def tablesAndProcsInit(self):
        cst.createCollectedGamesTable(self)
        cst.createDefaultPricingOnDatesTable(self)
        cst.createPurchaseTransactionsTable(self)
        cssp.createInsertCollectedGamesProc(self)
        cssp.createInsertDefaultPricingOnDatesProc(self)
        cssp.createInsertPurchaseTransactionsProc(self)

    


