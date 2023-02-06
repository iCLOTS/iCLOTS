"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-12-02 for version 1.0b1

Function to raise an error window with specified message

"""

import tkinter as tk
import tkinter.font as font

class ErrorWindow(tk.Toplevel):

    def __init__(self, message):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " message")

        # Video menu title
        menutitle = tk.Label(self, text="Message!")
        menutitle['font'] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)
        # Error message, blank initially
        self.error_label = tk.Label(self, text=message)
        self.error_label.grid(row=1, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)