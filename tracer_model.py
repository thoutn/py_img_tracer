# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:28:00 2021

@author: Tom
"""


import numpy as np
import cv2
import PIL.Image
import PIL.ImageTk





class Model:
    """
    Image Tracer
    
    Traverses the image extracting location of contour points for an object 
    of interest on the image.
    
    -- The current version -- 
    Works with 1-bit colour depth image only, i.e. any opened image is 
    automatically converted into black and white image. 
    It is recommended to preprocess the image to obtain the best result. 
    """

    def __init__(self, name: str=None, path: str=None) -> None:
        self.image_name = name
        self.image_path = path
        self.threshold = 0  # for grayscale image, currently uses 1-bit image
        
        self.edge_dir = {'LEFT': (-1, 0), 
                         'DOWN': (0, 1), 
                         'RIGHT': (1, 0),
                         'UP': (0, -1)}
        self.corner_dir = {'LEFT': (1, -1), 
                           'DOWN': (-1, -1), 
                           'RIGHT': (-1, 1), 
                           'UP': (1, 1)}
    
    def open_image(self) -> None:
        """
        Opens image with pillow and saves it to a numpy array for the tracer. 

        Returns
        -------
        None.

        """
        self.pil_image = PIL.Image.open(self.image_name)
        #self._image = np.array(self.pil_image.convert('L')) # grayscale
        self._image = np.array(self.pil_image.convert('1')) # black and white
        
    def close_image(self) -> None:
        """
        Safely closes pillow image. 

        Returns
        -------
        None.

        """
        self.pil_image.close()
        
    def set_start_position(self, x: int=None, y: int=None) -> None:
        """
        Sets the x, y coordinates of the start point, defined by the user. 

        Parameters
        ----------
        x : int, optional
            Start point x coordinate. The default is None.
        y : int, optional
            Start point y coordinate. The default is None.

        Returns
        -------
        None.

        """
        if not x or not y:
            return
        else:
            self.x = x
            self.y = y
    
    def start_trace(self, direction: str) -> str:  
        """
        Starts tracing image feature of interest. Identifies first contour 
        pixel if available >> identified by comparison to a predefined 
        threshold value = pixel value of grayscale image. 

        Parameters
        ----------
        direction : str
            Direction in which the pixels are traversed while searching for 
            the contour. 

        Raises
        ------
        IndexError
            No contour found >> pixel value in the traversed direction does
            not correspond to the predefined threshold.

        Returns
        -------
        str
            Confirmation that the trace is finished. 

        """
        self.prev_dir = direction
        self.contour = []
        self.change_dir = self.direction_gen()
        while True:
            _colour = self._image[self.y][self.x]
            if _colour <= self.threshold: 
                self.contour.extend((self.x, self.y))
                break
            elif direction == 'LEFT' and self.x != 0:
                self.x -= 1
            elif direction == 'RIGHT' and self.x != len(self._image[0]) - 1:
                self.x += 1
            else:
                raise IndexError(f'No contour found to the {direction}.')
        
        if direction == 'LEFT':
            self.prev_dir = next(self.change_dir)
        else: 
            for i in range(2):
                self.prev_dir = next(self.change_dir)

        return self.continue_trace()

    def continue_trace(self) -> str:
        """
        Continues with the trace function. 

        Returns
        -------
        str
            Confirmation that the trace is finished.

        """
        self.corner_position()
        _method = self.check_corner()
        
        while True:
            if _method == 'corner':
                _method = self.check_corner()
            elif _method == 'edge':
                _method = self.check_edge()
            elif _method == 'Done.':
                return _method
                
    def corner_position(self) -> None: 
        """
        Reads the next pixel (corner pixel for function 'check_corner'), which 
        value is compared with the threshold. 

        Returns
        -------
        None.

        """
        self.x, self.y = (sum(x) for x in zip((self.x, self.y), 
                                              self.corner_dir[self.prev_dir]))
        
    def check_corner(self) -> str:
        """
        Checks value of pixel diagonal to the previously identified contour 
        pixel: 
                        where: 
            #---#           X   ...previous contour pixel
            | X |           #   ...corner pixel
            #---#           -   ...edge pixel
        
        The specific corner is selected based on the previous direction, in
        which the image is traversed. 
            

        Returns
        -------
        str
            Information about next step to be taken or halting message. 

        """
        if (self.x, self.y) == (self.contour[0], self.contour[1]):
            return 'Done.'
        _colour = self._image[self.y][self.x]
        if _colour <= self.threshold:
            self.contour.extend((self.x, self.y))
            for i in range(3):
                self.prev_dir = next(self.change_dir)
            self.corner_position()
            return 'corner'
        else:
            return 'edge'

    def edge_position(self) -> None:
        """
        Reads the next pixel (edge pixel for function 'check_edge'), which 
        value is compared with the threshold. 

        Returns
        -------
        None.

        """
        self.x, self.y = (sum(x) for x in zip((self.x, self.y), 
                                              self.edge_dir[self.prev_dir]))
        
    def check_edge(self) -> str:
        """
        Checks value of pixel perpendicular to the previously identified 
        contour pixel: 
                        where: 
            #---#           X   ...previous contour pixel
            | X |           #   ...corner pixel
            #---#           -   ...edge pixel
        
        The specific edge is selected based on the previous direction, in
        which the image is traversed. 

        Returns
        -------
        str
            Information about next step to be taken or halting message. 

        """
        self.edge_position()
        if (self.x, self.y) == (self.contour[0], self.contour[1]):
            return 'Done.'
        _colour = self._image[self.y][self.x]
        if _colour <= self.threshold:
            self.contour.extend((self.x, self.y))
            self.corner_position()
        else:
            self.edge_position()
            self.prev_dir = next(self.change_dir)
        return 'corner'
        
    def direction_gen(self) -> str:
        """
        Generator function - generates a circular list containing the 
        directions. 

        Yields
        ------
        str
            Identifier of the current direction the image is traversed.

        """
        change_dir = ['LEFT', 'DOWN', 'RIGHT', 'UP']
        i = 0
        while True:
            i += 1
            yield change_dir[i - 1]
            if i == 4:
                i = 0     
        
    def save_contour(self, filename: str=None) -> None:
        """
        Saves traced contour into external file. 

        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        if filename:
            self.contour_name = filename.split('.')[0]
        with open(f'{self.contour_name}.txt', 'w') as f:
            for coord in self.contour:
                f.write(str(coord) + '\n')
        self.contour.clear()


    

    

if __name__ == '__main__':
    trace = Model(name='_input/Puzzle_02_cr2.png')
    trace.open_image()
    
    trace.set_start_position(x=710, y=650)
    print(trace.start_trace('LEFT'))
    #print(trace.check_trace_end())
    trace.save_contour('_output/first_try.txt')
    
    trace.close_image()
    #print(trace._image)
    

    data = np.reshape(trace.contour, (-1, 2))
    x = [x for i, x in enumerate(trace.contour) if i % 2 == 0]
    y = [y for j, y in enumerate(trace.contour) if j % 2 != 0]
    
    smooth_curve = 10
    x = [x for i, x in enumerate(x) if i % smooth_curve == 0]
    y = [y for j, y in enumerate(y) if j % smooth_curve == 0]
    from matplotlib import pyplot as plt
    #plt.imshow(data, interpolation='nearest')
    plt.plot(x, y)
    plt.title(label=f'reduction ratio: {smooth_curve}')
    #plt.axis('scaled')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    plt.show()

    with open('./_output/third.txt', 'r') as f:
        new = [int(x) for x in f]