"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-01-03 for version 1.0b1

Toplevel GUI window that facilitates choice of present stain color(s)
For fluorescent applications
Choices: red, green, and/or blue
Returns True/False values

"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class SelectMultiColors(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # Fonts
        boldfont = font.Font(weight='bold')

        # Variables
        self.rchannel = tk.BooleanVar(value=False)  # Present channels
        self.gchannel = tk.BooleanVar(value=False)
        self.bchannel = tk.BooleanVar(value=False)

        # Widgets
        self.title("Select staining channel(s)")

        # Stain check boxes
        check_red = tk.Checkbutton(self, text="Red channel", variable=self.rchannel, onvalue=True, offvalue=False)
        check_green = ttk.Checkbutton(self, text="Green channel", variable=self.gchannel, onvalue=True, offvalue=False)
        check_blue = ttk.Checkbutton(self, text="Blue channel", variable=self.bchannel, onvalue=True, offvalue=False)
        check_red.grid(row=1, column=0, padx=10, sticky='W')
        check_green.grid(row=2, column=0, padx=10,  sticky='W')
        check_blue.grid(row=3, column=0, padx=10, sticky='W')

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.destroy)
        submit_button.grid(row=4, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

    def setcolors(self):
        # Return values after window destroyed
        self.wait_window()
        return self.rchannel.get(), self.gchannel.get(), self.bchannel.get()

