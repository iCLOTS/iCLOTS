"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-09-06 for version 1.0b1

Main menu script directs to every iCLOTS application

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import sys
import os
from PIL import Image, ImageTk
from gui import velocity, ml_selectfiles
from menu import adhesionmenu, occlusionmenu, sct_menu, videomenu
from help import mainhelp
from accessoryfn import staytuned

class MainMenu(tk.Tk):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'
        name_ext = 'interactive Cellular assay Labeled\nObservation and Tracking experimental Software'
        tagline = 'Automated analysis software for\ncellular microscopy and microfluidic applications'
        version = 'v0.1.1'

        # Fonts
        titlefont = font.Font(size=24)
        smallfont = font.Font(size=8)

        # Widgets
        self.title(name + " main menu")
        # Software name, title
        app_label = tk.Label(self, text=name)
        app_label['font'] = titlefont
        app_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        # Program name
        ext_label = tk.Label(self, text=name_ext)
        ext_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        # Logo image
        logo_canvas = tk.Canvas(self, width=151, height=151)
        # logo_canvas = tk.Canvas(self, width=1, height=1)
        logo_canvas.grid(row=2, column=0, columnspan=3)
        new_path = self.resource_path('logo_sm.png')
        # logoimg = Image.open('/Users/meredithfay/Documents/PycharmProjects/iCLOTS_softwareonly/logo_sm.png')
        logoimg = Image.open(new_path)
        logoimg = ImageTk.PhotoImage(image=logoimg)  # A fix to keep image displayed
        self.logoimg = logoimg  # " "
        logo_canvas.create_image(2, 2, anchor='nw', image=logoimg)
        # Program description text
        desc_label = tk.Label(self, text=tagline)
        desc_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Adhesion menu button
        adh_button = tk.Button(self, text="Adhesion", command=self.adhmenu)
        adh_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        # Deformability GUI button
        def_button = tk.Button(self, text="Single cell tracking", command=self.sct_app)
        def_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        # Occlusion menu button
        occ_button = tk.Button(self, text="Multiscale microfluidic accumulation", command=self.occmenu)
        occ_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        # Velocity GUI button
        vel_button = tk.Button(self, text="Velocity profile analysis", command=self.velapp)
        vel_button.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        # Clustering menu button
        video_button = tk.Button(self, text="Clustering analysis", command=self.clustermenu)
        video_button.grid(row=9, column=0, columnspan=3, padx=5, pady=5)
        # Video button
        video_button = tk.Button(self, text="Video editing", command=self.videomenu)
        video_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.gethelp)
        help_button.grid(row=12, column=0, padx=5, pady=5)
        # Version, Lam lab text
        lamlab_label = tk.Label(self, text=version +", Lam Lab")
        lamlab_label['font'] = smallfont
        lamlab_label.grid(row=12, column=1, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=12, column=2, padx=5, pady=5)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def adhmenu(self):
        adhesionmenu.AdhesionMenu()

    def sct_app(self):
        sct_menu.SCTMenu()

    def occmenu(self):
        occlusionmenu.OcclusionMenu()

    def velapp(self):
        velocity.VelocityGUI()

    def videomenu(self):
        videomenu.VideoMenu()

    def clustermenu(self):
        ml_selectfiles.SelectExcel()

    def gethelp(self):
        mainhelp.HelpDisplay()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, needed to display logo in .app"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def on_closing(self):
        """Closing command, clear variables to improve speed, software won't close on Windows without"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

# def resource_path(relative_path):
#     """ Get absolute path to resource, needed to display logo in .app"""
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)

root = MainMenu()
root.mainloop()