"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Help window display shows help documents for fluorescence microscopy adhesion application help

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
        namelabel = tk.Label(self, text="Fluorescence microscopy adhesion application help")
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

        Fluorescent adhesion analysis GUI analyzes static, fluorescence microscopy images of cells 
        (e.g. platelets, RBCs, or WBCs) adhered to some surface. This application does not separate cells by type, 
        but you could use the post-processing machine learning clustering algorithm to group cells.

        Application relies heavily on skimage library region property analysis, tutorial available at:
        https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html
        
        Input files:
        --Application is designed to work with a single image or a folder of image files (.jpg, .png, and/or .tif)
        ----The same input parameters are applied to each image
        
        Users are lead to select colors for analysis:
        --Membrane stain (red, green, blue, or grayscale/white)
        ----Typically represents the area of a cell
        --Functional stain (red, green, blue, or N/A)
        ----Optional additional color channel that typically represents some activity or characteristic
        
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
        --Functional stain threshold: like the membrane stain threshold, but for the function/characteristic stain

        --Later functionality will require a parameter to describe the minimum distance between functional stain features
        ----To be used in quantifying intracellular structures        
        
        Output files
        --Single-cell resolution
        --Each original image with each detected cell labeled with an index
        --Each original image with threshold applied, each detected cell is labeled with the same index
        
        --A corresponding .xlsx sheet containing:
        ----Area, circularity, texture
        ----Presence of secondary functional stain, total fluorescence intensity
        ------For each cell - one sheet/image
        ------For all cells - one sheet (this combined sheet is best for analyzing replicates)
        ----Descriptive statistics (min, mean, max, standard deviation for all metrics)
        ------For each image and for all images combined
        ------Cell density (n/mm\u00b2) also provided
        ----Parameters used and time/date analysis was performed, for reference
        
        --Pairplot graph including area, circularity, and functional stain metrics
        ----Three types:
        ------For each image
        ------For all images, combined, one color represents all
        ------For all images, combined, each color represents a different image
        ----Each type exported with and without functional stain metrics
        
        Some tips from the iCLOTS team:
        
        Computational and experimental methods:
        --For all fluorescent applications, each stain to quantify must be solely in one RGB channel, no other colors
        ----See export options on your microscopy acquisition software
        --After application of the thresholds, the algorithm analyzes each interconnected region of 1/signal as a cell
        --Analysis methods cannot distinguish between overlapping cells
        ----If cells are significantly overlapping, repeat experiment with a lower cell concentration
        --Red blood cells can be difficult to stain
        ----Antibody staining signal is weak and we've found membrane stains can affect mechanical properties
        ----Consider using our brightfield adhesion application if this does not conflict with your experimental goals
        
        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not pixel-to-\u03bcm ratio
        --Sometimes cells (especially platelets) have a high-intensity "body" and low-intensity spreading or protrusions
        ----Choose a high threshold if you're primarily quantifying the number of cells
        ----Choose a low threshold if you're primarily quantifying the morphology of cells
        --Err on the high side of maximum and low side of minimum area parameters
        ---unless data is particularly noisy or there's a large amount of debris
        ----By sorting in excel, you can verify that small/large objects are/are not cells
        
        Output files:
        --Analysis files are named after the folder containing all images (.xlsx) or image names (.png)
        ----Avoid spaces, punctuation, etc. within file names
        --.xlsx and pairplot data includes a sheet/graph with all images combined
        ----Only use this when analyzing replicates of the same sample
        --Secondary stain metrics are reported in two ways:
        ----Signal (binary): 0 = no, 1 = yes binary value for presence of secondary stain
        ------Useful for calculating a percent expression
        ----Fn. stain intensity (a.u.): summed value of all functional stain pixels within the membrane stain shape
        ------Take care interpreting, as range of intensity can vary image-to-image due to changes in laser power, etc.
        ----No intensity metrics are reported from the main color, as this color should indicate morphology only
                
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
