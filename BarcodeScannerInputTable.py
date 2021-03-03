import sys 
from PySide6.QtWidgets import *

class VideoGameVariantButtons(QWidget):
    def __init__(self): 
        super().__init__() 

        self.gameVariantLayout = QVBoxLayout()
        self.setLayout(self.gameVariantLayout)
        

class BarscodeScannerInput(QLineEdit):
    def __init__(self): 
        super().__init__() 


