# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:06:05 2020

@author: chowe7
"""

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets


qtCreatorFile = 'tlef_calc.ui' # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.push_dlam.clicked.connect(self.CalculateDLam)
        self.push_flem.clicked.connect(self.CalculateTLEM)
        
    def CalculateDLam(self):
        c=3e8
        if self.tbp_ip.toPlainText() == "":
            tbp=0.44
        else:
            tbp=float(self.tbp_ip.toPlainText())
        fsec = float(self.pulse_duration.toPlainText())*10e-16
        lam = float(self.lam_ip.toPlainText())*10e-10
        dlam = (tbp  * lam**2)/(fsec*c)
        dlam_string = str.format('{0:.2f}',dlam/10e-10)
        self.dlam_result.setText(dlam_string)
        return dlam
        

    def CalculateTLEM(self):
        if self.bad_ip.toPlainText() == "":
            bad=14.4e-3
        else:
            bad=float(self.bad_ip.toPlainText())
        
        mag = float(self.mag_ip.toPlainText())
        lines_mm = float(self.grating.toPlainText())
        dlam = self.CalculateDLam()
        
        if self.comboBox.currentText() == "Olympus":
            tube_old=180
            self.tube_result.setText('180 mm')
        elif self.comboBox.currentText() == "Nikon":
            tube_old=200
            self.tube_result.setText('200 mm')
        elif self.comboBox.currentText() == "Zeiss":
            tube_old=165
            self.tube_result.setText('165 mm')

        
        flem = bad / (dlam * lines_mm)  
        flem_string = str.format('{0:.2f}',flem)
        eff_mag = mag * (flem / tube_old)
        eff_mag_string = str.format('{0:.2f}',eff_mag)
        self.flem_result.setText(flem_string)
        self.effmag_result.setText(eff_mag_string)
 
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())