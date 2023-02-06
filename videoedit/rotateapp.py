"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-13 for version 1.0b1

Resize file application rotates files for use with iCLOTS analysis applications

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

class RotateGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Tkinter variables
        self.angle = tk.DoubleVar(value=0)
        self.filelist = None

        # Widgets
        self.title(name + " file rotation application")

        # Application title
        menutitle = tk.Label(self, text="File rotation application")
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
        # Rotation angle label
        angle_label = tk.Label(self, text="Angle of rotation")
        angle_label.grid(row=7, column=0, padx=5, pady=5)
        # Rotation angle spin box
        angle_spin = tk.Spinbox(
            self,
            from_=-180,
            to=180,
            increment=0.5,
            textvariable=self.angle,
            width=10,
            wrap=True,
            command=self.changespinbox
        )
        angle_spin.grid(row=7, column=1, padx=5, pady=5)
        # Submit button
        submit_button = tk.Button(self, text="Submit for rotation", command=self.save_rotated_files)
        submit_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

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

    # Resize each file
    def rotate(self, mat):

        height, width = mat.shape[:2]  # image shape has 3 dimensions
        image_center = (width / 2,
                        height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, self.angle.get(), 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rmat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

        # Ensure dimensions are correct, important for videos
        out = cv2.resize(rmat, (width, height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

        return out

    # Save files with angle
    def save_rotated_files(self):
        if self.filelist is not None:
            # Format resize factor into string
            angle_str = str(self.angle.get()).replace(".", "p").replace("-", "n")
            # Make new directory to save images into, change directory
            outputfolder = os.path.join(os.path.dirname(self.filelist[0]), 'Rotated files, angle ' + angle_str)
            if os.path.exists(outputfolder):  # Set up outut folder
                shutil.rmtree(outputfolder)
            os.mkdir(outputfolder)
            os.chdir(outputfolder)
            # Resize each image
            for file in self.filelist:
                filename = os.path.basename(file).split(".")[0]
                newfilename = filename + "_rotated-" + angle_str + "." + os.path.basename(file).split(".")[1]

                if os.path.basename(file).split(".")[1] == "avi":  # If video
                    video = cv2.VideoCapture(file)
                    w = int(np.floor(video.get(3)))  # float
                    h = int(np.floor(video.get(4))) # float
                    fps = video.get(cv2.CAP_PROP_FPS)

                    # Video writer output
                    fourcc = cv2.VideoWriter_fourcc(*"XVID")
                    out = cv2.VideoWriter(newfilename, fourcc, fps, (w, h))

                    while True:
                        ret, frame = video.read()
                        if ret == True:
                            b = self.rotate(frame)
                            out.write(b)
                        else:
                            break

                    video.release()
                    out.release()
                    cv2.destroyAllWindows()

                elif os.path.basename(file).split(".")[1] in ["png", "jpg", "tif"]:
                    read = cv2.imread(file)
                    resizedimg = self.rotate(read)
                    cv2.imwrite(newfilename, resizedimg)

            complete.DoneWindow()

        else:
            error.ErrorWindow(message='Please select file(s) to rotate')

    # Display images as rotated on canvas
    def displayimg(self, img):

        out = self.rotate(img)

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
