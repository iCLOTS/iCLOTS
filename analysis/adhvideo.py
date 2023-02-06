"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Series of functions that handles analysis for video adhesion application

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from random import randint
import pandas as pd
import trackpy as tp
import warnings
warnings.filterwarnings("ignore", module="trackpy")
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import shutil

class RunBFDefAnalysis():

    def __init__(self, filelist, frames_crop, umpix, fps, maxdiameter, minintensity, maxintensity, x, y, w, h):
        super().__init__(filelist, frames_crop, umpix, fps, maxdiameter, minintensity, maxintensity, x, y, w, h)

    def analysis(self, filelist, frames_crop, umpix, fps, maxdiameter, minintensity, maxintensity, x, y, w, h):
        """Function runs final analysis based on the parameters chosen in GUI"""

        # Base name for files
        self.video_basename = os.path.basename(self.filelist[0].split(".")[0])

        cvfont = cv2.FONT_HERSHEY_SIMPLEX  # For labeling

        self.df_all = pd.DataFrame()  # For all events, good for plotting
        self.df_summary = pd.DataFrame()  # For descriptive statistics
        self.df_img = pd.DataFrame(columns=['name', 'graph'])  # For images, graphs

        # Begin trackpy tracking analysis
        tp.quiet()
        f = tp.batch(frames_crop[:len(frames_crop)], self.maxdiameter.get(),
                     minmass=self.minintensity.get(), invert=False, processes=1);  # Detect particles/cells
        # Filter by maximum mass
        f = f[f['mass'] < self.maxintensity.get()]
        # Link particles, cells into dataframe format
        # Search range criteria: must travel no further than 1/10 the channel length in one frame
        # Memory here signifies a particle/cell cannot "disappear" for more than three frames
        tr = tp.link_df(f, search_range=self.w.get() / 10, memory=3, adaptive_stop=1, adaptive_step=0.95)
        # Filter stubs criteria requires a particle/cell to be present for at least ten frames
        t_final = tp.filter_stubs(tr, 10)

        # Series of vectors for final results dataframe
        p_i = []  # Particle index
        f_start = []  # Start frame, frame where cell first detected
        f_end = []  # End frame, frame where cell last detected
        dist = []  # Distance traveled
        time = []  # Time for travel
        sizes = []  # Cell size
        circ = []  # Circularity
        self.t_tt = pd.DataFrame()  # Create dataframe
        # For each particle, calculate RDI and save data for results dataframe:
        for p in range(t_final['particle'].iloc[-1]):
            df_p = tr[tr['particle'] == p]  # Region of trackpy dataframe corresponding to individual particle index
            x_0 = df_p['x'].iloc[0]  # First x-position
            x_n = df_p['x'].iloc[-1]  # Last x-position
            f_0 = df_p['frame'].iloc[0]  # First frame number
            f_n = df_p['frame'].iloc[-1]  # Last frame number
            s = df_p['mass'].mean() / 255  # Area of cell (pixels)
            d = (x_n - x_0)  # Distance
            t = (f_n - f_0) / float(self.fps.get())  # Time (seconds)
            c = df_p['ecc'].mean()
            # Criteria to save cells as a valid data point:
            # Must travel no further than length of channel
            if d < self.w.get():
                self.t_tt = self.t_tt.append(df_p, ignore_index=True)  # Save trackpy metrics
                # Append data for particle/cell
                p_i.append(p)
                f_start.append(f_0)
                f_end.append(f_n)
                dist.append(d * float(self.umpix.get()))
                time.append(t)
                sizes.append(s * float(self.umpix.get()) * float(self.umpix.get()))
                circ.append(c)

        # Calculate sDI by dividing distance by time (um/sec)
        transit_time = []
        transit_time = np.asarray([u / v for u, v in zip(dist, time)])

        # Organize time, location, and speed data in a list format
        self.df_video = pd.DataFrame(
            {'Particle': p_i,
             'Start frame': f_start,
             'End frame': f_end,
             'Transit time (s)': time,
             'Distance traveled (\u03bcm)': dist,
             'Avg. velocity (\u03bcm/s)': transit_time,
             'Area (\u03bcm\u00b2)': sizes,  # Convert to microns^2
             'Circularity (a.u.)': circ
             })

        # Renumber particles 0 to n
        self.df_video['Particle'] = np.arange(len(self.df_video))
        uniqvals = self.t_tt['particle'].unique()
        newvals = np.arange(len(uniqvals))
        for val in newvals:
            uniqval = uniqvals[val]
            self.t_tt['particle'] = self.t_tt['particle'].replace(uniqval, val)

        # Graph for display
        graphs = plt.figure(figsize=(4, 6), dpi=80)
        graphs.suptitle(self.video_basename, fontweight='bold')

        # If cells exist within the image
        if len(f) != 0:
            # Subplot 311 (area histogram)
            plt.subplot(3, 1, 1)
            plt.hist(self.df_video['Area (\u03bcm\u00b2)'], rwidth=0.8, color='orangered')
            plt.xlabel('Area (\u03bcm\u00b2)')
            plt.ylabel('n')

            # Subplot 312 (circularity histogram)
            plt.subplot(3, 1, 2)
            plt.hist(self.df_video['Circularity (a.u.)'], rwidth=0.8, color='orangered')
            plt.xlabel('Circularity (a.u.)')
            plt.ylabel('n')

            # Subplot 312 (velocity histogram)
            plt.subplot(3, 1, 3)
            plt.hist(self.df_video['Transit time (s)'], rwidth=0.8, color='orangered')
            plt.xlabel('Transit time (s)')
            plt.ylabel('n')

            plt.tight_layout()

            # Prepare for saving to be later referenced in graph window and in exports
            graphs.canvas.draw()
            graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
            graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

            plt.close()

            # Save images to special dataframe
            self.df_img = self.df_img.append({'name': self.video_basename,
                                    'graph': [graphimg]}, ignore_index=True)

            # Append individual image dataframe to larger dataframe
            f.insert(0, 'Image', self.video_basename)
            self.df_all = self.df_all.append(f, ignore_index=True)

            # Append summary data
            self.df_summary = descriptive_statistics(self.df_video)
            self.df_summary.insert(0, 'Video', self.video_basename)


        GraphTopLevel(self.df_img)  # Raise graph window

    def expnum(self, filelist, umpix, fps, maxdiameter, minintensity, maxintensity, x, y, w, h):
        """Export numerical (excel) data, including descriptive statistics and parameters used"""

        writer = pd.ExcelWriter(self.video_basename + '_analysis.xlsx',
                                engine='openpyxl')

        # Write all data to special page
        self.df_video.to_excel(writer, sheet_name='Transit time data', index=False)

        # Write all data to special page
        self.t_tt.to_excel(writer, sheet_name='Trackpy details', index=False)

        # Write summary data to special page
        self.df_summary.to_excel(writer, sheet_name='Summary', index=False)

        now = datetime.datetime.now()
        # Print parameters to a sheet
        param_df = pd.DataFrame({'Ratio, \u03bcm-to-pixels': umpix,
                                 'FPS': fps,
                                 'Maximum cell diameter (px)': maxdiameter,
                                 'Minimum cell intensity': minintensity,
                                 'Maximum cell intensity': maxintensity,
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

        array = cv2.cvtColor(self.df_img['graph'].iloc[0][0], cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.df_img['name'].iloc[0] + '_graph.png', array)

        pp = plt.figure(figsize=(4, 4), dpi=300)
        df_subset = self.df_video[['Transit time (s)', 'Distance traveled (\u03bcm)',
                              'Avg. velocity (\u03bcm/s)', 'Area (\u03bcm\u00b2)', 'Circularity (a.u.)']]
        sns.pairplot(df_subset)
        plt.savefig(self.video_basename + '_pairplot.png', dpi=300)
        plt.close()

    def expimgs(self, frames_crop):
        """Export image data (.png image) with processing and labeling applied"""

        current_dir = os.getcwd()  # Select filepath
        img_folder = os.path.join(current_dir, 'Results, labeled image data')

        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)

        os.mkdir(img_folder)
        os.chdir(img_folder)

        # Set up colors - each event labeled with a different color
        color = []
        n = self.t_tt['particle'].max() + 1
        for i in range(n):
            color.append('#%06X' % randint(0, 0xFFFFFF))

        # For frame in cropped frames
        for i in range(len(frames_crop)):
            image_name = self.video_basename + '_frame_' + str(i).zfill(5)

            f = self.t_tt[self.t_tt['frame'] == i]
            # Set up image to label, including cropping
            PILimg = Image.fromarray(np.dstack((frames_crop[i], frames_crop[i], frames_crop[i])))  # Color
            drawimg = ImageDraw.Draw(PILimg)  # " "
            for j in range(len(f)):
                drawimg.text((f['x'].iloc[j], f['y'].iloc[j]), str(f['particle'].iloc[j]),
                             fill=color[f['particle'].iloc[j]])  # Label
            PILimg.save(image_name + "_labeled.png")  # Save image

        # Close large variables
        frames_crop = None
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
        self.img_canvas = tk.Canvas(self, width=320, height=480)
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
        graphimg = np.asarray(self.df_img['graph'].iloc[idx][0]).astype('uint8')
        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimg))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(0, 0, anchor='nw', image=graphimgr_tk)

