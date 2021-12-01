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
from win32api import GetMonitorInfo, MonitorFromPoint





class View(tk.Frame):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        #self.parent.lift()
        #self.parent.attributes('-topmost', True)
        
        self._init_main_geometry()
        self._init_menubar()
        self._init_imageframe()
        self._init_footer()
        
        self.controller = None
        
        # Custom closing-window handler to enable a safe termination of all 
        # running callbacks before destroying the window. 
        self.parent.protocol('WM_DELETE_WINDOW', self.close_main)
        self.grid(row=0, column=0, sticky='ewns')
    
    def _init_main_geometry(self):
        """
        Initialises geometry settings of the main app window.

        Returns
        -------
        None.

        """
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_area = monitor_info.get('Work')
        self._screenx = work_area[2]
        self._screeny = work_area[3]
        
        self._sizex = 500
        self._sizey = 500
        self._posx = self._screenx // 2 - self._sizex // 2
        self._posy = self._screeny // 2 - self._sizey // 2 - 25
        
        self.parent.geometry(f'{self._sizex}x{self._sizey}')
        self.parent.geometry(f'+{self._posx}+{self._posy}')
        self.parent.minsize(500, 500)
        self.parent.resizable(1,1)#False, False)
        
        self.parent.columnconfigure(index=0, weight=1)
        self.parent.rowconfigure(index=0, weight=1)
        
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=0)
    
    def _init_menubar(self):
        """
        Initialises the menubar of the main app window. 

        Returns
        -------
        None.

        """
        self.menubar = tk.Menu(self.parent)
        # By default, Tkinter adds a dashed line before the first menu item. 
        # When the dashed line is clicked, the main window will detach the 
        # menu from it. 
        # To remove the dashed line, the ['tearoff'] property of the menu is 
        # set to False. 
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label='Open...', underline=0, 
                                   command=self.open_image)
        self.file_menu.add_command(label='Close', underline=0, 
                                   command=self.close_image)
        self.file_menu.entryconfig(index=1, state='disabled')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', underline=1, 
                                   command=self.close_main)
        self.menubar.add_cascade(label='File', 
                                 menu=self.file_menu, underline=0)
        
        help_menu = tk.Menu(self.menubar, tearoff=False)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About', underline=0, 
                                      command=self.show_info_about)
        self.menubar.add_cascade(label='Help', menu=help_menu, underline=0)
        
        self.parent.config(menu=self.menubar)
    
    def _init_imageframe(self):
        """
        Initialises the Canvas area settings. 

        Returns
        -------
        None.

        """
        self.frame_w_bar = tk.Frame(self)
        self.canvas = PatchedCanvas(self.frame_w_bar)
        #self.canvas = tk.Canvas(self.frame_w_bar, 
        #                            scrollregion=(0, 0, 1000, 800), bg='grey')
        self.canvas.config(scrollregion=(0, 0, 1000, 800), bg='grey')
        self.hbar = ttk.Scrollbar(self.frame_w_bar, orient='horizontal', 
                                      command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, columnspan=6, sticky='ew')
        self.hbar.grid_forget()
        #self.vbar.pack(side='bottom', fill='x', expand=False)#grid(row=1)
        self.vbar = ttk.Scrollbar(self.frame_w_bar, orient='vertical', 
                                      command=self.canvas.yview)
        self.vbar.grid(row=0, column=6, sticky='ns')
        self.vbar.grid_forget()
        self.canvas.config(xscrollcommand=self.hbar.set, 
                           yscrollcommand=self.vbar.set)
        self.canvas.grid(row=0, column=0, columnspan=6, sticky='ewns')
        #self.canvas.pack(side='top', fill='both', expand=True)
        
        self.frame_w_bar.columnconfigure(index=0, weight=1)
        self.frame_w_bar.rowconfigure(index=0, weight=1)
        self.frame_w_bar.grid(row=0, column=0, columnspan=6, sticky='ewns')
    
    def _init_footer(self):
        """
        Initialises footer for main app window.

        Returns
        -------
        None.

        """
        self.file_info = tk.Label(self, text='', fg='grey')
        self.file_info.grid(row=1, column=0, sticky='w', padx=(10, 10))
        
        self.size_info = tk.Label(self, text='', fg='grey', width=8)
        self.size_info.grid(row=1, column=3, sticky='e', padx=(10, 10))
        
        self.position_info = tk.Label(self, text='', fg='grey', width=15)
        self.position_info.grid(row=1, column=4, sticky='e', padx=(10, 10))
        
        ttk.Sizegrip(self).grid(row=1, column=5, sticky='se')
        
    def set_controller(self, controller):
        """
        Sets the controller.

        Parameters
        ----------
        controller : tracer_controller.Controller
            Class onject blueprint. Reference to the app Controller, 
            which links the Viewer to the Model.

        Returns
        -------
        None.

        """
        self.controller = controller
    
    def show_info_about(self):
        """
        Shows information about the application. 

        Returns
        -------
        None.

        """
        _text = self.controller.get_info_about()
        tk.messagebox.showinfo(title='About', message=_text.center(40))
    
    def close_main(self):
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
            self.parent.destroy()
        except:
            pass
    

    ######################################################################
    #                                                                    #
    #                         IMAGE RELATED METHODS                      #
    #                                                                    #
    ######################################################################

    def open_image(self):
        """
        Reads the image. 

        Returns
        -------
        None.

        """
        filetypes = (('image', '*.jpg, *.jpeg'), 
                     ('image', '*.png'))
        _image_path = filedialog.askopenfilename(title='Open image', 
                                                 initialdir='./', 
                                                 filetypes=filetypes)
        if not _image_path:
            return
        self.controller.open_image(_image_path)
        self.draw_image()
        self.file_menu.entryconfig(index=1, state='normal')
    
    def draw_image(self):
        """
        Opens the selected image and initialises the relevant settings 
            > correct placement on canvas, 
            > cursor type over image, 
            > canvas scroll area settings, 
            > information to be displayed as footnote etc. 

        Returns
        -------
        None.

        """
        self._image = self.controller.pil_image
        self.size_info.config(text=f'{self._image.width()}x' 
                                 + f'{self._image.height()}', anchor='w')
        self.position_info.config(text='x, y = ...', anchor='w')
        
        self.tag_cursor = 'cursor'
        self.canvas.tag_bind(self.tag_cursor, '<Enter>', self._event_enter)
        self.canvas.tag_bind(self.tag_cursor, '<Leave>', self._event_leave)
        self.canvas.tag_bind(self.tag_cursor, '<Motion>', self._event_motion)
        self.canvas.tag_bind(self.tag_cursor, '<Button-1>', self._event_click)
        self.canvas.bind('<Configure>', self._event_resize_canvas)
        
        posx = self._image.width() // 2
        posy = self._image.height() // 2
        self.img_drawn = self.canvas.create_image((posx, posy), 
                                                  image=self._image, 
                                                  tag=self.tag_cursor)
        
        self.canvas.config(scrollregion=(0, 0, 
                                         self._image.width(), 
                                         self._image.height()))
        
        # In case the size of the image is larger than that of the image 
        # window, in which it is displayed, it adds the scrollbars and binds 
        # the mouse wheel events to it. 
        if self.canvas.winfo_width() < self._image.width():
            self.hbar.grid(row=1, column=0, columnspan=6, sticky='ew')
            self.canvas.bind('<Shift-MouseWheel>', self._event_hor_scroll)
        if self.canvas.winfo_height() < self._image.height():
            self.vbar.grid(row=0, column=6, sticky='ns')
            self.canvas.bind('<MouseWheel>', self._event_vert_scroll)

    def _event_enter(self, event): 
        """
        Changes cursor type when hovering over image area. 

        Parameters
        ----------
        event : tkinter.Event
            <Enter> - Cursor enters image area.

        Returns
        -------
        None.

        """
        self.canvas.config(cursor='tcross')
        
    def _event_leave(self, event):
        """
        Changes cursor type when leaving image area. 

        Parameters
        ----------
        event : tkinter.Event
            <Leave> - Cursor leaves image area.

        Returns
        -------
        None.

        """
        self.canvas.config(cursor='')
        self.position_info.config(text='x, y = ...', anchor='w')
    
    def _event_motion(self, event):
        """
        Gets cursor position and outputs it to the window footer. 

        Parameters
        ----------
        event : tkinter.Event
            <Motion> - Cursor motion over image area.

        Returns
        -------
        None.

        """
        posx, posy = self.canvas.winfo_pointerxy()
        posx -= self.parent.winfo_rootx()
        posy -= self.parent.winfo_rooty()
        self.position_info.config(text=f'x, y = {posx}, {posy}', anchor='w')

    def _event_resize_canvas(self, event):
        """
        Hides or unhides 'vbar' and 'hbar' based on the size of the opened 
        image and the size of canvas area at the moment of canvas resizing, 
        which activates this function itself.

        Parameters
        ----------
        event : tkinter.Event
            <Configure> - Canvas area resizing.

        Returns
        -------
        None.

        """
        if self._image.width() <= event.width:
            self.hbar.grid_forget()
            self.canvas.unbind('<Shift-MouseWheel>')
        else:
            self.hbar.grid(row=1, column=0, columnspan=6, sticky='ew')
            self.canvas.bind('<Shift-MouseWheel>', self._event_hor_scroll)
        if self._image.height() <= event.height:
            self.vbar.grid_forget()
            self.canvas.unbind('<MouseWheel>')
            self.parent.unbind('<KeyPress>')
            self.parent.unbind('<KeyRelease>')
        else:
            self.vbar.grid(row=0, column=6, sticky='ns')
            self.canvas.bind('<MouseWheel>', self._event_vert_scroll)
            self.parent.bind('<KeyPress>', self._event_key_down)
            self.parent.bind('<KeyRelease>', self._event_key_up)
            self.key_is_pressed = False
    
    def _event_vert_scroll(self, event):
        """
        Scrolls canvas area vertically if 'vbar' is active. 
        
        Check if there is a flag set up for any key press. Otherwise, the 
        'MouseWheel' event would work while any key is held down, 
        e.g. when 'hbar' is not mapped it might scroll the canvas area 
        vertically using the same Shift + MouseWheel combination. To eliminate
        this unwanted behaviour the flag is used. 

        Parameters
        ----------
        event : tkinter.Event
            <MouseWheel> - Vertical scrolling of canvas area.

        Returns
        -------
        None.

        """
        if not self.key_is_pressed:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
    
    def _event_hor_scroll(self, event):
        """
        Scrolls canvas area horizontally if 'hbar' is active. 

        Parameters
        ----------
        event : tkinter.Event
            <Shift-MouseWheel> - Horizontal scrolling of canvas area by 
            key + mouse wheel combination.

        Returns
        -------
        None.

        """
        self.canvas.xview_scroll(int(-1*event.delta/120), 'units')
        
    def _event_key_down(self, event):
        """
        Sets a flag on any key press to simulate button held down event. 

        Parameters
        ----------
        event : tkinter.Event
            <KeyPress> - Any key pressed by the user.

        Returns
        -------
        None.

        """
        if not self.key_is_pressed:
            self.key_is_pressed = True
    
    def _event_key_up(self, event):
        """
        Unsets the flag for button held down event. 

        Parameters
        ----------
        event : tkinter.Event
            <KeyRelease> - Release of the key pressed by the user.

        Returns
        -------
        None.

        """
        self.key_is_pressed = False
    
    def _event_click(self, event):
        """
        Invites the user to start the task (trace of image feature). 

        Parameters
        ----------
        event : tkinter.Event
            <Button-1> - Activates when clicked on the image.

        Returns
        -------
        None.

        """
        QuestionWindow(self, event.x, event.y)
    
    def message_trace_finished(self):
        """
        Informs the user about the successful completion of task and provides
        an option to save the result in an external file. 

        Returns
        -------
        None.

        """
        _message = 'Trace finished.\n\nSave traced contour to file?'
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
            self.message_trace_finished()
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
    
    def close_image(self):
        """
        Delets the image from the canvas and the image infromation contained
        in the footer. 
        Hides the scrollbars. 
        Closes the image file. 

        Returns
        -------
        None.

        """
        self.canvas.delete(self.img_drawn)
        self.controller.close_image()
        
        self.canvas.unbind('<Configure>')
        
        self.hbar.grid_forget()
        self.vbar.grid_forget()
        
        self.file_info.config(text='')
        self.position_info.config(text='')
        self.size_info.config(text='')
        
        self.file_menu.entryconfig(index=1, state='disabled')





