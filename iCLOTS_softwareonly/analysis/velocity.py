"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-31 for version 1.0b1

Series of functions that handles analysis for velocity application

"""

import tkinter as tk
import tkinter.font as font
import os
import cv2
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import shutil

class RunVelocityAnalysis():

    def __init__(self, filelist, umpix, fps, n_bins, n_points, block_size, winsize_x, winsize_y, x, y, w, h):
        super().__init__(filelist, umpix, fps, n_bins, n_points, block_size, winsize_x, winsize_y, x, y, w, h)

    def analysis(self, filelist, umpix, fps, n_bins, n_points, block_size, winsize_x, winsize_y, x, y, w, h):
        """Function runs final analysis based on the parameters chosen in GUI"""

        # Variables needed for other functions
        self.filelist_a = filelist  # Labeling with _a keeps values from overwriting if user selects new video
        self.umpix_a = umpix
        self.fps_a = fps
        self.n_bins_a = n_bins
        self.n_points_a = n_points
        self.block_size_a = block_size
        self.winsize_x_a = winsize_x
        self.winsize_y_a = winsize_y
        self.x_a = x
        self.y_a = y
        self.w_a = w
        self.h_a = h

        # Set up parameters
        # params for ShiTomasi corner detection
        # to be used in line of code: cv2.goodFeaturesToTrack
        # helpful: https://docs.opencv.org/master/d4/d8c/tutorial_py_shi_tomasi.html
        self.max_corners = self.n_points_a
        self.qual_level = 0.01
        self.min_dist_st = self.block_size_a/2
        block_size = self.block_size_a
        feature_params = dict(maxCorners=self.max_corners,  # n best corners to track, more = more computationally expensive
                              qualityLevel=self.qual_level,
                              # parameter characterizing the minimal accepted quality of image corners
                              minDistance=self.min_dist_st,  # minimum
                              # possible Euclidean distance between the returned corners (pix)
                              blockSize=block_size)  # size of an average block for computing a derivative covariation matrix over each pixel neighborhood

        # Parameters for lucas kanade optical flow
        # to be used in the line of code: cv2.calcOpticalFlowPyrLK
        # helpful: https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
        self.win_size = (int(self.winsize_y_a/2), int(self.winsize_x_a/2))  # Pyramid level (max_level) adjustment
        self.max_level = 2
        iter = 1  # Numer of iterations (for search criteria)
        min_dist_klt = 1  # Minimum distance that a corner must move (for search criteria)
        lk_params = dict(winSize=self.win_size,  # size of the search window at each pyramid level (w, h)
                         maxLevel=self.max_level,
                         # 0-based maximal pyramid level number, 0 = original, 1 = 2 levels used, 2 = 3 levels used
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, iter,
                                   min_dist_klt))  # termination criteria of the iterative search algorithm

        # Base name for files
        self.video_basename = os.path.basename(filelist[0].split(".")[0])

        # Set up dataframes to save data for export options
        self.df_frame = pd.DataFrame()  # Frame info, to be saved as excel, graphed
        self.df_img_first = pd.DataFrame(columns=['name', 'image'])  # For images, graphs - first 100
        self.df_img_linspace = pd.DataFrame(columns=['name', 'image'])

        # Read video
        cap = cv2.VideoCapture(filelist[0])
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        ret, first_frame = cap.read()

        init_frame = first_frame[self.y_a:(self.y_a + self.h_a), self.x_a:(self.x_a + self.w_a), :]  # Create cropped image
        init_gray = cv2.cvtColor(init_frame, cv2.COLOR_BGR2GRAY)

        count = 0  # Count initial value

        # Initial lists to save frame, position, velocity values (dataframe too computationally expensive)
        frames = []
        positions = []
        velocities = []

        cap_ret = True
        while count < n_frames - 1 and cap_ret:
            cap_ret, frame = cap.read()  # Read
            frame_crop = frame[self.y_a:(self.y_a + self.h_a), self.x_a:(self.x_a + self.w_a), :]  # Create cropped image
            frame_gray = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2GRAY)  # One layer

            # Select initial points
            p0 = cv2.goodFeaturesToTrack(frame_gray, mask=None, **feature_params)
            if p0 is not None:
                # Track points
                p1, st, err = cv2.calcOpticalFlowPyrLK(init_gray, frame_gray, p0, None, **lk_params)
                if p1.any():  # If points found
                    good_new = p1[st == 1]
                    good_old = p0[st == 1]

                    for i, (new, old) in enumerate(zip(good_new, good_old)):
                        a, b = new.ravel()
                        c, d = old.ravel()

                        # Calculate displacement/velocity
                        vel = np.sqrt(
                            (new[0] - old[0]) ** 2 + (new[1] - old[1]) ** 2) * float(fps) * float(umpix)  # With y displacement
                        # vel = (new[0] - old[0]) * fps * umpix  # Ignore y displacement

                        # Save frame, position, displacement
                        frames.append(count)
                        positions.append(new[1])
                        velocities.append(vel)

                        # Save first 100 images
                        if count < 100:
                            image = cv2.arrowedLine(frame_crop, (int(c), int(b)), (int(a), int(d)), (255, 255, 0),
                                                    1)  # Cyan arrow

                            # Save images to special dataframe
                            self.df_img_first = self.df_img_first.append({'name': self.video_basename + '_frame_' + str(count).zfill(5) + '.png',
                                                    'image': image}, ignore_index=True)

                        # Save every 100th image
                        if count % 100 == 0:
                            image = cv2.arrowedLine(frame_crop, (int(c), int(b)), (int(a), int(d)), (255, 255, 0),
                                                    1)  # Cyan arrow

                            # Save images to special dataframe
                            self.df_img_linspace = self.df_img_linspace.append({'name': self.video_basename + '_frame_' + str(count).zfill(5) + '.png',
                                                    'image': image}, ignore_index=True)

            count += 1

            # Now update the previous frame
            init_gray = frame_gray.copy()

        # Create a dataframe with frame, position, and displacement data
        dict_csv = {'Frame': frames, 'Channel pos. (pix)': positions, 'Velocity (\u03bcm/s)': velocities}
        self.data_all = pd.DataFrame(dict_csv)  # Convert to dictionary

        # Save minimum, mean, and maximum values per frame to an excel sheet
        # Group all tracked points by frame, take mean
        by_frame_min = self.data_all.groupby('Frame').min()
        by_frame_mean = self.data_all.groupby('Frame').mean()
        by_frame_max = self.data_all.groupby('Frame').max()

        by_frame_timepoint = np.linspace(0, len(by_frame_min), len(by_frame_min)) / float(fps)

        self.data_frame = pd.DataFrame({'Time (s)': by_frame_timepoint,
                                           'Min. velocity (\u03bcm/s)': by_frame_min['Velocity (\u03bcm/s)'],
                                           'Mean velocity (\u03bcm/s)': by_frame_mean['Velocity (\u03bcm/s)'],
                                           'Max. velocity (\u03bcm/s)': by_frame_max['Velocity (\u03bcm/s)']})

        # Calculate profiles based on all events, height of channel, n bins
        # Create a profile
        bins = np.linspace(0, self.h_a, self.n_bins_a+1)
        bins_um = bins * float(umpix)  # For graphing
        digitized = np.digitize(self.data_all['Channel pos. (pix)'], bins)  # Bins
        profile = [self.data_all['Velocity (\u03bcm/s)'][digitized == i].mean() for i in range(1, len(bins))]

        # Create a profile (standard deviation)
        digitized = np.digitize(self.data_all['Channel pos. (pix)'], bins)  # Bins
        profile_stdev = [self.data_all['Velocity (\u03bcm/s)'][digitized == i].std() for i in range(1, len(bins))]

        # Save
        self.profile_data = pd.DataFrame({'Bin coordinate (\u03bcm)': bins_um[1:],
                                           'Bin mean velocity (\u03bcm/s)': profile,
                                           'Bin stdev. velocity (\u03bcm/s)': profile_stdev})

        # Graph for display
        graphs = plt.figure(figsize=(6, 4), dpi=80)
        graphs.suptitle(self.video_basename, fontweight='bold')

        plt.scatter(self.data_all['Channel pos. (pix)'] * float(umpix), self.data_all['Velocity (\u03bcm/s)'], color='lightskyblue')
        plt.plot(bins_um[1:], profile, color='dodgerblue')
        plt.xlabel('Channel position (\u03bcm)')
        plt.ylabel('Velocity (\u03bcm/s)')

        # Prepare for saving to be later referenced in graph window and in exports
        graphs.canvas.draw()
        graphimg = np.frombuffer(graphs.canvas.tostring_rgb(), dtype=np.uint8)
        self.graphimg = graphimg.reshape(graphs.canvas.get_width_height()[::-1] + (3,))

        plt.close()

        # Timecourse graph for saving
        graphs_tc = plt.figure(figsize=(6, 4), dpi=80)
        graphs_tc.suptitle(self.video_basename, fontweight='bold')

        plt.scatter(by_frame_timepoint, by_frame_min['Velocity (\u03bcm/s)'], color='springgreen', label='Min.')
        plt.scatter(by_frame_timepoint, by_frame_mean['Velocity (\u03bcm/s)'], color='dodgerblue', label='Mean')
        plt.scatter(by_frame_timepoint, by_frame_max['Velocity (\u03bcm/s)'], color='tomato', label='Max.')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (\u03bcm/s)')
        plt.legend()

        # Prepare for saving to be later referenced in graph window and in exports
        graphs_tc.canvas.draw()
        graphimg_tc = np.frombuffer(graphs_tc.canvas.tostring_rgb(), dtype=np.uint8)
        self.graphimg_tc = graphimg_tc.reshape(graphs_tc.canvas.get_width_height()[::-1] + (3,))

        plt.close()

        GraphTopLevel(self.graphimg)  # Raise graph window

        # Profile graph


    def expnum(self):
        """Export numerical (excel) data, including descriptive statistics and parameters used"""

        # Save all data to a .csv file (all values typically too large for excel)
        self.data_all.to_csv(self.video_basename + '_all_data.csv')

        writer = pd.ExcelWriter(self.video_basename + '_analysis.xlsx',
                                engine='openpyxl')
        # Write to excel

        # Frame data
        self.data_frame.to_excel(writer, sheet_name='Frame data',
                                    index=False)

        self.profile_data.to_excel(writer, sheet_name='Profile data',
                                    index=False)

        # Descriptive statistics
        dict_stats = {'n events tracked': len(self.data_all),
                u'Mean velocity (\u03bcm/s)': self.data_all['Velocity (\u03bcm/s)'].mean(),
                u'Stdev, velocity (\u03bcm/s)': self.data_all['Velocity (\u03bcm/s)'].std()
                }
        self.dict_df = pd.DataFrame(dict_stats, index=[0])
        self.dict_df.to_excel(writer, sheet_name='Descriptive statistics',
                                    index=False)

        # Parameters
        # Save parameters
        now = datetime.datetime.now()
        param_df = pd.DataFrame({u'Ratio, \u03bcm-to-pixels': self.umpix_a,
                                 'FPS': self.fps_a,
                                 'Histogram bins (n)': self.n_bins_a,
                                 'Max. corners': self.max_corners,
                                 'Quality level': self.qual_level,
                                 'Min. dist., Shi-Tomasi': self.min_dist_st,
                                 'Block size': self.block_size_a,
                                 'Window size': str(self.win_size[0]) + ", " + str(self.win_size[1]),
                                 'Pyramid level': self.max_level,
                                 'X coordinate (top)': self.x_a,
                                 'Y coordinate (top)': self.y_a,
                                 'ROI width': self.w_a,
                                 'ROI height': self.h_a,
                                 'Analysis date': now.strftime("%D"),
                                 'Analysis time': now.strftime("%H:%M:%S")}, index=[1])
        param_df.to_excel(writer, sheet_name='Parameters used', index=False)


        writer.save()
        writer.close()

        # Clear large variables after use
        self.data_frame = []
        self.data_all = []

    def expgraph(self):
        """Export graphical (.png image) data, including pairplots"""

        # Convert timecourse graph image to BGR
        array = cv2.cvtColor(self.graphimg_tc, cv2.COLOR_RGB2BGR)
        cv2.imwrite('Timecourse_graph.png', array)

        # Create profile
        array = cv2.cvtColor(self.graphimg, cv2.COLOR_RGB2BGR)
        cv2.imwrite('Profile_graph.png', array)

    def expimgs(self, expall_first, expall_linspace):
        """Export image data (.png image) with processing and labeling applied"""

        current_dir = os.getcwd()  # Select filepath

        # If user has requested first 100 images
        if expall_first is True:

            img_folder = os.path.join(current_dir, 'First 100 labeled images')
            if os.path.exists(img_folder):
                shutil.rmtree(img_folder)
            os.mkdir(img_folder)
            os.chdir(img_folder)

            for i in range(len(self.df_img_first)):
                array = (self.df_img_first['image'].iloc[i]).astype('uint8')
                cv2.imwrite(self.df_img_first['name'].iloc[i], array)

        # If user has requested every 100th image
        if expall_linspace is True:

            img_folder = os.path.join(current_dir, 'Every 100th labeled image')
            if os.path.exists(img_folder):
                shutil.rmtree(img_folder)
            os.mkdir(img_folder)
            os.chdir(img_folder)

            for j in range(len(self.df_img_linspace)):
                array = (self.df_img_linspace['image'].iloc[j]).astype('uint8')
                cv2.imwrite(self.df_img_linspace['name'].iloc[j], array)

        # Clear large variables after use
        self.df_img_first = []
        self.df_img_linspace = []

class GraphTopLevel(tk.Toplevel):
    def __init__(self, graphimg):
        super().__init__()

        # Fonts
        boldfont = font.Font(weight='bold')

        # Widgets
        self.title("Analysis results")

        self.graphimg = graphimg

        # Label
        title_label = tk.Label(self, text="Graphical results")
        title_label['font'] = boldfont
        title_label.grid(row=0, column=0, padx=10, pady=10)
        # Canvas
        self.img_canvas = tk.Canvas(self, width=480, height=320)
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
        graphimg_window = np.asarray(self.graphimg).astype('uint8')
        graphimgr_tk = ImageTk.PhotoImage(image=Image.fromarray(graphimg_window))
        self.graphimgr_tk = graphimgr_tk  # Some fix?
        self.img_canvas.create_image(0, 0, anchor='nw', image=graphimgr_tk)
