
def createCollectedGamesTable(self):
        createTable = '''
                    IF NOT EXISTS(
                        SELECT * FROM sys.tables WHERE name = 'CollectedGames'
                        AND schema_id = SCHEMA_ID('dbo')
                    )
                    CREATE TABLE [dbo].[CollectedPickles](
                    [barcode] [varchar](12) NOT NULL,
	                [gameTitle] [varchar](100) NOT NULL,
                    [gamePlatform] [varchar](50) NOT NULL,
	                [gameVariant] [varchar](50) NOT NULL,
                    PRIMARY KEY (barcode, gameVariant)
                    )'''
        self.cursor.execute(createTable)

def createDefaultPricingOnDatesTable(self):
        createTable = '''
                    IF NOT EXISTS(
                        SELECT * FROM sys.tables WHERE name = 'DefaultPricingOnDates'
                        AND schema_id = SCHEMA_ID('dbo')
                    )
                    CREATE TABLE [dbo].[DefaultPricingOnDates](
                    [barcode] [varchar](12) NOT NULL,
                    [variant] [varchar](50) NOT NULL,
                    [pricingDate] [date] NOT NULL,
                    [loosePrice] [numeric](18, 2) NULL,
                    [completePrice] [numeric](18, 2) NULL,
                    [newPrice] [numeric](18, 2) NULL,
                    [gradedPrice] [numeric](18, 2) NULL,
                    [boxPrice] [numeric](18, 2) NULL,
                    [manualPrice] [numeric](18, 2) NULL,
                    PRIMARY KEY (barcode, pricingDate, variant),
                    FOREIGN KEY (barcode, variant) REFERENCES dbo.CollectedGames(barcode, gameVariant)
                    )'''
        self.cursor.execute(createTable)

def createPurchaseTransactionsTable(self):
        createTable = '''
                    IF NOT EXISTS(
                        SELECT * FROM sys.tables WHERE name = 'PurchaseTransactions'
                        AND schema_id = SCHEMA_ID('dbo')
                    )
                    CREATE TABLE [dbo].[PurchaseTransactions](
                    [purchaseId] [int] IDENTITY(1,1) NOT NULL,
                    [barcode] [varchar](12) NOT NULL,
                    [purchaseDate] [date] NOT NULL,
                    [gameName] [varchar](100) NOT NULL,
                    [gameVariant] [varchar](50) NOT NULL,
                    [gameCondition] [varchar](50) NOT NULL,
                    [standardPrice] [numeric](18, 2) NOT NULL,
                    [purchasePrice] [numeric](18, 2) NOT NULL,
                    PRIMARY KEY (purchaseId),
                    FOREIGN KEY (barcode, gameVariant) REFERENCES dbo.CollectedGames(barcode, gameVariant)
                    )'''
        self.cursor.execute(createTable)