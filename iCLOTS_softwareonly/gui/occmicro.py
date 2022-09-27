"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-18 for version 1.0b1

Fluorescent occlusion and accumulation analysis in microchannels GUI provides interface
to analyze single or time series fluoresence microscopy image files
See help window or help documentation at iCLOTS.org for more information

A later version of this application will incorporate channel detection for brightfield microscopy images


"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import os
import glob
import cv2
from PIL import Image, ImageTk
import numpy as np
from help import occmicrohelp as hp  # Edit
from analysis import occmicro as an  # Edit
from accessoryfn import chooseinput, error, fluor_multi  # Edit
import datetime


class MicrochannelOccGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Fonts
        boldfont = font.Font(weight="bold")
        smallfont = font.Font(size=8)

        # Tkinter variables
        self.umpix = tk.DoubleVar(value=1)  # micron-to-pixel ratio
        self.rchannel = tk.BooleanVar(value=False)  # Present channels
        self.gchannel = tk.BooleanVar(value=False)
        self.bchannel = tk.BooleanVar(value=False)
        self.rthresh = tk.IntVar(value=50)  # Channel thresholds
        self.gthresh = tk.IntVar(value=50)
        self.bthresh = tk.IntVar(value=50)
        self.x = tk.IntVar(value=0)  # ROI
        self.y = tk.IntVar(value=0)
        self.w = tk.IntVar(value=0)
        self.h = tk.IntVar(value=0)
        self.analysisbool = tk.BooleanVar(value=False)  # To indicate if final analysis has been run

        # Widgets
        self.title(name + " microchannel occlusion and accumulation analysis")

        # Input single image button
        single_button = tk.Button(self, text="Select single image", command=self.singlefile)
        single_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        # Input directory button
        dir_button = tk.Button(self, text="Select folder of images", command=self.dirfile)
        dir_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Selected single file name label
        self.single_label = tk.Label(self, text="")
        self.single_label.grid(row=0, column=2, columnspan=5, padx=5, pady=5, sticky='W')
        # Selected directory file name label
        self.dir_label = tk.Label(self, text="")
        self.dir_label.grid(row=1, column=2, columnspan=5, padx=5, pady=5, sticky='W')

        # Set parameters label
        setparam_label = tk.Label(self, text="Set parameters")
        setparam_label['font'] = boldfont
        setparam_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Choose colors button
        color_button = tk.Button(self, text="Set colors for analysis", command=self.colorchoice)
        color_button['font'] = smallfont
        color_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # Micron-to-pixel ratio entry box label
        umpix_label = tk.Label(self, text=u"\u03bcm to pixel\nratio")
        umpix_label['font'] = smallfont
        umpix_label.grid(row=5, column=0, padx=5, pady=5)
        # Micron-to-pixel ratio entry box
        self.umpix_entry = tk.Entry(self, textvariable=self.umpix, width=8)
        self.umpix_entry.grid(row=5, column=1, padx=5, pady=5)

        # Red threshold spin box label
        self.red_label = tk.Label(self, text="Red threshold\n(a.u.)")
        self.red_label['font'] = smallfont
        # Red channel threshold spin box
        self.red_spin = tk.Spinbox(
            self,
            from_=0,
            to=255,
            increment=1,
            textvariable=self.rthresh,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        # Green threshold spin box label
        self.green_label = tk.Label(self, text="Green threshold\n(a.u.)")
        self.green_label['font'] = smallfont
        # Green channel threshold spin box
        self.green_spin = tk.Spinbox(
            self,
            from_=0,
            to=255,
            increment=1,
            textvariable=self.gthresh,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        # Blue threshold spin box label
        self.blue_label = tk.Label(self, text="Blue threshold\n(a.u.)")
        self.blue_label['font'] = smallfont
        # Blue channel threshold spin box
        self.blue_spin = tk.Spinbox(
            self,
            from_=0,
            to=255,
            increment=1,
            textvariable=self.bthresh,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        # pack_forget until color is chosen
        self.red_label.grid_forget()
        self.red_spin.grid_forget()
        self.green_label.grid_forget()
        self.green_spin.grid_forget()
        self.blue_label.grid_forget()
        self.blue_spin.grid_forget()

        # Image display label
        imgdisp_label = tk.Label(self, text="Image display with fluorescent signal detection")
        imgdisp_label['font'] = boldfont
        imgdisp_label.grid(row=2, column=2, columnspan=5, padx=5, pady=5)
        # Current image name label
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=3, column=2, rowspan=2, columnspan=5, padx=5, pady=5)
        # Original image canvas
        self.img_canvas = tk.Canvas(self, width=150, height=500)
        self.img_canvas.grid(row=5, column=2, rowspan=6, padx=5, pady=5)
        # Map canvas
        self.map_canvas = tk.Canvas(self, width=150, height=500)
        self.map_canvas.grid(row=5, column=3, rowspan=6, padx=5, pady=5)
        # Red canvas, "forget" until color choice
        self.red_canvas = tk.Canvas(self, width=150, height=500)
        self.red_canvas.grid_forget()
        # Original image canvas, "forget" until color choice
        self.green_canvas = tk.Canvas(self, width=150, height=500)
        self.green_canvas.grid_forget()
        # Original image canvas, "forget" until color choice
        self.blue_canvas = tk.Canvas(self, width=150, height=500)
        self.blue_canvas.grid_forget()

        # Help button
        help_button = tk.Button(self, text="Help", command=self.help)
        help_button.grid(row=12, column=0, padx=5, pady=5, sticky='W')

        # Scale
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=1,
                                 command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid_forget()
        # Obtain results label
        obtain_label = tk.Label(self, text="Obtain results")
        obtain_label['font'] = boldfont
        obtain_label.grid(row=2, column=7, padx=5, pady=5)
        # Run analysis button
        run_button = tk.Button(self, text="Run analysis\nwith current parameters", command=self.runanalysis)
        run_button.grid(row=3, column=7, rowspan=2, padx=5, pady=5)
        # Export results label
        results_label = tk.Label(self, text="Export results")
        results_label['font'] = boldfont
        results_label.grid(row=5, column=7, padx=5, pady=5)
        # Export all button
        expall_button = tk.Button(
            self, text="Export all results", command=self.expall)
        expall_button.grid(row=6, column=7, padx=5, pady=5)

        # # Have temporarily removed option for individual type imports, will return in future versions
        # # Export numerical results button
        # expnum_button = tk.Button(
        #     self, text="Export numerical results", command=self.expnum)
        # expnum_button.grid(row=7, column=7, padx=5, pady=5)
        # # Export graphical results button
        # expgraph_button = tk.Button(
        #     self, text="Export graphical results", command=self.expgraph)
        # expgraph_button.grid(row=8, column=7, padx=5, pady=5)
        # # Export images button
        # expimg_button = tk.Button(
        #     self, text="Export labeled images", command=self.expimgs)
        # expimg_button.grid(row=9, column=7, padx=5, pady=5)

        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=12, column=7, padx=5, pady=5, sticky='E')

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
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=2)

    # Functions

    # Choose single image, return one-element list
    def singlefile(self):
        """Call a toplevel GUI to choose one image file"""

        global filelist  # Required for other functions within class

        filename = chooseinput.singleimgfile()
        filelist = [filename]
        self.single_label.config(text=filename)
        self.dir_label.config(text="")

        # Choose ROI
        self.chooseroi(filelist[0])

        # Call function to display image
        self.displayimg(filename)

    # Choose folder of images, return sorted list
    def dirfile(self):
        """Call a toplevel GUI to choose a folder of image files"""

        global filelist  # Required for other functions within class

        dirname, filelist = chooseinput.dirimgfile()
        self.dir_label.config(text=dirname)
        self.single_label.config(text="")

        # Choose ROI
        self.chooseroi(filelist[-1])  # Last image, hypothetically most signal

        # Call function to display image
        self.displayimg(filelist[0])  # Call displayimg on first image

        # Configure scale
        self.img_scale['to'] = len(filelist)
        self.img_scale.grid(row=11, column=2, columnspan=6, padx=5, pady=5)

    # Choose ROI with microchannels
    def chooseroi(self, filename):
        """Choose region of interest, ideally, straight portions of microchannel(s) using a draggable rectangle

        toplevel immediately appears after selection of file(s)"""

        # Read image
        imgarray = cv2.imread(filename)
        fromCenter = False  # Set up to choose as a drag-able rectangle rather than a rectangle chosen from center
        r = cv2.selectROI("Image", imgarray, fromCenter)  # Choose ROI function from cv2 - opens a window to choose
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

    # Select colors
    def colorchoice(self):
        """Call a toplevel GUI to choose channels (red, green, blue) as BooleanVar

        """

        # Set by resetting canvases to empty
        self.red_label.grid_forget()
        self.red_spin.grid_forget()
        self.red_canvas.grid_forget()

        self.green_label.grid_forget()
        self.green_spin.grid_forget()
        self.green_canvas.grid_forget()

        self.blue_label.grid_forget()
        self.blue_spin.grid_forget()
        self.blue_canvas.grid_forget()

        rchannel, gchannel, bchannel = fluor_multi.SelectMultiColors().setcolors()
        self.rchannel.set(rchannel)
        self.gchannel.set(gchannel)
        self.bchannel.set(bchannel)

        # Show threshold parameters and canvas depending on colors chosen
        if self.rchannel.get() is True:
            self.red_label.grid(row=6, column=0, padx=5, pady=5)
            self.red_spin.grid(row=6, column=1, padx=5, pady=5)
            self.red_canvas.grid(row=5, column=4, rowspan=6, padx=5, pady=5)

        if self.gchannel.get() is True:
            self.green_label.grid(row=7, column=0, padx=5, pady=5)
            self.green_spin.grid(row=7, column=1, padx=5, pady=5)
            self.green_canvas.grid(row=5, column=5, rowspan=6, padx=5, pady=5)

        if self.bchannel.get() is True:
            self.blue_label.grid(row=8, column=0, padx=5, pady=5)
            self.blue_spin.grid(row=8, column=1, padx=5, pady=5)
            self.blue_canvas.grid(row=5, column=6, rowspan=6, padx=5, pady=5)

        self.displayimg(filelist[self.img_scale.get() - 1])

    # Function calls display function after each change in parameters
    def changeparameter(self):
        """As user interactively edits a parameter, the center display updates"""

        self.displayimg(filelist[self.img_scale.get() - 1])

    # Manage scale events
    def managescale(self, event):
        """As user interactively edits position of scale bar, the center display updates"""

        self.displayimg(filelist[self.img_scale.get()-1])

    # Display images
    def displayimg(self, filename):
        """Display current image, manipulated analysis images, and image name,
        incl. resize images to fit canvas, maintaining aspect ratio

        Input:
        -filename (either single file or selected from list from scale value
        -colors (rchannel, gchannel, bchannel boolean values)"""

        # Label
        name_img = os.path.basename(filename).split(".")[0]
        self.name_label.config(text=name_img)

        img = cv2.imread(filename)
        # Crop
        crop = img[self.y.get():(self.y.get() + self.h.get()),
               self.x.get():(self.x.get() + self.w.get()), :]  # Create cropped image

        # Display original
        # Resize
        imgrs = self.resizeimg(crop)
        # Match layers to pillow convention
        imgrs_rgb = cv2.cvtColor(imgrs, cv2.COLOR_BGR2RGB)
        # Add images to canvas
        imgrs_tk = ImageTk.PhotoImage(image=Image.fromarray(imgrs_rgb))
        self.imgrs_tk = imgrs_tk  # A fix to keep image displayed
        self.img_canvas.create_image(75, 250, anchor='c', image=imgrs_tk)

        # Create and display map
        # Convert images to binary with thresholds
        ret, img_th_red = cv2.threshold(crop[:, :, 2], self.rthresh.get(), 255, cv2.THRESH_BINARY)  # Red
        ret, img_th_green = cv2.threshold(crop[:, :, 1], self.gthresh.get(), 255, cv2.THRESH_BINARY)  # Green
        ret, img_th_blue = cv2.threshold(crop[:, :, 0], self.bthresh.get(), 255, cv2.THRESH_BINARY)  # Blue

        # Set up holder
        mapbin = np.zeros((self.h.get(), self.w.get()))
        mapbin_ext = mapbin.copy()
        # Threshold map
        layered_arr = np.array([img_th_red, img_th_green, img_th_blue]).sum(axis=0)
        mapbin[layered_arr >= 1] = 1
        # Compress into one line
        mapbin_1d = np.sum(mapbin, axis=1)
        # Extend to width of channel
        mapbin_ext[np.hstack(mapbin_1d * self.w.get()) > 1] = 255
        mapbin_tl = np.dstack((mapbin_ext, mapbin_ext, mapbin_ext)).astype(np.uint8)
        # Display
        # Resize
        imgrs_map = self.resizeimg(mapbin_tl)
        # Add images to canvas
        imgrs_map_tk = ImageTk.PhotoImage(image=Image.fromarray(imgrs_map))
        self.imgrs_map_tk = imgrs_map_tk  # A fix to keep image displayed
        self.map_canvas.create_image(75, 250, anchor='c', image=imgrs_map_tk)

        # Display red if rchannel is True
        if self.rchannel.get() is True:
            # Layer threshold over map
            mapbin_red = mapbin_tl.copy()
            mapbin_red[np.where(img_th_red == 255)] = [255, 0, 0]
            # Display
            # Resize
            imgrs_red = self.resizeimg(mapbin_red)
            # Add images to canvas
            imgrs_red_tk = ImageTk.PhotoImage(image=Image.fromarray(imgrs_red))
            self.imgrs_red_tk = imgrs_red_tk  # A fix to keep image displayed
            self.red_canvas.create_image(75, 250, anchor='c', image=imgrs_red_tk)

        # Display green if gchannel is True
        if self.gchannel.get() is True:
            # Layer threshold over map
            mapbin_green = mapbin_tl.copy()
            mapbin_green[np.where(img_th_green == 255)] = [0, 255, 0]
            # Display
            # Resize
            imgrs_green = self.resizeimg(mapbin_green)
            # Add images to canvas
            imgrs_green_tk = ImageTk.PhotoImage(image=Image.fromarray(imgrs_green))
            self.imgrs_green_tk = imgrs_green_tk  # A fix to keep image displayed
            self.green_canvas.create_image(75, 250, anchor='c', image=imgrs_green_tk)

        # Display blue if bchannel is True
        if self.bchannel.get() is True:
            # Layer threshold over map
            mapbin_blue = mapbin_tl.copy()
            mapbin_blue[np.where(img_th_blue == 255)] = [0, 0, 255]
            # Display
            # Resize
            imgrs_blue = self.resizeimg(mapbin_blue)
            # Add images to canvas
            imgrs_blue_tk = ImageTk.PhotoImage(image=Image.fromarray(imgrs_blue))
            self.imgrs_blue_tk = imgrs_blue_tk  # A fix to keep image displayed
            self.blue_canvas.create_image(75, 250, anchor='c', image=imgrs_blue_tk)

    def resizeimg(self, img):
        """Resizes original or manipulated image to fit 500x150 canvas, maintaining aspect ratio"""

        # Calculate new dimensions
        height, width, layers = img.shape
        if width/150 > height/500:
            factor = 150 / width
        else:  # If height ratio greater or if equal (if equal factor same)
            factor = 500/height

        dim = (int(width * factor), int(height * factor))
        # Resize both
        imgr = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        return imgr

    # Run analysis
    def runanalysis(self):
        """Run final analysis using parameters from GUI"""

        self.analysisbool.set(True)  # Indicate analysis has been run

        an.RunOccAccMicroAnalysis.analysis(
                    self,
                    filelist,
                    self.umpix.get(),
                    self.rchannel.get(),
                    self.rthresh.get(),
                    self.gchannel.get(),
                    self.gthresh.get(),
                    self.bchannel.get(),
                    self.bthresh.get(),
                    self.x.get(),
                    self.y.get(),
                    self.w.get(),
                    self.h.get()
                    )

    # From analysis, call export functions if final analysis has already been run
    def expall(self):
        """Export all, references additional export functions"""

        if self.analysisbool.get() is True:
            now = datetime.datetime.now()
            # Create timestamped results directory
            current_dir = os.getcwd()  # Select filepath

            # # No longer applies while single export option, will return in future versions
            # if current_dir.split('/')[-1] == 'Results, labeled image data':
            #     current_dir = os.path.dirname(current_dir)

            output_folder = os.path.join(current_dir, 'Results, ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
            os.mkdir(output_folder)
            os.chdir(output_folder)

            # Run all export options
            # Numerical data
            an.RunOccAccMicroAnalysis.expnum(
                    self,
                    filelist,
                    self.umpix.get(),
                    self.rchannel.get(),
                    self.rthresh.get(),
                    self.gchannel.get(),
                    self.gthresh.get(),
                    self.bchannel.get(),
                    self.bthresh.get(),
                    self.x.get(),
                    self.y.get(),
                    self.w.get(),
                    self.h.get()
                    )
            # Export graphs
            an.RunOccAccMicroAnalysis.expgraph(self)
            # Export images
            an.RunOccAccMicroAnalysis.expimgs(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expnum(self):
        """Export numerical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            # Export numbers
            an.RunOccAccMicroAnalysis.expnum(
                    self,
                    filelist,
                    self.umpix.get(),
                    self.rchannel.get(),
                    self.rthresh.get(),
                    self.gchannel.get(),
                    self.gthresh.get(),
                    self.bchannel.get(),
                    self.bthresh.get(),
                    self.x.get(),
                    self.y.get(),
                    self.w.get(),
                    self.h.get()
                    )
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expgraph(self):
        """Export graphical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunOccAccMicroAnalysis.expgraph(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expimgs(self):
        """Export processed and/or labeled image data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunOccAccMicroAnalysis.expimgs(self)
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
            crop = None
            imgrs = None
            imgrs_rgb = None
            imgrs_tk = None
            img_th_red = None
            img_th_green = None
            img_th_blue = None
            map_bin = None
            mapbin_ext = None
            layered_arr = None
            mapbin_tl = None
            imgrs_map = None
            imgrs_map_tk = None
            mapbin_red = None
            mapbin_green = None
            mapbin_blue = None
            imgrs_red = None
            imgrs_green = None
            imgrs_blue = None
            imgrs_red_tk = None
            imgrs_blue_tk = None
            imgrs_green_tk = None
