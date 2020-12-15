# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 09:29:23 2018

@author: Firefly
"""

import unittest
from keithley import keithley


class TestKeithley(unittest.TestCase):
    
    def setUp(self):
        self.keithley = keithley(0,virtual = True)
    
    def test_ranging(self):
        self.assertEqual(self.keithley.__get_best_range__(0.9),1)
        


if __name__ == '__main__':
    unittest.main()