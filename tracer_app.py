# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:28:00 2021

@author: Tom
"""


import tkinter as tk
from win32api import GetMonitorInfo, MonitorFromPoint
import tracer_model as tm
import tracer_view as tv
import tracer_controller as tc



class MainApp(tk.Tk):
    """
    Blueprint of the Main application window. 
    """
    
    def __init__(self):
        super().__init__()
        
        self.title('Image Tracer')
        #self.iconbitmap('./')
        
        model = tm.Model()
        
        view = tv.View(self)
        
        controller = tc.Controller(model, view)
        
        view.set_controller(controller)
    
    

if __name__ == '__main__':
    MainApp().mainloop()

    


