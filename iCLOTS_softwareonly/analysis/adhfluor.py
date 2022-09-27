"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-05 for version 1.0b1

Series of functions that handles analysis for fluorescence microscopy adhesion application

A later version of this application will optionally count regions of a functional stain

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from skimage import measure, img_as_float  # Region analysis
from skimage.feature import peak_local_max
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import shutil

class RunAdhFluorAnalysis():


    def __init__(self, filelist, umpix, minarea, maxarea, mainthresh, fnthresh, ps, fs):
        super().__init__(filelist, umpix, minarea, maxarea, mainthresh, fnthresh, ps, fs)


    def analysis(self, filelist, umpix, minarea, maxarea, mainthresh, fnthresh, ps, fs):
        """Function runs final analysis based on the parameters chosen in GUI"""

        # Global variables for use with additional export functions within class
        global df_img, df_summary, df_all, total_area

        cvfont = cv2.FONT_HERSHEY_SIMPLEX  # For labeling

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
            # Find functional color layer
            if fs is 'r':
                fimg = img[:, :, 2]
                fcolor = [255, 0, 0]
            elif fs is 'g':
                fimg = img[:, :, 1]
                fcolor = [0, 255, 0]
            elif fs is 'b':
                fimg = img[:, :, 0]
                fcolor = [0, 0, 255]
            else:  # Default none
                fimg = np.zeros((img.shape[0], img.shape[1]))  # Blank array
                fcolor = [0, 0, 0]  # Holder

            # Apply thresholds
            thp, pimg_t = cv2.threshold(pimg, self.mainthresh.get(), 255, cv2.THRESH_BINARY)  # Original
            thf, fimg_t = cv2.threshold(fimg, self.fnthresh.get(), 255, cv2.THRESH_BINARY)

            # Calculate size, eccentricity of each "blob"/cell event
            # Label cell events - detect primary stain "blobs"
            p_label_img = measure.label(pimg_t)  # Create a labeled image as an input
            p_props = measure.regionprops_table(p_label_img, properties=('centroid', 'area',
                                                                         'bbox', 'eccentricity', 'coords'))
            # Convert to dataframe, filter
            p_df = pd.DataFrame(p_props)
            if p_df is not None:  # If any cells found
                # Filter by min, max size (two step)
                p_df_filt = p_df[p_df['area'] > self.minarea.get()]
                p_df_filt = p_df_filt[p_df_filt['area'] < self.maxarea.get()]

            # If there is a functional stain, calculate total intensity from within image
            # Calculate texture of main channel image
            co_vector = []
            int_vector = []
            texture_vector = []

            for i in range(len(p_df_filt)):
                indices = np.array(p_df_filt['coords'].iloc[i]).astype(int)
                texture_vector.append(np.std(pimg[indices[:, 0], indices[:, 1]]))

                if np.any(fimg_t[indices[:, 0], indices[:, 1]] > 0):
                    co_vector.append(1)  # 1: colocalization yes/no
                    int_vector.append(np.sum(fimg[indices[:, 0], indices[:, 1]])) # intensity of colocalization

                else:
                    co_vector.append(0)  # 0: no colocalization
                    int_vector.append(0)

            # Append vectors to dataframe as column
            p_df_filt['Signal (binary)'] = co_vector
            p_df_filt['Fn. stain intensity (a.u.)'] = int_vector
            p_df_filt['Texture (a.u.)'] = texture_vector

            # Calculated values: area (um)
            p_df_filt[u'Area (\u03bcm\u00b2)'] = p_df_filt['area'] * float(self.umpix.get()) * float(self.umpix.get())

            # Add index to resultant dataframe
            index = range(len(p_df_filt))
            p_df_filt.insert(0, 'Index', index)

            # Rename additional columns to be saved
            p_df_filt = p_df_filt.rename(columns={'centroid-0': 'y', 'centroid-1': 'x',
                                              'area': 'Area (pix)', 'eccentricity': 'Circularity (a.u.)'})
            p_df_filt['Image'] = imgbasename

            p_df_filt = p_df_filt[['Image', 'Index', 'x', 'y', 'Area (pix)', u'Area (\u03bcm\u00b2)',
                          'Circularity (a.u.)', 'Texture (a.u.)', 'Signal (binary)',
                          'Fn. stain intensity (a.u.)']]

            # Create labeled image, add to dataframe (primary: white, functional: cyan, index: magenta)
            manip = np.zeros((img.shape[0], img.shape[1], 3))  # Base - rows, columns, 3 layers
            manip[np.where(pimg_t == 255)] = pcolor  # Primary color
            manip[np.where(fimg_t == 255)] = fcolor  # Secondary stain cyan

            # Flip layer orientation of original image
            img = np.dstack((img[:, :, 2], img[:, :, 1], img[:, :, 0]))

            # Write ID text on saved image (cyan)
            for j in range(len(p_df_filt)):
                # Original
                cv2.putText(
                            img,
                            str(p_df_filt['Index'].iloc[j]),
                            (int(p_df_filt['x'].iloc[j]), int(p_df_filt['y'].iloc[j])),
                            cvfont,
                            fontScale=0.3,
                            color=(255, 0, 255),
                            thickness=1)

                # Threshold
                cv2.putText(
                            manip,
                            str(p_df_filt['Index'].iloc[j]),
                            (int(p_df_filt['x'].iloc[j]), int(p_df_filt['y'].iloc[j])),
                            cvfont,
                            fontScale=0.3,
                            color=(255, 0, 255),
                            thickness=1)


            # Graph for display
            graphs = plt.figure(figsize=(6, 4), dpi=80)
            graphs.suptitle(imgbasename, fontweight='bold')

            # If cells exist within the image
            if len(p_df_filt) != 0:
                # Subplot 311 (area hist)
                plt.subplot(2, 3, (1, 2))
                plt.hist(p_df_filt[u'Area (\u03bcm\u00b2)'], rwidth=0.8, color='orangered')
                plt.xlabel(u'Area (\u03bcm\u00b2)')
                plt.ylabel('n')
                # Subplot 312 (eccentricity hist)
                plt.subplot(2, 3, (4, 5))
                plt.hist(p_df_filt['Circularity (a.u.)'], rwidth=0.8, color='orangered')
                plt.xlabel('Circularity (a.u.)')
                plt.ylabel('n')
                # Subplot 313 (colocalization pie)
                plt.subplot(2, 3, (3, 6))
                perpos = np.sum(p_df_filt['Signal (binary)'])/len(p_df_filt)
                labels = ['Positive', 'Negative']
                colors = ['orangered', 'orange']
                sizes = [perpos, 1-perpos]
                plt.title('Functional staining')
                plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')

                plt.tight_layout()

            graphs.canvas.draw()
            graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
            graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

            plt.close()

            # Save images to special dataframe
            df_img = df_img.append({'name': imgbasename, 'img orig': [img], 'img thresh': [manip],
                                    'graph': [graphimg]}, ignore_index=True)

            # Append individual image dataframe to larger dataframe
            df_all = df_all.append(p_df_filt, ignore_index=True)

            # Append summary data
            df_image = descriptive_statistics(p_df_filt, img_size)
            df_image.insert(0, 'Image', imgbasename)
            df_summary = df_summary.append(df_image, ignore_index=True)

            # Clear variables
            pimg = None
            pimg_t = None
            fimg = None
            fimg_t = None
            p_label_img = None
            p_props = None
            p_df = None
            p_df_filt = None
            manip = None
            img = None


        # Raise toplevel to show graphs
        GraphTopLevel(df_img)


    def expnum(self, filelist, umpix, minarea, maxarea, mainthresh, fnthresh, ps, fs):
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
                      'Functional stain color': fs,
                      'Threshold, functional stain': fnthresh,
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
            byname_subset = byname_df[['Image', u'Area (\u03bcm\u00b2)', 'Circularity (a.u.)', 'Texture (a.u.)',
                                    'Fn. stain intensity (a.u.)']]
            sns.pairplot(byname_subset)
            plt.savefig(un + '_pairplot.png', dpi=300)
            plt.close()

        # all image pairplots
        # Create pairplots (with and without functional stain intensity data)
        # One color
        df_all_subset = df_all[['Image', u'Area (\u03bcm\u00b2)', 'Circularity (a.u.)',
                                'Texture (a.u.)', 'Fn. stain intensity (a.u.)']]
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
        self.img_canvas = tk.Canvas(self, width=480, height=320)
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
        # rf = 300 / np.max((graphimg.shape[0], graphimg.shape[1]))
        # dim = (int(graphimg.shape[1] * rf), int(graphimg.shape[0] * rf))
        # graphimgr = cv2.resize(graphimg, dim, interpolation=cv2.INTER_AREA)
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
            'Fn. stain positive cells (%)': df_input['Signal (binary)'].sum() / len(df_input) * 100,
            'Min. fn. stain intensity (a.u.)': df_input['Fn. stain intensity (a.u.)'].min(),
            'Mean fn. stain intensity (a.u.)': df_input['Fn. stain intensity (a.u.)'].mean(),
            'Max. fn. stain intensity (a.u.)': df_input['Fn. stain intensity (a.u.)'].max(),
            'Stdev, fn. stain intensity (a.u.)': df_input['Fn. stain intensity (a.u.)'].std(),
            'Field of view (mm\u00b2)': img_size,
            'Cell density (n/mm\u00b2)': len(df_input)/img_size
            # 'Min. fn. stain regions (n)': df_input['Fn. stain regions (n)'].min(),  # Will be included in later release
            # 'Mean fn. stain regions (n)': df_input['Fn. stain regions (n)'].mean(),
            # 'Max. fn. stain regions (n)': df_input['Fn. stain regions (n)'].max(),
            # 'Stdev, fn. stain regions (n)': df_input['Fn. stain regions (n)'].std()
            }
    dict_df = pd.DataFrame(dict, index=[0])

    return dict_df