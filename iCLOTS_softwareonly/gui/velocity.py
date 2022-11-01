"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-01 for version 1.0b1

Velocity analysis GUI analyzes a single brightfield video, fluorescent would also work if there's a range of intensities
of cells transiting any microfluidic device

"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import os
import cv2
import pims
import trackpy as tp
import warnings
warnings.filterwarnings("ignore", module="trackpy")
from PIL import Image, ImageTk
import numpy as np
from help import velocityhelp as hp
from analysis import velocity as an
from accessoryfn import chooseinput, error
import datetime


class VelocityGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Fonts
        boldfont = font.Font(weight="bold")
        smallfont = font.Font(size=8)

        # Tkinter variables
        self.umpix = tk.StringVar(value='1')  # micron-to-pixel ratio
        self.fps = tk.StringVar(value='1')  # Frames per second imaging rate
        self.n_bins = tk.IntVar(value=7)  # Number of bins to divide channel into
        self.n_points = tk.IntVar(value=500)  # Number of possible points
        self.block_size = tk.IntVar(value=5)  # Block size
        self.winsize_x = tk.IntVar(value=50)  # Window size
        self.winsize_y = tk.IntVar(value=20)
        self.analysisbool = tk.BooleanVar(value = True)# To indicate if final analysis has been run
        # To indicate if user would like frames exported
        self.expall_first = tk.BooleanVar(value=False)
        self.expall_linspace = tk.BooleanVar(value=False)
        self.x = tk.IntVar(value=0)  # ROI
        self.y = tk.IntVar(value=0)
        self.w = tk.IntVar(value=0)
        self.h = tk.IntVar(value=0)

        # Widgets
        # self.title(name + " brightfield deformability analysis")
        self.title(name + " velocity timecourse and profile analysis")

        # Input single video button
        single_video = tk.Button(self, text="Select single video", command=self.singlefile)
        single_video.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        # Selected single file name label
        self.single_label = tk.Label(self, text="")
        self.single_label.grid(row=0, column=2, padx=5, pady=5, sticky='W')

        # Set parameters label
        setparam_label = tk.Label(self, text="Set parameters")
        setparam_label['font'] = boldfont
        setparam_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Micron-to-pixel ratio entry box label
        umpix_label = tk.Label(self, text=u"\u03bcm to pixel\nratio")
        umpix_label['font'] = smallfont
        umpix_label.grid(row=2, column=0, padx=5, pady=5)
        # Micron-to-pixel ratio entry box
        self.umpix_entry = tk.Entry(self, textvariable=self.umpix, width=8)
        self.umpix_entry.grid(row=2, column=1, padx=5, pady=5)

        # FPS entry box label
        fos_label = tk.Label(self, text="Frames per second\nimaging rate (FPS)")
        fos_label['font'] = smallfont
        fos_label.grid(row=3, column=0, padx=5, pady=5)
        # FPS ratio entry box
        self.fps_entry = tk.Entry(self, textvariable=self.fps, width=8)
        self.fps_entry.grid(row=3, column=1, padx=5, pady=5)

        # Number of bins label (green)
        n_bins_label = tk.Label(self, text="Number of profile\nbins (n)", foreground='red')
        n_bins_label['font'] = smallfont
        n_bins_label.grid(row=4, column=0, padx=5, pady=5)

        # Number of bins spin box
        n_bins_spin = tk.Spinbox(
            self,
            from_=3,
            to=100,
            increment=1,
            textvariable=self.n_bins,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        n_bins_spin.grid(row=4, column=1, padx=5, pady=5)

        # Number of possible points label (cyan)
        n_bins_label = tk.Label(self, text="Maximum number of\nfeatures (n)", foreground='cyan')
        n_bins_label['font'] = smallfont
        n_bins_label.grid(row=5, column=0, padx=5, pady=5)

        # Number of possible points spinbox
        n_points_spin = tk.Spinbox(
            self,
            from_=100,
            to=1500,
            increment=50,
            textvariable=self.n_points,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        n_points_spin.grid(row=5, column=1, padx=5, pady=5)

        # Block size label (blue)
        block_label = tk.Label(self, text="Block size\ndiameter (pix)", foreground='blue')
        block_label['font'] = smallfont
        block_label.grid(row=6, column=0, padx=5, pady=5)

        # Block size spin box
        block_spin = tk.Spinbox(
            self,
            from_=3,
            to=100,
            increment=1,
            textvariable=self.block_size,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        block_spin.grid(row=6, column=1, padx=5, pady=5)

        # Window x label (red)
        win_x_label = tk.Label(self, text="Window size\nx direction (pix)", foreground='green')
        win_x_label['font'] = smallfont
        win_x_label.grid(row=7, column=0, padx=5, pady=5)

        # Window x spin box
        win_x_spin = tk.Spinbox(
            self,
            from_=10,
            to=500,
            increment=5,
            textvariable=self.winsize_x,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        win_x_spin.grid(row=7, column=1, padx=5, pady=5)

        # Window y label (red)
        win_y_label = tk.Label(self, text="Window size\ny direction (pix)", foreground='green')
        win_y_label['font'] = smallfont
        win_y_label.grid(row=8, column=0, padx=5, pady=5)

        # Window y spin box
        win_y_spin = tk.Spinbox(
            self,
            from_=10,
            to=500,
            increment=5,
            textvariable=self.winsize_y,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        win_y_spin.grid(row=8, column=1, padx=5, pady=5)

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.help)
        help_button.grid(row=9, column=0, padx=5, pady=5, sticky='W')

        # Image display label
        imgdisp_label = tk.Label(self, text="Frame display with parameters and displacement (frame 2+) indicated")
        imgdisp_label['font'] = boldfont
        imgdisp_label.grid(row=1, column=2, padx=5, pady=5)
        # Current video name label
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=2, column=2, rowspan=1, padx=5, pady=5)
        # Manipulated image canvas
        self.manip_canvas = tk.Canvas(self, width=500, height=300)
        self.manip_canvas.grid(row=2, column=2, rowspan=6, padx=5, pady=5)
        # Scale
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=1,
                                 command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid_forget()
        # Obtain results label
        obtain_label = tk.Label(self, text="Obtain results")
        obtain_label['font'] = boldfont
        obtain_label.grid(row=1, column=3, padx=5, pady=5)
        # Run analysis button
        run_button = tk.Button(self, text="Run analysis\nwith current parameters", command=self.runanalysis)
        run_button.grid(row=2, column=3, rowspan=1, padx=5, pady=5)
        # Export results label
        results_label = tk.Label(self, text="Export results")
        results_label['font'] = boldfont
        results_label.grid(row=3, column=3, padx=5, pady=5)

        # Export first 100 images checkbox
        first_100_cb = tk.Checkbutton(self, text='Export first 100 frames', variable=self.expall_first, onvalue=True, offvalue=False)
        first_100_cb.grid(row=4, column=3, columnspan=3, sticky='W')
        # Export every 100th image checkbox
        every_100_cb = tk.Checkbutton(self, text='Export every 100th frame', variable=self.expall_linspace, onvalue=True, offvalue=False)
        every_100_cb.grid(row=5, column=3, columnspan=3, sticky='W')

        # Export all button
        expall_button = tk.Button(
            self, text="Export graphical, numerical,\nand selected image results", command=self.expall)
        expall_button.grid(row=6, column=3, padx=5, pady=5)

        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=9, column=4, padx=5, pady=5, sticky='E')

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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)

    # Functions

    # Choose single image, return one-element list
    def singlefile(self):
        """Call a toplevel GUI to choose one video file"""

        global filelist, frames_crop, frames_bgr  # Required for other functions within class

        filename = chooseinput.videofile()
        self.filelist = [filename]
        # self.inputtype.set(True)
        self.single_label.config(text=filename)

        # Read video
        cap = cv2.VideoCapture(filename)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Record width of video frame (pixels)
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Record height of video frame (pixels)
        ret, self.first_frame = cap.read()

        # Choose ROI
        # From last window, sometimes video quality can be spotty as recording starts
        self.chooseroi(self.first_frame)

        # Create set of 10 frames
        cap_ret = True
        count = 0
        self.test_frames = []  # Init list
        while count < 10 and cap_ret:
            cap_ret, frame = cap.read()  # Read
            frame_crop = frame[self.y.get():(self.y.get() + self.h.get()), self.x.get():(self.x.get() + self.w.get()), :]  # Create cropped image
            frame_gray = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2GRAY)  # One layer
            self.test_frames.append(frame_gray)
            count += 1

        # Configure scale
        self.img_scale['to'] = 10
        self.img_scale.grid(row=8, column=2, padx=5, pady=5)

        # Call function to display image
        self.displayimg(filename)

        self.analysisbool.set(False)  # Indicate analysis has been run


    # Choose ROI with microchannels
    def chooseroi(self, frame):
        """Choose region of interest, ideally, straight portions of microchannel(s) using a draggable rectangle

        toplevel immediately appears after selection of file(s)"""

        fromCenter = False  # Set up to choose as a drag-able rectangle rather than a rectangle chosen from center
        r = cv2.selectROI("Select region of interest", frame, fromCenter)  # Choose ROI function from cv2 - opens a window to choose
        x = int(r[0])  # Take result of selectROI and put into a variable
        y = int(r[1])  # " "
        w = int(r[2])  # " "
        h = int(r[3])  # " "
        cv2.destroyAllWindows()  # Destroy window when ready - requires any keyboard input

        # Set variables
        self.x.set(x)
        self.y.set(y)
        self.w.set(w)
        self.h.set(h)

    # Function calls display function after each change in parameters
    def changeparameter(self):
        """As user interactively edits a parameter, the center display updates"""

        self.displayimg(self.test_frames[self.img_scale.get() - 1])

    def setumpix(self, event=None):
        """Special parameter edit to set micron to pixel ratio"""

        self.umpix = self.umpix_entry.get()

    # Manage scale events
    def managescale(self, event):
        """As user interactively edits position of scale bar, the center display updates"""
        self.displayimg(self.test_frames[self.img_scale.get()-1])

    # Display images
    def displayimg(self, filename):
        """Display current image and image name, incl. resize images to fit canvas, maintaining aspect ratio

        Input:
        -filename (either single file or selected from list from scale value"""

        # Label
        frame_number = self.img_scale.get()
        self.name_label.config(text='Frame %d' % frame_number)

        img = self.test_frames[frame_number-1]

        # Detect cells within main image
        manip = self.trajdetect(frame_number)

        # Resize image
        manipr = self.resizeimg(manip)
        manipr_rgb = cv2.cvtColor(manipr, cv2.COLOR_BGR2RGB)  # Match layers to pillow convention

        # Add image to canvas
        manipr_tk = ImageTk.PhotoImage(image=Image.fromarray(manipr_rgb))  # Manipulated/detection image
        self.manipr_tk = manipr_tk  # A fix to keep image displayed
        self.manip_canvas.create_image(250, 150, anchor='c', image=manipr_tk)

    def trajdetect(self, frame_number):
        """Returns original image with parameters applied and trajectories detected"""

        # Set up parameters
        # params for ShiTomasi corner detection
        # to be used in line of code: cv2.goodFeaturesToTrack
        # helpful: https://docs.opencv.org/master/d4/d8c/tutorial_py_shi_tomasi.html
        max_corners = self.n_points.get()
        qual_level = 0.01
        min_dist_st = self.block_size.get()/2
        block_size = self.block_size.get()
        feature_params = dict(maxCorners=max_corners,  # n best corners to track, more = more computationally expensive
                              qualityLevel=qual_level,
                              # parameter characterizing the minimal accepted quality of image corners
                              minDistance=min_dist_st,  # minimum
                              # possible Euclidean distance between the returned corners (pix)
                              blockSize=block_size)  # size of an average block for computing a derivative covariation matrix over each pixel neighborhood

        # Parameters for lucas kanade optical flow
        # to be used in the line of code: cv2.calcOpticalFlowPyrLK
        # helpful: https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
        win_size = (int(self.winsize_y.get()/2), int(self.winsize_x.get()/2))  # Pyramid level (max_level) adjustment
        max_level = 2
        iter = 1  # Numer of iterations (for search criteria)
        min_dist_klt = 1  # Minimum distance that a corner must move (for search criteria)
        lk_params = dict(winSize=win_size,  # size of the search window at each pyramid level (w, h)
                         maxLevel=max_level,
                         # 0-based maximal pyramid level number, 0 = original, 1 = 2 levels used, 2 = 3 levels used
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, iter,
                                   min_dist_klt))  # termination criteria of the iterative search algorithm

        frame_gray = self.test_frames[frame_number]  # Image
        frame_color = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)

        if frame_number >= 2:  # If second or greater frame (need first for initial points)

            init_gray = self.test_frames[frame_number - 1]  # Init. image

            # Select initial points
            p0 = cv2.goodFeaturesToTrack(frame_gray, mask=None, **feature_params)
            if p0 is not None:
                # Track points
                p1, st, err = cv2.calcOpticalFlowPyrLK(init_gray, frame_gray, p0, None, **lk_params)
                if p1.any():  # If points found
                    good_new = p1[st == 1]
                    good_old = p0[st == 1]

                    for i, (new, old) in enumerate(zip(good_new, good_old)):
                        a, b = new.ravel()
                        c, d = old.ravel()

                        frame_color = cv2.arrowedLine(frame_color, (int(c), int(b)), (int(a), int(d)), (255, 255, 0), 1)  # Cyan arrow

        # Add nbins in red (horizontal)
        bin_y_height = self.h.get()/self.n_bins.get()  # Divide height by length bins - 1 (9 lines indicate 10 bins)
        for i in range(self.n_bins.get()):  # For each line
            cv2.line(frame_color, (0, int(bin_y_height*i)), (self.w.get(), int(bin_y_height*i)), (0, 0, 255), thickness=2)  # (x1, y1) (x2, y2)

        # Add block size in blue (top left)
        cv2.rectangle(frame_color, (0, 0), (self.block_size.get(), self.block_size.get()), (255, 0, 0), thickness=2)

        # Add window size (bottom right)
        cv2.rectangle(frame_color, (self.w.get()-self.winsize_x.get(), self.h.get()-self.winsize_y.get()),
                      (self.w.get(), self.h.get()), (0, 255, 0), thickness=2)

        return frame_color

    def resizeimg(self, manip):
        """Resizes both the original and manipulated image to fit 150x500 canvas, maintaining aspect ratio"""

        # Calculate new dimensions
        height, width, layer = manip.shape
        if width/500 > height/300:
            factor = 500 / width
        else:  # If height ratio greater or if equal (if equal factor same)
            factor = 300/height

        dim = (int(width * factor), int(height * factor))
        # Resize both
        imgr = cv2.resize(manip, dim, interpolation=cv2.INTER_AREA)

        return imgr

    # Run analysis
    def runanalysis(self):
        """Run final analysis using parameters from GUI"""

        self.analysisbool.set(True)  # Indicate analysis has been run

        an.RunVelocityAnalysis.analysis(
            self,
            self.filelist,
            self.umpix.get(),
            self.fps.get(),
            self.n_bins.get(),
            self.n_points.get(),
            self.block_size.get(),
            self.winsize_x.get(),
            self.winsize_y.get(),
            self.x.get(),
            self.y.get(),
            self.w.get(),
            self.h.get())


    # From analysis, call export functions if final analysis has already been run
    def expall(self):
        """Export all, references additional export functions"""

        if self.analysisbool.get() is True:

            now = datetime.datetime.now()
            # Create timestamped results directory
            current_dir = os.getcwd()  # Select filepath

            output_folder = os.path.join(current_dir, 'Results, ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
            os.mkdir(output_folder)
            os.chdir(output_folder)

            # Run all export options
            # Numerical data
            an.RunVelocityAnalysis.expnum(self)
            # Export graphs
            an.RunVelocityAnalysis.expgraph(self)
            # Images
            an.RunVelocityAnalysis.expimgs(self, self.expall_first.get(), self.expall_linspace.get())

        else:
            error.ErrorWindow(message='Please run analysis first')

    # Open help window
    def help(self):
        """All applications have a button to reference help documentation"""

        # Display specified help file
        hp.HelpDisplay()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()  # Self

            # Clear variables
            self.filelist = None
            self.imgr = None
            self.manipr = None
            frame_crop = None
            test_frames = None
            frame_color = None
            frame_gray = None

