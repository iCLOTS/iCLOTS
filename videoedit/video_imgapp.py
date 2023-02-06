"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-13 for version 1.0b1

Video-to-image app converts frames of an .avi video to a series of .png images

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import os
import shutil
import cv2
from accessoryfn import chooseinput, error, complete

class VideoToImg(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Widgets
        self.title(name + " video-to-image application")

        # Application title
        menutitle = tk.Label(self, text="Video-to-image application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Input single video button
        single_video_button = tk.Button(self, text="Select single video\nto automatically convert to images", command=self.singlevideofile)
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
    def singlevideofile(self):
        filename = chooseinput.videofile()

        # Make new directory to save images into, change directory
        outputfolder = os.path.join(os.path.dirname(filename), os.path.basename(filename).split('.')[0] + ' split frames')
        if os.path.exists(outputfolder):  # Set up outut folder
            shutil.rmtree(outputfolder)
        os.mkdir(outputfolder)
        os.chdir(outputfolder)

        capture = cv2.VideoCapture(filename)
        length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # Save frames
        success, frame = capture.read()
        count = 0
        while success and count < length - 1:  # Length - 1 prevents "empty frame" error at end of video
            image_name = os.path.basename(filename).split('.')[0] + '_frame_' + str(count).zfill(5) + '.png'
            success, image = capture.read()
            cv2.imwrite(image_name, image)  # save frame as .png file
            count += 1

        capture.release()
        cv2.destroyAllWindows()

        complete.DoneWindow()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            filename = None
            capture = None
            image = None

