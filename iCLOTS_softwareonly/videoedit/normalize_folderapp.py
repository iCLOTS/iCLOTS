"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Image normalization app normalizes images so that all pixel values of all color channels are scaled from [0, 255]

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import os
import shutil
import cv2
import numpy as np
from accessoryfn import chooseinput, error, complete

class NormalizeImgs(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " image normalization application")

        # Application title
        menutitle = tk.Label(self, text="Pixel range normalization application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Input single video button
        single_video_button = tk.Button(self, text="Select folder of images\nto normalize to a [0, 255] pixel range", command=self.normalize_images)
        single_video_button.grid(row=1, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=2, column=0, padx=5, pady=5)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Choose single video, convert to avi
    def normalize_images(self):

        dirname, filelist = chooseinput.dirimgfile()

        # Make new directory to save video into, change directory
        outputfolder = os.path.join(dirname, 'Normalized images')
        if os.path.exists(outputfolder):  # Set up outut folder
            shutil.rmtree(outputfolder)
        os.mkdir(outputfolder)
        os.chdir(outputfolder)

        for imgname in filelist:

            img = cv2.imread(imgname)

            h, w, l = img.shape  # Dimensions of frame

            for i in range(l):  # For each layer
                # Normalize
                img[l] = (img[l] - np.amin(img)) / (np.amax(img) - np.amin(img)) * 255

            name = os.path.basename(imgname).split(".")[0] + '_normalized.png'  # String to save image as

            cv2.imwrite(name, img)

        complete.DoneWindow()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            dirname = None
            filelist = None
            img = None

