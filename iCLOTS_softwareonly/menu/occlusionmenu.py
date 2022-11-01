"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-06-29 for version 1.0b1

Occlusion menu script directs to microchannel, region of interest, and microfluidic device
occlusion/accumulation iCLOTS applications

All applications are designed for RGB fluorescent data only

"""

import tkinter as tk
import tkinter.font as font
from gui import occmicro, occroi, occdevice
from accessoryfn import staytuned

class OcclusionMenu(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " occlusion menu")

        # Occlusion menu title
        menutitle = tk.Label(self, text="Occlusion and accumulation applications")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Microfluidic device analysis button
        uf_button = tk.Button(self, text="Microfluidic device analysis", command=self.ufapp)
        uf_button.grid(row=1, column=0, padx=5, pady=5)
        # Region of interest analysis button
        roi_button = tk.Button(self, text="Region of interest analysis", command=self.roiapp)
        roi_button.grid(row=2, column=0, padx=5, pady=5)
        # Occlusion menu button
        uc_button = tk.Button(self, text="Microchannel analysis", command=self.ucapp)
        uc_button.grid(row=3, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=4, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

    def ufapp(self):
        occdevice.DeviceOccGUI()

    def roiapp(self):
        occroi.ROIOccGUI()

    def ucapp(self):
        occmicro.MicrochannelOccGUI()
