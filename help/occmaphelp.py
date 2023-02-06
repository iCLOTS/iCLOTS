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
        namelabel = tk.Label(self, text="Multi-scale microfluidic accumulation/occlusion application help\n"
                                        "sub-application specialized for use with full microfluidic device")
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

        Microfluidic accumulation/occlusion analysis GUI analyzes single or timeseries images
        of cells adhered to an any-dimension microfluidic device
        Accomodates red, blue, and/or green channels
        
        Application relies heavily on skimage library region property analysis, tutorial available at:
        https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html
        
        Input files:
        --Application is designed to work with a folder of images (.jpg, .png, and/or .tif)
        ----The same input parameters are applied to each image
        ----This code will work on a single image
        ----It's important that frames are labeled sequentially in timeseries order (i.e. 01, 02.. 10 vs. 1, 2... 10)
        ----After uploading one or several images, the user is prompted to choose an ROI from the first image
        ------The same ROI is applied to all images, take care that all images represent the same field of view
        
        Input parameters:
        --\u03bcm to pixel ratio: The ratio of microns (1e-6 m) to pixels for the image
        ----Use value = 1 for no conversion
        --Red, green, and/or blue threshold(s)
        ----Users may select which color channel(s) they would like to analyze
        ----After selection, a spinbox to choose a threshold for each channel appears
        
        Output files
        --ROI from each image
        --The "map" used - the channel region(s) as detected
        --Images with image processing (threshold) steps applied
        ----For each frame, each selected color as detected by the set threshold overlaid on the channel map
        
        --A corresponding .xlsx sheet containing:
        ----For each selected channel:
        ------Frame data: mean signal area, signal accumulation (all channels)
        ------Conversion notes:
        --------To convert accumulation per frame into per timepoint, divide frame # by FPS imaging rate
        
        --Future versions of iCLOTS will include obstruction, the percent of the y-direction for each channel
        ---containing some signal
        
        --Occlusion/accumulation graph:
        ----For the time series, a line graph showing:
        ------Occlusion (titled, left) for each color
        ------Accumulation (titled, right) - " "
        
        Some tips from the iCLOTS team:
        
        Computational and experimental methods:
        --See input requirements: a time series, in the same field of view, with "complete" signal
        ----Creating the map requires some signal at every point in that channel
        ------Consider staining the microfluidic channels - if this isn't possible, you may benefit from the ROI app
        ------We are planning a brightfield/fluoresence microscopy combo. app for future iCLOTS releases
        --Time series images must be in the proper alphabetical/numerical order
        ----If image names contain numbers, use preceding zeros to order properly
        ------i.e. 01, 02... 10 instead of 1, 2... 10
        --The Lam lab has developed these methods on an "endothelialized" branching microfluidic device
        ----See "Endothelialized Microfluidics for Studying Microvascular Interactions in Hematologic Diseases"
        -----manuscript by Myers and Sakurai et al., 2012, JOVE
        ----We are happy to share a detailed endothelialization protocol upon request
        ----We are happy to share the mask design files and instructions for fabrication upon request
        
        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not \u03bcm-to-micron ratio
        --If you indicate more than one color channel, you might find that colors overlap, and you can't accurately
        ---see parameters as described
        ----Individually choose each color, select a good threshold, and then combine with the thresholds you chose.
        --Depending on the threshold you set, while the "trend" of accumulation/occlusion will stay constant,
        ---the degree of accumulation/occlusion will decrease as threshold increases
        ----If you are comparing conditions, make sure they were taken with the same imaging settings
        -----and use the same threshold values
        ------Ideally these experiments are direct control-to-experimental comparisons taken on the same day
        
        Output files:
        --Analysis files are named after the folder containing all images (.xlsx) or image names (.png)
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