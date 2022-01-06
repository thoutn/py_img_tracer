# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:28:00 2021

@author: Tom
"""



from tkextend import *



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
        




class FlatButton(tk.Canvas):
    
    def __init__(self, master, *, hoverbg='#E0DDDD', activebg='#C1CDCD', 
                 image=None, file=None, text=None, command=None, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.hoverbg = hoverbg
        self.activebg = activebg
        self.defaultbg = master['bg']
        if image:
            self.image = image
        elif file:
            self.image = tk.PhotoImage(file=file)
        self.text = text
        self.command = command
        
        self.config(bd=0, highlightthickness=0)
        self._init_btn()
        
        self.bind('<Enter>', self.on_enter, add='+')
        self.bind('<Leave>', self.on_leave, add='+')
        self.bind('<Button-1>', self.on_click, add='+')
        self.bind('<B1-Motion>', self.on_click, add='+')
        self.bind('<ButtonRelease-1>', self.on_release, add='+')
    
    def _init_btn(self):
        x_ = 4 
        y_ = 4
        
        if self.image:
            id_img = self.create_image((x_, y_), 
                                       image=self.image, 
                                       anchor='nw')
            bbox_img = self.bbox(id_img)
            x_ += bbox_img[-2]
            
        if self.text:
            id_txt = self.create_text((x_, y_), 
                                      text=self.text, 
                                      anchor='nw')
            bbox_txt = self.bbox(id_txt)
        
        try:
            if bbox_img[-1] > bbox_txt[-1]:
                self.move(id_txt, x_, (bbox_img[-1] - bbox_txt[-1]) // 2)
            else:
                self.move(id_img, 4, (bbox_txt[-1] - bbox_img[-1]) // 2)
        except Exception:
            pass
            
        bbox_ = self.bbox('all')
        self.config(width=bbox_[2] + 4, height=bbox_[3] + 4)
    
    def on_enter(self, event):
        self['background'] = self.hoverbg

    def on_leave(self, event):
        self['background'] = self.defaultbg
    
    def on_click(self, event):
        self['background'] = self.activebg
        if self.command:
            self.command()
    
    def on_drag(self, event):
        self['background'] = self.activebg
    
    def on_release(self, event):
        self['background'] = self.hoverbg
        
        





class CustomButton(ttk.Button):
    
    def __init__(self, master, **kwargs):
        self.activebg = kwargs.pop('activebg')
        self.pressedbg = kwargs.pop('pressedbg')
        
        super().__init__(master=master, **kwargs)
        
        #self.config(relief='flat')
        #self.defaultbg = self['background']
        
        s = ttk.Style()
        s.map('TButton', 
              background=[('disabled', '#D9D9D9'), ('active', self.activebg), ('pressed', self.pressedbg)],
              foreground=[('disabled', '#A3A3A3')],
              relief=[('pressed', '!disabled', 'flat'), ('active', 'flat'), ('disabled', 'flat')])
        
        #self.config(style='TButton')
"""        
        self.bind('<Enter>', self.on_enter, add='+')
        self.bind('<Leave>', self.on_leave, add='+')
        self.bind('<Button-1>', self.on_click, add='+')
        self.bind('<B1-Motion>', self.on_click, add='+')
        self.bind('<ButtonRelease-1>', self.on_release, add='+')

    def on_enter(self, event):
        self['background'] = self.hoverbg

    def on_leave(self, event):
        self['background'] = self.default_background
    
    def on_click(self, event):
        self['background'] = self['activebackground']
        #return 'break'
    
    def on_drag(self, event):
        self['background'] = self['activebackground']
        #return 'break'
    
    def on_release(self, event):
        self.config(relief='flat')
        self['background'] = self.hoverbg
"""






class Tooltip:
    """
    It creates a tooltip for a given widget as the mouse goes on it.

    see:

    http://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-
           in-tkinter/36221216#36221216

    http://www.daniweb.com/programming/software-development/
           code/484591/a-tooltip-class-for-tkinter

    - Originally written by vegaseat on 2014.09.09.

    - Modified to include a delay time by Victor Zaccardo on 2016.03.25.

    - Modified
        - to correct extreme right and extreme bottom behavior,
        - to stay inside the screen whenever the tooltip might go out on
          the top but still the screen is higher than the tooltip,
        - to use the more flexible mouse positioning,
        - to add customizable background color, padding, waittime and
          wraplength on creation
      by Alberto Vassena on 2016.11.05.

      Tested on Ubuntu 16.04/16.10, running Python 3.5.2

    TODO: themes styles support
    """

    def __init__(self, widget,
                 *,
                 bg='#FFFFEA',
                 fg='#000000', 
                 bd='#000000', 
                 pad=(5, 3, 5, 3),
                 text='widget info',
                 waittime=800,
                 wraplength=250):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter, add='+')
        self.widget.bind("<Leave>", self.onLeave, add='+')
        self.widget.bind("<Button-1>", self.onLeave, add='+')
        self.bg = bg
        self.fg = fg
        self.bd = bd
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label,
                               *,
                               tip_delta=(10, 15), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automatically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw, 
                       background=self.bg, 
                       borderwidth=0, 
                       highlightbackground=self.bd, 
                       highlightthickness=1)
        label = tk.Label(win,
                         text=self.text,
                         justify=tk.LEFT,
                         background=self.bg,
                         foreground=self.fg,
                         relief=tk.SOLID,
                         borderwidth=0,
                         wraplength=self.wraplength)

        label.grid(padx=(self.pad[0], self.pad[2]),
                   pady=(self.pad[1], self.pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(self.widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None
        








