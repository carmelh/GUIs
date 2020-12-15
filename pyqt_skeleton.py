# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:06:05 2020

@author: chowe7
"""

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets


qtCreatorFile = 'NAME.ui' # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())