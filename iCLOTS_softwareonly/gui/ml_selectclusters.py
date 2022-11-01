"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Portion of machine learning application, window to assist user in selecting number of clusters for analysis

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image, ImageTk, ImageDraw
from help import mlhelp as hp
from accessoryfn import error
from gui import ml_clustering as cl


class SelectNClusters(tk.Toplevel):
    def __init__(self, df, dirname, final_features):
        super().__init__()

        self.df = df
        self.dirname = dirname
        self.final_features = final_features

        name = "iCLOTS"
        # Fonts
        boldfont = font.Font(weight='bold')

        # Variables
        self.clusters = tk.IntVar(value=2)

        # Widgets
        self.title(name + " machine learning")

        # Application title
        menutitle = tk.Label(self, text="Select number of clusters for machine learning")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Canvas for scree plot
        self.img_canvas = tk.Canvas(self, width=480, height=320)
        self.img_canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Guidance label
        info_label = tk.Label(self, text="Elbow point informs optimal number of\n"
                                         "mathematically significant clusters to retain")
        info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Rotation angle label
        angle_label = tk.Label(self, text="n clusters")
        angle_label.grid(row=3, column=0, padx=5, pady=5)
        # Number of clusters spinbox
        cluster_spin = tk.Spinbox(
            self,
            from_=2,
            to=12,
            increment=1,
            textvariable=self.clusters,
            width=10,
            wrap=True
        )
        cluster_spin.grid(row=3, column=1, padx=5, pady=5)

        # Help, submit, and quit button

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.help)
        help_button.grid(row=5, column=0, padx=5, pady=5)

        # Submit button
        submit_button = tk.Button(self, text="Submit features", command=self.select_clusters)
        submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Quit
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=5, column=1, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Display scree plot
        self.displaygraph()

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def displaygraph(self):
        """Display scree plot based on categories from previous window"""

        graphs = plt.figure(figsize=(6, 4), dpi=80)

        # Create scree plot
        sse = {}
        df_scree = self.df[self.final_features]  # Leave original X set unchanged
        for k in range(1, 12):  # Range of 1 to 12 clusters, could easily edit
            kmeans = KMeans(n_clusters=k, max_iter=1000).fit(df_scree)
            # print(data["clusters"])
            sse[k] = kmeans.inertia_  # Inertia: Sum of distances of samples to their closest cluster center

        plt.plot(list(sse.keys()), list(sse.values()))
        plt.xlabel("Number of clusters")
        plt.ylabel("SSE")

        plt.tight_layout()
        plt.savefig(self.dirname + '_scree-plot.png', dpi=300)  # Save in results folder

        graphs.canvas.draw()
        graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
        graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimg))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(0, 0, anchor='nw', image=graphimgr_tk)

        plt.close()

    def select_clusters(self):
        cl.ApplyClustering(self.df, self.dirname, self.final_features, self.clusters.get())  # Raise graph window

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