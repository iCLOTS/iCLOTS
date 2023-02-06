"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Toplevel GUI window that facilitates choice of a membrane/primary stain color
Choices: red, green, blue, grayscale

"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class SelectPrimaryFn(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # Fonts
        boldfont = font.Font(weight='bold')

        # Variables
        self.ps = tk.StringVar(value='gs')  # Primary stain color, default grayscale (r, g, b, gs)

        # Widgets
        self.title("Select staining channel\nindicating cell membrane")

        # Primary stain radio buttons
        primary_red = ttk.Radiobutton(self, text="Red channel", value='r', variable=self.ps)
        primary_green = ttk.Radiobutton(self, text="Green channel", value='g', variable=self.ps)
        primary_blue = ttk.Radiobutton(self, text="Blue channel", value='b', variable=self.ps)
        primary_gray = ttk.Radiobutton(self, text="Greyscale", value='gs', variable=self.ps)
        primary_red.grid(row=0, column=0, padx=10, sticky='W')
        primary_green.grid(row=1, column=0, padx=10,  sticky='W')
        primary_blue.grid(row=2, column=0, padx=10, sticky='W')
        primary_gray.grid(row=3, column=0, padx=10, sticky='W')

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
        return self.ps.get()

