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

import tkextend as tke_





class AdjustContourWindow(tke_.PopUpsMixin, tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.controller = parent.controller

        self._init_geometry()
        self._init_taskbar()
        self._init_canvas()
        
        self.protocol('WM_DELETE_WINDOW', self.close_window)

    def _init_geometry(self):
        self._screenx = self.parent._screenx
        self._screeny = self.parent._screeny

        self.size_x = 500  # self.canvas.winfo_width()
        self.size_y = 500  # self.canvas.winfo_height()
        self.resizable(0, 0)
        self.geometry(f'{self.size_x}x{self.size_y}'
                      + f'+{self._screenx // 2 - self.size_x // 2}'
                      + f'+{self._screeny // 2 - self.size_y // 2}')

        #self.wait_visibility()
        #self.grab_set()

    def _init_taskbar(self):
        self.edit_status = tk.BooleanVar()
        self.edit_status = True
        
        self.frame_taskbar = tk.Frame(self)
        
        # initialises save button
        # =======================
        self._init_btn(file='./_resources/00_save-icon.png', 
                       text='Save current',
                       command=self.save_result)
        
        # initialises undo button 
        # =======================
        self._init_btn(file='./_resources/00_undo-icon.png', 
                       text='Undo',
                       command=self.undo_last_action)
        
        # initialises redo button 
        # =======================
        self._init_btn(file='./_resources/00_redo-icon.png', 
                       text='Redo',
                       command=self.redo_next_action)
        
        # initialises reset button 
        # ========================
        self._init_btn(file='./_resources/00_refresh-icon.png', 
                       text='Reset all changes',
                       command=self.reset_original)
        
        ttk.Separator(self.frame_taskbar, orient=tk.VERTICAL).pack(side=tk.LEFT, 
                                                                   fill=tk.Y, 
                                                                   padx=3)
        
        # initialises select button 
        # =========================
        self._init_btn(file='./_resources/01-select-icon.png', 
                       text='Select',
                       command=self.select_pts)
        
        # initialises zoom in button 
        # ==========================
        self._init_btn(file='./_resources/01_zoom-in.png', 
                       text='Zoom in',
                       command=self.zoom_in)
        
        # initialises zoom out button 
        # ===========================
        self._init_btn(file='./_resources/01_zoom-out.png', 
                       text='Zoom out',
                       command=self.zoom_out)

        # initialises zoom fit button 
        # ===========================
        self._init_btn(file='./_resources/01_zoom-extend.png', 
                       text='Zoom fit',
                       command=self.zoom_fit)
        
        ttk.Separator(self.frame_taskbar, orient=tk.VERTICAL).pack(side=tk.LEFT, 
                                                                   fill=tk.Y, 
                                                                   padx=3)
        
        # initialises add button 
        # ======================
        self._init_btn(file='./_resources/01_add-icon.png', 
                       text='Increase no. of pts',
                       command=self.add_pts)

        # initialises delete button 
        # =========================
        self._init_btn(file='./_resources/01_delete-icon.png', 
                       text='Reduce no. of pts',
                       command=self.delete_pts)
        
        self.frame_taskbar.pack(side=tk.TOP ,fill=tk.X)
        
    def _init_btn(self, image=None, command=None, text=None, file=None):
        _btn = tke_.FlatButton(master=self.frame_taskbar, 
                               image=image, file=file, 
                               hoverbg='#E0DDDD', activebg='#C1CDCD', 
                               command=command)
        _btn.pack(side=tk.LEFT, padx=2)
        tke_.Tooltip(_btn, bg='#F08080', text=text)
    
    def _init_canvas(self):
        self.canvas = tke_.PatchedCanvas(self)
        self.canvas.config(bg='grey')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<Enter>', self._event_enter)
        self.canvas.bind('<Leave>', self._event_leave)
        self.canvas.bind('<Button-1>', self._event_on_click)
        self.canvas.bind('<B1-Motion>', self._event_on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._event_on_release)

    def close_window(self):
        self.message_confirm_save()
        self.parent.parent.deiconify()
        try:
            self.destroy()
        except:
            pass

    def _event_enter(self, event):
        pass
        #self.edit_status = True

    def _event_leave(self, event):
        pass
        #self.edit_status = False

    def _event_on_click(self, event):
        self.start_posx = event.x
        self.start_posy = event.y
        self.tag_highlight = 'rect'

    def _event_on_drag(self, event):
        self.canvas.delete('rect')
        
        if self.edit_status:
            self._create_rectangle(self.start_posx, self.start_posy, 
                                   event.x, event.y, tag=self.tag_highlight, 
                                   fill='#00FFFF', outline='#00EEEE', alpha=.2)
        else:
            self._create_rectangle(self.start_posx, self.start_posy,
                                   event.x, event.y, tag=self.tag_highlight, 
                                   fill='#EEDD82', outline='#F0FFF0', alpha=.2)

    def _event_on_release(self, event):
        self.canvas.delete('rect')

    def _create_rectangle(self, x1, y1, x2, y2, **kwargs):
        tag_ = kwargs.pop('tag')
        
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            colour = self.winfo_rgb(fill) + (alpha, )
            
            
            self.image = PIL.Image.new('RGBA', (abs(x2 - x1), abs(y2 - y1)), 
                                       color=colour)
            self.image = PIL.ImageTk.PhotoImage(self.image)

            self.canvas.create_image(min(x1, x2), min(y1, y2), 
                                     image=self.image, anchor='nw', tag=tag_)
        self.canvas.create_rectangle(x1, y1, x2, y2, tag=tag_, **kwargs)
    
    def undo_last_action(self):
        print('works')
    
    def redo_next_action(self):
        print('here we are')
    
    def reset_original(self):
        pass
    
    def zoom_in(self):
        self.canvas.config(cursor='@./_resources/zoom_in.cur')
        self.edit_status = False
    
    def zoom_out(self):
        pass
    
    def zoom_fit(self):
        pass
    
    def select_pts(self):
        self.canvas.config(cursor='arrow')
        self.edit_status = True
    
    def add_pts(self):
        pass
    
    def delete_pts(self):
        pass
    



