"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-08-04 for version 1.0b1

Filopodia analysis GUI provides interface to analyze fluorescence microscopy images of cells for morphology
See help window or help documentation at iCLOTS.org for more information

A later version of this application will optionally quantify a second stain indicating some biological function

"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import math
from skimage import measure
from skimage.feature import corner_harris, corner_peaks
from help import adhfilopodia as hp
from analysis import adhfil as an
from accessoryfn import chooseinput, error, fluor_single
import datetime


class FilAdhesionGUI(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = "iCLOTS"

        # Fonts
        boldfont = font.Font(weight="bold")
        smallfont = font.Font(size=8)

        # Tkinter variables
        # self.inputtype = tk.BooleanVar(value=True)  # Input type reference, true = single, false = directory
        self.umpix = tk.StringVar(value='1')  # micron-to-pixel ratio
        self.minarea = tk.IntVar(value=0)
        self.maxarea = tk.IntVar(value=10000)
        self.mainthresh = tk.IntVar(value=50)
        self.k = tk.DoubleVar(value=0.2)  # sharpness
        self.tr = tk.DoubleVar(value=0.5)  # relative threshold
        self.min_distance = tk.IntVar(value=5)  # minimum distance between peaks
        self.ps = tk.StringVar(value='gs')  # Primary stain color, default grayscale (r, g, b, gs)
        self.analysisbool = tk.BooleanVar(value=False)  # To indicate if final analysis has been run

        # Widgets
        self.title(name + " fluorescent filopodia analysis")

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

        # Minimum area label
        min_label = tk.Label(self, text="Minimum area\n(pix)")
        min_label['font'] = smallfont
        min_label.grid(row=6, column=0, padx=5, pady=5)
        # Minimum area spinbox
        min_spin = tk.Spinbox(
            self,
            from_=0,
            to=10000,
            increment=5,
            textvariable=self.minarea,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        min_spin.grid(row=6, column=1, padx=5, pady=5)
        # Maximum area label
        max_label = tk.Label(self, text="Maximum area\n(pix)")
        max_label['font'] = smallfont
        max_label.grid(row=7, column=0, padx=5, pady=5)
        # Maximum area spinbox
        max_spin = tk.Spinbox(
            self,
            from_=0,
            to=10000,
            increment=5,
            textvariable=self.maxarea,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        max_spin.grid(row=7, column=1, padx=5, pady=5)
        # Primary stain threshold label
        thresh_label = tk.Label(self, text="Membrane stain\nthreshold (a.u.)")
        thresh_label['font'] = smallfont
        thresh_label.grid(row=8, column=0, padx=5, pady=5)
        # Primary stain threshold spinbox
        thresh_spin = tk.Spinbox(
            self,
            from_=0,
            to=255,
            increment=1,
            textvariable=self.mainthresh,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        thresh_spin.grid(row=8, column=1, padx=5, pady=5)
        # Sharpness label
        sh_label = tk.Label(self, text="Sharpness (a.u.)")
        sh_label['font'] = smallfont
        sh_label.grid(row=9, column=0, padx=5, pady=5)
        # Function stain threshold spinbox
        sh_spin = tk.Spinbox(
            self,
            from_=0,
            to=2,
            increment=0.01,
            textvariable=self.k,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        sh_spin.grid(row=9, column=1, padx=5, pady=5)

        # Relative threshold label
        tr_label = tk.Label(self, text="Relative threshold\n(a.u.)")
        tr_label['font'] = smallfont
        tr_label.grid(row=10, column=0, padx=5, pady=5)
        # Function stain threshold spinbox
        tr_spin = tk.Spinbox(
            self,
            from_=0,
            to=1,
            increment=0.01,
            textvariable=self.tr,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        tr_spin.grid(row=10, column=1, padx=5, pady=5)

        # Minimum distance label
        md_label = tk.Label(self, text="Min. distance\n(pix)")
        md_label['font'] = smallfont
        md_label.grid(row=11, column=0, padx=5, pady=5)
        # Function stain threshold spinbox
        md_spin = tk.Spinbox(
            self,
            from_=1,
            to=1000,
            increment=1,
            textvariable=self.min_distance,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        md_spin.grid(row=11, column=1, padx=5, pady=5)

        # Help button
        help_button = tk.Button(self, text="Help", command=self.help)
        help_button.grid(row=12, column=0, padx=5, pady=5, sticky='W')

        # Image display label
        imgdisp_label = tk.Label(self, text="Image display with filopodia detection")
        imgdisp_label['font'] = boldfont
        imgdisp_label.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        # Current image name label
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=3, column=2, rowspan=2, columnspan=2, padx=5, pady=5)
        # Original image canvas
        self.img_canvas = tk.Canvas(self, width=300, height=300)
        self.img_canvas.grid(row=5, column=2, rowspan=6, padx=5, pady=5)
        # Manipulated image canvas
        self.manip_canvas = tk.Canvas(self, width=300, height=300)
        self.manip_canvas.grid(row=5, column=3, rowspan=6, padx=5, pady=5)
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
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=12, column=4, padx=5, pady=5, sticky='E')

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
        self.single_label.config(text=filename)
        self.dir_label.config(text="")

        # Call function to display image
        self.displayimg(filename)

    # Choose folder of images, return sorted list
    def dirfile(self):
        """Call a toplevel GUI to choose a folder of image files"""

        global filelist  # Required for other functions within class

        dirname, filelist = chooseinput.dirimgfile()


        self.dir_label.config(text=dirname)
        self.single_label.config(text="")

        # Call function to display image
        self.displayimg(filelist[0])  # Call displayimg on first image

        # Configure scale
        self.img_scale['to'] = len(filelist)
        self.img_scale.grid(row=11, column=2, columnspan=2, padx=5, pady=5)

    # Select colors
    def colorchoice(self):
        """Call a toplevel GUI to choose membrane (primary) stain as StringVar

        Primary stain options: red (r), blue (b), green (g), greyscale (gs)"""

        ps = fluor_single.SelectPrimaryFn().setcolors()
        self.ps.set(ps)

        # Update display
        self.displayimg(filelist[self.img_scale.get() - 1])

    # Function calls display function after each change in parameters
    def changeparameter(self):
        """As user interactively edits a parameter, the center display updates"""

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
        """Returns original image with threshold(s) applied and filopodia detected"""

        top, bottom, left, right = [10] * 4  # Used for creating border around individual cell images

        # Find primary color layer, set up color for labeling images
        # Here use an 'RGB' color scheme
        if self.ps.get() is 'r':
            pimg = img[:, :, 2]
            pcolor = [255, 0, 0]
        elif self.ps.get() is 'g':
            pimg = img[:, :, 1]
            pcolor = [0, 255, 0]
        elif self.ps.get() is 'b':
            pimg = img[:, :, 0]
            pcolor = [0, 0, 255]
        else:  # Default greyscale
            pimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pcolor = [128, 128, 128]

        # Apply current threshold settings to each layer
        thp, pimg_t = cv2.threshold(pimg, self.mainthresh.get(), 255, cv2.THRESH_BINARY)
        pimg_t = cv2.morphologyEx(pimg_t, cv2.MORPH_CLOSE, (5,5))  # Morphological closing to remove small holes

        # Layer images to create a three layer image to display
        manip = np.zeros((img.shape[0], img.shape[1], 3))  # Base - rows, columns, 3 layers
        manip[np.where(pimg_t == 255)] = pcolor   # Primary color

        # Label cell events - detect primary stain "blobs"
        label_img = measure.label(pimg_t)  # Create a labeled image as an input

        main_props = measure.regionprops_table(label_img, properties=('centroid', 'area', 'filled_area', 'image',
                                                                      'convex_area', 'convex_image',
                                                                      'bbox', 'eccentricity',
                                                                      'coords'))  # Image for count

        df = pd.DataFrame(main_props)
        if df is not None:  # If any cells found
            # Filter by min, max size (two step)
            df_filt = df[df['area'] > self.minarea.get()]
            df_filt = df_filt[df_filt['area'] < self.maxarea.get()]

            for i in range(len(df_filt)):
                indices = np.array(df_filt['coords'].iloc[i]).astype(int)  # Pixels comprising single cell

                # Filopodia count
                # Convex area is used so that inner corners don't also get counted - just outermost points
                # # This could result in some points within the convex shape being missed
                convex = df_filt['convex_image'].iloc[i]
                convex_image = np.asarray(convex * 255).astype(np.uint8)  # Convert to uint8 image for openCV
                # Border allows outermost points to be counted - corner detection doesn't work on points at edge
                image_with_border = cv2.copyMakeBorder(convex_image, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                                       value=0)


                # Find coordinates of corners
                coords = corner_peaks(corner_harris(image_with_border, k=self.k.get()), threshold_rel=self.tr.get(),
                                      min_distance=self.min_distance.get())
                # Use below if including blockSize and ksize
                # coords = cv2.corner_peaks(cv2.corner_harris(image_with_border, blockSize=1, ksize=1, k=k), min_distance=min_distance)

                if coords.any():
                    for pt in coords:  # This probably doesn't need to be a loop, would appreciate github pull requests

                        # Label filopodia on original and threshold image
                        pt1 = int(df_filt['centroid-1'].iloc[i] - convex_image.shape[1] / 2 + pt[1] - 10)
                        pt0 = int(df_filt['centroid-0'].iloc[i] - convex_image.shape[0] / 2 + pt[0] - 10)

                        cv2.circle(manip, tuple((pt1, pt0)), 1, (255, 255, 0), 2)

        manip = manip.astype(np.uint8)  # Convert to uint8 for pillow display

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

        an.RunAdhFilAnalysis.analysis(
                    self,
                    filelist,
                    self.umpix.get(),
                    self.minarea.get(),
                    self.maxarea.get(),
                    self.mainthresh.get(),
                    self.k.get(),
                    self.tr.get(),
                    self.min_distance.get(),
                    self.ps.get()
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
            an.RunAdhFilAnalysis.expnum(self,
                            filelist,
                            self.umpix.get(),
                            self.minarea.get(),
                            self.maxarea.get(),
                            self.mainthresh.get(),
                            self.k.get(),
                            self.tr.get(),
                            self.min_distance.get(),
                            self.ps.get()
                            )
            # Export graphs
            an.RunAdhFilAnalysis.expgraph(self)
            # Export images
            an.RunAdhFilAnalysis.expimgs(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expnum(self):
        """Export numerical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            # Export numbers
            an.RunAdhFilAnalysis.expnum(self,
                            filelist,
                            self.umpix.get(),
                            self.minarea.get(),
                            self.maxarea.get(),
                            self.mainthresh.get(),
                            self.k.get(),
                            self.tr.get(),
                            self.min_distance.get(),
                            self.ps.get()
                            )
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expgraph(self):
        """Export graphical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunAdhFilAnalysis.expgraph(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expimgs(self):
        """Export processed and/or labeled image data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunAdhFilAnalysis.expimgs(self)
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
            pimg = None
            pimg_t = None
            label_img = None
            df = None
            df_filt = None

