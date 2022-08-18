"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-01 for version 1.0b1

Series of functions that handles analysis for brightfield adhesion application

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from math import pi
import trackpy as tp
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import shutil

class RunAdhBrightfieldAnalysis():

    def __init__(self, filelist, umpix, maxdiameter, minintensity, invert):
        super().__init__(filelist, umpix, maxdiameter, minintensity, invert)

    def analysis(self, filelist, umpix, maxdiameter, minintensity, invert):
        """Function runs final analysis based on the parameters chosen in GUI"""

        # Global variables for use with additional export functions within class
        global df_img, df_summary, df_all, total_area

        cvfont = cv2.FONT_HERSHEY_SIMPLEX  # For labeling

        df_all = pd.DataFrame()  # For all events, good for plotting
        df_summary = pd.DataFrame()  # For descriptive statistics
        df_img = pd.DataFrame(columns=['name', 'img', 'graph'])  # For images, graphs

        # For each image
        total_area = 0  # For calculating final density measurement
        for imgname in filelist:

            # Read image
            img = cv2.imread(imgname)
            img_gray = cv2.imread(imgname, 0)
            imgbasename = os.path.basename(imgname.split(".")[0])

            # Convert area of image (one layer) to mm2
            img_size = img_gray.size * float(self.umpix.get()) * float(self.umpix.get()) / 1E6
            total_area += img_size  # Record total area of all images for final density calculation

            # Locate particles (ideally, cells) using Trackpy
            # See walkthrough: http://soft-matter.github.io/trackpy/dev/tutorial/walkthrough.html
            f = tp.locate(img_gray, self.maxdiameter.get(), minmass=self.minintensity.get(),
                          invert=self.invert.get())

            # Add index to resultant dataframe
            index = range(len(f))
            f.insert(0, 'Index', index)

            # Take most useful subset
            f = f[['Index', 'x', 'y', 'mass', 'size', 'ecc']]

            # Calculate additional metrics
            f['Area (pix)'] = f['size'] * f['size'] * pi  # pi*r^2
            f[u'Area (\u03bcm\u00b2)'] = f['Area (pix)'] * float(self.umpix.get()) * float(self.umpix.get())

            # Rename columns
            f = f.rename(columns={'size': 'Radius (pix)',
                                  'ecc': 'Circularity (a.u.)',
                                  'mass': 'Mass (a.u.)'
                                  })

            # Write ID text on saved image (red)
            for i in range(len(f)):
                # Original
                cv2.putText(
                    img,
                    str(f['Index'].iloc[i]),
                    (int(f['x'].iloc[i]), int(f['y'].iloc[i])),
                    cvfont,
                    fontScale=0.3,
                    color=(255, 0, 0),
                    thickness=1)

            # Graph for display
            graphs = plt.figure(figsize=(4, 4), dpi=80)
            graphs.suptitle(imgbasename, fontweight='bold')

            # If cells exist within the image
            if len(f) != 0:
                # Subplot 211 (area hist)
                plt.subplot(2, 1, 1)
                plt.hist(f[u'Area (\u03bcm\u00b2)'], rwidth=0.8, color='orangered')
                plt.xlabel(u'Area (\u03bcm\u00b2)')
                plt.ylabel('n')
                # Subplot 212 (circularity hist)
                plt.subplot(2, 1, 2)
                plt.hist(f['Circularity (a.u.)'], rwidth=0.8, color='orangered')
                plt.xlabel('Circularity (a.u.)')
                plt.ylabel('n')

                plt.tight_layout()

            # Prepare for saving to be later referenced in graph window and in exports
            graphs.canvas.draw()
            graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
            graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

            plt.close()

            # Save images to special dataframe
            df_img = df_img.append({'name': imgbasename, 'img orig': [img],
                                    'graph': [graphimg]}, ignore_index=True)

            # Append individual image dataframe to larger dataframe
            f.insert(0, 'Image', imgbasename)
            df_all = df_all.append(f, ignore_index=True)

            # Append summary data
            df_image = descriptive_statistics(f, img_size)
            df_image.insert(0, 'Image', imgbasename)
            df_summary = df_summary.append(df_image, ignore_index=True)

        GraphTopLevel(df_img)  # Raise graph window

    def expnum(self, filelist, umpix, maxdiameter, minintensity, invert):
        """Export numerical (excel) data, including descriptive statistics and parameters used"""

        # Create naming convention for excel sheet
        if len(filelist) == 1:  # Single file
            nameconvention = os.path.basename(filelist[0]).split(".")[0]
        elif len(filelist) > 1:  # Directory of files
            nameconvention = os.path.dirname(filelist[0]).split("/")[-1]

        # Create writer to save results to
        writer = pd.ExcelWriter(nameconvention + '_analysis.xlsx', engine='openpyxl')
        # Crop to avoid excel error
        # Calculate summary metrics, write individual sheets to excel file writer
        # Individual image names
        unique_names = df_all.Image.unique()

        # Write individual data sheets
        for un in unique_names:
            # Find all rows corresponding to unique name
            byname_df = df_all[df_all['Image'] == un]
            # Write individual frame data to specific sheet
            byname_df.to_excel(writer, sheet_name=un[0:30], index=False)  # Crop name to prevent errors

        # Write all data to special page
        df_all.to_excel(writer, sheet_name='All data', index=False)

        # Calculate values of all summary
        # Append summary data
        df_image = descriptive_statistics(df_all, total_area)
        df_image.insert(0, 'Image', 'All data')
        df_summary_hold = df_summary.copy()
        df_summary_hold = df_summary_hold.append(df_image, ignore_index=True)

        # Write summary data to special page
        df_summary_hold.to_excel(writer, sheet_name='Summary', index=False)

        now = datetime.datetime.now()
        # Print parameters to a sheet
        param_df = pd.DataFrame({'Ratio, \u03bcm-to-pixels': umpix,
                                 'Maximum cell diameter (px)': maxdiameter,
                                 'Minimum cell intensity': minintensity,
                                 'Invert': invert,
                                 'Analysis date': now.strftime("%D"),
                                 'Analysis time': now.strftime("%H:%M:%S")}, index=[1])
        param_df.to_excel(writer, sheet_name='Parameters used', index=False)

        writer.save()
        writer.close()

    def expgraph(self):
        """Export graphical (.png image) data, including pairplots"""

        # Create timestamped results directory
        current_dir = os.getcwd()  # Select filepath
        if current_dir.split('/')[-1] == 'Results, labeled image data':
            current_dir = os.path.dirname(current_dir)
        graph_folder = current_dir + '/Results, graphical data'

        if os.path.exists(graph_folder):
            shutil.rmtree(graph_folder)

        os.mkdir(graph_folder)
        os.chdir(graph_folder)

        for i in range(len(df_img)):
            # Convert image to BGR
            array = cv2.cvtColor(df_img['graph'].iloc[i][0], cv2.COLOR_RGB2BGR)
            cv2.imwrite(df_img['name'].iloc[i] + '_graph.png', array)

            unique_names = df_all.Image.unique()

        for un in unique_names:
            # Find all rows corresponding to unique name
            byname_df = df_all[df_all['Image'] == un]

            # Create pairplots (with and without functional stain intensity data)
            # One color
            pp = plt.figure(figsize=(4, 4), dpi=300)
            byname_subset = byname_df[['Image', u'Area (\u03bcm\u00b2)', 'Circularity (a.u.)']]
            sns.pairplot(byname_subset)
            plt.savefig(un + '_pairplot.png', dpi=300)
            plt.close()

        # All-image pairplots
        # One color
        df_all_subset = df_all[['Image', u'Area (\u03bcm\u00b2)', 'Circularity (a.u.)']]
        sns.pairplot(df_all_subset)
        plt.savefig('All-data_pairplot.png', dpi=300)
        plt.close()

        # One color per image
        sns.pairplot(df_all_subset, hue='Image')
        plt.savefig('All-data_multicolor_pairplot.png', dpi=300)
        plt.close()

    def expimgs(self):
        """Export image data (.png image) with processing and labeling applied"""

        current_dir = os.getcwd()  # Select filepath

        if current_dir.split('/')[-1] == 'Results, graphical data':
            current_dir = os.path.dirname(current_dir)
        img_folder = current_dir + '/Results, labeled image data'

        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)

        os.mkdir(img_folder)
        os.chdir(img_folder)

        for j in range(len(df_img)):
            array_orig = cv2.cvtColor((df_img['img orig'].iloc[j][0]).astype(np.uint8), cv2.COLOR_RGB2BGR)
            cv2.imwrite(df_img['name'].iloc[j] + '_original_image.png', array_orig)


