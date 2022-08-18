"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-12-02 for version 1.0b1

Resize file application resizes files for use with iCLOTS analysis applications:

Inputs:
--A single image (.png, .jpg, .tif) file or a single video file (.avi)
--A directory of files, which will all be resized using the same resize factor

Parameters chosen by user:
--Resize factor: a number (e.g. 0.5, 2) to decrease (<1) or increase (>1) dimensions by

Outputs:
--Each file(s), resized, saved in a new 'resized' directory within the folder the files were chosen from
----Resize factor will be appended to the file name for reference

"""

import tkinter as tk
import tkinter.font as font
import os
import shutil
import cv2
import numpy as np
from accessoryfn import chooseinput, error, complete

class ResizeGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Tkinter variables
        self.resizefactor = tk.DoubleVar(value=1)  # micron-to-pixel ratio
        self.filelist = None

        # Widgets
        self.title(name + " file resizing application")

        # Application title
        menutitle = tk.Label(self, text="File resizing application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input single image button
        single_button = tk.Button(self, text="Select single file", command=self.singlefile)
        single_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Input directory button
        dir_button = tk.Button(self, text="Select folder of files", command=self.dirfile)
        dir_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # File label, blank initially
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # Resize factor entry box label
        resizefactor_label = tk.Label(self, text="Resize factor")
        resizefactor_label.grid(row=4, column=0, padx=5, pady=5)
        # Resize factor entry box
        resizefactor_entry = tk.Entry(self, width=10, textvariable=self.resizefactor)
        resizefactor_entry.grid(row=4, column=1, padx=5, pady=5)
        # Resize files button
        dir_button = tk.Button(self, text="Submit for resizing", command=self.resize)
        dir_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    # Choose single image, return one-element list
    def singlefile(self):
        filename = chooseinput.anyfile()
        self.filelist = [filename]
        self.name_label.config(text=filename)

    # Choose folder of images, return sorted list
    def dirfile(self):
        dirname, self.filelist = chooseinput.diranyfile()
        self.name_label.config(text=dirname)

    # Resize each file
    def resize(self):
        if self.filelist is not None:
            # Format resize factor into string
            rf_str = str(self.resizefactor.get()).replace(".", "p")
            # Make new directory to save images into, change directory
            outputfolder = os.path.dirname(self.filelist[0]) + '/Resized files, resize factor ' + rf_str
            if os.path.exists(outputfolder):  # Set up outut folder
                shutil.rmtree(outputfolder)
            os.mkdir(outputfolder)
            os.chdir(outputfolder)
            # Resize each image
            for file in self.filelist:
                filename = os.path.basename(file).split(".")[0]
                newfilename = filename + "_resized-" + rf_str + "." + os.path.basename(file).split(".")[1]

                if os.path.basename(file).split(".")[1] == "avi":  # If video
                    cap = cv2.VideoCapture(file)
                    wn = int(np.floor(cap.get(3) * self.resizefactor.get()))  # float
                    hn = int(np.floor(cap.get(4) * self.resizefactor.get()))  # float
                    fps = cap.get(cv2.CAP_PROP_FPS)

                    # Video writer output
                    fourcc = cv2.VideoWriter_fourcc(*"XVID")
                    out = cv2.VideoWriter(newfilename, fourcc, fps, (wn, hn))

                    while True:
                        ret, frame = cap.read()
                        if ret == True:
                            b = cv2.resize(frame, (wn, hn), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                            out.write(b)
                        else:
                            break

                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                elif os.path.basename(file).split(".")[1] in ["png", "jpg", "tif"]:
                    read = cv2.imread(file)
                    size = read.shape
                    wn = int(size[1] * self.resizefactor.get())
                    hn = int(size[0] * self.resizefactor.get())
                    resizedimg = cv2.resize(read, (wn, hn), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(newfilename, resizedimg)
            complete.DoneWindow()

        else:
            error.ErrorWindow(message='Please select file(s) to resize')