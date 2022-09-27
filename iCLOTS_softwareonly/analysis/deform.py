"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-08-01 for version 1.0b1

Series of functions that handles analysis for brightfield deformability adhesion application

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import pandas as pd
import trackpy as tp
import warnings
warnings.filterwarnings("ignore", module="trackpy")
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import shutil

class RunBFDefAnalysis():

    def __init__(self, filelist, frames_crop, frames_bgr, umpix, fps, maxdiameter, minintensity, x, y, w, h):
        super().__init__(filelist, frames_crop, frames_bgr, umpix, fps, maxdiameter, minintensity, x, y, w, h)

    def analysis(self, filelist, frames_crop, frames_bgr, umpix, fps, maxdiameter, minintensity, x, y, w, h):
        """Function runs final analysis based on the parameters chosen in GUI"""

        # Global variables for use with additional export functions within class
        global df_img, df_summary, df_video, video_basename, t_sdi

        # Base name for files
        video_basename = os.path.basename(filelist[0].split(".")[0])

        cvfont = cv2.FONT_HERSHEY_SIMPLEX  # For labeling

        df_all = pd.DataFrame()  # For all events, good for plotting
        df_summary = pd.DataFrame()  # For descriptive statistics
        df_img = pd.DataFrame(columns=['name', 'graph'])  # For images, graphs

        # Begin trackpy tracking analysis
        tp.quiet()
        f = tp.batch(frames_bgr[:len(frames_bgr)], self.maxdiameter.get(),
                     minmass=self.minintensity.get(), invert=False, processes=1);  # Detect particles/cells
        # Link particles, cells into dataframe format
        # Search range criteria: must travel no further than 1/3 the channel length in one frame
        # Memory here signifies a particle/cell cannot "disappear" for more than one frame
        tr = tp.link_df(f, search_range=self.w.get() / 3, memory=1, adaptive_stop=1, adaptive_step=0.95)
        # Filter stubs criteria requires a particle/cell to be present for at least three frames
        t_final = tp.filter_stubs(tr, 3)

        # Series of vectors for final results dataframe
        p_i = []  # Particle index
        f_start = []  # Start frame, frame where cell first detected
        f_end = []  # End frame, frame where cell last detected
        dist = []  # Distance traveled
        time = []  # Time for travel
        sizes = []  # Cell size
        t_sdi = pd.DataFrame()  # Create dataframe
        # For each particle, calculate RDI and save data for results dataframe:
        for p in range(t_final['particle'].iloc[-1]):
            df_p = tr[tr['particle'] == p]  # Region of trackpy dataframe corresponding to individual particle index
            x_0 = df_p['x'].iloc[0]  # First x-position
            x_n = df_p['x'].iloc[-1]  # Last x-position
            f_0 = df_p['frame'].iloc[0]  # First frame number
            f_n = df_p['frame'].iloc[-1]  # Last frame number
            s = df_p['mass'].mean() / 255  # Area of cell (pixels)
            d = (x_n - x_0)  # Distance (pixels) - x direction only
            t = (f_n - f_0) / float(self.fps.get())  # Time (seconds)
            # Criteria to save cells as a valid data point:
            # Must travel no less than 1/3 the length of channel
            # Must travel no further than length of channel
            if d < self.w.get() and d > self.w.get() / 3:
                t_sdi = t_sdi.append(df_p, ignore_index=True)  # Save trackpy metrics
                # Append data for particle/cell
                p_i.append(p)
                f_start.append(f_0)
                f_end.append(f_n)
                dist.append(d * float(self.umpix.get()))  # Convert to microns
                time.append(t)
                sizes.append(s)  # Background subtractor changes size of cell, size is a relative measurement

        # Calculate sDI by dividing distance by time (um/sec)
        sdi = []
        sdi = np.asarray([u / v for u, v in zip(dist, time)])

        # Organize time, location, and RDI data in a list format
        df_video = pd.DataFrame(
            {'Particle': p_i,
             'Start frame': f_start,
             'End frame': f_end,
             'Transit time (s)': time,
             'Distance traveled (\u03bcm)': dist,
             'Velocity (\u03bcm/s)': sdi,
             'Area (pix)': sizes
             })

        # Renumber particles 0 to n
        df_video['Particle'] = np.arange(len(df_video))
        uniqvals = t_sdi['particle'].unique()
        newvals = np.arange(len(uniqvals))
        for val in newvals:
            uniqval = uniqvals[val]
            t_sdi['particle'] = t_sdi['particle'].replace(uniqval, val)

        # Graph for display
        graphs = plt.figure(figsize=(4, 4), dpi=80)
        graphs.suptitle(video_basename, fontweight='bold')

        # If cells exist within the image
        if len(f) != 0:
            # Subplot 212 (circularity hist)
            plt.subplot(2, 1, 1)
            plt.hist(df_video['Velocity (\u03bcm/s)'], rwidth=0.8, color='orangered')
            plt.xlabel('Velocity (\u03bcm/s)')
            plt.ylabel('n')

            # Subplot 211 (area hist)
            plt.subplot(2, 1, 2)
            plt.hist(df_video['Area (pix)'], rwidth=0.8, color='orangered')
            plt.xlabel('Area (pix)')
            plt.ylabel('n')

            plt.tight_layout()

            # Prepare for saving to be later referenced in graph window and in exports
            graphs.canvas.draw()
            graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
            graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

            plt.close()

            # Save images to special dataframe
            df_img = df_img.append({'name': video_basename,
                                    'graph': [graphimg]}, ignore_index=True)

            # Append individual image dataframe to larger dataframe
            f.insert(0, 'Image', video_basename)
            df_all = df_all.append(f, ignore_index=True)

            # Append summary data
            df_summary = descriptive_statistics(df_video)
            df_summary.insert(0, 'Video', video_basename)


        GraphTopLevel(df_img)  # Raise graph window

    def expnum(self, filelist, umpix, fps, maxdiameter, minintensity, x, y, w, h):
        """Export numerical (excel) data, including descriptive statistics and parameters used"""

        writer = pd.ExcelWriter(video_basename + '_analysis.xlsx',
                                engine='openpyxl')

        # Write all data to special page
        df_video.to_excel(writer, sheet_name='Velocity data', index=False)

        # Write all data to special page
        t_sdi.to_excel(writer, sheet_name='Trackpy details', index=False)

        # Write summary data to special page
        df_summary.to_excel(writer, sheet_name='Summary', index=False)

        now = datetime.datetime.now()
        # Print parameters to a sheet
        param_df = pd.DataFrame({'Ratio, \u03bcm-to-pixels': umpix,
                                 'FPS': fps,
                                 'Maximum cell diameter (px)': maxdiameter,
                                 'Minimum cell intensity': minintensity,
                                 'ROI x': x,
                                 'ROI y': y,
                                 'ROI w': w,
                                 'ROI h': h,
                                 'Analysis date': now.strftime("%D"),
                                 'Analysis time': now.strftime("%H:%M:%S")}, index=[1])
        param_df.to_excel(writer, sheet_name='Parameters used', index=False)

        writer.save()
        writer.close()

    def expgraph(self):
        """Export graphical (.png image) data, including pairplots"""

        array = cv2.cvtColor(df_img['graph'].iloc[0][0], cv2.COLOR_RGB2BGR)
        cv2.imwrite(df_img['name'].iloc[0] + '_graph.png', array)

        pp = plt.figure(figsize=(4, 4), dpi=300)
        df_subset = df_video[['Transit time (s)', 'Distance traveled (\u03bcm)',
                              'Velocity (\u03bcm/s)', 'Area (pix)']]
        sns.pairplot(df_subset)
        plt.savefig(video_basename + '_pairplot.png', dpi=300)
        plt.close()

    def expimgs(self, frames_crop):
        """Export image data (.png image) with processing and labeling applied"""

        current_dir = os.getcwd()  # Select filepath
        img_folder = os.path.join(current_dir, 'Results, labeled image data')

        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)

        os.mkdir(img_folder)
        os.chdir(img_folder)

        # For frame in cropped frames
        for i in range(len(frames_crop)):
            image_name = video_basename + '_frame_' + str(i).zfill(5)

            f = t_sdi[t_sdi['frame'] == i]
            # Set up image to label, including cropping
            PILimg = Image.fromarray(np.dstack((frames_crop[i], frames_crop[i], frames_crop[i])))  # Color
            drawimg = ImageDraw.Draw(PILimg)  # " "
            for j in range(len(f)):
                drawimg.text((f['x'].iloc[j], f['y'].iloc[j]), str(f['particle'].iloc[j]),
                             fill="#ff0000")  # Label
            PILimg.save(image_name + "_labeled.png")  # Save image

        # Close large variables
        frames_crop = None
        frames_bgr = None
        df_video = None


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
        # Canvas
        self.img_canvas = tk.Canvas(self, width=320, height=320)
        self.img_canvas.grid(row=1, column=0, padx=5, pady=5)

        self.displaygraph(idx=0)

        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=2, column=0, padx=5, pady=5)

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
        graphimg = np.asarray(df_img['graph'].iloc[idx][0]).astype('uint8')
        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimg))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(0, 0, anchor='nw', image=graphimgr_tk)

def descriptive_statistics(df_input):
    """Function to calculate descriptive statistics for each population, represented as a dataframe"""

    dict = {'n cells': len(df_input),
                  u'Min. velocity (\u03bcm/s)': df_input['Velocity (\u03bcm/s)'].min(),
                  u'Mean velocity (\u03bcm/s)': df_input['Velocity (\u03bcm/s)'].mean(),
                  u'Max. velocity (\u03bcm/s)': df_input['Velocity (\u03bcm/s)'].max(),
                  u'Stdev, velocity (\u03bcm/s)': df_input['Velocity (\u03bcm/s)'].std(),
                  u'Min. area (pix)': df_input['Area (pix)'].min(),
                  u'Mean area (pix)': df_input['Area (pix)'].mean(),
                  u'Max. area (pix)': df_input['Area (pix)'].max(),
                  u'Stdev, area (pix)': df_input['Area (pix)'].std()
                  }
    dict_df = pd.DataFrame(dict, index=[0])

    return dict_df