class QuestionWindow(tk.Toplevel):
    
    def __init__(self, parent, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.contr = parent.controller
        self.title('Please Select')
        self.resizable(0, 0)
        self.geometry('200x90')
        self.geometry(f'+{parent.winfo_rootx() - 107 + x}' 
                      + f'+{parent.winfo_rooty() - 65 + y}')
        #self.overrideredirect(True)
        #self.transient(True)
        self.attributes('-toolwindow', True)
        self.focus_set()
        
        _label = tk.Label(self, text='Start trace to the...')
        _label.pack(side='top', pady=10)#fill='x', expand=True)
        
        self.l_icon = tk.PhotoImage(file='./_resources/left.png')
        _left = ttk.Button(self, text=' Left', width=8, 
                           image=self.l_icon, compound=tk.LEFT, 
                           command=lambda: self._event_btn_clicked('LEFT'))
        _left.pack(side='left', padx=10, pady=10, fill='x')
        
        self.r_icon = tk.PhotoImage(file='./_resources/right.png')
        _right = ttk.Button(self, text='Right ', width=8, 
                            image=self.r_icon, compound=tk.RIGHT, 
                            command=lambda: self._event_btn_clicked('RIGHT'))
        _right.pack(side='right', padx=10, pady=10, fill='x')
        
        #_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        #_cancel.pack(side='bottom', pady=10)
        
    def _event_btn_clicked(self, direction):
        self.destroy()
        self.contr.start_trace(direction=direction, x=self.x, y=self.y)
        
        
       
    

class PatchedCanvas(tk.Canvas):
    """
    A fix for the tk.Canvas class, specifically of the 'unbind' method. 
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
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
        


