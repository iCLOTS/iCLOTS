"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-01 for version 1.0b1

Main menu window display shows generalized help data for iCLOTS use

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
        namelabel = tk.Label(self, text="General information for use")
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
        iCLOTS software generates quantitative metrics from microscopy data obtained during use of a wide range 
        of microfluidic and static assays.
        
        --Computational methods adapt to microscopy images and videomicroscopy of cells and cell solutions 
        ---in a variety of common assay formats.
        --In the iCLOTS manuscript, we demonstrate the use of these algorithms as applied to blood cells. 
        ----Experimental assays performed with blood cells are subject to unique requirements and constraints, 
        -----including samples comprised of heterogenous cell types as well as frequent integration of fluid flow
        -----to better recapitulate physiologic conditions, and as such provide ideal test cases to demonstrate the
        -----adaptability of iCLOTS.
        --iCLOTS has been extensively tested on all blood cell types (including red blood cells, white blood cells, 
        ---platelets, and cell lines) and on various blood cell suspensions. 
        --The presented tools can be applied to other fields who share the same objective of tracking single cell 
        ---or body features or conditions as a function of time.
        
        --iCLOTS can accommodate data obtained using:
        ----Standard microscopy slide or dish assays
        ----Flow-based systems including:
        ------Custom-made microfluidics
        ------Commercially available microfluidics (the Lam lab likes ibidi)
        ------Traditional flow chamber devices
        
        --iCLOTS has been designed with versatility and adaptability in mind: it has been lightly tested with 
        ---animal cells and/or other, non-hematological types of cells as well.
        
        --iCLOTS is a post-processing image analysis software
        ----Users can continue to acquire imaging data using the methods they are accustomed to.
        --iCLOTS can be used with both previously collected data or new assays planned with the software's 
        ---capabilities in mind.
        
        --Image processing capabilities are separated into four main categories:
        ----Adhesion applications, useful for single-cell resolution measures of biological functionality.
        ----Single cell tracking applications, useful for single-cell velocity measurements, 
        -----typically as they flow through a microfluidic device. 
        ------Video frames may contain multiple cells at once. 
        ------We share the necessary methods and tools for a specialized biophysical flow cytometer assay 
        -------capable of quantifying cellular mechanical properties via relative deformability measurements.
        ----Velocity profile applications, useful for investigating rheological properties of suspensions under flow. 
        -----Minimum, mean, and maximum velocity values for each video frame are also provided, 
        -----suitable for monitoring changes in cell suspension speed.
        --Multiscale microfluidic accumulation applications
        ----Useful for insight into pathologic processes such as occlusion and obstruction in thrombosis.
        --A suite of file pre-processing applications assists users with preparing their data for analysis. 
        ----Type of file required is specific to each application and is provided in the documentation below.
        
        Each application produces detailed output files.
        --iCLOTS detects "events" in the imaging data provided by the user.
        ----Events typically represent individual cells or patterns of cells. Each event is labeled with a number/index 
        -----on the original imaging files and the imaging files as processed by the image processing algorithms applied.
        --Numerical output metrics are calculated for each event and are returned within an Excel sheet.
        ----For example, each cell "event" may be described by metrics like cell area and/or total fluoresence 
        -----intensity of the cell.
        --Metrics are given for every cell (single-cell resolution) and can be traced back to the original image 
        ---using the labeled index.
        
        --iCLOTS may produce a large amount of data. In an effort to help researchers quickly make sense 
        ---of their imaging dataset, iCLOTS automatically graphs results from the image processing analysis 
        ---in common formats such as histograms or scatter plots.
        --A specialized set of graphs called a "pairplot" is included in the file outputs. 
        ----A pairplot plots the pairwise relationships in a dataset by creating a grid of graphs 
        -----such that each metric output by iCLOTS will be shared in the y-axis across a single row and in 
        -----the x-axis across a single column. Graphs on the leading diagonal are histograms describing a single metric.
        --The developers would like users to keep in mind that computational analysis is never perfect.
        ----Some spurious features are to be expected. 
        ----Users might find these data points don't significantly affect their conclusions.
        ----Users may find that manually removing obvious outliers is less time consuming than performing the analysis by hand.
        
        --Should the user need further interpretation of their results, the produced Excel files can be used in the 
        ---machine learning-based clustering application.
        --Machine learning is a subset of artificial intelligence.
        ----Machine learning clustering algorithms are an unsupervised approach designed to 
        -----detect and mathematically characterize natural groupings and patterns within complex datasets, 
        -----e.g. healthy/clinical sample dichotomies or subpopulations from a single sample.
        --iCLOTS implements k-means clustering algorithms, understood to be a strong general-purpose approach to clustering.
        ----Each data point is returned with an assigned cluster label.
        
        All iCLOTS applications follow a common, easy-to-use interactive format.
        --Users follow a series of software menus to open a specific analysis window.
        --All analysis windows are designed with the inputs on the left, the image processing steps as applied in the center, 
        ---and the outputs on the right.
        --The user uploads one or several microscopy images, time course microscopy series, or videomicroscopy files as inputs. 
        ----These files automatically display on the screen and can be scrolled through using the scale beneath the files.
        --Users are guided through a series of steps to describe their data.
        ----This could including choosing a region of interest (ROI) or indicating immunofluorescence staining present.
        --Users must then adjust parameters to fit the iCLOTS image processing algorithms to their specific set of data.
        ----Parameters are numerical factors that define how image processing algorithms should be applied.
        ------This could be a number such as minimum or maximum cell area.
        --Note that in iCLOTS, “a.u.” represents arbitrary units, typically used to describe pixel intensity values.
        --Effects of changing parameters are shown in real time.
        --iCLOTS currently does not have a zoom function, but this is planned for a later release. 
        ----In the meantime, if your data is relatively low-magnification, we suggest cropping a small region of interest
        -----using the video processing tools and testing parameters on that image, then applying the same parameters 
        -----to the larger image.
        --The "Run analysis" button on the top right of the analysis screen initiates the finalized analysis 
        ---using the parameters provided.
        --Typically an analysis takes seconds-to-minutes - this depends heavily on file size and number.
        --Graphical results are automatically displayed when the analysis is complete.
        
        --Output files include:
        ---Tabular data as an Excel file
        ---Graphical results as .png images
        ---The initial imaging dataset as transformed by the image processing algorithms and/or labeled with indices.
        ---Videos are optionally returned as individual, sequentially numbered frames.
        
        Users may always access the application-specific documentation available here using the "Help" 
        button in the bottom left of the analysis window.
    
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
        for common cell microscopy-based assays, particularly microfluidic assays.

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')