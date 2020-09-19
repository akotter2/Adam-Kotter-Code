#session_gui.py

"""This file holds the GUI interface for the data-driven productivity-
tracking software. The central feature of this file is the Session_GUI 
object, which manages the GUI for the Session."""

from tkinter import Tk, Label, Button, StringVar, Scale



class Session_GUI:
    """The GUI interface for Session objects, which has a settable 
    text box at the top center and variable user input widgets at the 
    bottom center.
    
    Methods:
    
        __init__;
        
        display: Changes the text displayed by the current window.
        
        set_scale: Sets the user input section of the window to a 
            given number of scales with given parameters.
        
        set_button: Sets the user input section of the window to a 
            button with given parameters.
        
        set_scale: Sets the user input section of the window to a box 
            that accepts text from the user."""