"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Resize file application edits contrast of files for use with iCLOTS analysis applications

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageTk
from accessoryfn import chooseinput, error, complete

class EditContrastGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Tkinter variables
        self.alpha = tk.DoubleVar(value=1)
        self.beta = tk.IntVar(value=0)
        self.filelist = None

        # Widgets
        self.title(name + " file contrast application")

        # Application title
        menutitle = tk.Label(self, text="Contrast editing application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input single image button
        single_img_button = tk.Button(self, text="Select single image", command=self.singleimgfile)
        single_img_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Input directory button
        dir_img_button = tk.Button(self, text="Select folder of images", command=self.dirimgfile)
        dir_img_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Input single video button
        single_video_button = tk.Button(self, text="Select single video", command=self.singlevideofile)
        single_video_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # Input directory button
        dir_video_button = tk.Button(self, text="Select folder of videos", command=self.dirvideofile)
        dir_video_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # File label, blank initially
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        # Canvas with image
        self.img_canvas = tk.Canvas(self, width=300, height=300)
        self.img_canvas.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        # Alpha label
        alpha_label = tk.Label(self, text="Alpha (gain)")
        alpha_label.grid(row=7, column=0, padx=5, pady=5)
        # Alpha spin box
        alpha_spin = tk.Spinbox(
            self,
            from_=-10,
            to=10,
            increment=0.01,
            textvariable=self.alpha,
            width=10,
            wrap=True,
            command=self.changespinbox
        )
        alpha_spin.grid(row=7, column=1, padx=5, pady=5)
        # Beta label
        beta_label = tk.Label(self, text="Beta (bias)")
        beta_label.grid(row=8, column=0, padx=5, pady=5)
        # Alpha spin box
        beta_spin = tk.Spinbox(
            self,
            from_=-255,
            to=255,
            increment=1,
            textvariable=self.beta,
            width=10,
            wrap=True,
            command=self.changespinbox
        )
        beta_spin.grid(row=8, column=1, padx=5, pady=5)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.save_rotated_files)
        submit_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

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
        self.columnconfigure(1, weight=1)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Choose single image, return one-element list
    def singleimgfile(self):
        filename = chooseinput.singleimgfile()
        self.filelist = [filename]
        self.name_label.config(text=os.path.basename(filename))

        # Call display with image
        self.img = cv2.imread(filename)
        self.displayimg(self.img)

    # Choose folder of images, return sorted list
    def dirimgfile(self):
        dirname, self.filelist = chooseinput.dirimgfile()
        self.name_label.config(text=os.path.basename(dirname))

        # Call display with first image
        self.img = cv2.imread(self.filelist[0])  # First image
        self.displayimg(self.img)

    # Choose single video, return one-element list
    def singlevideofile(self):
        filename = chooseinput.videofile()
        self.filelist = [filename]
        self.name_label.config(text=filename)

        # Call display with first frame
        video = cv2.VideoCapture(filename)
        status, self.img = video.read()
        self.displayimg(self.img)

    # Choose folder of videos, return sorted list
    def dirvideofile(self):
        dirname, self.filelist = chooseinput.dirvideofile()
        self.name_label.config(text=dirname)

        # Call display with first frame of first video
        video = cv2.VideoCapture(self.filelist[0])
        status, self.img = video.read()
        self.displayimg(self.img)

    # Save files with angle
    def save_rotated_files(self):
        if self.filelist is not None:
            # Create strings to indicate operations performed
            str_alpha = str(self.alpha.get()).replace('.', 'p')
            str_beta = str(self.beta.get()).replace('-', 'n')

            outputfolder = os.path.join(os.getcwd(), 'Contrast a' + str_alpha + ', b' + str_beta)

            if os.path.exists(outputfolder):  # Set up outut folder
                shutil.rmtree(outputfolder)
            os.mkdir(outputfolder)
            os.chdir(outputfolder)

            # Resize each image
            for file in self.filelist:
                if '.avi' in file:
                    capture = cv2.VideoCapture(file)

                    # Dimensions, must be exact for videos
                    w = int(np.floor(capture.get(3)))  # float
                    h = int(np.floor(capture.get(4)))  # float
                    fps = capture.get(cv2.CAP_PROP_FPS)  # frames per second

                    name = os.path.basename(file).split(".")[0] + '_a' + str_alpha + '_b' + \
                           str_beta + '.avi'  # String to save image as, .avi

                    # Set up video writer object
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # .avi
                    out = cv2.VideoWriter(name, fourcc, fps, (w, h))

                    # Edit contrast of each frame
                    while True:
                        ret, frame = capture.read()
                        if ret == True:
                            out_frame = self.editcontrast(frame, w, h)
                            out.write(out_frame)
                        else:
                            break

                    # Finish
                    capture.release()
                    out.release()
                    cv2.destroyAllWindows()

                else:  # For images
                    frame = cv2.imread(file)

                    h, w, l = frame.shape  # Dimensions of frame

                    out_frame = self.editcontrast(frame, w, h)  # Apply function
                    name = os.path.basename(file).split(".")[0] + '_a' + str_alpha + '_b' + \
                           str_beta + '.png'  # String to save image as
                    cv2.imwrite(name, out_frame)

            complete.DoneWindow()

    def editcontrast(self, frame, w, h):
        """Function to edit contrast of a frame - can be an image file or a video frame"""

        # Apply changes in contrast
        out_frame = frame * self.alpha.get() + self.beta.get()
        out_frame[out_frame < 0] = 0
        out_frame[out_frame > 255] = 255  # Prevents high values from 'looping' to 0 as uint8
        out_frame = np.uint8(out_frame)  # Prevents video errors

        # Ensure dimensions are correct, important for videos
        out_frame = cv2.resize(out_frame, (w, h), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

        return out_frame

    # Display images as rotated on canvas
    def displayimg(self, img):

        h, w, l = img.shape

        out = self.editcontrast(img, w, h)

        # Resize to fit on canvas
        rf = 300 / np.max((out.shape[0], out.shape[1]))
        dim = (int(out.shape[1] * rf), int(out.shape[0] * rf))
        imgr = cv2.resize(out, dim, interpolation=cv2.INTER_AREA)

        imgr_rgb = cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB)  # Match layers to pillow convention

        # Add image to canvas
        imgr_tk = ImageTk.PhotoImage(image=Image.fromarray(imgr_rgb))
        self.imgr_tk = imgr_tk  # " "
        self.img_canvas.create_image(150, 150, anchor='c', image=imgr_tk)

    # Spinbox function
    def changespinbox(self):
        self.displayimg(self.img)

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            filelist = None
            video = None
            out = None
            img = None
            imgr = None
            imgr_tk = None
