"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-11 for version 1.0b1

Toplevel GUI window that facilitates choice of a primary stain color and functional stain color
For fluorescent applications
Choices: red, green, blue, grayscale, none (fn only)

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
        self.fs = tk.StringVar(value='n')  # Functional stain color, default none (r, g, b, n)

        # Widgets
        self.title("Select staining channel(s)")

        # Primary stain selection label
        primary_label = tk.Label(self, text="Membrane stain")
        primary_label['font'] = boldfont
        primary_label.grid(row=0, column=0, padx=10, pady=10)
        # Primary stain radio buttons
        primary_red = ttk.Radiobutton(self, text="Red channel", value='r', variable=self.ps)
        primary_green = ttk.Radiobutton(self, text="Green channel", value='g', variable=self.ps)
        primary_blue = ttk.Radiobutton(self, text="Blue channel", value='b', variable=self.ps)
        primary_gray = ttk.Radiobutton(self, text="Greyscale", value='gs', variable=self.ps)
        primary_red.grid(row=1, column=0, padx=10, sticky='W')
        primary_green.grid(row=2, column=0, padx=10,  sticky='W')
        primary_blue.grid(row=3, column=0, padx=10, sticky='W')
        primary_gray.grid(row=4, column=0, padx=10, sticky='W')

        # Functional stain selection label
        fn_label = tk.Label(self, text="Functional stain")
        fn_label['font'] = boldfont
        fn_label.grid(row=5, column=0, padx=10, pady=10)
        # Functional stain radio buttons
        fn_red = ttk.Radiobutton(self, text="Red channel", value='r', variable=self.fs)
        fn_green = ttk.Radiobutton(self, text="Green channel", value='g', variable=self.fs)
        fn_blue = ttk.Radiobutton(self, text="Blue channel", value='b', variable=self.fs)
        fn_none = ttk.Radiobutton(self, text="No functional stain", value='n', variable=self.fs)
        fn_red.grid(row=6, column=0, padx=10, sticky='W')
        fn_green.grid(row=7, column=0, padx=10, sticky='W')
        fn_blue.grid(row=8, column=0, padx=10, sticky='W')
        fn_none.grid(row=9, column=0, padx=10, sticky='W')

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.destroy)
        submit_button.grid(row=10, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.columnconfigure(0, weight=1)

    def setcolors(self):
        # Return values after window destroyed
        self.wait_window()
        return self.ps.get(), self.fs.get()

