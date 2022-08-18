"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-12-02 for version 1.0b1

Crop app allows user to select a region of interest (ROI) to save:

Inputs:
--A single image (.png, .jpg, .tif) file or a single video file (.avi)

Parameters chosen by user:
--ROI, via draggable rectangle

Outputs:
--Chosen file, cropped to ROI, saved with original file name appended with 'cropped' for reference

Notes:
--In a video, ROI is chosen from the last frame
--Application does not currently support selecting the same ROI for multiple files
----In situations where this is appropriate, a cropping function has been built into the analysis GUI
--OpenCV library, the library that allows the user to select an ROI, does not resize files to fit on the screen
----If the file is too large, and you can sacrifice some resolution, first use the iCLOTS resize application

"""

# import tkinter as tk
# import tkinter.font as font
# import os
# import shutil
# import cv2
# import numpy as np
# from accessoryfn import chooseinput, error, complete
#
# class CropROIGUI(tk.Toplevel):
#
#     def __init__(self):
#         super().__init__()
#
#         # App details, subject to change
#         name = 'iCLOTS'
#
#         # Fonts
#         boldfont = font.Font(weight="bold")
#
#         # Tkinter variables
#         self.filelist = None
#
#         # Widgets
#         self.title(name + " select ROI application")
#
#         # Application title
#         menutitle = tk.Label(self, text="File cropping to ROI application")
#         menutitle["font"] = boldfont
#         menutitle.grid(row=0, column=0, padx=10, pady=10)
#
#         # Input single image button
#         single_button = tk.Button(self, text="Select single file and choose ROI", command=self.singlefile)
#         single_button.grid(row=1, column=0, padx=5, pady=5)
#         # Quit button
#         quit_button = tk.Button(self, text="Quit", command=self.destroy)
#         quit_button.grid(row=2, column=0, padx=5, pady=5)
#
#         self.rowconfigure(0, weight=1)
#         self.rowconfigure(1, weight=1)
#         self.rowconfigure(2, weight=1)
#         self.columnconfigure(0, weight=1)
#
#     # Choose ROI for cropping
#     def croptoROI(self, frame):
#         region = cv2.selectROI("Image", frame, fromCenter=True)  # Choose ROI function from cv2 - opens a window to choose
#         ROI_x = int(region[0])  # Take result of selectROI and put into a variable
#         ROI_y = int(region[1])  # " "
#         ROI_w = int(region[2])  # " "
#         ROI_h = int(region[3])  # " "
#
#         return ROI_x, ROI_y, ROI_w, ROI_h
#
#
#     # Choose single image, return one-element list
#     def singlefile(self):
#         filename_selected = chooseinput.anyfile()
#         filename = os.path.basename(filename_selected).split(".")[0]
#
#         newfilename = filename + "_cropped" + os.path.basename(filename).split(".")[1]
#
#         if os.path.basename(filename).split(".")[1] == "avi":  # If video
#             cap = cv2.VideoCapture(filename)
#             w = int(cap.get(3)  # float
#             h = int(cap.get(4))  # float
#             fps = cap.get(cv2.CAP_PROP_FPS)
#
#             # Video writer output
#             fourcc = cv2.VideoWriter_fourcc(*"XVID")
#             out = cv2.VideoWriter(newfilename, fourcc, fps, (w, h))
#
#             # Choose ROI from last frame
#             last_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#             ROI_x, ROI_y, ROI_w, ROI_h = self.croptoROI(last_frame)
#
#             while True:
#                 ret, frame = cap.read()
#                 if ret == True:
#                     b = frame[ROI_y: (ROI_y + ROI_h), ROI_x: (ROI_x + ROI_w)]
#                     out.write(b)
#                 else:
#                     break
#
#             cap.release()
#             out.release()
#             cv2.destroyAllWindows()
#
#         elif os.path.basename(filename).split(".")[1] in ["png", "jpg", "tif"]:
#             read = cv2.imread(filename)
#             ROI_x, ROI_y, ROI_w, ROI_h = self.croptoROI(read)
#             croppedimg = read[ROI_y: (ROI_y + ROI_h), ROI_x: (ROI_x + ROI_w)]
#             cv2.imwrite(newfilename, croppedimg)
#     complete.DoneWindow()