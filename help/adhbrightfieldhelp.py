"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-04 for version 1.0b1

Help window display shows help documents for brightfield adhesion application

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
        namelabel = tk.Label(self, text="Brightfield microscopy adhesion application help")
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

        Brightifled adhesion analysis GUI analyzes static, brightfield microscopy images of cells 
        (e.g. platelets, RBCs, or WBCs) adhered to some surface
        May also be suitable for use with preliminary digital pathology approaches with blood smears 
        This application does not separate cells by type, but you could use the post-processing 
        machine learning clustering algorithm to group cells

        Application relies heavily on Trackpy python library, documentation available at:
        http://soft-matter.github.io/trackpy/v0.5.0/

        Input files:
        --Application is designed to work with a single image or a folder of image files (.jpg, .png, and/or .tif)
        ----The same input parameters are applied to each image

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
        ----Minimum summed intensity of the cell, helps filter out obvious noise or debris

        Output files
        --Single cell resolution
        --Each original image with each detected cell labeled with an index
        --Each original image with threshold applied, each detected cell is labeled with the same index

        --A corresponding .xlsx sheet containing:
        ----Intensity, area, and circularity for each cell - one sheet/image
        ----Intensity, area, and circularity for all cells - one sheet (this combined sheet is best for analyzing replicates)
        ----Descriptive statistics (min, mean, max, standard deviation for area and circularity)
        ------For each image and for all images combined
        ------Cell density (n/mm\u00b2) also provided
        ----Parameters used and time/date analysis was performed, for reference

        --Pairplot graph including area and circularity metrics
        ----Three types:
        ------For each image
        ------For all images, combined, one color represents all
        ------For all images, combined, each color represents a different image

        Some tips from the iCLOTS team:

        Computational and experimental methods:
        --The algorithm searches for particles represented by image regions with Gaussian-like distributions
        ---of pixel brightness
        ----Cells with an especially heterogenous appearance, such as bi-concave RBCs or actived WBCs, may
        -----be hard to detect. While count will be accurate, take care in interpreting area or circularity
        --Analysis methods cannot distinguish between overlapping cells
        ----If cells are significantly overlapping, repeat experiment with a lower cell concentration
        --Owing to the heterogenous appearance of blood cell types, brightfield analysis is always challenging
        ----Consider using a fluorescent membrane stain coupled with our fluorescent adhesion applications
        -----if this does not conflict with your experimental goals, especially for WBCs/neutrophils
        
        Choosing parameters:
        --Be sure to use \u03bcm-to-pixel ratio, not pixel-to-\u03bcm ratio
        --Err on the high side of maximum diameter and low side of minimum intensity parameters
        ---unless data is particularly noisy or there's a large amount of debris
        ----By sorting in excel, you can verify that small/large objects are/are not cells

        Output files:
        --Analysis files are named after the folder containing all images (.xlsx) or image names (.png)
        ----Avoid spaces, punctuation, etc. within file names
        --.xlsx and pairplot data includes a sheet/graph with all images combined
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
        --Issues with software, requests for help troubleshooting, new application ideas, and general comments, suggestions, 
        ---and concerns are all welcome
        --The authors hope this will become a field-wide effort to improve quantitative data analysis precision 
        for common cell microscopy-based assays, particularly microfluidic assays

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')