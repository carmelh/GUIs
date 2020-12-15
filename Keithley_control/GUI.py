# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 17:21:40 2018

@author: Firefly
"""

import sys
from PyQt4 import QtCore, QtGui, uic
import keithley
 
qtCreatorFile = "./keithley_GUI.ui" 
 
Ui_MainWindow, _ = uic.loadUiType(qtCreatorFile)
virtual = False
keithley_com_port = 'COM29'


style_sheet_pressed = """
        .QPushButton {
            background-color: red;
            font: bold;
            }
        """
style_sheet_unpressed = """
        .QPushButton {
            }
        """

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.keithley = keithley.keithley(keithley_com_port,virtual = virtual)
        self.current_status = False
        self.current_value = 0
        self.time_value = 0.1
        self.time_input.setText(str(self.time_value))
        self.repeats_disabled = False
        self.dc_curr_disabled = False
        
        self.on_off_button.clicked.connect(self.toggle_current)
        self.set_current_button.clicked.connect(self.set_current)
        self.set_time_button.clicked.connect(self.set_time)
        self.prepare_repeat_button.clicked.connect(self.prepare_repeat)
        self.start_triggered_button.clicked.connect(lambda: self.start_repeat('triggered'))
        self.start_bus_triggered_button.clicked.connect(lambda: self.start_repeat('bus'))
        self.start_untriggered_button.clicked.connect(lambda: self.start_repeat('untriggered'))
        self.send_trigger_button.clicked.connect(self.send_trigger)
        self.abort_button.clicked.connect(self.abort)
    
    
    def prepare_repeat(self):
        self.keithley.set_up_sweep(self.current_value,self.time_value)
    
    def start_repeat(self,triggering):
        if triggering == 'triggered':
            self.keithley.start_sweep_triggered()
            self.start_triggered_button.setStyleSheet(style_sheet_pressed)
        elif triggering == 'bus':
            self.keithley.start_sweep_bus_trig()
            self.start_bus_triggered_button.setStyleSheet(style_sheet_pressed)
        elif triggering == 'untriggered':
            self.keithley.start_sweep_no_trig()
            self.start_untriggered_button.setStyleSheet(style_sheet_pressed)
        
        self.dc_curr_disabled = True
        self.repeats_disabled = True
        self.__toggle_DC_buttons__()
        self.__toggle_repeat_buttons__()
        
            
    def send_trigger(self):
        self.keithley.send_trigger()
        
    def abort(self):
        self.keithley.send_abort()
        self.keithley.turn_off()
        self.start_triggered_button.setStyleSheet(style_sheet_unpressed)
        self.start_bus_triggered_button.setStyleSheet(style_sheet_unpressed)
        self.start_untriggered_button.setStyleSheet(style_sheet_unpressed)
        self.dc_curr_disabled = False
        self.repeats_disabled = False
        self.__toggle_DC_buttons__()
        self.__toggle_repeat_buttons__()

    def set_current(self):
        self.current_value = float(self.current_input.text())
        self.keithley.set_current(self.current_value)
        self.current_display.setText(str(self.current_value)[:4])
    
    def set_time(self):
        self.time_value = float(self.time_input.text())
        
    def toggle_current(self):
        if self.current_status:
            self.keithley.turn_off()
            self.on_off_button.setStyleSheet(style_sheet_unpressed)
            self.repeats_disabled = False
            self.__toggle_repeat_buttons__()
        else:
            self.keithley.turn_on()
            self.on_off_button.setStyleSheet(style_sheet_pressed)
            self.repeats_disabled = True
            self.__toggle_repeat_buttons__()
               
        self.current_status = not(self.current_status)
        
    def closeEvent(self, event):
        self.keithley.shutdown()
        event.accept()
        
    def __toggle_repeat_buttons__(self):
        for button in [self.prepare_repeat_button, self.start_triggered_button,self.start_untriggered_button,self.start_bus_triggered_button,self.send_trigger_button]:
            button.setDisabled(self.repeats_disabled)
            
    def __toggle_DC_buttons__(self):
        for button in [self.set_current_button, self.set_time_button,self.on_off_button]:
            button.setDisabled(self.repeats_disabled)
        
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())