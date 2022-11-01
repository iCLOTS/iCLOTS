"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Portion of machine learning application, window to assist user in selecting features for analysis

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageDraw
from help import mlhelp as hp
from accessoryfn import error
from gui import ml_selectclusters as snc

class SelectFeatures(tk.Toplevel):
    def __init__(self, df, dirname):
        super().__init__()

        self.df = df
        self.dirname = dirname

        name = "iCLOTS"
        # Fonts
        boldfont = font.Font(weight='bold')

        # Widgets
        self.title(name + " machine learning")

        # Application title
        menutitle = tk.Label(self, text="Select features for machine learning")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Canvas for correlation matrix
        self.img_canvas = tk.Canvas(self, width=480, height=320)
        self.img_canvas.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Find common numerical columns with no NaN values
        numeric_df = self.df[self.df._get_numeric_data().columns]
        categories = numeric_df.columns[~numeric_df.isnull().any()]

        # Set of check boxes
        self.var_categories = {}
        self.chckbx_categories = {}

        for i in range(len(categories)):
            item = categories[i]
            self.var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(self, text=item, variable=self.var, onvalue=True, offvalue=False, anchor="w")
            cb.grid(row=i+2, column=0, columnspan=3)

            self.var_categories[item] = self.var
            self.chckbx_categories[item] = cb

        # Help, submit, and quit button

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.help)
        help_button.grid(row=3+len(categories), column=0, padx=5, pady=5)

        # Submit button
        submit_button = tk.Button(self, text="Submit features", command=self.select_features)
        submit_button.grid(row=3+len(categories), column=1, padx=5, pady=5)

        # Quit
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=3+len(categories), column=2, padx=5, pady=5)

        # Row and column configures
        for r in range(len(categories) + 3):
            self.rowconfigure(r, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

       # Display correlation matrix
        self.displaygraph(categories)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def displaygraph(self, categories):
        """Displays correlation matrix based on selected datasheets"""

        graphs = plt.figure(figsize=(6, 4), dpi=80)

        # Add image name to image name label
        df_X = self.df[categories]  # Numerical data only, will also be used for clustering
        corrMatrix = df_X.corr()
        sns.heatmap(corrMatrix, annot=True)
        plt.tight_layout()
        plt.savefig(self.dirname + '_correlation-matrix.png', dpi=300)  # Save in results folder

        graphs.canvas.draw()
        graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
        graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimg))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(0, 0, anchor='nw', image=graphimgr_tk)

        plt.close()

    def select_features(self):
        self.final_features = []  # Init.
        for var in self.var_categories:  # Save features where value is true
            if self.var_categories[var].get() is True:
                self.final_features.append(var)

        # Include error minimum of two must be selected
        if len(self.final_features) < 2:
            error.ErrorWindow(message='Please choose 2 or more features')
        else:
            # Call next window: correlation matrix/variable selection
            snc.SelectNClusters(self.df, self.dirname, self.final_features)  # Raise graph window



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
            # Clear variables
            graphs = None