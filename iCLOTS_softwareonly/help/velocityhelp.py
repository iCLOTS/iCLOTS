"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Help window display shows help documents for microchannel accumulation/adhesion application help

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
        namelabel = tk.Label(self, text="Velocity timecourse and profile application")
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
        iCLOTS is a free software created for the analysis of common hematology workflow image data

        Analyze that analyzes videomicroscopy of cell suspensions under flow
        A separate application (single cell tracking) analyzes individual cells under flow
        
        Script relies heavily on OpenCV optical flow methods, documentation available at:
        https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
        
        Input files:
        --Script is designed to work with a single videomicroscopy files (.avi)
        ----If your data is saved as a series of frames, please see the suite of video editing tools to convert to .avi
        
        Input parameters, general:
        --\u03bcm to pixel ratio: The ratio of microns (1e-6 m) to pixels for the video
        ----Use \u03bcm to pixel ratio = 1 for no conversion
        --fps: Frames per second, the rate of imaging
        ----Note that FPS values pulled directly from videos can be inaccurate, especially if the video
        -----has been resized or edited in any way
        --Number of bins: Number of bins to divide channel into for profile
        ----Typically aiming for roughly the size of a cell is best - e.g. enough bins so that each is 5 um
        --Maximum number of features: The maximum number of corners (features, typically a pattern of cells) to track
        
        Input parameters, Shi-Tomasi corner finding:
        --Number of points: choose highest n possible without adding unnecessary computational expense - I like ~500
        ----Keep in mind, this total number of features may not be tracked - there's a minimum distance between points
        -----and a minimum quality parameter also imposed (set as 1/2 block size and 0.1, respectively, after testing on multiple datasets)
        --Block size: Block size to compute eigenvalues over, I find roughly the dimensions of a cell is useful
        
        Input parameters, Kanade-Lucas-Tomasi feature tracking:
        --Window size: The most important parameter! Area (in pixels) to search for a feature in the subsequent frame (displacement)
        ----Err on the high side, as values to small can miss fastest moving features
        ----Can reduce y to reduce computational expense if flow is uni-directional in x direction
        ----Keep in mind, even if flow is uni-directional, the algorithm will search in all directions
        
        Output files
        --Users can indicate if they'd like labeled image data: first 100 frames
        --Users can indicate if they'd like labeled image data: every 100th frame
        ----Specified original frames of the provided video with each detected event (cell cluster pattern)
        -----labeled with an arrow indicating displacement
        
        --A corresponding .csv sheet for each video containing location and velocity of all features tracked
        ----Typically a very large file
        
        --A corresponding .xlsx sheet containing:
        ----Minimum, mean, and maximum velocity per frame - one sheet/video
        ----Descriptive statistics (min, mean, max, standard deviation for velocity) per video
        ----Profile information: mean velocity and standard deviation of velocity (separate sheets)
        ------Calculated based on number of bins
        ------If profile seems erroneously blunted, increase window size - fastest values are being missed
        ----Parameters used and time/date analysis was performed, for reference
        
        --Graphical data for each video
        ----Timecourse data, including minimum, maximum, and mean values per frame
        ----Profile data overlaid on each displacement data point
        
        Some tips from the iCLOTS team:
        
        Computational and experimental methods:
        --Bins are calculated in the x-direction, so rely on perfectly horizontal channels
        ----The suite of video editing tools can rotate a video with no change to aspect ratio
        ----Displacement is calculated in every direction
        --All test data was taken at a frame rate of ~160 FPS, may need a fast camera to perform experiments
        --Channel size was set artificially shallow (~15 um) - deeper channels are hard to get distinct features from
        
        --Features are typically patterns of cells rather than a single individual cell
        ----As such, no label index is provided
        --To reduce computational expense:
        ----Use relatively short video clips - 10 seconds is oftentimes sufficient to establish a profile
        ----Carefully choose window size - too high increases expense (but, too low misses critical displacement measurements)
        
        Output files:
        --Analysis files are named after the folder containing all videos (.xlsx) or video names (.png)
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