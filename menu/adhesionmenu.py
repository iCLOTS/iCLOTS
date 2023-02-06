"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Adhesion menu script directs to brightfield adhesion, fluorescent adhesion,
and filopodia counting iCLOTS applications

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from gui import adhfluor, adhbrightfield, adhfil, adhvideo

class AdhesionMenu(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " adhesion menu")

        # Adhesion menu title
        menutitle = tk.Label(self, text="Adhesion applications")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Brightfield analysis button
        bf_button = tk.Button(self, text="Brightfield microscopy analysis", command=self.bfapp)
        bf_button.grid(row=1, column=0, padx=5, pady=5)
        # Fluorescent analysis button
        fluor_button = tk.Button(self, text="Fluorescence microscopy analysis", command=self.fluorapp)
        fluor_button.grid(row=2, column=0, padx=5, pady=5)
        # Filopodia menu button
        fil_button = tk.Button(self, text="Fluorescence microscopy\nfilopodia counter", command=self.filapp)
        fil_button.grid(row=3, column=0, padx=5, pady=5)
        # Transient adhesion menu button
        ta_button = tk.Button(self, text="Transient adhesion time", command=self.ta_app)
        ta_button.grid(row=4, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=5, column=0, padx=5, pady=5)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

    def bfapp(self):
        adhbrightfield.BrightfieldAdhesionGUI()

    def fluorapp(self):
        adhfluor.FluorAdhesionGUI()

    def filapp(self):
        adhfil.FilAdhesionGUI()

    def ta_app(self):
        adhvideo.AdhesionVideoGUI()

    def on_closing(self):
        """Closing command, clear variables to improve speed, software won't close on Windows without"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
