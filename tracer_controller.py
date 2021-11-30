            # -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:28:00 2021

@author: Tom
"""


import PIL.Image
import PIL.ImageTk





class Controller:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
    def open_image(self, _image_path):
        _image_name = './' + (_image_path[::-1].split('/')[0])[::-1]
        self.view.file_info.config(text=_image_name)
        
        self.model.image_name = _image_name
        self.model.open_image()
        self.pil_image = PIL.ImageTk.PhotoImage(image=self.model.pil_image)
        
    def close_image(self):
        self.model.close_image()
        
    def get_info_about(self):
        return self.model.__doc__
    
    def start_trace(self, direction=None, x=None, y=None):
        if not direction or not x or not y:
            raise ValueError('Something went wrong!')
        else:
            self.model.set_start_position(x, y)
            self.model.start_trace(direction)
            self.check_trace_end()
            
    def check_trace_end(self):
        if self.model.check_trace_end():
            self.view.message_trace_finished()
 
    def save_result(self, _filename):
        self.model.save_contour(filename=_filename)

                
        