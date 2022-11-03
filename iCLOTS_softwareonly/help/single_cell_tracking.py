"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-27 for version 1.0b1

Help window display shows help documents for single cell tracking applications

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
        namelabel = tk.Label(self, text="Single cell tracking application help")
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

        Script that analyzes videomicroscpy of individual cells transiting some microfluidic device
        Two separate applications for single cell tracking exist, one for brightfield microscopy
        and one for fluorescence microscopy. Both quantify relative size and velocity of moving cells. 
        The fluorescence microscopy application quantifies summed total fluorescence intensity as well.
        The fluorescence microscopy application begins by creating a map of all signal present within the video,
        which users then choose a region of interest from - this can help users find microfluidic channels
        within an otherwise dark background.

        Script relies heavily on Trackpy python library, documentation available at:
        http://soft-matter.github.io/trackpy/v0.5.0/
        
        Input files:
        --Application is designed to analyze a single video (.avi)
        ----The same input parameters are applied to each image
        ----If your data is saved as a series of frames, please convert to .avi using the video processing tools
        ----Video is displayed in the center of the analysis window
        ------Users can scroll through frames using the scale bar below
        --Users are automatically lead to choose a region of interest from the video for analysis
        
        Input parameters:
        --\u03bcm to pixel ratio: The ratio of microns (1e-6 m) to pixels for the image
        ----Use value = 1 for no conversion
        --Maximum diameter (pix)
        ----Maximum diameter of a cell to be considered, MUST be an odd integer
        ----This parameter can behave non-intuitively if set unnecessarily high
        ------If you are missing obvious cells, try lowering
        --Minimum cell intensity (a.u.)
        ----Minimum summed intensity of the cell, helps filter out obvious noise, debris, or clumped cells
        --Search area: the area (in pixels) to search for a feature in the subsequent frame
        ----Keep in mind that even if flow is unidirectional, the algorithm will search for cells/features in every direction
        ------e.g., if you're pretty sure cells travel no more than 10 pixels to the right in the subsequent frame,
        -------you would set your window as 20 pixels to account for the algorithm treating both sides as potential next locations
        --Minimum distance: The minimum detected distance traveled to be considered a valid data point (in pixels)
        ----This should mostly be used to filter out obvious noise
        ----Depending on the rate of imaging you may not see a cell at every position within the channel
        
        Output files
        --Single cell resolution
        --Optionally, each original frame with each detected cell labeled with an index exported as .png
        ----Exporting all frames can be computationally expensive (take a long time),
        -----but the developers suggest doing so anyways, at least for some portion of sample videos.
        ------It is useful for troubleshooting outliers, etc.
        
        --A corresponding .xlsx sheet containing:
        ----Distance traveled, transit time, velocity, area
        ------Start frame and end frame are also provided for reference
        ------Image processing algorithms applied to the video can make cells appear artificially large
        ------Area in pixels is a relative measurement, background subtraction can alter actual size     
        ----Descriptive statistics (min, mean, max, standard deviation for all metrics)
        ----Parameters used and time/date analysis was performed, for reference
        
        --Pairplot graph including area and velocity metrics
        
        Some tips from the iCLOTS team:
        
        Computational and experimental methods:
        --An algorithm called "background subtraction" is applied to the video frames 
        ---before tracking algorithms are used to detect cell movement. This removes features 
        ---that don't move - like microfluidic channel walls, etc. If cells are stuck in the channels 
        ---for exceedingly long amounts of time, the background subtraction algorithm may also remove them 
        ---You may need to adjust experimental variables, like pump speed or device height, 
        ---if cells are stuck for too long
        --Right now velocity is calculated as a mean from the first/last positions
        ---Later iterations of iCLOTS will calculate velocity and acceleration on a per-frame basis
        ----Cells should be traveling in a roughly straight line for most accurate results
        --Cells transiting the device so closely that they clump together will be detected as one cell 
        ---Check area measurements for especially large values to ensure this has not happened
        ---You may need to adjust experimental variables such as cell concentration to prevent clumping
        --Some quality measures are imposed on data points which may affect quantitative results
        ----To calculate an accurate velocity measurement, cells must be present in at least 3 frames 
        ----Users may need to reduce pump speed if cells are transiting the device too quickly
        
        --Trackpy searches for particles represented by image regions with Gaussian-like distributions
        ---of pixel brightness
        --Analysis methods cannot distinguish between cells transiting the channel together, in contact
        ----If cells are significantly contacting, repeat experiment with a lower cell concentration
        --If the analysis is taking an unacceptably long time, you can resize videos to be smaller
        ----This may cause you to miss the smallest cells - if size is important, we suggest waiting it out
        
        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not pixel-to-\u03bcm ratio
        --Err on the high side of maximum diameter and low side of minimum intensity parameters
        ---unless data is particularly noisy or there's a large amount of debris
        --The display screen only detects individual cells - it does not show which will/will not be included
        ---based on the two quality parameters you select, the search range for cells and the minimum
        ---distance a cell must travel
        ----Finding the correct parameters for your data set may take some trial and error - compare
        -----your labeled image data with your sorted excel sheet to figure out the best parameters
        -----for your individual data set
        
        Output files:
        --Analysis files are named after the folder containing all videos (.xlsx) or video names (.png)
        ----Avoid spaces, punctuation, etc. within file names
        --Library used to write excel sheets crops filenames for returned data sheets to avoid corrupted files
        ----Make sure the first 15 characters of each video name are distinct
        --.xlsx and pairplot data includes a sheet/graph with all videos combined
        ----Only use this when analyzing replicates of the same sample
        

        iCLOTS is under continuous development:
        --Feel free to contact the authors:
        ----Using the form at iCLOTS.org/contact
        ----By emailing lamlabcomputational@gmail.com
        ------If your question is about use with a particular set of data, please attach a sample file
        ------Data will not be shared outside of the iCLOTS development team
        --For those users who also code, please feel free to submit a pull request:
        ----github.com/iCLOTS
        ----You can also find analysis methods-only at github.com/LamLabEmory
        ------Analysis methods for this application are presented such that a folder of videos
        -------are analyzed at once - this may be useful for processing large numbers of videos
        --Issues with software, requests for help troubleshooting, new application ideas, and general comments, suggestions, 
        ---and concerns are all welcome
        --The authors hope this will become a field-wide effort to improve quantitative data analysis precision 
        for common cell microscopy-based assays, particularly microfluidic assays

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')