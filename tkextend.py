# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:28:00 2021

@author: Tom
"""


import PIL.Image
import PIL.ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from abc import abstractmethod

from tk_button import *
from tk_canvas import *




class PopUpsMixin:
    """
    Used with the MVC GUI design approach. 
    It is necessary to define the 'controller.save_result()' method and 
    to set the controller in the main application. 
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = None
    
    @abstractmethod
    def set_controller(self, controller):
        pass
    
    def message_confirm_save(self):
        """
        Provides an option to save the result in an external file. 

        Returns
        -------
        None.

        """
        _message = 'Save result to file?'
        _result = tk.messagebox.askquestion(title='Confirmation', 
                                            message=_message)
        if _result == 'yes':
            self.save_result()
        else: 
            self.message_confirm_delete()
    
    def message_confirm_delete(self):
        """
        Invites the user to confirm the possible loss of the result. 

        Returns
        -------
        None.

        """
        _message = 'Are you sure?\n\nResult will be lost!!'
        _result = tk.messagebox.askquestion(title='Warning', default='no', 
                                            message=_message, icon='warning')
        if _result == 'no':
            self.message_confirm_save()
        else:
            pass
        
    def save_result(self):
        """
        Saves the result into an external file. 

        Returns
        -------
        None.

        """
        _filename = filedialog.asksaveasfilename(confirmoverwrite=False, 
                                                 defaultextension='.txt')
        if _filename:
            self.controller.save_result(_filename)
        else:
            self.message_confirm_delete()





