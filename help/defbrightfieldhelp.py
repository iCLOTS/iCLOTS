"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Help window display shows help documents for brightfield deformability application

"""

import tkinter as tk
import tkinter.scrolledtext as st


class HelpDisplay(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Widgets
        self.title(name + " help")

        # Widgets
        namelabel = tk.Label(self, text="Brightfield microscopy deformability application help\n"
                                        "a subset of our single cell tracking application")
        namelabel.grid(row=0, column=0, pady=10, padx=10)

        # Text box
        self.helptext = st.ScrolledText(self,
                                        width=100,
                                        height=20,
                                        font=("Arial",
                                              10))
        self.helptext.grid(row=1, column=0, pady=10, padx=10)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=2, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Inserting Text which is read only

        # Making the text read only
        self.helptext.insert(tk.INSERT, u"""\
        iCLOTS is a free software created for the analysis of common microfluidic and hematology workflow image data

        Brightfield deformability application is a subset of the single cell tracking algorithms
        that has been designed for specific use with the Lam lab 
        "biophysical flow cytometer" microfluidic device, a research-developed microfluidic designed 
        to provide a relative measure of cell deformability, a mechanical property. 
        The primary output of this application is a "single-cell deformability index," (units: \u03bcm/s)
        the speed at which a compressed cell transits the smallest microchannels. 
        A low sDI indicates that the cell transited the device slowly, unable to deform to fit through. 
        This device was first described in the manuscript 
        "Analyzing cell mechanics in hematologic diseases with microfluidic biophysical flow cytometry" 
        by Rosenbluth, Lam, and Fletcher published in 2008 in the journal Lab on a Chip. 
        It has since been used in manuscripts describing mechanical properties of red blood cells, 
        neutrophils, and hematopoietic stem cells (see relevant citations at iCLOTS.org). 
        The Lam lab is happy to share the design files and instructions for fabrication for 
        this microfluidic device upon request.
        
        A specialized secondary application analyzes fluoresence microscopy deformability device videos.
        In theory, this device could be used to monitor speed of single cells transiting any device in the
        x-direction.

        Application relies heavily on Trackpy python library, documentation available at:
        http://soft-matter.github.io/trackpy/v0.5.0/

        Input files:
        --Application is designed to analyze a single video (.avi)
        ----The same input parameters are applied to each image
        ----If your data is saved as a series of frames, please convert to .avi using the video processing tools
        ----Video is displayed in the center of the analysis window
        ------Users can scroll through frames using the scale bar below
        --Users are automatically lead to choose a region of interest from the video for analysis
        ----When using with the biophysical flow cytometer, please choose only the area of the microchannels

        Input parameters:
        --\u03bcm to pixel ratio: The ratio of microns (1e-6 m) to pixels for the image
        ----Use value = 1 for no conversion
        --Maximum diameter (pix)
        ----Maximum diameter of a cell to be considered, MUST be an odd integer
        ----This parameter can behave non-intuitively if set unnecessarily high
        ------If you are missing obvious cells, try lowering
        --Minimum cell intensity (a.u.)
        ----Minimum summed intensity of the cell, helps filter out obvious noise, debris, or clumped cells

        Output files
        --Single cell resolution
        --Optionally, each original frame with each detected cell labeled with an index exported as .png
        ----Exporting all frames can be computationally expensive (take a long time),
        -----but the developers suggest doing so anyways, at least for some portion of sample videos.
        ------It is useful for troubleshooting outliers, etc.

        --A corresponding .xlsx sheet containing:
        ----Area (pixels) and sDI (\u03bcm/s) per cell
        ------Start frame, end frame, distance traveled, and transit time are also provided
        ------Image processing algorithms applied to the video can make cells appear artificially large
        ------Area in pixels is a relative measurement        
        ----Descriptive statistics (min, mean, max, standard deviation for area and sDI)
        ----Parameters used and time/date analysis was performed, for reference

        --Pairplot graph including area and sDI metrics

        Some tips from the iCLOTS team:

        Computational and experimental methods:
        --An algorithm called "background subtraction" is applied to the video frames 
        ---before tracking algorithms are used to detect cell movement. This removes features 
        ---that don't move - like microfluidic channel walls, etc. If cells are stuck in the channels 
        ---for exceedingly long amounts of time, the background subtraction algorithm may also remove them. 
        ---You may need to adjust experimental variables, like pump speed or device height, 
        ---if cells are stuck for too long.
        --Cells transiting the device so closely that they clump together will be detected as one cell. 
        ---Check area measurements for especially large values to ensure this has not happened. 
        ---You may need to adjust experimental variables such as cell concentration to prevent clumping.
        --Some quality measures are imposed on data points which may affect quantitative results. 
        ----To calculate an accurate sDI measurement, cells must be present in at least 3 frames. 
        ----Users may need to reduce pump speed if cells are transiting the device too quickly.
        --Choose the target device height during fabrication methods carefully. 
        ----The width of the smallest channels in the device is about 6 µm. 
        ----The Lam lab typically fabricates microfluidic device masks at a height of 5 µm 
        ------for red blood cells or a height of 12-15 µm for white blood cells and associated cell lines.
        ----Cells must deform to fit through the device for meaningful deformability metrics.
        --Depending on how "sticky" cells are, the assay may measure adherence vs. deformability. 
        ----Coat channels with a bovine serum albumin (BSA) solution prior to using to prevent 
        -----non-specific binding. The developers suggest not reusing devices for multiple experiments.
        
        Some quality metrics are set with the biophysical flow cytometer in mind
        --Minimum number of frames (3)
        --Minimum distance traveled (1/3 the width of the rOI)
        --Search range (1/3 the width of the ROI)
        --Distance is calculated as x-direction only 

        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not pixel-to-\u03bcm ratio
        --Err on the high side of maximum diameter and low side of minimum intensity parameters
        ---unless data is particularly noisy or there's a large amount of debris
        ----By sorting in excel and comparing to labeled indices,
        -----you can verify that small/large objects are/are not cells

        Output files:
        --Analysis files are named after the video name (.xlsx, .png)
        ----Avoid spaces, punctuation, etc. within file names
        
        iCLOTS is under continuous development:
        --Feel free to contact the authors:
        ----Using the form at iCLOTS.org/contact
        ----By emailing lamlabcomputational@gmail.com
        ------If your question is about use with a particular set of data, please attach a sample file
        ------Data will not be shared outside of the iCLOTS development team
        --For those users who also code, please feel free to submit a pull request:
        ----github.com/iCLOTS
        ----You can also find analysis methods-only at github.com/LamLabEmory
        ------Analysis methods for this application are presented such that a folder of images
        -------are analyzed at once - this may be useful for processing large numbers of videos.
        --Issues with software, requests for help troubleshooting, new application ideas, and general comments, suggestions, 
        ---and concerns are all welcome
        --The authors hope this will become a field-wide effort to improve quantitative data analysis precision 
        for common cell microscopy-based assays, particularly microfluidic assays

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')