def descriptive_statistics(df_input):
    """Function to calculate descriptive statistics for each population, represented as a dataframe"""

    dict = {'n cells': len(df_input),
                  u'Min. transit time (s)': df_input['Transit time (s)'].min(),
                  u'Mean transit time (s)': df_input['Transit time (s)'].mean(),
                  u'Max. transit time (s)': df_input['Transit time (s)'].max(),
                  u'Stdev, transit time (s)': df_input['Transit time (s)'].std(),
                  u'Min. avg. velocity (\u03bcm/s)': df_input['Avg. velocity (\u03bcm/s)'].min(),
                  u'Mean avg. velocity (\u03bcm/s)': df_input['Avg. velocity (\u03bcm/s)'].mean(),
                  u'Max. avg. velocity (\u03bcm/s)': df_input['Avg. velocity (\u03bcm/s)'].max(),
                  u'Stdev, avg. velocity (\u03bcm/s)': df_input['Avg. velocity (\u03bcm/s)'].std(),
                  u'Min. area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].min(),
                  u'Mean area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].mean(),
                  u'Max. area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].max(),
                  u'Stdev, area (\u03bcm\u00b2)': df_input[u'Area (\u03bcm\u00b2)'].std(),
                  'Min. circularity (a.u.)': df_input['Circularity (a.u.)'].min(),
                  'Mean circularity (a.u.)': df_input['Circularity (a.u.)'].mean(),
                  'Max. circularity (a.u.)': df_input['Circularity (a.u.)'].max(),
                  'Stdev, circularity (a.u.)': df_input['Circularity (a.u.)'].std()
                  }
    dict_df = pd.DataFrame(dict, index=[0])

    return dict_df