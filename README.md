# Image tracer

A small application with a GUI that enables to scan and return / save the contour of a shape in an image. 
It traces an object of interest in a loaded image. 

> **Note** *This is an older / unfinished project. Initially started as an experiment with GUI applications in Python. 
> The basic functionality is implemented - Edit mode functionality not yet available.* 

> **Warning** *Abandon hope all ye who enter here. This code might not follow clean code principles, and may 
> contain code snippets that should have been long deleted.* 

## How to run the project

The GUI app can be started running file `tracer_app.py`. This will open the following window. 

<p align="center" width="100%">
    <img width="50%" src="images/tracer_startpg.PNG"> 
</p>

## How to use the project

### Trace a shape in the img
Please follow the steps below. 

1. First an image has to be loaded. Please click on *File* in the menubar, then click *Open*. 
It can be accessed also by using the keyboard shortcut ***Alt+F***, then hitting ***O***. 

<p align="center">
    <img width="50%" src="images/tracer_openpg.png"> 
</p>

> **Note** *This will open the filedialog and prompt the user to select an image to be loaded into the app.* 
2. Select an image to be loaded. 

> **Note** *It is recommended to use a black-and-white (bilevel) or grayscale image. 
> The application has not been tested on colour images.*
> 
> *The application will convert any loaded image to black-and-white by default.*

3. After the image has been loaded, select a point of the image (ideally a location near the shape to be traced) 
by clicking on the image. The following popup will appear. 

<p align="center">
    <img width="20%" src="images/select.png"> 
</p>

4. Select the direction the application is supposed to start the trace by choosing *Left* or *Right*.

### Edit the contour

After the trace is finished, the following window will appear. 

<p align="center">
    <img width="20%" src="images/tracer_edit.png"> 
</p>

Choose *Yes* to enter **Edit mode**. 

<p align="center">
    <img width="50%" src="images/tracer_editpg.png"> 
</p>

> **Note** *Edit mode is not finished, the functionalities are not yet implemented (except **Save**).* 
> 
> *The tooltip will give more information on the planned functionalities. Hovering over the icons in the menubar will 
> display the extra information.*


## License

[MIT License](LICENSE)