"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-07-18 for version 1.0b1

Series of functions that handles analysis for fluorescent occlusion/accumulation region of interest app

A later version of this application will incorporate channel detection for brightfield microscopy images

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from skimage import measure
from scipy.ndimage import label
import matplotlib.pyplot as plt
import datetime
import shutil


def occ_acc(filelist, colorname, thresh, layer, x, y, w, h):
    occlusion = [0]  # init
    accumulation = [0]
    time = [0]

    df_img_single = pd.DataFrame()

    for img in filelist:
        imgname = os.path.basename(img).split(".")[0]
        channelimg = cv2.imread(img)

        crop = channelimg[y:(y + h), x:(x + w), :]  # Create cropped image

        channelimg_l = crop[:, :, layer]  # Pull out correct layer

        ret, array_bin = cv2.threshold(channelimg_l, thresh, 255, cv2.THRESH_BINARY)

        img_to_save = np.zeros(crop.shape)
        color = [0, 0, 0]
        color[layer] = 255
        img_to_save[np.where(array_bin == 255)] = color

        df_img_single = df_img_single.append({'name': imgname + '_' + colorname, 'img': img_to_save}, ignore_index=True)

        occ = np.sum(array_bin / 255)
        time.append(imgname)
        occlusion.append(occ)

    # Calculate accumulation as change in occlusion between frames
    for i in range(len(occlusion) - 1):
        accumulation.append(occlusion[i + 1] - occlusion[i])

    return (colorname, time, occlusion, accumulation, df_img_single)


