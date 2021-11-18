# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:28:00 2021

@author: Tom
"""


import numpy as np
import cv2
import PIL.Image
import PIL.ImageTk
import tkinter as tk




class MainApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title('Tracer')
        self.resizable(0, 0)
    
        self.canvas = PuzzleBox(self)
        self.canvas.pack()
        


class PuzzleBox(tk.Canvas):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.config(width=1200, height=900, 
                    highlightthickness=1, highlightbackground='black')
        self.create_rectangle(0, 0, 800, 800)
                
        #_image = cv2.imread('Puzzle_02_cr.jpg', cv2.IMREAD_GRAYSCALE)
        #cv2.imshow('image', _image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        try:
            _image = PIL.Image.open('Puzzle_02_cr2.png')
            self.pil_image = PIL.ImageTk.PhotoImage(image=_image)
            self.create_image((440, 420), image=self.pil_image)
        except AttributeError:
            print('Error has occured. The image is not loaded.')
            
        self.bind('<Button-1>', self.get_coord)
        
    def get_coord(self, event):
        print(f'x = {event.x}, y = {event.y}')
        pos_info = FloatingWindow(event.x, event.y, self.parent)
        pos_info.grab_set()
        
        

class FloatingWindow(tk.Toplevel):
    def __init__(self, *args):
        super().__init__()
        
        self.geometry(f'+{args[2].winfo_rootx()+args[0]}+{args[2].winfo_rooty()+args[1]-20}')
        self.overrideredirect(True)

        pos_info = tk.Label(self, text=f'x = {args[0]}, y = {args[1]}')
        pos_info.pack()
        self.bind('<Motion>', self.hide_pos)

    def hide_pos(self, event):
        self.destroy()

    

    

if __name__ == '__main__':
    window = MainApp()
    window.mainloop()
    


