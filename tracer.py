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
from tkinter import ttk
from tkinter import filedialog
import time
from win32api import GetMonitorInfo, MonitorFromPoint





class MainApp(tk.Tk):
    """
    Blueprint of the Main application window. 
    """
    
    def __init__(self):
        super().__init__()
        
        #self.exit_requested = tk.BooleanVar()
        #self.exit_requested = False
        
        self._image_path = None
        self._image_name = None
        self._image = None
        self.pil_image = None
        self.image_on = None
        
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_area = monitor_info.get('Work')
        self._screenx = work_area[2]
        self._screeny = work_area[3]
        
        self._sizex = 500
        self._sizey = 500
        self._posx = self._screenx // 2 - self._sizex // 2
        self._posy = self._screeny // 2 - self._sizey // 2 - 25
        
        self.geometry(f'{self._sizex}x{self._sizey}+{self._posx}+{self._posy}')
        self.resizable(False, False)
        
        self.title('Image Tracer')
        #self.iconbitmap('./')
        
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.menubar = AddAppMenu(self)
        self.config(menu=self.menubar)
        
        self.image_frame = ImageFrame(self)
        
        self.file_info = tk.Label(self, fg='grey')
        self.file_info.grid(row=1, column=0, sticky='w', padx=(10, 10))
        
        self.position_info = tk.Label(self, fg='grey')
        self.position_info.grid(row=1, column=3, sticky='e', padx=(10, 10))
        
        self.position_info_img = tk.Label(self, fg='grey')
        self.position_info_img.grid(row=1, column=4, sticky='e', padx=(10, 10))
        
        #ttk.Sizegrip(self).grid(row=1, column=5, sticky='e')
        
        # Cutom closing-window handler to enable a safe termination of all 
        # running callbacks before destroying the window. 
        self.protocol('WM_DELETE_WINDOW', self._close_main)
        
    def _close_main(self):
        """
        Safely closes the after() method of the tk.Canvas() and only then 
        closes the main app window by calling the destroy() method. 
        
        NOTE: This ensures that all data processing of the callback is 
        finished without being abruptly killed. 
        
        Returns
        -------
        None.

        """
        try:
            #self.exit_requested = True
            self.destroy()
        except:
            pass
    
    def _get_image(self):
        filetypes = (('image', '*.jpg, *.jpeg'), 
                     ('image', '*.png'))
        self._image_path = filedialog.askopenfilename(title='Open image', 
                                                         initialdir='./', 
                                                         filetypes=filetypes)
        self._image_name = './' + (self._image_path[::-1].split('/')[0])[::-1]
        
        try:
            self._image = PIL.Image.open(self._image_name)
            self.pil_image = PIL.ImageTk.PhotoImage(image=self._image)
            self.image_frame.draw_image(self.pil_image, self._image_name)
        except AttributeError:
            _message = 'Couldn\'t load the image.'
            tk.messagebox.showerror(title='Error 01', message=_message)
        
    def _close_image(self):
        self.file_info.config(text='')
        #self.image_frame.canvas.bind('<Enter>', self.image_frame
        #                                 .canvas.config(cursor='arrow'))
        self.image_frame.canvas.unbind('<Enter>')#, self.image_frame.cursor)
        self.image_frame.canvas.delete(self.image_on)
        self.geometry(f'{self._sizex}x{self._sizey}+{self._posx}+{self._posy}')
        self._image_path = None
        self._image_name = None
        self._image = None
        self.pil_image = None
        self.image_on = None
        
        



class AddAppMenu(tk.Menu):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        
        # By default, Tkinter adds a dashed line before the first menu item. 
        # When the dashed line is clicked, the main window will detach the 
        # menu from it. 
        # To remove the dashed line, the ['tearoff'] property of the menu is 
        # set to False. 
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(label='Open...', underline=0, 
                                   command=self.parent._get_image)
        self.file_menu.add_command(label='Close', underline=0, 
                                   command=self.parent._close_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', underline=1, 
                                   command=self.parent._close_main)
        self.add_cascade(label='File', menu=self.file_menu, underline=0)
        
        self.help_menu = tk.Menu(self, tearoff=False)
        self.help_menu.add_command(label='Welcome')
        self.help_menu.add_command(label='About')
        self.add_cascade(label='Help', menu=self.help_menu, underline=0)
       
        

class ImageFrame(tk.Frame):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.cursor = None ###############################################
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=0)
               
        #self.canvas = ImageBox(self)
        self.canvas = PatchedCanvas(self)
        self.canvas.grid(row=0, column=0, columnspan=6, sticky='ewns')#, padx=3)
        
        self.grid()

    def draw_image(self, pil_image, _image_name):
        try: 
            self.parent.file_info.config(text=_image_name)
            posx = pil_image.width() // 2
            posy = pil_image.height() // 2
            self.parent.image_on = self.canvas.create_image((posx, posy), 
                                                            image=pil_image)
            
            main_posx = self.parent._screenx // 2 - posx
            main_posy = self.parent._screeny // 2 - posy - 25
            self.parent.geometry(f'{posx*2}x{posy*2 + 23}')
            self.parent.geometry(f'+{main_posx}+{main_posy}')
            self.cursor = self.canvas.bind('<Enter>', self.canvas.config(cursor='tcross'))
        except Exception:
            _message = 'Couldn\'t draw the image.'
            tk.messagebox.showerror(title='Error 02', message=_message)
        
        


class PatchedCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__()
        self.config(bg='grey')
        
    def unbind(self, sequence, funcid=None):
        """
        See:
            http://stackoverflow.com/questions/6433369/
            deleting-and-changing-a-tkinter-event-binding-in-python
        """

        if not funcid:
            self.tk.call('bind', self._w, sequence, '')
            return
        func_callbacks = self.tk.call(
            'bind', self._w, sequence, None).split('\n')
        new_callbacks = [
            l for l in func_callbacks if l[6:6 + len(funcid)] != funcid]
        self.tk.call('bind', self._w, sequence, '\n'.join(new_callbacks))
        self.deletecommand(funcid)
        


class ImageBox(tk.Canvas):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self._sizex = 1200
        self._sizey = 805
        self.posx = None
        self.posy = None
        self.pos_info = None
        self.mh = None          # variable to reference the after() method
        
        #self.config(width=self._sizex, height=self._sizey, bg='black', 
        #            highlightthickness=1, highlightbackground='black')
        self.config(bg='grey')#, 
                    #highlightthickness=1, highlightbackground='black')
                
        #_image = cv2.imread('Puzzle_02_cr.jpg', cv2.IMREAD_GRAYSCALE)
        #cv2.imshow('image', _image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        
        
        ###self._init_events()
        #self._motion_halt()
    
    def _init_events(self):
        self.bind('<Enter>', self.config(cursor='tcross'))
        #self.bind('<Motion>', self.parent.footer.)
        #self.bind('<Button-1>', self.get_coord)
        
    def _event_enter(self):
        pass
        
    def get_coord(self):
        """
        Returns the current coordinates of the cursor relative to the 
        app window. 

        Returns
        -------
        posx : int
            Current x coordinate of the cursor.
        posy : int
            Current y coordinate of the cursor.

        """
        posx, posy = self.parent.winfo_pointerxy()
        posx -= self.parent.winfo_rootx()
        posy -= self.parent.winfo_rooty()
        return (posx, posy)

    

    

if __name__ == '__main__':
    MainApp().mainloop()

    


