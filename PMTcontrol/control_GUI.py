# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:06:05 2020

@author: chowe7
"""

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import pyvisa as visa
import time

qtCreatorFile = 'control_layout.ui' # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#Create a resource manager
# resources = visa.ResourceManager()
# ps = resources.open_resource('USB0::0x0483::0x7540::NPD3ECAD2R0407::INSTR', write_termination='\n',read_termination = '\n')
# ps.timeout = 2000
        
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # self.psstat_push.clicked.connect(self.ps_status)
        self.recall_button.clicked.connect(self.set_settings)
        self.push_on.clicked.connect(self.switch_on)
        self.push_off.clicked.connect(self.switch_off)
        self.push_disconnect.clicked.connect(self.disconnect)
    

    def ps(self):
        self.resource = visa.ResourceManager()
        ps = self.resource.open_resource('USB0::0x0483::0x7540::NPD3ECAD2R0407::INSTR', write_termination='\n',read_termination = '\n')
        ps.timeout = 2000
        return ps
    
    def ps_status(self):
        # Check its there
        ps =self.ps()
        print(ps.write('*IDN?'))
        time.sleep(0.05)
        print(ps.read('*IDN?'))
    

    def set_settings(self):
        ps =self.ps()
        ps.write('CH1:VOLTage 5')
        time.sleep(0.05)
        ps.write('CH2:VOLTage 5')
        time.sleep(0.05)
        ps.write('CH1:CURRent 0.12')
        time.sleep(0.05)
        ps.write('CH2:CURRent 0.12')
        self.current_voltage.setText('5')
        self.current_current.setText(str.format('{0:.2f}',0.12))
        return ps

    def switch_on(self):
        ps =self.ps()
        ps.write('OUTput CH1,ON')
        time.sleep(0.04)
        ps.write('OUTput CH2,ON')
        self.status_window.setTextColor(QtGui.QColor(255, 51, 0))
        self.status_window.setText('PMTs are on')

    def switch_off(self):
        ps =self.ps()
        ps.write('OUTput CH1,OFF')
        time.sleep(0.04)
        ps.write('OUTput CH2,OFF')
        self.status_window.setTextColor(QtGui.QColor(0, 0, 0))
        self.status_window.setText('PMTs are off')

    def disconnect(self):
        ps =self.ps()
        ps.close()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
