"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Portion of machine learning application, window to finalize clustering analysis

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.mosaicplot import mosaic
from sklearn.cluster import KMeans
from sklearn import metrics
import itertools
from PIL import Image, ImageTk, ImageDraw
from help import mlhelp as hp
from accessoryfn import complete
import os


class ApplyClustering(tk.Toplevel):
    def __init__(self, df, dirname, final_features, n_clusters):
        super().__init__()

        self.df = df
        self.dirname = dirname
        self.final_features = final_features
        self.n_clusters = n_clusters

        name = "iCLOTS"
        # Fonts
        boldfont = font.Font(weight='bold')

        # Variables
        self.clusters = tk.IntVar(value=2)

        # Widgets
        self.title(name + " machine learning")

        # Application title
        menutitle = tk.Label(self, text="Clustering analysis results")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Guidance label
        info_label = tk.Label(self, text="Analysis complete! Numerical and graphical data\n"
                                         "has been saved in a dated results folder\n\n"
                                         "Please repeat entire workflow for new results")
        info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Help and quit button

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.help)
        help_button.grid(row=2, column=0, padx=5, pady=5)

        # Quit
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=2, column=1, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Run analysis, display mosaic plot
        self.ml_analysis()

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def ml_analysis(self):
        """Display scree plot based on categories from previous window"""

        # Machine learning analysis
        df_X = self.df[self.final_features]  # Numerical data

        # Drop any rows with any NaN values
        df_X = df_X.dropna()

        # Partition clusters
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=100)
        kmeans_labels = kmeans.fit_predict(df_X)  # Note each label will be an integer, starting at 0 (0, 1, 2.. etc.)

        df_final = df_X.copy()
        df_final.insert(0, 'Sample', self.df['Sample'])
        df_final['Label'] = kmeans_labels

        # Write all data to excel
        writer = pd.ExcelWriter(self.dirname + '_clustering.xlsx', engine='openpyxl')

        # Labeled data
        df_final.to_excel(writer, sheet_name='Labeled data')

        # Descriptive statistics - min, mean, max, stdev for all clusters (4 sheets)
        # Min
        df_min = df_final.groupby(['Label']).min()
        df_min.to_excel(writer, sheet_name='Min. by cluster')

        # Mean
        df_mean = df_final.groupby(['Label']).mean()
        df_mean.to_excel(writer, sheet_name='Mean by cluster')

        # Max
        df_max = df_final.groupby(['Label']).max()
        df_max.to_excel(writer, sheet_name='Max by cluster')

        # Stdev
        df_std = df_final.groupby(['Label']).std()
        df_std.to_excel(writer, sheet_name='Stdev. by cluster')

        # Cluster counts
        df_size = df_final.groupby(['Sample', 'Label']).size()
        count_series_df = df_size.to_frame(name='size').reset_index()
        count_series_df.to_excel(writer, sheet_name='Counts')

        # Silhouette score
        silhouette_coefficient = metrics.silhouette_score(df_X, kmeans_labels)
        dict_sc = {'Silhouette coefficient': silhouette_coefficient}  # Dict
        dict_df = pd.DataFrame(dict_sc, index=[0])  # Dataframe
        dict_df.to_excel(writer, sheet_name='Sil. coeff.', index=False)

        writer.save()
        writer.close()

        # Display and save a pairplot showing relationships between features
        sns.color_palette(palette='bright')
        sns.pairplot(df_final, hue="Label")
        plt.savefig(self.dirname + '_pairplot.png', dpi=300)  # Save in results folder

        plt.close()

        # Also create individual pairwise graphs
        # Create a 2D scatter plot of labels from all combinations of two features
        graph_count = 1  # For saving figures

        for pair in itertools.combinations(self.final_features, 2):
            plt.figure(figsize=(6,4))
            sns.scatterplot(data=df_final, x=pair[0], y=pair[1], hue='Label',
                            style='Sample')  # Color: sample, shape: label
            plt.xlabel(pair[0])
            plt.ylabel(pair[1])
            plt.tight_layout()
            plt.savefig(self.dirname + '_scatterplot-' + str(graph_count) + '.png', dpi=300)
            plt.close()
            graph_count += 1  # Some feature column names may contain unicode characters unsuitable for file names

        plt.figure()

        mosaic(df_final, ['Sample', 'Label'])

        plt.tight_layout()
        plt.savefig(self.dirname + '_mosaic-plot.png', dpi=300)  # Save in results folder

        plt.close()

    # Open help window
    def help(self):
        """All applications have a button to reference help documentation"""

        # Display specified help file
        hp.HelpDisplay()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            plt.close()