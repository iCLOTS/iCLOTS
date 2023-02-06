"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Help window display shows help documents for video adhesion application

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
        namelabel = tk.Label(self, text="Transient (video) adhesion time application")
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
        
        Script that analyzes transient adhesion in videomicroscopy of cells (e.g. platelets, RBCs, or WBCs)

        Script relies heavily on Trackpy python library, documentation available at:
        http://soft-matter.github.io/trackpy/v0.5.0/
        
        Input files:
        --Script is designed to work with a single .avi file
        ----If your data is saved as a series of frames, please see the suite of video editing tools to convert to .avi
        
        Users are lead to select an "invert" setting for analysis:
        --You can indicate that you would like to look for:
        ----Dark cells on a light background
        ----Light cells on a dark background
       
        Input parameters:
        --\u03bcm to pixel ratio: The ratio of microns (1e-6 m) to pixels for the image
        ----Use value = 1 for no conversion
        --Maximum diameter (pix)
        ----Maximum diameter of a cell to be considered, MUST be an odd integer
        ----This parameter can behave non-intuitively if set unnecessarily high
        ------If you are missing obvious cells, try lowering
        --Minimum cell intensity (a.u.)
        ----Minimum summed intensity of the cell, helps filter out obvious noise, debris, or clumped cells
        --Maximum cell intensity (a.u.)
        ----Maximum summed intensity of the cell, also helps filter out noise
        --FPS: Frames per second, the rate of imaging
        ----Note that FPS values pulled directly from videos can be inaccurate, especially if the video
        -----has been resized or edited in any way
        
        Output files
        --Single cell resolution
        --Optionally, each original frame with each detected cell labeled with an index exported as .png
        ----Exporting all frames can be computationally expensive (take a long time),
        -----but the developers suggest doing so anyways, at least for some portion of sample videos.
        ------It is useful for troubleshooting outliers, etc.
        
        --A corresponding .xlsx sheet containing:
        ----Area, circularity, and transit time for each cell - one sheet/video
        ----Descriptive statistics (min, mean, max, standard deviation for area, circularity, and transit time)
        ----Parameters used and time/date analysis was performed, for reference
        
        --Pairplot including area and circularity metrics

        Some tips from the iCLOTS team:
        
        Computational and experimental methods:
        --Trackpy searches for particles represented by image regions with Gaussian-like distributions
        ---of pixel brightness
        --It can be very tricky to get a good brightfield microfluidic video without significant debris
        ----It can also be tricky to adjust parameters to exclude this debris
        ----If it does not conflict with your experimental goals, try staining the cells
        ----If cells aren't in the channel for a significantly long time, you can also use the single cell tracking methods
        ------The primary difference between this application and the single cell tracking application is that this
        -------application does not include background subtraction, which would remove cells stuck for an exceedingly long time
        --Analysis methods cannot distinguish between overlapping cells
        ----If cells are significantly overlapping, repeat experiment with a lower cell concentration
        --It can be tricky to choose a good min_mass:max_mass range
        ----Try running with a very low/high value, respectively, and look at outputs to find a more suitable, narrow range
        --Owing to the heterogenous appearance of blood cell types, brightfield analysis is always challenging
        ----Consider using a fluorescent membrane stain
        -----if this does not conflict with your experimental goals, especially for WBCs/neutrophils
        --If the analysis is taking an unacceptably long time, you can resize videos to be smaller
        ----This may cause you to miss the smallest cells - if size is important, we suggest waiting it out
        
        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not pixel-to-\u03bcm ratio
        --Err on the high side of maximum intensity, low side of minimum mass parameter, and high side of maximum mass parameters
        ---unless data is particularly noisy or there's a large amount of debris
        
        Output files:
        --Analysis files are named after the video (.xlsx, .png)
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
        --Issues with software, requests for help troubleshooting, new application ideas, and general comments, suggestions, 
        ---and concerns are all welcome
        --The authors hope this will become a field-wide effort to improve quantitative data analysis precision 
        for common cell microscopy-based assays, particularly microfluidic assays

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')