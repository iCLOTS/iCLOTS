"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Help window display shows help documents for fluorescence microscopy adhesion application help
This adhesion application specifically for filopodia counting

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
        namelabel = tk.Label(self, text="Filopodia counting in fluorescence microscopy\nadhesion assay application help")
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
        micron = u"""micron"""
        self.helptext.insert(tk.INSERT, u"""\
        iCLOTS is a free software created for the analysis of common hematology workflow image data

        Script that analyzes static, fluorescence microscopy images of cells (e.g. platelets or WBCs)
        adhered to some surface specifically for a single-cell resolution filopodia count and characterization

        Application relies heavily on:
        --skimage library region property analysis, tutorial available at:
        https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html
        --skimage library Harris corner detection, tutorial available at:
        https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_corner.html

        Input files:
        --Script is designed to work with a single image or a folder of image files (.jpg, .png, and/or .tif)
        ----The same input parameters are applied to each image

        Users are lead to select colors for analysis:
        --Membrane stain (red, green, blue, or grayscale/white)
        ----Typically represents the area of a cell
        --Future versions of iCLOTS will also incorporate methods for quantifying a secondary stain indicating
        ---some biological characteristic or process as well

        Input parameters:
        --\u03bcm to pixel ratio: The ratio of microns (1e-6 m) to pixels for the image
        ----Use value = 1 for no conversion
        --Minimum area: Minimum area (pixels) of a region (ideally, cell) to be quantified
        ----Can be used to filter out obvious noise
        --Maximum area: Maximum area (pixels) of a region to be quantified
        ----Can be used to filter out debris or cell clusters
        --Membrane stain threshold: integer between 0 (black), 255 (white) to be used for main channel threshold
        ----Any value below this threshold becomes 0, or background
        ----Any value greater than or equal to this threshold becomes 1, or signal to further quantify
        
        Harris corner detection parameters
        --Corner sharpness (a.u.)
        ----k (a.u.): Harris detector free parameter
        ----Sharpness parameter ranging from 0 to 2, with 0 indicating you'd like the most defined filopodia only
        --Relative intensity (a.u.): Corner peak finding relative threshold
        ----Used with a "peak finding" algorithm
        ----Minimum intensity of peaks, calculated as max(image) * thresh_relative
        --Minimum distance (pix): Minimum distance between detected filopodia
        ----Also used with a "peak finding" algorithm
        

        Output files
        --Single-cell resolution
        --Each original image with each detected cell labeled with an index
        --Each original image with threshold applied, each detected cell is labeled with the same index
        --In each image type each filopdia counted is indicated with a small circle

        --A corresponding .xlsx sheet containing:
        ----Area, circularity, texture, filopdia count, min/mean/max/stdev length of individual filopodia (if any)
        ------Length of filopodia is calculated as distance of detected end point to center point of cell
        --------Future versions of this code will give length of each as a vector
        ------For each cell - one sheet/image
        ------For all cells - one sheet (this combined sheet is best for analyzing replicates)
        ----Descriptive statistics (min, mean, max, standard deviation for all metrics)
        ------For each image and for all images combined
        ------Descriptive statistics sheet also includes a density measurement (n cells/mm\u00b2)
        ----Parameters used and time/date analysis was performed, for reference

        --Pairplot graph including area, circularity, texture, and filopodia count metrics
        ----Three types:
        ------For each image
        ------For all images, combined, one color represents all
        ------For all images, combined, each color represents a different image

        Some tips from the iCLOTS team:

        Computational and experimental methods:
        --We suggest high microscope magnification for this application, iCLOTS was tested on 100x magnification images
        --For all fluorescent applications, each stain to quantify must be solely in one RGB channel, no other colors
        ----See export options on your microscopy acquisition software
        --After application of the thresholds, the algorithm analyzes each interconnected region of 1/signal as a cell
        --Analysis methods cannot distinguish between overlapping cells
        ----If cells are significantly overlapping, repeat experiment with a lower cell concentration
        --Keep in mind that searching for the number of filopodia cell can be computationally expensive
        ----Analysis for filopodia may take longer than other iCLOTS adhesion applications

        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not pixel-to-\u03bcm ratio
        --Sometimes cells (especially platelets) have a high-intensity "body" and low-intensity spreading or protrusions
        ----Choose a low threshold since by counting filopodia you're primarily quantifying the morphology of the cells
        --Err on the high side of maximum and low side of minimum area parameters
        ---unless data is particularly noisy or there's a large amount of debris
        ----By sorting in excel, you can verify that small/large objects are/are not cells
        --It can be tricky to adjust all 3 parameters to get a roughly accurate filopodia count
        ----We suggest doing robust sensitivity analysis (trying a wide range of parameters and comparing results)
        ------Ideally, conclusions are not significantly affected by small changes in parameters
        ------See iCLOTS manuscript, iCLOTS.org/documentation, or reach out to the iCLOTS development team for more information

        Output files:
        --Analysis files are named after the folder containing all images (.xlsx) or image names (.png)
        ----Avoid spaces, punctuation, etc. within file names
        --.xlsx and pairplot data includes a sheet/graph with all images combined
        ----Only use this when analyzing replicates of the same sample
        ----No intensity metrics are reported from the membrane color, as this color should indicate morphology only

        iCLOTS is under continuous development:
        --Feel free to contact the authors:
        ----Using the form at iCLOTS.org/contact
        ----By emailing lamlabcomputational@gmail.com
        ------If your question is about use with a particular set of data, please attach a sample file
        ------Data will not be shared outside of the iCLOTS development team
        --For those users who also code, please feel free to submit a pull request:
        ----github.com/iCLOTS
        ----You can also find analysis methods-only and test data at github.com/LamLabEmory
        --Issues with software, requests for help troubleshooting, new application ideas, and general comments, suggestions, 
        ---and concerns are all welcome
        --The authors hope this will become a field-wide effort to improve quantitative data analysis precision 
        for common cell microscopy-based assays, particularly microfluidic assay

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')