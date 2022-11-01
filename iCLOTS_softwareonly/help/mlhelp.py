"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-27 for version 1.0b1

Help window display shows help documents for machine learning application

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
        namelabel = tk.Label(self, text="Machine learning application help")

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

        This machine learning application applies clustering algorithms to any properly-formatted data,
        including iCLOTS data. Typically, a series of data points (e.g., cells) are represented by multiple metrics
        (e.g. velocity, size, or fluorescence intensity).
        
        Clustering is an unsupervised machine learning technique designed to mathematically characterize natural
        groupings within datasets (e.g., cell subpopulations from a single dataset or healthy-clinical dichotomies).
        
        The iCLOTS development team suggests the review paper "A guide to machine learning for biologists" 
        (Greener, Nature Reviews Molecular Cell Biology, 2021) for a better understanding of machine learning. 
        You may also see our documentation at iclots.org for tips on reporting computational results.

        Application relies heavily on scikit-learn python library, documentation available at:
        https://scikit-learn.org/stable/
        
        Machine learning workflow (steps), briefly:
        
        Step 1: load data
        --User provides one or more excel files, each representing a single sample. Excel files must have only
        ---one sheet, which should contain only individual data points (e.g. cells) described using the same features
        ---(numerical metrics, e.g. velocity, size, or fluorescence intensity). A minimum of two features are required.
        ---File loading is set up such that user selects a folder that contains all relevant excel sheets.
        
        Step 2: select features
        --After data is loaded, all datasets are combined into one "pool." Clustering is an unsupervised algorithm:
        ---no "labels" such as sample names are considered during clustering. Later outputs do provide the number
        ---of sample data points found in each cluster.
        --iCLOTS all numerical columns shared between files. Because iCLOTS does not produce any text metrics
        ---that could be considered a feature, opportunity to use text-based metrics are not included in v1.0b1.
        ---This will be included in later versions. In the meantime, you could change text-based categories to
        ---numerical categories on your own in Excel.
        --A correlation matrix is automatically displayed. A correlation matrix is a visualization of how much each
        ---pairwise combination of variables is correlated, or related. Highly related variables (value
        ---approaching -1 or 1) may bias results, e.g. considering both area (pix) and area (\u03bcm\u00b2)
        ---gives area undue influence on clustering.
        --In this step, users have the option to select what metrics they would like to retain for final analysis.
        
        Step 3: select number of clusters to retain
        --After features are selected and submitted, a scree plot is generated. 
        ----A scree plot indicates a suggested optimal number of mathematically significant clusters to retain.
        ----It is presented as a line plot of the sum of squared errors (SSE) of the distance to the closest centroid
        -----for all data points for each number of potential clusters (iCLOTS allows up to 12 clusters).
        ----Typically, as the number of clusters increases, the variance, or sum of squares, for each cluster
        -----group decreases.
        ----The "elbow" point of the graph represents the best balance between minimizing the number of clusters
        -----and minimizing the variance in each cluster. 
        ----The user can choose any number of clusters to group data into using the clustering algorithm.
        
        Step 4: k-means clustering algorithms are applied
        --After the number of clusters are selected and submitted, k-means clustering algorithms are applied
        ---to the pooled datasets. 
        ----Several types of clustering algorithms exist, but a k-means algorithm was selected for iCLOTS
        -----v1.0b1 as it is understood to be a robust general-purpose approach to discovering natural
        -----groupings within high-dimensional data. 
        --The pooled data points are automatically partitioned into clusters that minimize differences between
        ---shared metrics. 
        
        Step 5: review outputs
        --iCLOTS creates a series graphs:
        ----A mosaic plot (automatically displayed), a specialized stacked bar chart, displays the number of
        -----stacked data points from each dataset in each of the clusters. This is designed to assist the user
        -----in visualizing the contribution of each dataset to each cluster.
        ----A pair plot, a pairwise series of scatterplots and histograms, shows each dataset (marker type)
        -----and cluster (color). 
        --An excel file with all data points is also created.
        ----This sheet has the original sample name, all numerical metrics used, and a cluster label for each data point.
        ----Descriptive statistics for clusters, cluster label count per dataset, cluster number, and silhouette score 
        -----are also included.
        ------Silhouette score is a metric with a value from -1 (inappropriate clusters) to 1 (best clustering)

        Some tips from the iCLOTS team:
        --Clustering techniques are well-suited to exploring distinguishing features between known populations 
        ---and to finding new, previously imperceptible groupings within a single population. 
        --However, metrics describing populations of cells typically follow Gaussian distributions 
        ---which may have significant overlap. 
        ----Cluster label count by group may 
        --In an effort to guide users through the analysis and interpretation process, the authors have prepared 
        ---the application-specific help documentation located here and at https://www.iCLOTS.org/.

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
        ---for common cell microscopy-based assays, particularly microfluidic assays

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')