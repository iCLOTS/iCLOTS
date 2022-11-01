"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-11-01 for version 1.0b1

Single cell tracking analysis GUI analyzes a single brightfield video for velocity measurements
of individual cells

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
from help import single_cell_tracking as hp
from analysis import sct_fluor as an
from accessoryfn import chooseinput, error
import datetime


class FluorSCTGUI(tk.Toplevel):

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
        self.maxdiameter = tk.IntVar(value=15)  # maximum diameter of cells, must be odd integer
        self.search_range = tk.IntVar(value=60)  # search range for individual cells
        self.min_dist = tk.IntVar(value=100)  # minimum distance a cell must travel to be recorded
        self.analysisbool = tk.BooleanVar(value=False)  # To indicate if final analysis has been run
        # To indicate if numerical data has been exported
        self.analysis_exp_bool = tk.BooleanVar(value=False)
        self.x = tk.IntVar(value=0)  # ROI
        self.y = tk.IntVar(value=0)
        self.w = tk.IntVar(value=0)
        self.h = tk.IntVar(value=0)

        # Widgets
        # self.title(name + " brightfield deformability analysis")
        self.title(name + " single cell tracking analysis")

        # Input single video button
        single_video = tk.Button(self, text="Select single video", command=self.singlefile)
        single_video.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        # Selected single file name label
        self.single_label = tk.Label(self, text="")
        self.single_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky='W')

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
        # Micron-to-pixel ratio entry box
        self.fps_entry = tk.Entry(self, textvariable=self.fps, width=8)
        self.fps_entry.grid(row=3, column=1, padx=5, pady=5)

        # Maximum diameter label
        max_diam_label = tk.Label(self, text="Maximum\ndiameter (pix)")
        max_diam_label['font'] = smallfont
        max_diam_label.grid(row=4, column=0, padx=5, pady=5)
        # Maximum diameter spinbox
        max_diam = tk.Spinbox(
            self,
            from_=3,
            to=501,
            increment=2,
            textvariable=self.maxdiameter,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        max_diam.grid(row=4, column=1, padx=5, pady=5)

        # Search range label
        search_label = tk.Label(self, text="Search range\n(pix))")
        search_label['font'] = smallfont
        search_label.grid(row=5, column=0, padx=5, pady=5)
        # Search range spinbox
        search_spin = tk.Spinbox(
            self,
            from_=5,
            to=10000,
            increment=5,
            textvariable=self.search_range,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        search_spin.grid(row=5, column=1, padx=5, pady=5)

        # Min. distance label
        min_dist_label = tk.Label(self, text="Min. distance\ntraveled (pix))")
        min_dist_label['font'] = smallfont
        min_dist_label.grid(row=6, column=0, padx=5, pady=5)
        # Min. distance spinbox
        min_dist_spin = tk.Spinbox(
            self,
            from_=5,
            to=10000,
            increment=5,
            textvariable=self.min_dist,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        min_dist_spin.grid(row=6, column=1, padx=5, pady=5)

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.help)
        help_button.grid(row=8, column=0, padx=5, pady=5, sticky='W')

        # Image display label
        imgdisp_label = tk.Label(self, text="Frame display with background subtraction and cell detection")
        imgdisp_label['font'] = boldfont
        imgdisp_label.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        # Current video name label
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=2, column=2, rowspan=1, columnspan=2, padx=5, pady=5)
        # Original image canvas
        self.img_canvas = tk.Canvas(self, width=300, height=300)
        self.img_canvas.grid(row=3, column=2, rowspan=3, padx=5, pady=5)
        # Manipulated image canvas
        self.manip_canvas = tk.Canvas(self, width=300, height=300)
        self.manip_canvas.grid(row=3, column=3, rowspan=3, padx=5, pady=5)
        # Scale
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=1,
                                 command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid_forget()
        # Obtain results label
        obtain_label = tk.Label(self, text="Obtain results")
        obtain_label['font'] = boldfont
        obtain_label.grid(row=1, column=4, padx=5, pady=5)
        # Run analysis button
        run_button = tk.Button(self, text="Run analysis\nwith current parameters", command=self.runanalysis)
        run_button.grid(row=2, column=4, rowspan=1, padx=5, pady=5)
        # Export results label
        results_label = tk.Label(self, text="Export results")
        results_label['font'] = boldfont
        results_label.grid(row=3, column=4, padx=5, pady=5)
        # Export all button
        expall_button = tk.Button(
            self, text="Export graphical and numerical results", command=self.expall)
        expall_button.grid(row=4, column=4, padx=5, pady=5)
        # # Have temporarily removed option for individual type graph/numerical imports,
        # # will return in future versions
        # # Export numerical results button
        # expnum_button = tk.Button(
        #     self, text="Export numerical results", command=self.expnum)
        # expnum_button.grid(row=7, column=4, padx=5, pady=5)
        # # Export graphical results button
        # expgraph_button = tk.Button(
        #     self, text="Export graphical results", command=self.expgraph)
        # expgraph_button.grid(row=8, column=4, padx=5, pady=5)
        # Export images button
        # Crucial as exporting frames can be very computationally expensive
        expimg_button = tk.Button(
            self, text="Export labeled images", command=self.expimgs)
        expimg_button.grid(row=5, column=4, padx=5, pady=5)

        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=8, column=4, padx=5, pady=5, sticky='E')

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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=2)

    # Functions

    # Choose single image, return one-element list
    def singlefile(self):
        """Call a toplevel GUI to choose one video file"""

        global filelist, frames_crop, frames_bgr  # Required for other functions within class

        filename = chooseinput.videofile()
        filelist = [filename]
        # self.inputtype.set(True)
        self.single_label.config(text=filename)

        # Create set of frames
        # Defining a function to grayscale the image
        @pims.pipeline
        def gray(image):
            return image[:, :, 1]

        # Create a frames object using pims
        frames = gray(pims.PyAVReaderTimed(filename))
        frame_count = len(frames)

        # Generate map of all signal to assist with fluorescent ROI selection
        map = sum(frames)  # Sum along layer axis
        map_scaled = map * 255 // map.max()  # Scale max. value to 255
        map_scaled_img = map_scaled.astype(np.uint8)  # Convert to uint8

        # Apply a threshold
        threshold = np.percentile(map_scaled_img,
                                  10)  # Create a threshold by selecting signal above the 50th percentile
        d_c_ret, img_for_roi = cv2.threshold(map_scaled_img, threshold, 255,
                                             cv2.THRESH_BINARY)  # Apply binary threshold to create final map
        # Something like an Otsu threshold won't work because most of the signal is very light

        # Choose ROI
        # From last window, sometimes video quality can be spotty as recording starts
        self.chooseroi(img_for_roi)

        # Create background subtractor for analysis
        fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        kernel = np.ones((5,5), np.uint8)

        # Apply ROI to frames, create a series with background removed
        frames_crop = []
        frames_bgr = []
        for i in range(frame_count):
            frame_crop = frames[i][self.y.get():(self.y.get() + self.h.get()),
               self.x.get():(self.x.get() + self.w.get())]  # Create cropped image

            frame_bgr = fgbg.apply(frame_crop)  # Apply background removal
            frame_bgr_closed = cv2.morphologyEx(frame_bgr, cv2.MORPH_CLOSE, kernel)  # Morphological closing operation

            frames_crop.append(frame_crop.copy())
            frames_bgr.append(frame_bgr_closed.copy())

        # Configure scale
        self.img_scale['to'] = frame_count
        self.img_scale.grid(row=8, column=2, columnspan=2, padx=5, pady=5)

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

        # If maximum diameter parameter is odd, throw error
        if self.maxdiameter.get() % 2 == 0:
            error.ErrorWindow(message='Maximum diameter parameter\nmust be odd integer > 1')
        else:
            self.displayimg(frames_crop[self.img_scale.get() - 1])

    def setumpix(self, event=None):
        """Special parameter edit to set micron to pixel ratio"""

        self.umpix = self.umpix_entry.get()

    # Manage scale events
    def managescale(self, event):
        """As user interactively edits position of scale bar, the center display updates"""
        self.displayimg(frames_crop[self.img_scale.get()-1])

    # Display images
    def displayimg(self, filename):
        """Display current image and image name, incl. resize images to fit canvas, maintaining aspect ratio

        Input:
        -filename (either single file or selected from list from scale value"""

        # Label
        frame_number = self.img_scale.get()
        self.name_label.config(text='Frame %d' % frame_number)

        img = frames_crop[frame_number-1]

        # Detect cells within main image
        manip = self.celldetect(frames_bgr[frame_number-1])

        # Resize both images:
        imgr, manipr = self.resizeimg(img, manip)
        imgr_rgb = cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB)  # Match layers to pillow convention

        # Add images to canvas
        imgr_tk = ImageTk.PhotoImage(image=Image.fromarray(imgr_rgb))  # Original
        self.imgr_tk = imgr_tk  # A fix to keep image displayed
        self.img_canvas.create_image(150, 150, anchor='c', image=imgr_tk)
        manipr_tk = ImageTk.PhotoImage(image=Image.fromarray(manipr))  # Manipulated/detection image
        self.manipr_tk = manipr_tk  # A fix to keep image displayed
        self.manip_canvas.create_image(150, 150, anchor='c', image=manipr_tk)

    def celldetect(self, img):
        """Returns original image with parameters applied and cells detected"""

        # Convert image back to color to label with circles
        img_to_label = np.dstack((img, img, img))

        # Locate particles (ideally, cells) using Trackpy
        # See walkthrough: http://soft-matter.github.io/trackpy/dev/tutorial/walkthrough.html
        # Invert false - bg removal
        f = tp.locate(img, self.maxdiameter.get(), minmass=3000, invert=False)

        if f is not None:  # If any cells found

            # Label each cell event within image (red)
            for i in list(zip(f['x'], f['y'])):
                cv2.circle(img_to_label, (int(i[0]), int(i[1])), 5, (255, 0, 0), -1)  # Detection circle magenta

        manip = img_to_label.astype(np.uint8)  # Convert to uint8 for pillow display

        return manip

    def resizeimg(self, img, manip):
        """Resizes both the original and manipulated image to fit 150x500 canvas, maintaining aspect ratio"""

        # Calculate new dimensions
        height, width = img.shape
        factor = 300 / np.max((height, width))
        dim = (int(width * factor), int(height * factor))
        # Resize both
        imgr = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        manipr = cv2.resize(manip, dim, interpolation=cv2.INTER_AREA)

        return imgr, manipr

        return imgr, manipr

    # Run analysis
    def runanalysis(self):
        """Run final analysis using parameters from GUI"""

        self.analysisbool.set(True)  # Indicate analysis has been run

        an.RunFlSCTAnalysis.analysis(
                    self,
                    filelist,
                    frames_crop,
                    frames_bgr,
                    self.umpix.get(),
                    self.fps.get(),
                    self.maxdiameter.get(),
                    self.search_range.get(),
                    self.min_dist.get(),
                    self.x.get(),
                    self.y.get(),
                    self.w.get(),
                    self.h.get()
                    )
    # From analysis, call export functions if final analysis has already been run
    def expall(self):
        """Export all, references additional export functions"""

        self.analysis_exp_bool.set(True)  # Indicate numerical data has been exported

        if self.analysisbool.get() is True:
            now = datetime.datetime.now()
            # Create timestamped results directory
            current_dir = os.getcwd()  # Select filepath

            # # No longer applies while single export option, will return in future versions
            # if current_dir.split('/')[-1] == 'Results, graphical data':
            #     current_dir = os.path.dirname(current_dir)
            # elif current_dir.split('/')[-1] == 'Results, labeled image data':
            #     current_dir = os.path.dirname(current_dir)

            output_folder = os.path.join(current_dir, 'Results, ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
            os.mkdir(output_folder)
            os.chdir(output_folder)

            # Run all export options
            # Numerical data
            an.RunFlSCTAnalysis.expnum(self,
                    filelist,
                    self.umpix.get(),
                    self.fps.get(),
                    self.maxdiameter.get(),
                    self.search_range.get(),
                    self.min_dist.get(),
                    self.x.get(),
                    self.y.get(),
                    self.w.get(),
                    self.h.get())
            # Export graphs
            an.RunFlSCTAnalysis.expgraph(self)

        else:
            error.ErrorWindow(message='Please run analysis first')

    def expimgs(self):
        """Export processed and/or labeled image data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            if self.analysis_exp_bool.get() is True:
                an.RunFlSCTAnalysis.expimgs(self, frames_crop)
            else:
                error.ErrorWindow(message="Please export numerical data first")
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
            self.destroy()
            # Clear variables
            filelist = None
            img = None
            imgr = None
            manip = None
            manipr = None
            imgr_tk = None
            manipr_tk = None
            img_to_label = None
            frames = None
            frames_crop = None
            frames_bgr = None
            frame_bgr = None
            frame_bgr_closed = None
            f = None

