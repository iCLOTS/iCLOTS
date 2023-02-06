"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Image-to-video app converts a sequence of images to a video file with an input frames-per-second value

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import os
import shutil
import cv2
from accessoryfn import chooseinput, complete

class ImgtoVideo(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")
        smallfont = font.Font(size=8)

        # Tkinter variables
        self.fps = tk.DoubleVar(value=10)

        # Widgets
        self.title(name + " image-to-video application")

        # Application title
        menutitle = tk.Label(self, text="Image-to-video application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # FPS entry box label
        fos_label = tk.Label(self, text="Frames per second\nimaging rate (FPS)")
        fos_label['font'] = smallfont
        fos_label.grid(row=1, column=0, padx=5, pady=5)
        # Micron-to-pixel ratio entry box
        self.fps_entry = tk.Entry(self, textvariable=self.fps, width=8)
        self.fps_entry.grid(row=1, column=1, padx=5, pady=5)

        # Input series of images button
        single_video_button = tk.Button(self, text="Select series of images\nto automatically convert to single video", command=self.choose_folder_images)
        single_video_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Choose single video, convert to avi
    def choose_folder_images(self):

        dirname, filelist = chooseinput.dirimgfile()

        # Format resize factor into string
        fps_str = str(self.fps.get()).replace(".", "p")

        # Make new directory to save video into, change directory
        outputfolder = os.path.join(dirname, 'Video, FPS ' + fps_str)
        if os.path.exists(outputfolder):  # Set up outut folder
            shutil.rmtree(outputfolder)
        os.mkdir(outputfolder)
        os.chdir(outputfolder)

        # Set up video writer
        testimg = cv2.imread(filelist[0])
        h, w, l = testimg.shape  # Dimensions of frame, use last called

        name = os.path.basename(dirname) + '_fps_' + fps_str + '.avi'  # String to save new video as, .avi

        # Set up video writer object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
        out = cv2.VideoWriter(name, fourcc, self.fps.get(), (w, h))

        # Add frames to videowriter
        for imgname in filelist:
            img = cv2.imread(imgname)
            out.write(img)

        # Finish
        out.release()

        cv2.destroyAllWindows()

        complete.DoneWindow()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            dirname = None
            filelist = None
            img_array = None
            out = None

