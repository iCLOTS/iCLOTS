"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-06-29 for version 1.0b1

Holder function to indicate applications still in progress
Should all be removed by release of v1.0b1

"""

import tkinter as tk
import tkinter.font as font

class StayTuned(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Widgets
        self.title(name + " status update")

        # Error message, blank initially
        self.error_label = tk.Label(self, text="Application under construction,\nplease stay tuned!")
        self.error_label.grid(row=0, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)