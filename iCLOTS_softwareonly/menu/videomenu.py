"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-06-29 for version 1.0b1

Video menu script directs to iCLOTS video editing applications
These are useful for preparing data for analysis

"""

import tkinter as tk
import tkinter.font as font
from videoedit import resizeapp, cropframeapp
from accessoryfn import staytuned

class VideoMenu(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " video editing menu")

        # Video menu title
        menutitle = tk.Label(self, text="Video editing applications")
        menutitle['font'] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Video editing applications
        # Resize app
        resize_button = tk.Button(self, text="Resize file", command=self.resizeapp)
        resize_button.grid(row=1, column=0, padx=5, pady=5)
        # Rotate app
        rotate_button = tk.Button(self, text="Rotate file", command=self.rotateapp)
        rotate_button.grid(row=2, column=0, padx=5, pady=5)
        # Edit contrast app
        contrast_button = tk.Button(self, text="Edit file contrast", command=self.contrastapp)
        contrast_button.grid(row=3, column=0, padx=5, pady=5)
        # Crop to region of interest app
        croproi_button = tk.Button(self, text="Crop file to region of interest", command=self.croproi)
        croproi_button.grid(row=4, column=0, padx=5, pady=5)
        # Crop video length app
        croplength_button = tk.Button(self, text="Crop video length", command=self.croplength)
        croplength_button.grid(row=5, column=0, padx=5, pady=5)
        # Image sequence to video app
        img_video_button = tk.Button(self, text="Convert image sequence to video file", command=self.img_video)
        img_video_button.grid(row=6, column=0, padx=5, pady=5)
        # Video to image sequence app
        video_img_button = tk.Button(self, text="Convert video file to image sequence", command=self.video_img)
        video_img_button.grid(row=7, column=0, padx=5, pady=5)
        # Normalize intensity app
        norm_int_button = tk.Button(self, text="Normalize intensity of a folder of files", command=self.norm_int)
        norm_int_button.grid(row=8, column=0, padx=5, pady=5)
        # Help window
        help_button = tk.Button(self, text="Help, all applications", command=self.help)
        help_button.grid(row=9, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=10, column=0, padx=5, pady=5)

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
        self.columnconfigure(0, weight=1)

    def resizeapp(self):
        resizeapp.ResizeGUI()

    def rotateapp(self):
        staytuned.StayTuned()

    def contrastapp(self):
        staytuned.StayTuned()

    def croproi(self):
        cropframeapp.CropROIGUI()

    def croplength(self):
        staytuned.StayTuned()

    def img_video(self):
        staytuned.StayTuned()

    def video_img(self):
        staytuned.StayTuned()

    def norm_int(self):
        staytuned.StayTuned()

    def help(self):
        staytuned.StayTuned()
