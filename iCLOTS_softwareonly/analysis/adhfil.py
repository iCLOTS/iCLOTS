"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-05 for version 1.0b1

Series of functions that handles analysis for filopodia-counting fluorescence microscopy adhesion application

A later version of this application will quantify area and intensity of a functional stain

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from skimage import measure # Region analysis
from skimage.feature import corner_harris, corner_peaks  # Corner finding/filopodia counting
import math
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import shutil

class RunAdhFilAnalysis():


    def __init__(self, filelist, umpix, minarea, maxarea, mainthresh, k, tr, min_distance, ps):
        super().__init__(filelist, umpix, minarea, maxarea, mainthresh, k, tr, min_distance, ps)


    def analysis(self, filelist, umpix, minarea, maxarea, mainthresh, k, tr, min_distance, ps):
        """Function runs final analysis based on the parameters chosen in GUI"""

        # Global variables for use with additional export functions within class
        global df_img, df_summary, df_all, total_area

        cvfont = cv2.FONT_HERSHEY_SIMPLEX  # For labeling
        top, bottom, left, right = [10] * 4  # Used for creating border around individual cell images

        df_all = pd.DataFrame()  # For all events, good for plotting
        df_summary = pd.DataFrame()  # For descriptive statistics
        df_img = pd.DataFrame(columns=['name', 'img', 'graph'])

        # For each image
        total_area = 0  # For calculating final density measurement
        for imgname in filelist:

            # Read image
            img = cv2.imread(imgname)
            imgbasename = os.path.basename(imgname.split(".")[0])

            # Convert area of image (one layer) to mm2
            img_size = img.size / 3 * float(self.umpix.get()) * float(self.umpix.get()) / 1E6
            total_area += img_size  # Record total area of all images for final density calculation

            # Choose correct channels, set up color for saved images
            # Find primary color layer
            # OpenCV uses a 'BGR' color scheme, new colors in RGB
            if ps is 'r':
                pimg = img[:, :, 2]
                pcolor = [255, 0, 0]
            elif ps is 'g':
                pimg = img[:, :, 1]
                pcolor = [0, 255, 0]
            elif ps is 'b':
                pimg = img[:, :, 0]
                pcolor = [0, 0, 255]
            else:  # Default greyscale
                pimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                pcolor = [128, 128, 128]

            # Apply thresholds
            thp, pimg_t = cv2.threshold(pimg, self.mainthresh.get(), 255, cv2.THRESH_BINARY)  # Membrane stain

            # Calculate size, eccentricity of each "blob"/cell event
            # Label cell events - detect primary stain "blobs"
            p_label_img = measure.label(pimg_t)  # Create a labeled image as an input
            p_props = measure.regionprops_table(p_label_img, properties=('centroid', 'area', 'filled_area', 'image',
                                                                  'convex_area', 'convex_image',
                                                                  'bbox', 'eccentricity', 'coords'))  # Image for count
            # Convert to dataframe, filter
            p_df = pd.DataFrame(p_props)
            if p_df is not None:  # If any cells found
                # Filter by min, max size (two step)
                p_df_filt = p_df[p_df['area'] > self.minarea.get()]
                p_df_filt = p_df_filt[p_df_filt['area'] < self.maxarea.get()]

            # Calculate additional properties of cells, including functional stain measurements
            filopodia_count_vector = []  # n filopodia
            min_length = []  # minimum filopodia length
            mean_length = []  # mean length of filopodia
            max_length = []  # maximum filopodia length
            stdev_length = []  # standard deviation of length of filopodia
            texture_vector = []  # Texture, a membrane property

            # Set up images to label
            # Flip layer orientation of original image from BGR to RGB
            img_tolabel = np.dstack((img[:, :, 2], img[:, :, 1], img[:, :, 0]))

            # Create thresholded image
            t_tolabel = np.zeros((img.shape[0], img.shape[1], 3))  # Base - rows, columns, 3 layers
            t_tolabel[np.where(pimg_t == 255)] = pcolor  # Primary color

            for i in range(len(p_df_filt)):
                indices = np.array(p_df_filt['coords'].iloc[i]).astype(int)
                texture_vector.append(np.std(pimg[indices[:, 0], indices[:, 1]]))

                # Filopodia count
                # Convex area is used so that inner corners don't also get counted - just outermost points
                # # This could result in some points within the convex shape being missed
                convex = p_df_filt['convex_image'].iloc[i]
                convex_image = np.asarray(convex * 255).astype(np.uint8)  # Convert to uint8 image for openCV
                # Border allows outermost points to be counted - corner detection doesn't work on points at edge
                image_with_border = cv2.copyMakeBorder(convex_image, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                                       value=0)

                # Find coordinates of corners
                coords = corner_peaks(corner_harris(image_with_border, k=self.k.get()), threshold_rel=self.tr.get(),
                                      min_distance=self.min_distance.get())

                if coords.any():
                    filopodia_count_vector.append(len(coords))
                    cell_center = [image_with_border.shape[1] / 2,
                                   image_with_border.shape[0] / 2]  # Find center of cell
                    distances = []  # Distance of coordinates from center
                    for pt in coords:  # This probably doesn't need to be a loop, would appreciate github pull requests
                        # Would also appreciate github pull requests for saving distances as a list within pandas dataframe
                        distances.append(math.sqrt((cell_center[0] - pt[0]) ** 2
                                                   + (cell_center[1] - pt[1]) ** 2) * float(self.umpix.get()))

                        # Label filopodia on original and threshold image
                        pt1 = int(p_df_filt['centroid-1'].iloc[i] - convex_image.shape[1] / 2 + pt[1] - 10)
                        pt0 = int(p_df_filt['centroid-0'].iloc[i] - convex_image.shape[0] / 2 + pt[0] - 10)

                        cv2.circle(img_tolabel, tuple((pt1, pt0)), 1, (255, 255, 0), 2)
                        cv2.circle(t_tolabel, tuple((pt1, pt0)), 1, (255, 255, 0), 2)

                    min_length.append(np.min(distances))  # minimum filopodia length
                    mean_length.append(np.mean(distances))  # mean length of filopodia
                    max_length.append(np.max(distances))  # maximum filopodia length
                    stdev_length.append(np.std(distances))  # standard deviation of length of filopodia

                # If not, append 0 to indicate no signal or N/A
                else:
                    filopodia_count_vector.append(0)
                    min_length.append(0)
                    mean_length.append(0)
                    max_length.append(0)
                    stdev_length.append(0)

            # Append vectors to dataframe as column
            p_df_filt['Texture (a.u.)'] = texture_vector
            p_df_filt['Filopodia (n)'] = filopodia_count_vector
            p_df_filt['Min. filopodia length (\u03bcm)'] = min_length
            p_df_filt['Mean filopodia length (\u03bcm)'] = mean_length
            p_df_filt['Max. filopodia length (\u03bcm)'] = max_length
            p_df_filt['Stdev. filopodia length (\u03bcm)'] = stdev_length

            # Calculated values: area (um)
            p_df_filt[u'Area (\u03bcm\u00b2)'] = p_df_filt['area'] * float(self.umpix.get()) * float(self.umpix.get())

            # Add index to resultant dataframe
            index = range(len(p_df_filt))
            p_df_filt.insert(0, 'Index', index)

            # Rename additional columns to be saved
            p_df_filt = p_df_filt.rename(columns={'centroid-0': 'y', 'centroid-1': 'x',
                                              'area': 'Area (pix)', 'eccentricity': 'Circularity (a.u.)'})
            p_df_filt['Image'] = imgbasename

            # Select and reorder columns
            p_df_filt = p_df_filt[['Image', 'Index', 'x', 'y', 'Area (pix)', u'Area (\u03bcm\u00b2)',
                          'Circularity (a.u.)', 'Texture (a.u.)', 'Filopodia (n)', 'Min. filopodia length (\u03bcm)',
                          'Mean filopodia length (\u03bcm)', 'Max. filopodia length (\u03bcm)',
                          'Stdev. filopodia length (\u03bcm)']]

            # Write ID text on saved image (cyan)
            for j in range(len(p_df_filt)):
                # Original
                cv2.putText(
                            img_tolabel,
                            str(p_df_filt['Index'].iloc[j]),
                            (int(p_df_filt['x'].iloc[j]), int(p_df_filt['y'].iloc[j])),
                            cvfont,
                            fontScale=0.3,
                            color=(255, 0, 255),
                            thickness=1)

                # Threshold
                cv2.putText(
                            t_tolabel,
                            str(p_df_filt['Index'].iloc[j]),
                            (int(p_df_filt['x'].iloc[j]), int(p_df_filt['y'].iloc[j])),
                            cvfont,
                            fontScale=0.3,
                            color=(255, 0, 255),
                            thickness=1)


            # Graph for display
            graphs = plt.figure(figsize=(4, 4), dpi=80)
            graphs.suptitle(imgbasename, fontweight='bold')

            # If cells exist within the image
            if len(p_df_filt) != 0:

                # Subplot 211 (n filopodia histogram)
                plt.subplot(2, 1, 1)
                plt.hist(p_df_filt['Filopodia (n)'], rwidth=0.8, color='orangered')
                plt.xlabel('Filopodia per cell (n)')
                plt.ylabel('n')
                # Subplot 212 (circularity hist)
                plt.subplot(2, 1, 2)
                plt.hist(p_df_filt['Mean filopodia length (\u03bcm)'], rwidth=0.8, color='orangered')
                plt.xlabel('Mean filopodia length (\u03bcm)')
                plt.ylabel('n')

                plt.tight_layout()

            graphs.canvas.draw()
            graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
            graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

            plt.close()




            # Save images to special dataframe
            df_img = df_img.append({'name': imgbasename, 'img orig': [img_tolabel], 'img thresh': [t_tolabel],
                                    'graph': [graphimg]}, ignore_index=True)

            # Append individual image dataframe to larger dataframe
            df_all = df_all.append(p_df_filt, ignore_index=True)

            # Append summary data
            df_image = descriptive_statistics(p_df_filt, img_size)
            df_image.insert(0, 'Image', imgbasename)
            df_summary = df_summary.append(df_image, ignore_index=True)

            # Clear image variables
            img = None
            pimg = None
            pimg_t = None
            p_label_img = None
            p_props = None
            p_df = None
            p_df_filt = None
            img_tolabel = None
            t_tolabel = None
            graphimg = None


        # Raise toplevel to show graphs
        GraphTopLevel(df_img)


    def expnum(self, filelist, umpix, minarea, maxarea, mainthresh, k, tr, min_distance, ps):
        """Export numerical (excel) data, including descriptive statistics and parameters used"""

        # Create naming convention for excel sheet
        if len(filelist) == 1:  # Single file
            nameconvention = os.path.basename(filelist[0]).split(".")[0]
        elif len(filelist) > 1:  # Directory of files
            nameconvention = os.path.dirname(filelist[0]).split("/")[-1]

        # Create writer to save   to
        writer = pd.ExcelWriter(nameconvention[0:14] + '_analysis.xlsx', engine='openpyxl')  # Crop to avoid excel error

        # Calculate summary metrics, write individual sheets to excel file writer
        # Individual image names
        unique_names = df_all.Image.unique()

        # summary_df = pd.DataFrame()
        for un in unique_names:
            # Find all rows corresponding to unique name
            byname_df = df_all[df_all['Image'] == un]
            # Write individual frame data to specific sheet
            byname_df.to_excel(writer, sheet_name=un[0:30], index=False)  # Crop name to prevent errors

        df_all.to_excel(writer, sheet_name='All data', index=False)

        # Calculate values of all summary
        # Append summary data
        df_image = descriptive_statistics(df_all, total_area)
        df_image.insert(0, 'Image', 'All data')
        df_summary_hold = df_summary.copy()
        df_summary_hold = df_summary_hold.append(df_image, ignore_index=True)

        df_summary_hold.to_excel(writer, sheet_name='Summary', index=False)



        now = datetime.datetime.now()
        # Print parameters to a sheet
        param_df = pd.DataFrame({'Ratio, \u03bcm-to-pixels': umpix,
                      'Minimum cell area (px)': minarea,
                      'Maximum cell area (px)': maxarea,
                      'Membrane stain color': ps,
                      'Threshold, membrane stain': mainthresh,
                      'Sharpness (k, a.u.)': k,
                      'Relative threshold of intensity (tr, a.u.)': tr,
                      'Min. dist. between fil. (px)': min_distance,
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
        graph_folder = os.path.join(current_dir, 'Results, graphical data')

        if os.path.exists(graph_folder):
            shutil.rmtree(graph_folder)

        os.mkdir(graph_folder)
        os.chdir(graph_folder)

        for i in range(len(df_img)):

            # Convert image to BGR
            array = cv2.cvtColor(df_img['graph'].iloc[i][0], cv2.COLOR_RGB2BGR)
            cv2.imwrite(df_img['name'].iloc[i] + '_graph.png', array)

            unique_names = df_all.Image.unique()

            # summary_df = pd.DataFrame()
        for un in unique_names:
            # Find all rows corresponding to unique name
            byname_df = df_all[df_all['Image'] == un]
                # Write individual frame data to specific sheet

            # Create pairplots (with and without functional stain intensity data)
            # One color
            pp = plt.figure(figsize=(6, 6), dpi=300)
            byname_subset = byname_df[[u'Area (\u03bcm\u00b2)',
                               'Circularity (a.u.)', 'Texture (a.u.)', 'Filopodia (n)', 'Min. filopodia length (\u03bcm)',
                               'Mean filopodia length (\u03bcm)', 'Max. filopodia length (\u03bcm)',
                               'Stdev. filopodia length (\u03bcm)']]
            sns.pairplot(byname_subset)
            plt.savefig(un + '_pairplot.png', dpi=300)
            plt.close()

        # all image pairplots
        # Create pairplots (with and without functional stain intensity data)
        # One color
        df_all_subset = df_all[['Image', u'Area (\u03bcm\u00b2)',
                           'Circularity (a.u.)', 'Texture (a.u.)', 'Filopodia (n)', 'Min. filopodia length (\u03bcm)',
                           'Mean filopodia length (\u03bcm)', 'Max. filopodia length (\u03bcm)',
                           'Stdev. filopodia length (\u03bcm)']]
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
        img_folder = os.path.join(current_dir, 'Results, labeled image data')

        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)

        os.mkdir(img_folder)
        os.chdir(img_folder)

        for j in range(len(df_img)):
            array_orig = cv2.cvtColor((df_img['img orig'].iloc[j][0]).astype(np.uint8), cv2.COLOR_RGB2BGR)
            cv2.imwrite(df_img['name'].iloc[j] + '_original_image.png', array_orig)
            array_thresh = cv2.cvtColor((df_img['img thresh'].iloc[j][0]).astype(np.uint8), cv2.COLOR_RGB2BGR)
            cv2.imwrite(df_img['name'].iloc[j] + '_threshold_image.png', array_thresh)

        # Clear variables
        df_all = None
        df_all_subset = None
        df_summary = None
        df_summary_hold = None

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
                  'Min. texture (a.u.)': df_input['Texture (a.u.)'].min(),
                  'Mean texture (a.u.)': df_input['Texture (a.u.)'].mean(),
                  'Max. texture (a.u.)': df_input['Texture (a.u.)'].max(),
                  'Stdev, texture (a.u.)': df_input['Texture (a.u.)'].std(),
                  'Min. filopodia (n)': df_input['Filopodia (n)'].min(),
                  'Mean filopodia (n)': df_input['Filopodia (n)'].mean(),
                  'Max. filopodia (n)': df_input['Filopodia (n)'].max(),
                  'Stdev, filopodia (n)': df_input['Filopodia (n)'].std(),
                  'Field of view (mm\u00b2)': img_size,
                  'Cell density (n/mm\u00b2)': len(df_input)/img_size
                  }
    dict_df = pd.DataFrame(dict, index=[0])

    return dict_df