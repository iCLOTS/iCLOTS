"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-06-29 for version 1.0b1

Toplevel GUI window that facilitates "invert" parameter choice for applications using trackpy, where:
-True: indicates looking for dark features on light background
-False: indicates looking for light features on dark background

"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class SelectInvertChoice(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # Variables
        self.invert = tk.BooleanVar(value='True')  # Boolean

        # Widgets
        self.title("Describe image features")

        # Primary stain radio buttons
        invert_true = ttk.Radiobutton(self, text="Dark cells on light background", value=True, variable=self.invert)
        invert_false = ttk.Radiobutton(self, text="Light cells on dark background", value=False, variable=self.invert)
        invert_true.grid(row=1, column=0, padx=10, sticky='W')
        invert_false.grid(row=2, column=0, padx=10,  sticky='W')

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.destroy)
        submit_button.grid(row=3, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

    def setinvert(self):
        # Return values after window destroyed
        self.wait_window()
        return self.invert.get()