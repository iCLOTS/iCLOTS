"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-13 for version 1.0b1

Video length cropping app cuts video to a specified start and end frame

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageTk
import pims
from accessoryfn import chooseinput, error, complete

class CropLengthGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")

        # Tkinter variables
        self.startframe = tk.IntVar(value=0)
        self.endframe = tk.IntVar(value=0)
        self.filename = None

        # Widgets
        self.title(name + " video file length cropping application")

        # Application title
        menutitle = tk.Label(self, text="Video file length cropping application")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input single video button
        single_video_button = tk.Button(self, text="Select single video", command=self.singlevideofile)
        single_video_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # File label, blank initially
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Frame number, blank initially
        self.frame_label = tk.Label(self, text="")
        self.frame_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # Canvas with image
        self.img_canvas = tk.Canvas(self, width=300, height=300)
        self.img_canvas.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        # Scale, not present initially
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=1,
                                 command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid_forget()
        # Start frame label
        start_label = tk.Label(self, text="New start frame")
        start_label.grid(row=6, column=0, padx=5, pady=5)
        # Resize factor entry box
        start_entry = tk.Entry(self, width=10, textvariable=self.startframe)
        start_entry.grid(row=6, column=1, padx=5, pady=5)
        # Start frame label
        end_label = tk.Label(self, text="New end frame")
        end_label.grid(row=7, column=0, padx=5, pady=5)
        # Resize factor entry box
        end_entry = tk.Entry(self, width=10, textvariable=self.endframe)
        end_entry.grid(row=7, column=1, padx=5, pady=5)
        # Submit button
        submit_button = tk.Button(self, text="Submit for shortening", command=self.crop_video_length)
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


    # Choose single video, display
    def singlevideofile(self):
        self.filename = chooseinput.videofile()
        self.name_label.config(text=os.path.basename(self.filename))

        # Create set of frames
        # Defining a function to grayscale the image
        @pims.pipeline
        def gray(image):
            return image[:, :, 1]

        # Create a frames object using pims
        self.frames = gray(pims.PyAVReaderTimed(self.filename))
        frame_count = len(self.frames)

        # Configure scale
        self.img_scale['to'] = frame_count - 1
        self.img_scale.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Set up frame number label
        self.frame_label.config(text='Frame 0')

        # Auto-set endframe value in entry box
        self.endframe.set(frame_count)

        # Call function to display image
        self.displayimg(self.frames[0])

    # Display images as rotated on canvas
    def displayimg(self, frame):

        # Resize to fit on canvas
        rf = 300 / np.max((frame.shape[0], frame.shape[1]))
        dim = (int(frame.shape[1] * rf), int(frame.shape[0] * rf))
        imgr = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

        imgr_rgb = cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB)  # Match layers to pillow convention

        # Add image to canvas
        imgr_tk = ImageTk.PhotoImage(image=Image.fromarray(imgr_rgb))
        self.imgr_tk = imgr_tk  # " "
        self.img_canvas.create_image(150, 150, anchor='c', image=imgr_tk)


    # Manage scale events
    def managescale(self, event):
        """As user interactively edits position of scale bar, the center display updates"""
        self.displayimg(self.frames[self.img_scale.get()])

        # Set up frame number label
        text_label = 'Frame ' + str(self.img_scale.get())
        self.frame_label.config(text=text_label)

    # Crop and save video
    def crop_video_length(self):
        if self.filename is not None:
            # Make new directory to save images into, change directory
            range_text = str(self.startframe.get()) + '-' + (str(self.endframe.get()))
            outputfolder = os.path.join(os.path.dirname(self.filename), 'Shortened video, ' + range_text)
            if os.path.exists(outputfolder):  # Set up outut folder
                shutil.rmtree(outputfolder)
            os.mkdir(outputfolder)
            os.chdir(outputfolder)

            video = cv2.VideoCapture(self.filename)
            w = int(np.floor(video.get(3)))  # float
            h = int(np.floor(video.get(4))) # float
            fps = video.get(cv2.CAP_PROP_FPS)

            newfilename = os.path.basename(self.filename).split(".")[0] + "_shortened-" + range_text + ".avi"

            # Video writer output
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(newfilename, fourcc, fps, (w, h))

            # Only write frames within range
            count = 0
            while True:
                ret, frame = video.read()
                if ret == True:
                    if (count > self.startframe.get()) and (count < self.endframe.get()):
                        out.write(frame)
                else:
                    break
                count += 1

            video.release()
            out.release()
            cv2.destroyAllWindows()

            complete.DoneWindow()

        else:
            error.ErrorWindow(message='Please select video to shorten')

    # Display images as rotated on canvas
    def displayimg(self, img):

        # Resize to fit on canvas
        rf = 300 / np.max((img.shape[0], img.shape[1]))
        dim = (int(img.shape[1] * rf), int(img.shape[0] * rf))
        imgr = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        imgr_rgb = cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB)  # Match layers to pillow convention

        # Add image to canvas
        imgr_tk = ImageTk.PhotoImage(image=Image.fromarray(imgr_rgb))
        self.imgr_tk = imgr_tk  # " "
        self.img_canvas.create_image(150, 150, anchor='c', image=imgr_tk)

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            filelist = None
            img = None
            imgr_rgb = None
            imgr_tk = None
            frames = None
            video = None
            out = None
