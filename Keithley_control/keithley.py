# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 15:40:07 2018

@author: Firefly
"""
# A scratch interface with the kiethley sourcemeter

import serial
import numpy as np
import xlrd


command_dict = {}
wb = xlrd.open_workbook('D:\Keithley_control\command_list.xlsx')
sh = wb.sheet_by_index(0)   
for i in range(sh.nrows):
    command_name = sh.cell(i,0).value
    command_code = sh.cell(i,1).value
    command_dict[command_name] = command_code



class keithley():
    '''
    This class is designed to talk to a keithley source meter 2401 and use it as a current controller.
    Setting static current in mA is possible.
    Setting a variable length triggered output is also possible.
    Currently not implemented: any error handling.
    '''    
    
    def __init__(self,port,virtual = False):
        self.virtual = virtual
        self.command_dict = command_dict
        self.current_ranges = 10**np.arange(7)*10**-6
        
        if virtual: #for testing without serial communication
            self.port = open('./testing.txt','w')
        else:
            self.port = serial.Serial(port,timeout = 0.1)
        
        self.__write__(self.command_dict['clear'])
        
        self.__write__(self.command_dict['set_current_source'])
        
        
        
    def set_current(self,current_in_ma):
        curr = current_in_ma*10**-3
        best_range = self.__get_best_range__(curr)
        self.__write__(self.command_dict['set_current_range']+' '+str(best_range))
        #set the current level
        self.__write__(self.command_dict['set_current_level']+' '+str(curr))
        
    def turn_on(self):
        self.__write__(self.command_dict['set_output']+' ON')
        
    
    def turn_off(self):
        self.__write__(self.command_dict['set_output']+' OFF')
        

    
    def shutdown(self):
        self.send_abort()
        self.__write__(self.command_dict['turn_off_remote_command'])
        self.port.close()
        
    def set_up_sweep(self,current_in_ma,time):
        current = current_in_ma*10**-3
        self.__sweep_config__(current,time)
        
    def start_sweep_triggered(self):
        self.set_current(0)
        self.__write__(self.command_dict['arm_source_tlink'])
        self.turn_on()
        self.__write__(self.command_dict['init'])
    
    def start_sweep_bus_trig(self):
        self.set_current(0)
        self.__write__(self.command_dict['arm_source_bus'])
        self.turn_on()
        self.__write__(self.command_dict['init'])
        
    def start_sweep_manual_trig(self):
        self.set_current(0)
        self.__write__(self.command_dict['set_trig_line']+' 1')
        self.__write__(self.command_dict['arm_source_manual'])
        self.turn_on()
        self.__write__(self.command_dict['init'])
        
    def start_sweep_no_trig(self):
        self.set_current(0)
        self.__write__(self.command_dict['arm_source_immediate'])
        self.turn_on()
        self.__write__(self.command_dict['init'])
    
    def send_trigger(self):
        self.__write__(self.command_dict['trigger'])
    
    def send_abort(self):
        self.__write__(self.command_dict['abort'])
        
    def send_clear(self):
        self.__write__(self.command_dict['clear'])
        
    def __sweep_config__(self,current,time):
        self.__write__(self.command_dict['set_current_source'])
        best_range = self.__get_best_range__(current)
        self.__write__(self.command_dict['set_current_range']+' '+str(best_range))
        self.__write__(self.command_dict['set_measure_mode']+' "CURR"')
        self.__write__(self.command_dict['custom_current_sweep_mode'])
        self.__write__(self.command_dict['set_sweep_currents']+' '+str(current)+', '+str(0))
        self.__write__(self.command_dict['set_trigger_counts']+' 1')
        self.__write__(self.command_dict['set_delay_length']+' '+str(time))
        self.__write__(self.command_dict['set_arm_count']+' '+str(2500))
        self.__write__(self.command_dict['trigger_source_immediate'])
        
        
    def __get_best_range__(self,current):
        #finds the best range for the current
        best_range = self.current_ranges[np.where(self.current_ranges>=current)[0][0]]
        return best_range
    
    def __write__(self,string):
        if not self.virtual:
            self.port.write((string+'\r').encode())
        else:
            self.port.write((string+'\n'))
        
    def __read__(self):
        msg = self.port.readline()
        return msg