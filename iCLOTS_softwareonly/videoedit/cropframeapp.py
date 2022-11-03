"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-12-02 for version 1.0b1

Crop app allows user to select a region of interest (ROI) to save:

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import os
import shutil
import cv2
from accessoryfn import chooseinput, error, complete

class CropFrames(tk.Toplevel):

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
        self.title(name + " frame cropping application")

        # Application title
        menutitle = tk.Label(self, text="Region-of-interest cropping application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, padx=10, pady=10)

        # Input single file button
        single_button = tk.Button(self, text="Select a single file to crop\n to individualized regions of interest", command=self.choose_single)
        single_button.grid(row=1, column=0, padx=5, pady=5)
        # Input series of images button
        multi_button = tk.Button(self, text="Select series of files to crop\n to individualized regions of interest", command=self.choose_folder)
        multi_button.grid(row=2, column=0, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=3, column=0, padx=5, pady=5)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Choose single file
    def choose_single(self):
        filename = chooseinput.anyfile()

        self.crop_and_save([filename])

    # Choose folder of any file types
    def choose_folder(self):

        dirname, filelist = chooseinput.diranyfile()

        self.crop_and_save(filelist)

    # Choose ROI function
    def chooseROI(self, frame):
        """Function to resize a frame - can be an image file or a video frame"""

        # Choose ROI from image, pull out values
        cv2.namedWindow("Select region of interest and press enter", cv2.WINDOW_NORMAL)
        fromCenter = False  # Set up to choose as a drag-able rectangle rather than a rectangle chosen from center
        r = cv2.selectROI("Select region of interest and press enter", frame, fromCenter)  # Choose ROI function from cv2 - opens a window to choose
        ROI_x = int(r[0])  # Take result of selectROI and put into a variable
        ROI_y = int(r[1])  # " "
        ROI_w = int(r[2])  # " "
        ROI_h = int(r[3])  # " "

        cv2.destroyAllWindows()

        return ROI_x, ROI_y, ROI_w, ROI_h

    # Crop files
    def crop_and_save(self, filelist):

        # Make new directory to save video into, change directory
        outputfolder = os.path.join(os.getcwd(), 'Cropped files')
        if os.path.exists(outputfolder):  # Set up outut folder
            shutil.rmtree(outputfolder)
        os.mkdir(outputfolder)
        os.chdir(outputfolder)

        for file in filelist:
            if '.avi' in file:
                capture = cv2.VideoCapture(file)
                # Dimensions, must be exact for videos
                fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

                name = os.path.basename(file).split(".")[0] + '_ROI.avi'  # String to save image as, .avi

                ret, frame_0 = capture.read()
                ROI_x, ROI_y, ROI_w, ROI_h = self.chooseROI(frame_0)  # Find ROI by applying function

                # Set up video writer object
                fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
                out = cv2.VideoWriter(name, fourcc, fps, (ROI_w, ROI_h))

                # Resize each frame
                while True:
                    ret, frame = capture.read()
                    if ret == True:
                        out_frame = frame[ROI_y: (ROI_y + ROI_h), ROI_x: (ROI_x + ROI_w)]  # Crop
                        out.write(out_frame)
                    else:
                        break

                # Finish
                capture.release()
                out.release()
                cv2.destroyAllWindows()

            else:  # If an image file
                frame = cv2.imread(file)
                ROI_x, ROI_y, ROI_w, ROI_h = self.chooseROI(frame)  # Find ROI by applying function

                out_frame = frame[ROI_y: (ROI_y + ROI_h), ROI_x: (ROI_x + ROI_w)]  # Crop
                name = os.path.basename(file).split(".")[0] + '_ROI.png'  # String to save image as
                cv2.imwrite(name, out_frame)

        complete.DoneWindow()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            dirname = None
            frame = None
            out_frame = None
            img_array = None
            out = None

