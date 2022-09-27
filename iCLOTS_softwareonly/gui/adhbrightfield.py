"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-01 for version 1.0b1

Brightfield adhesion analysis GUI analyzes brightfield microscopy images of cells
See help window or help documentation at iCLOTS.org for more information

"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import os
import cv2
import trackpy as tp
from PIL import Image, ImageTk
import numpy as np
from help import adhbrightfieldhelp as hp
from analysis import adhbrightfield as an
from accessoryfn import chooseinput, error, invertchoice
import datetime


class BrightfieldAdhesionGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Fonts
        boldfont = font.Font(weight="bold")
        smallfont = font.Font(size=8)

        # Tkinter variables
        self.umpix = tk.StringVar(value='1')  # micron-to-pixel ratio
        self.maxdiameter = tk.IntVar(value=15)  # maximum diameter of cells, must be odd integer
        self.minintensity = tk.IntVar(value=1000)  # minimum intensity of cells
        self.invert = tk.BooleanVar(value='True')  # invert parameter, true = dark on light, false = light on dark
        self.analysisbool = tk.BooleanVar(value=False)  # To indicate if final analysis has been run

        # Widgets
        self.title(name + " brightfield adhesion analysis")

        # Input single image button
        single_button = tk.Button(self, text="Select single image", command=self.singlefile)
        single_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        # Input directory button
        dir_button = tk.Button(self, text="Select folder of images", command=self.dirfile)
        dir_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Selected single file name label
        self.single_label = tk.Label(self, text="")
        self.single_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky='W')
        # Selected directory file name label
        self.dir_label = tk.Label(self, text="")
        self.dir_label.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky='W')

        # Set parameters label
        setparam_label = tk.Label(self, text="Set parameters")
        setparam_label['font'] = boldfont
        setparam_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Choose invert parameter button
        color_button = tk.Button(self, text="Set detection parameters", command=self.invertchoice)
        color_button['font'] = smallfont
        color_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # Micron-to-pixel ratio entry box label
        umpix_label = tk.Label(self, text=u"\u03bcm to pixel\nratio")
        umpix_label['font'] = smallfont
        umpix_label.grid(row=5, column=0, padx=5, pady=5)
        # Micron-to-pixel ratio entry box
        self.umpix_entry = tk.Entry(self, textvariable=self.umpix, width=8)
        self.umpix_entry.grid(row=5, column=1, padx=5, pady=5)

        # Maximum diameter label
        max_diam_label = tk.Label(self, text="Maximum\ndiameter (pix)")
        max_diam_label['font'] = smallfont
        max_diam_label.grid(row=6, column=0, padx=5, pady=5)
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
        max_diam.grid(row=6, column=1, padx=5, pady=5)
        #
        # Minimum intensity label
        min_int_label = tk.Label(self, text="Minimum\nintensity (a.u.)")
        min_int_label['font'] = smallfont
        min_int_label.grid(row=7, column=0, padx=5, pady=5)
        # Maximum area spinbox
        min_int = tk.Spinbox(
            self,
            from_=0,
            to=50000,
            increment=50,
            textvariable=self.minintensity,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        min_int.grid(row=7, column=1, padx=5, pady=5)

        # Help button
        help_button = tk.Button(self, text="Help", command=self.help)
        help_button.grid(row=10, column=0, padx=5, pady=5, sticky='W')

        # Image display label
        imgdisp_label = tk.Label(self, text="Image display with adhesion detection")
        imgdisp_label['font'] = boldfont
        imgdisp_label.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        # Current image name label
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=3, column=2, rowspan=2, columnspan=2, padx=5, pady=5)
        # Original image canvas
        self.img_canvas = tk.Canvas(self, width=300, height=300)
        self.img_canvas.grid(row=5, column=2, rowspan=3, padx=5, pady=5)
        # Manipulated image canvas
        self.manip_canvas = tk.Canvas(self, width=300, height=300)
        self.manip_canvas.grid(row=5, column=3, rowspan=3, padx=5, pady=5)
        # Scale
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=1,
                                 command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid_forget()
        # Obtain results label
        obtain_label = tk.Label(self, text="Obtain results")
        obtain_label['font'] = boldfont
        obtain_label.grid(row=2, column=4, padx=5, pady=5)
        # Run analysis button
        run_button = tk.Button(self, text="Run analysis\nwith current parameters", command=self.runanalysis)
        run_button.grid(row=3, column=4, rowspan=2, padx=5, pady=5)
        # Export results label
        results_label = tk.Label(self, text="Export results")
        results_label['font'] = boldfont
        results_label.grid(row=5, column=4, padx=5, pady=5)
        # Export all button
        expall_button = tk.Button(
            self, text="Export all results", command=self.expall)
        expall_button.grid(row=6, column=4, padx=5, pady=5)
        # # Have temporarily removed option for individual type imports, will return in future versions
        # # Export numerical results button
        # expnum_button = tk.Button(
        #     self, text="Export numerical results", command=self.expnum)
        # expnum_button.grid(row=7, column=4, padx=5, pady=5)
        # # Export graphical results button
        # expgraph_button = tk.Button(
        #     self, text="Export graphical results", command=self.expgraph)
        # expgraph_button.grid(row=8, column=4, padx=5, pady=5)
        # # Export images button
        # expimg_button = tk.Button(
        #     self, text="Export labeled images", command=self.expimgs)
        # expimg_button.grid(row=9, column=4, padx=5, pady=5)

        # Quit button
        # quit_button = tk.Button(self, text="Quit", command=self.destroy)
        # quit_button.grid(row=10, column=4, padx=5, pady=5, sticky='E')
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=10, column=4, padx=5, pady=5, sticky='E')

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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=2)

    # Functions

    # Choose single image, return one-element list
    def singlefile(self):
        """Call a toplevel GUI to choose one image file"""

        global filelist  # Required for other functions within class

        filename = chooseinput.singleimgfile()
        filelist = [filename]
        # self.inputtype.set(True)
        self.single_label.config(text=filename)
        self.dir_label.config(text="")

        # Call function to display image
        self.displayimg(filename)

    # Choose folder of images, return sorted list
    def dirfile(self):
        """Call a toplevel GUI to choose a folder of image files"""

        global filelist  # Required for other functions within class


        dirname, filelist = chooseinput.dirimgfile()
        # self.inputtype.set(False)
        self.dir_label.config(text=dirname)
        self.single_label.config(text="")

        # Call function to display image
        self.displayimg(filelist[0])  # Call displayimg on first image

        # Configure scale
        self.img_scale['to'] = len(filelist)
        self.img_scale.grid(row=9, column=2, columnspan=2, padx=5, pady=5)

    # Select colors
    def invertchoice(self):
        """Call a toplevel GUI to choose dark cell/light background or light cell/dark background

        True indicates dark on light, false indicates light on dark"""

        invertvar = invertchoice.SelectInvertChoice().setinvert()
        self.invert.set(invertvar)
        self.displayimg(filelist[self.img_scale.get() - 1])

    # Function calls display function after each change in parameters
    def changeparameter(self):
        """As user interactively edits a parameter, the center display updates"""

        # If maximum diameter parameter is odd, throw error
        if self.maxdiameter.get() % 2 == 0:
            error.ErrorWindow(message='Maximum diameter parameter\nmust be odd integer > 1')
        else:
            self.displayimg(filelist[self.img_scale.get() - 1])

    def setumpix(self, event=None):
        """Special parameter edit to set micron to pixel ratio"""

        self.umpix = self.umpix_entry.get()

    # Manage scale events
    def managescale(self, event):
        """As user interactively edits position of scale bar, the center display updates"""
        self.displayimg(filelist[self.img_scale.get()-1])

    # Display images
    def displayimg(self, filename):
        """Display current image and image name, incl. resize images to fit canvas, maintaining aspect ratio

        Input:
        -filename (either single file or selected from list from scale value"""

        # Label
        name_img = os.path.basename(filename).split(".")[0]
        self.name_label.config(text=name_img)

        img = cv2.imread(filename)

        # Detect cells within main image
        manip = self.celldetect(img)

        # Resize both images:
        imgr, manipr = self.resizeimg(img, manip)
        imgr_rgb = cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB)  # Match layers to pillow convention

        # Add images to canvas
        imgr_tk = ImageTk.PhotoImage(image=Image.fromarray(imgr_rgb))  # Original
        self.imgr_tk = imgr_tk  # A fix to keep image displayed
        self.img_canvas.create_image(125, 125, anchor='c', image=imgr_tk)
        manipr_tk = ImageTk.PhotoImage(image=Image.fromarray(manipr))  # Manipulated/detection image
        self.manipr_tk = manipr_tk  # A fix to keep image displayed
        self.manip_canvas.create_image(125, 125, anchor='c', image=manipr_tk)

    def celldetect(self, img):
        """Returns original image with parameters applied and cells detected"""

        # Convert image to grayscale for trackpy
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_to_label = img.copy()

        # Locate particles (ideally, cells) using Trackpy
        # See walkthrough: http://soft-matter.github.io/trackpy/dev/tutorial/walkthrough.html
        f = tp.locate(img_gray, self.maxdiameter.get(), minmass=self.minintensity.get(), invert=self.invert.get())

        if f is not None:  # If any cells found

            # Label each cell event within image (red)
            for i in list(zip(f['x'], f['y'])):
                cv2.circle(img_to_label, (int(i[0]), int(i[1])), 5, (0, 0, 255), -1)  # Detection circle magenta

        manip = img_to_label.astype(np.uint8)  # Convert to uint8 for pillow display

        return manip

    def resizeimg(self, img, manip):
        """Resizes both the original and manipulated image to fit 300x300 canvas, maintaining aspect ratio"""

        # Calculate new dimensions
        height, width, layers = img.shape
        factor = 300 / np.max((height, width))
        dim = (int(width * factor), int(height * factor))
        # Resize both
        imgr = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        manipr = cv2.resize(manip, dim, interpolation=cv2.INTER_AREA)

        return imgr, manipr


    # Run analysis
    def runanalysis(self):
        """Run final analysis using parameters from GUI"""

        self.analysisbool.set(True)  # Indicate analysis has been run

        an.RunAdhBrightfieldAnalysis.analysis(
                    self,
                    filelist,
                    self.umpix.get(),
                    self.maxdiameter.get(),
                    self.minintensity.get(),
                    self.invert.get()
                    )

    # From analysis, call export functions if final analysis has already been run
    def expall(self):
        """Export all, references additional export functions"""

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
            an.RunAdhBrightfieldAnalysis.expnum(self,
                    filelist,
                    self.umpix.get(),
                    self.maxdiameter.get(),
                    self.minintensity.get(),
                    self.invert.get()
                                          )
            # Export graphs
            an.RunAdhBrightfieldAnalysis.expgraph(self)
            # Export images
            an.RunAdhBrightfieldAnalysis.expimgs(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expnum(self):
        """Export numerical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            # Export numbers
            an.RunAdhBrightfieldAnalysis.expnum(self,
                    filelist,
                    self.umpix.get(),
                    self.maxdiameter.get(),
                    self.minintensity.get(),
                    self.invert.get()
                    )
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expgraph(self):
        """Export graphical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunAdhBrightfieldAnalysis.expgraph(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expimgs(self):
        """Export processed and/or labeled image data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunAdhBrightfieldAnalysis.expimgs(self)
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
            imgr_rgb = None
            imgr_tk = None
            manipr_tk = None
            img_gray = None
            img_to_label = None


