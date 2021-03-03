def createInsertCollectedGamesProc(self):
        createProc = '''
                    CREATE OR ALTER PROCEDURE [dbo].[InsertCollectedGames](
                    @barcode_num VARCHAR(12),
                    @game_title VARCHAR(100),
                    @game_platform VARCHAR(50),
                    @game_variant VARCHAR(50)
                    )
                    AS
                    BEGIN
                        SET NOCOUNT ON

                        IF NOT EXISTS (
                        SELECT 1 FROM dbo.CollectedGames CG
                        WHERE @barcode_num = CG.barcode
                        AND @game_title = CG.gameTitle
                        AND @game_platform = CG.gamePlatform
                        AND @game_variant = CG.gameVariant)
                        BEGIN
                            INSERT INTO dbo.CollectedGames (barcode, gameTitle, gamePlatform, gameVariant)
                            VALUES
                            (@barcode_num, @game_title, @game_platform, @game_variant)
                        END
                    END
                    '''
        self.cursor.execute(createProc)

def createInsertDefaultPricingOnDatesProc(self):
        createProc = '''
                    CREATE OR ALTER PROCEDURE [dbo].[InsertDefaultPricingOnDatesPICKLES](
                    @barcode_num VARCHAR(12),
                    @game_variant VARCHAR(50),
                    @pricing_date DATE,
                    @loose_price NUMERIC (18,2),
                    @complete_price NUMERIC (18,2),
                    @new_price NUMERIC (18,2),
                    @graded_price NUMERIC (18,2),
                    @box_price NUMERIC (18,2),
                    @manual_price NUMERIC (18,2)
                    )
                    AS
                    BEGIN
                        SET NOCOUNT ON

                        IF NOT EXISTS (
                            SELECT 1 FROM dbo.DefaultPricingOnDates pd
                            WHERE @barcode_num = pd.barcode
                            AND @game_variant = pd.variant
                            AND @pricing_date = pd.pricingDate
                        )
                        BEGIN
                            INSERT INTO dbo.DefaultPricingOnDates
                            (barcode, variant, pricingDate, loosePrice, completePrice, newPrice, gradedPrice, boxPrice, manualPrice)
                            VALUES
                            (@barcode_num, @game_variant, @pricing_date, @loose_price, @complete_price, @new_price, @graded_price, @box_price, @manual_price)
                        END
                    END
                    '''
        self.cursor.execute(createProc)

def createInsertPurchaseTransactionsProc(self):
        createProc = '''
                    CREATE OR ALTER PROCEDURE [dbo].[insertPurchaseTransactionsPICKLES](
                    @barcode VARCHAR(12),
                    @purchase_date DATE,
                    @game_variant VARCHAR(50),
                    @game_condition VARCHAR(50),
                    @standard_price NUMERIC (18,2),
                    @purchase_price NUMERIC (18,2)
                    )
                    AS
                    BEGIN
                        SET NOCOUNT ON

                        DECLARE @game_name VARCHAR(100)
                        SET @game_name = (Select gameTitle from CollectedGames where barcode = @barcode AND gameVariant = @game_variant)

                        INSERT INTO dbo.PurchaseTransactions (barcode, purchaseDate, gameName, gameVariant, gameCondition, standardPrice, purchasePrice)
                        Values
                        (
                        @barcode, @purchase_date, @game_name, @game_variant, @game_condition, @standard_price, @purchase_price
                        )
                    END
                    '''
        self.cursor.execute(createProc)