class GraphTopLevel(tk.Toplevel):
    def __init__(self, df_img):
        super().__init__()

        self.df_img = df_img

        # Fonts
        boldfont = font.Font(weight='bold')

        # Widgets
        self.title("Analysis results")

        # Label
        title_label = tk.Label(self, text="Graphical results")
        title_label['font'] = boldfont
        title_label.grid(row=0, column=0, padx=10, pady=10)
        # Current image name label
        self.name_label = tk.Label(self, text="")
        self.name_label.grid(row=1, column=0, padx=5, pady=5)
        # Canvas
        self.img_canvas = tk.Canvas(self, width=320, height=320)
        self.img_canvas.grid(row=2, column=0, padx=5, pady=5)
        # Scale
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=len(df_img),
                                  command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid(row=3, column=0, padx=5, pady=5)

        if len(df_img) == 1:  # If only one image, remove scale
            self.img_scale.grid_forget()

        self.displaygraph(idx=0)

        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=4, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

    def displaygraph(self, idx):
        """Display graphs in toplevel window immediately after analysis is run"""
        # Add image name to image name label
        self.name_label.config(text=df_img['name'].iloc[idx])
        graphimg = np.asarray(df_img['graph'].iloc[idx][0]).astype('uint8')
        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimg))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(0, 0, anchor='nw', image=graphimgr_tk)

    def managescale(self, event):
        """Handle changes to scale to switch between possibly many graphs"""

        self.displaygraph(idx=(self.img_scale.get() - 1))

def descriptive_statistics(df_input, img_size):
    """Function to calculate descriptive statistics for each population, represented as a dataframe"""

    dict = {'n cells': len(df_input),
            u'Min. area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].min(),
            u'Mean area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].mean(),
            u'Max. area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].max(),
            u'Stdev, area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].std(),
            'Min. area (pix)': df_input['Area (pix)'].min(),
            'Mean area (pix)': df_input['Area (pix)'].mean(),
            'Max. area (pix)': df_input['Area (pix)'].max(),
            'Stdev, area (pix)': df_input['Area (pix)'].std(),
            'Min. circularity (a.u.)': df_input['Circularity (a.u.)'].min(),
            'Mean circularity (a.u.)': df_input['Circularity (a.u.)'].mean(),
            'Max. circularity (a.u.)': df_input['Circularity (a.u.)'].max(),
            'Stdev, circularity (a.u.)': df_input['Circularity (a.u.)'].std(),
            'Field of view (mm\u00b2)': img_size,
            'Cell density (n/mm\u00b2)': len(df_input)/img_size
            }
    dict_df = pd.DataFrame(dict, index=[0])

    return dict_df