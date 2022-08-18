"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-07-18 for version 1.0b1

Fluorescent adhesion analysis GUI provides interface to analyze fluorescence microscopy images of cells
See help window or help documentation at iCLOTS.org for more information

A later version of this application will optionally count regions of a functional stain

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from skimage import measure
from help import adhfluorhelp as hp
from analysis import adhfluor as an
from accessoryfn import chooseinput, error, fluor_ps
import datetime


class FluorAdhesionGUI(tk.Toplevel):

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
        self.fnthresh = tk.IntVar(value=30)
        self.ps = tk.StringVar(value='gs')  # Primary stain color, default grayscale (r, g, b, gs)
        self.fs = tk.StringVar(value='n')  # Functional stain color, default none (r, g, b, n)
        self.analysisbool = tk.BooleanVar(value=False)  # To indicate if final analysis has been run

        # Widgets
        self.title(name + " fluorescent adhesion analysis")

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
        # Functional stain threshold label
        fnl_label = tk.Label(self, text="Functional stain\nthreshold (a.u.)")
        fnl_label['font'] = smallfont
        fnl_label.grid(row=9, column=0, padx=5, pady=5)
        # Function stain threshold spinbox
        fnl_spin = tk.Spinbox(
            self,
            from_=0,
            to=255,
            increment=1,
            textvariable=self.fnthresh,
            width=6,
            wrap=True,
            command=self.changeparameter
            )
        fnl_spin.grid(row=9, column=1, padx=5, pady=5)
        # Help button
        help_button = tk.Button(self, text="Help", command=self.help)
        help_button.grid(row=12, column=0, padx=5, pady=5, sticky='W')

        # Image display label
        imgdisp_label = tk.Label(self, text="Image display with adhesion detection")
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
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=12, column=4, padx=5, pady=5, sticky='E')

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
        """Call a toplevel GUI to choose membrane (primary), functional stains as StringVar

        Primary stain options: red (r), blue (b), green (g), greyscale (gs)
        Functional stain options: red (r), blue (b), green (g), none (n)"""

        ps, fs = fluor_ps.SelectPrimaryFn().setcolors()
        self.ps.set(ps)
        self.fs.set(fs)

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
        """Returns original image with threshold(s) applied and cells detected

        Primary stain: returned as white, functional stain: returned as magenta, detected events: cyan circle"""

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
        # Find functional color layer
        if self.fs.get() is 'r':
            fimg = img[:, :, 2]
            fcolor = [255, 0, 0]
        elif self.fs.get() is 'g':
            fimg = img[:, :, 1]
            fcolor = [0, 255, 0]
        elif self.ps.get() is 'b':
            fimg = img[:, :, 0]
            fcolor = [0, 0, 255]
        else:  # Default none
            fimg = np.zeros((img.shape[0], img.shape[1]))  # Blank array
            fcolor = [0, 0, 0]  # Holder

        # Apply current threshold settings to each layer
        thp, pimg_t = cv2.threshold(pimg, self.mainthresh.get(), 255, cv2.THRESH_BINARY)
        thf, fimg_t = cv2.threshold(fimg, self.fnthresh.get(), 255, cv2.THRESH_BINARY)

        # Layer images to create a three layer image to display
        manip = np.zeros((img.shape[0], img.shape[1], 3))  # Base - rows, columns, 3 layers
        manip[np.where(pimg_t == 255)] = pcolor   # Primary color
        manip[np.where(fimg_t == 255)] = fcolor  # Secondary stain

        # Label cell events - detect primary stain "blobs"
        p_label_img = measure.label(pimg_t)  # Create a labeled image as an input
        p_props = measure.regionprops_table(p_label_img, properties=('centroid', 'area'))
        p_df = pd.DataFrame(p_props)
        if p_df is not None:  # If any cells found
            # Filter by min, max size (two step)
            p_df_filt = p_df[p_df['area'] > self.minarea.get()]
            p_df_filt = p_df_filt[p_df_filt['area'] < self.maxarea.get()]

            # Label each cell event within image (cyan)
            for i in list(zip(p_df_filt['centroid-1'], p_df_filt['centroid-0'])):
                cv2.circle(manip, (int(i[0]), int(i[1])), 5, (0, 255, 255), -1)  # Detection circle magenta

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

        an.RunAdhFluorAnalysis.analysis(
                    self,
                    filelist,
                    self.umpix.get(),
                    self.minarea.get(),
                    self.maxarea.get(),
                    self.mainthresh.get(),
                    self.fnthresh.get(),
                    self.ps.get(),
                    self.fs.get()
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
            an.RunAdhFluorAnalysis.expnum(self,
                                          filelist,
                                          self.umpix.get(),
                                          self.minarea.get(),
                                          self.maxarea.get(),
                                          self.mainthresh.get(),
                                          self.fnthresh.get(),
                                          self.ps.get(),
                                          self.fs.get()
                                          )
            # Export graphs
            an.RunAdhFluorAnalysis.expgraph(self)
            # Export images
            an.RunAdhFluorAnalysis.expimgs(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expnum(self):
        """Export numerical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            # Export numbers
            an.RunAdhFluorAnalysis.expnum(self,
                    filelist,
                    self.umpix.get(),
                    self.minarea.get(),
                    self.maxarea.get(),
                    self.mainthresh.get(),
                    self.fnthresh.get(),
                    self.ps.get(),
                    self.fs.get()
                    )
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expgraph(self):
        """Export graphical data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunAdhFluorAnalysis.expgraph(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    def expimgs(self):
        """Export processed and/or labeled image data, referenced by Export all option"""

        if self.analysisbool.get() is True:
            an.RunAdhFluorAnalysis.expimgs(self)
        else:
            error.ErrorWindow(message='Please run analysis first')

    # Open help window
    def help(self):
        """All applications have a button to reference help documentation"""

        # Display specified help file
        hp.HelpDisplay()