class RunOccAccROIAnalysis():

    def __init__(self, filelist, umpix, rchannel, rthresh, gchannel, gthresh, bchannel, bthresh, x, y, w, h):
        super().__init__(filelist, umpix, rchannel, rthresh, gchannel, gthresh, bchannel, bthresh, x, y, w, h)


    def analysis(self, filelist, umpix, rchannel, rthresh, gchannel, gthresh, bchannel, bthresh, x, y, w, h):
        """Function runs final analysis based on the parameters chosen in GUI"""

        self.filelist_a = filelist
        self.umpix_a = umpix


        foldername = os.path.dirname(filelist[0])
        name = os.path.basename(foldername)

        # Read image
        img = cv2.imread(filelist[-1])

        crop = img[y:(y + h), x:(x + w), :]  # Create cropped image

        graphs = plt.figure()
        graphs.suptitle(name, fontweight='bold')

        # Set up dataframes
        self.df = pd.DataFrame()  # For raw data
        self.df_img = pd.DataFrame()

        # For each present color, run analysis_math for by-color spatial dataframe and mean, max dataframes
        # Add to graph

        graphs = plt.figure()

        # Red
        if rchannel is True:
            colorname, time, occlusion, accumulation, df_img_single = occ_acc(self.filelist_a, 'red', rthresh, 2, x, y, w, h)  # Name, threshold, layer

            occlusion_umpix = np.asarray(occlusion) * self.umpix_a * self.umpix_a
            accumulation_umpix = np.asarray(accumulation) * self.umpix_a * self.umpix_a
            print(len(accumulation_umpix))
            self.df['Image'] = time
            self.df['Red occlusion (pix)'] = occlusion
            self.df['Red occlusion (\u03bcm\u00b2)'] = occlusion_umpix
            self.df['Red accumulation (pix/timepoint)'] = accumulation
            self.df['Red accumulation (\u03bcm\u00b2/timepoint)'] = accumulation_umpix

            # Plot mean as darker color
            # Occlusion
            timevec = range(len(time))
            plt.subplot(1, 2, 1)
            plt.plot(timevec, occlusion_umpix, color=colorname)
            # Accumulation
            plt.subplot(1, 2, 2)
            plt.plot(timevec, accumulation_umpix, color=colorname)

            # Append single image df to full image df
            self.df_img = self.df_img.append(df_img_single)

        # Green
        if gchannel is True:
            colorname, time, occlusion, accumulation, df_img_single = occ_acc(self.filelist_a, 'green', gthresh, 1, x, y, w, h)  # Name, threshold, layer

            occlusion_umpix = np.asarray(occlusion) * self.umpix_a * self.umpix_a
            accumulation_umpix = np.asarray(accumulation) * self.umpix_a * self.umpix_a

            self.df['Image'] = time
            self.df['Green occlusion (pix)'] = occlusion
            self.df['Green occlusion (\u03bcm\u00b2)'] = occlusion_umpix
            self.df['Green accumulation (pix/timepoint)'] = accumulation
            self.df['Green accumulation (\u03bcm\u00b2/timepoint)'] = accumulation_umpix

            # Plot mean as darker color
            # Occlusion
            timevec = range(len(time))
            plt.subplot(1, 2, 1)
            plt.plot(timevec, occlusion_umpix, color=colorname)
            # Accumulation
            plt.subplot(1, 2, 2)
            plt.plot(timevec, accumulation_umpix, color=colorname)

            # Append single image df to full image df
            self.df_img = self.df_img.append(df_img_single)

        # Blue
        if bchannel is True:
            colorname, time, occlusion, accumulation, df_img_single = occ_acc(self.filelist_a, 'blue', bthresh, 0, x, y, w, h)  # Name, threshold, layer

            occlusion_umpix = np.asarray(occlusion) * self.umpix_a * self.umpix_a
            accumulation_umpix = np.asarray(accumulation) * self.umpix_a * self.umpix_a

            self.df['Image'] = time
            self.df['Blue occlusion (pix)'] = occlusion
            self.df['Blue occlusion (\u03bcm\u00b2)'] = occlusion_umpix
            self.df['Blue accumulation (pix/timepoint)'] = accumulation
            self.df['Blue accumulation (\u03bcm\u00b2/timepoint)'] = accumulation_umpix

            # Plot mean as darker color
            # Occlusion
            timevec = range(len(time))
            plt.subplot(1, 2, 1)
            plt.plot(timevec, occlusion_umpix, color=colorname)
            # Accumulation
            plt.subplot(1, 2, 2)
            plt.plot(timevec, accumulation_umpix ,color=colorname)

            # Append single image df to full image df
            self.df_img = self.df_img.append(df_img_single)

        # Titles, xlabels, ylabels
        # Occlusion
        plt.subplot(1, 2, 1)
        plt.title('Region occlusion')
        plt.xlabel('Time point (n)')
        plt.ylabel('Occlusion (\u03bcm\u00b2)')
        # Accumulation
        plt.subplot(1, 2, 2)
        plt.title('Region accumulation')
        plt.xlabel('Time point (n)')
        plt.ylabel(u'Accumulation (\u03bcm\u00b2)/timepoint')

        plt.tight_layout()

        # Set up graph for toplevel graph display window
        graphs.canvas.draw()
        graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
        self.graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

        # Clear image variables
        img = None
        crop = None
        img_th_red = None
        img_th_blue = None
        img_th_green = None
        mapbin = None
        mapbin_ext = None
        layered_arr = None

        # Raise toplevel to show graphs
        GraphTopLevel(self.graphimg)

    def expnum(self, filelist, umpix, rchannel, rthresh, gchannel, gthresh, bchannel, bthresh, x, y, w, h):

        # Create naming convention for excel sheet
        if len(filelist) == 1:  # Single file
            nameconvention = os.path.basename(filelist[0]).split(".")[0]
        elif len(filelist) > 1:  # Directory of files
            nameconvention_d = os.path.dirname(filelist[0])
            nameconvention = os.path.basename(nameconvention_d)

        # Create writer to save results to
        writer = pd.ExcelWriter(nameconvention[0:14] + '_analysis.xlsx', engine='openpyxl')  # Crop to avoid excel error

        self.df.to_excel(writer, sheet_name='Data', index=False)

        now = datetime.datetime.now()
        # Print parameters to a sheet
        param_df = pd.DataFrame({'Ratio, \u03bcm-to-pixels': umpix,
                      'Red channel': rchannel,
                      'Threshold, red channel': rthresh,
                      'Green channel': gchannel,
                      'Threshold, green channel': gthresh,
                      'Blue channel': bchannel,
                      'Threshold, blue channel': bthresh,
                      'X coordinate (top)': x,
                      'Y coordinate (top)': y,
                      'ROI width': w,
                      'ROI height': h,
                      'Analysis date': now.strftime("%D"),
                      'Analysis time': now.strftime("%H:%M:%S")}, index=[1])
        param_df.to_excel(writer, sheet_name='Parameters used', index=False)

        writer.save()
        writer.close()

    def expgraph(self):

        current_dir = os.getcwd()  # Select filepath

        if os.path.basename(current_dir) == 'Results, labeled image data':
            os.chdir(os.path.dirname(current_dir))

        # Convert image to BGR
        array = cv2.cvtColor(self.graphimg, cv2.COLOR_RGB2BGR)
        cv2.imwrite('Analysis_graph.png', array)

    def expimgs(self):

        current_dir = os.getcwd()  # Select filepath


        # if 'Results' in current_dir.split('/')[-1]:
        #     current_dir = os.path.dirname(current_dir)
        img_folder = os.path.join(current_dir, 'Results, labeled image data')

        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)

        os.mkdir(img_folder)
        os.chdir(img_folder)

        for j in range(len(self.df_img)):
            array = (self.df_img['img'].iloc[j]).astype('uint8')
            cv2.imwrite(self.df_img['name'].iloc[j] + '_image.png', array)

        # Clear large dataframe variables
        df = None
        df_img = None
        df_summary_all = None
        df_frame = None


class GraphTopLevel(tk.Toplevel):
    def __init__(self, graphimg):
        super().__init__()

        self.graphimg = graphimg

        self.title("Analysis results")

        # Canvas widget
        self.img_canvas = tk.Canvas(self, width=480, height=320)
        self.img_canvas.grid(row=0, column=0, padx=5, pady=5)
        # Show graph
        graphimg = np.asarray(graphimg).astype('uint8')
        # Resize
        height, width, layers = graphimg.shape
        if width/480 > height/320:
            factor = 480 / width
        else:  # If height ratio greater or if equal (if equal factor same)
            factor = 320/height
        dim = (int(width * factor), int(height * factor))
        graphimgr = cv2.resize(graphimg, dim, interpolation=cv2.INTER_AREA)
        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimgr))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(240, 160, anchor='c', image=graphimgr_tk)

        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=1, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)