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
    """
    Blueprint of the Main application window. 
    """
    
    def __init__(self):
        super().__init__()
        
        self.title('Tracer')
        self.resizable(0, 0)
            
        self.canvas = ImageBox(self)
        self.canvas.pack()
        
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
            self.canvas.after_cancel(self.canvas.mh)
            self.destroy()
        except:
            pass
        


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
        
        self.config(width=self._sizex, height=self._sizey, 
                    highlightthickness=1, highlightbackground='black')
        #self.create_rectangle(0, 0, 800, 800)
                
        #_image = cv2.imread('Puzzle_02_cr.jpg', cv2.IMREAD_GRAYSCALE)
        #cv2.imshow('image', _image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        try:
            _image = PIL.Image.open('Puzzle_02_cr2.png')
            self.pil_image = PIL.ImageTk.PhotoImage(image=_image)
            self.create_image((425, 403), image=self.pil_image)
        except AttributeError:
            print('Error has occured. The image couldn\'t be loaded.')
            
        #self.bind('<Button-1>', self.get_coord)
        self._motion_halt()
        
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
    
    def _motion_halt(self):
        """
        Checks the movement of cursor, and when movement stops it creates a 
        floating window with the x, y coordinates appearing near the cursor. 
        
        NOTE: It's a custom 'event'-like feature, as there is only event for
        <Motion> available in tkinter, but no event for <<Motion-stopped>>. 

        Returns
        -------
        None.

        """
        posx, posy = self.get_coord()
        if (self.posx, self.posy) == (posx, posy):
            self.pos_info = FloatingPosWindow(posx, posy, self)
            #self.pos_info.grab_set()
        else:
            self.posx, self.posy = (posx, posy)
            
        # The after() method to create a callback to this function,  
        # which will be executed in the main loop as scheduled when the main 
        # thread is not busy.
        self.mh = self.after(300, self._motion_halt)
        
        

class FloatingPosWindow(tk.Toplevel):
    def __init__(self, *args):
        super().__init__()
        
        self._x = args[0]
        self._y = args[1]
        self.parent = args[2]
        self.hp = None
        
        # To display this floating position window near the cursor, it needs
        # to calculate the cursor's position on the screen. 
        # The first two arguments provide the position of the cursor relative
        # to the main app window. 
        self.geometry(f'+{self._x + self.parent.winfo_rootx() + 15}' 
                      + f'+{self._y + self.parent.winfo_rooty() + 12}')
        # if True hides the title bar with buttons [_ ]
        self.overrideredirect(True)
        self._cursor_in_main()
        
    def _cursor_in_main(self):
        """
        Checks if cursor is in the main window. If yes, it prints the x, y
        coordinates into the floating position window. Otherwise, closes the 
        window. 
        
        NOTE: Not having this condition would mean that the cursor info is 
        shown even when cursor is outside of the main app window borders. 

        Returns
        -------
        None.

        """
        if (0 <= self._x <= self.parent._sizex) and \
                (0 <= self._y <= self.parent._sizey):
            tk.Label(self, text=f'x = {self._x}, y = {self._y}').pack()
            self.hp = self.after(150, self._hide_pos)
        else:
            self.destroy()

    def _hide_pos(self):
        """
        Checks if there's a movement of cursor after creating the floating
        position window. It leaves the position information on screen until
        movement with cursor is recommenced. Then, it hides the x, y 
        coordinate information, by first safely terminating the after() 
        method then calling self.destroy(). 

        Returns
        -------
        None.

        """
        try:
            posx, posy = self.parent.get_coord()
            if (self.parent.posx, self.parent.posy) != (posx, posy):
                self.after_cancel(self.hp)
                self.destroy()
            else:
                self.hp = self.after(33, self._hide_pos)
        except tk._tkinter.TclError:
            pass

    

    

if __name__ == '__main__':
    MainApp().mainloop()

    


