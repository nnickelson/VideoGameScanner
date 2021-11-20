import sys
from PySide6 import QtCore
from PySide6.QtCore import Slot, QTimer
from PySide6.QtGui import ( QPalette,  QColor, QImage, QPixmap, QFont )
from PySide6.QtWidgets import (QMainWindow, QStackedLayout, QWidget, QPushButton, 
                             QApplication, QGridLayout, QVBoxLayout, QSizePolicy, QLabel, QHBoxLayout )

from BarcodeScannerInputTable import *
from GamePriceTableView import *
from BarcodeInfo import Barcode
import MainPageInfoHandler as mp
from VideoGameSqlHandler import *


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        #self.dbTableConnection = SqLite()

        self.mainWidget = QWidget()
    
        self.setWindowTitle("Video Game Scanner Inventory")
        self.left = 2500
        self.top = 100
        self.width = 1200
        self.height = 900
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.mainWindowGrid = QGridLayout()
        
        self.barcode = Barcode()
        self.barcodeNumber = None

        # Stores info on a single game
        self.videoGameInfo = None
        # A List of video games
        self.videoGameInfoList = []
        

        self.gameVariantDict = dict([])
        self.variant = 'Standard'

        self.dbHandler = SqlHandler()


        
        # Barcode Number and Game Variant Buttons
        self.barcodeWindow = QWidget()
        self.setBackgroundColor(self.barcodeWindow, 'orange')

        self.barcodeListLayout = QGridLayout()
        self.barcodeScannerInput = BarscodeScannerInput()
        self.barcodeScannerInput.textChanged.connect(self.updateGamePriceTable)
        
        self.variantButtonList = []
        self.variantButtons = VideoGameVariantButtons()
        self.standardBarcode = ''

        self.barcodeListLayout.addWidget(self.barcodeScannerInput, 0,0)
        self.barcodeListLayout.addWidget(self.variantButtons, 1,0)
        self.barcodeWindow.setLayout(self.barcodeListLayout)

        self.mainWindowGrid.addWidget(self.barcodeWindow, 0, 1, 2, 2)   
        
        # Console Label - Unused (potentially for game logos)
        self.barcodeWindow2 = QWidget()
        self.setBackgroundColor(self.barcodeWindow2, 'blue')
       
        self.flashyBoxLayout = QGridLayout()
        self.barcodeWindow2.setLayout(self.flashyBoxLayout)

        self.mainWindowGrid.addWidget(self.barcodeWindow2, 0, 3, 2, 2)
        
        # Side Buttons
        self.barcodeWindow3 = QWidget()
        self.setBackgroundColor(self.barcodeWindow3, 'grey')
        self.mainWindowGrid.addWidget(self.barcodeWindow3, 0, 0, 4, 1)
        #------ Button List
        self.layout = QVBoxLayout()
        
        self.b1 = QPushButton("Process Table")
        self.layout.addWidget(self.b1)
        self.b1.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)
        self.b1.clicked.connect(self.processTableAndInfo)
        
        self.b2 = QPushButton("Button2")
        self.layout.addWidget(self.b2)
        self.b2.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)
        
        self.b3 = QPushButton("Button3")
        self.layout.addWidget(self.b3)
        self.b3.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)
        
        self.b4 = QPushButton("Button4")
        self.layout.addWidget(self.b4)
        self.b4.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)
        
        self.barcodeWindow3.setLayout(self.layout)
        
        self.barcodeWindow4 = QWidget()
        self.setBackgroundColor(self.barcodeWindow4, 'pink')
        
        self.mainWindowGrid.addWidget(self.barcodeWindow4, 2, 1, 2, 4)

        ################ Pricing and Table Widget ####################################
        
        self.gridLayout = QGridLayout()
        self.barcodeWindow4.setLayout(self.gridLayout)

        #------- unprocessed table values -----------------
        self.gamePriceWidget = QWidget()
        self.setBackgroundColor(self.gamePriceWidget, 'blue')
        self.gamePriceTableLayout = QVBoxLayout()
        self.gamePriceTable = TableView()
        self.gamePriceTable.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.gamePriceTableLayout.addWidget(self.gamePriceTable)
        self.gamePriceWidget.setLayout(self.gamePriceTableLayout)
        self.gridLayout.addWidget(self.gamePriceWidget, 0,0,2,6)
        
        #------- verify game info labels ------------------
        self.gameInfoWidget = QWidget()
        self.setBackgroundColor(self.gameInfoWidget, 'indigo')
        self.gameInfoLayout = QGridLayout()
        self.gameInfoWidget.setLayout(self.gameInfoLayout)
        self.gridLayout.addWidget(self.gameInfoWidget, 3,0,1,6)
        
        self.gameNameBox = QLineEdit()
        self.gameSystemBox = QLineEdit()
        self.gameUsedPrice = QLineEdit()
        self.gameCompletePrice = QLineEdit()
        self.gameNewPrice = QLineEdit()
        self.totalPriceLabel = QLabel()

        self.totalPriceLabel.setFont(QFont('Arial', 15))

        self.setBackgroundColor(self.totalPriceLabel, 'beige')

        self.gameNameBox.setAlignment(QtCore.Qt.AlignCenter)
        self.gameSystemBox.setAlignment(QtCore.Qt.AlignCenter)
        self.gameUsedPrice.setAlignment(QtCore.Qt.AlignCenter)
        self.gameCompletePrice.setAlignment(QtCore.Qt.AlignCenter)
        self.gameNewPrice.setAlignment(QtCore.Qt.AlignCenter)

        self.gameInfoLayout.addWidget(self.gameNameBox, 0,0,1,3)
        self.gameInfoLayout.addWidget(self.gameSystemBox, 1,0,1,3)
        self.gameInfoLayout.addWidget(self.totalPriceLabel, 0,4,2,2)
        self.gameInfoLayout.addWidget(self.gameUsedPrice, 2,0,1,2)
        self.gameInfoLayout.addWidget(self.gameCompletePrice, 2,2,1,2)
        self.gameInfoLayout.addWidget(self.gameNewPrice, 2,4,1,2)
        
        
        
        #------------Button Box --------------------------------    
        self.horizontalGroupBox = QGroupBox("Which Price To Use?")
        self.buttonLayout = QGridLayout()
        self.horizontalGroupBox.setLayout(self.buttonLayout)
        self.gridLayout.addWidget(self.horizontalGroupBox, 6,0,1,6)
        
        self.buttonLoose = QPushButton('Loose Price', self)
        self.buttonLoose.clicked.connect(self.on_click)
        self.buttonLayout.addWidget(self.buttonLoose, 0,0,1,1)
        
        self.buttonComplete = QPushButton('Complete Price', self)
        self.buttonComplete.clicked.connect(self.on_click)
        self.buttonLayout.addWidget(self.buttonComplete, 0,1,1,1)
        
        self.buttonNew = QPushButton('New Price', self)
        self.buttonNew.clicked.connect(self.on_click)
        self.buttonLayout.addWidget(self.buttonNew, 0,2,1,1)

        self.label1 = QLabel('Alternative Bulk Price')
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLayout.addWidget(self.label1, 1,1,1,1)

        self.label2 = QLabel('Alternative Single Price')
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLayout.addWidget(self.label2, 1,2,1,1)

        self.orderNumber = QLineEdit('Bad Info', self)
        self.buttonLayout.addWidget(self.orderNumber, 2,0,1,1)
        self.orderNumber.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.orderNumber.setAlignment(QtCore.Qt.AlignCenter)

        self.bulkPrice = QLineEdit()
        self.buttonLayout.addWidget(self.bulkPrice, 2,1,1,1)
        self.bulkPrice.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.bulkPrice.setAlignment(QtCore.Qt.AlignCenter)

        self.singleAltPrice = QLineEdit('')
        self.buttonLayout.addWidget(self.singleAltPrice, 2,2,1,1)
        self.singleAltPrice.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.singleAltPrice.setAlignment(QtCore.Qt.AlignCenter)

        self.bulkPriceCheckbox = QCheckBox('Order Number')
        self.buttonLayout.addWidget(self.bulkPriceCheckbox, 1,0)
        #-------------------------------------------------------------
        
        ##################################################
        
        self.mainWidget.setLayout(self.mainWindowGrid)
        self.setCentralWidget(self.mainWidget)
        
        self.show()

    def setBackgroundColor(self, widget, color):
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        palette.setColor(QPalette.Window, QColor(color))
        widget.setPalette(palette)

          
    def closeEvent(self,event):
        print('I Quit')
        self.dbHandler.conn.close()
        QApplication.quit()

    #When you click 'Loose Price','Complete Price','New Price'
    #This slot puts that info on the table
    @Slot()
    def on_click(self):
        mp.putGameInfoInTable(self, self.sender().text(), self.gamePriceTable, self.barcodeNumber)
        self.barcodeScannerInput.setFocus()

    #Once a barcod has star, this slot processes it
    @Slot(str)
    def updateGamePriceTable(self, barcode):
        if ('*' in barcode):
            self.barcodeNumber = barcode.strip('*')
            self.standardBarcode = self.barcodeNumber
            self.barcodeScannerInput.clear()
            print(barcode)
            mp.readBarcodesFromMain(self, self.barcodeNumber, self.barcodeNumber)

    # Clicking Process Table button - clears the table and enters is into the database
    @Slot()
    def processTableAndInfo(self):
        if (len(self.videoGameInfoList) < 1):
            return
        self.dbHandler.processMainWindowTable(self.videoGameInfoList, self.gamePriceTable)
        self.bulkPrice.clear()
        self.totalPriceLabel.clear()

    # Some games variants with different prices. When clicking on a button, this slot handles swapping prices
    @Slot()
    def variantClicked(self):
        self.variant = self.sender().text()
        variantURL = self.gameVariantDict[self.sender().text()]
        items = (self.variantButtons.gameVariantLayout.itemAt(i) for i in range(self.variantButtons.gameVariantLayout.count()))
        for btn in items:
            btn.widget().deleteLater()
        mp.readBarcodesFromMain(self, variantURL, self.standardBarcode)
        pass
            