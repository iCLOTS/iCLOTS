"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-01 for version 1.0b1

Single cell tracking menu script directs to brightfield and fluoresence microscopy iCLOTS applications
Specialized app versions for the deformability assay are also available

"""

import tkinter as tk
import tkinter.font as font
from gui import deform
from accessoryfn import staytuned

class SCTMenu(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " single cell tracking menu")

        # Deformability menu title
        menutitle = tk.Label(self, text="Single cell tracking applications")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Brightfield analysis button
        bf_button = tk.Button(self, text="Brightfield microscopy analysis", command=self.bfapp)
        bf_button.grid(row=1, column=0, padx=5, pady=5)
        # Fluorescence analysis button
        fl_button = tk.Button(self, text="Fluoresence microscopy analysis", command=self.flapp)
        fl_button.grid(row=2, column=0, padx=5, pady=5)

        # Deformability-assay specific applications
        # Brightfield analysis button
        bf_def_button = tk.Button(self, text="Specialized deformability assay\n"
                                         "brightfield microscopy analysis", command=self.bf_def_app)
        bf_def_button.grid(row=3, column=0, padx=5, pady=5)
        # Fluorescence analysis button
        fl_def_button = tk.Button(self, text="Specialized deformability assay\n"
                                         "fluoresence microscopy analysis", command=self.fl_def_app)
        fl_def_button.grid(row=4, column=0, padx=5, pady=5)


        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=5, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

    def bfapp(self):
        staytuned.StayTuned()

    def flapp(self):
        staytuned.StayTuned()

    def bf_def_app(self):
        deform.BrightfieldDeformGUI()

    def fl_def_app(self):
        staytuned.StayTuned()

