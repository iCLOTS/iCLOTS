"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-12-02 for version 1.0b1

Series of functions that handles creating a list of file(s)

"""

import tkinter as tk
from tkinter import filedialog
import glob
import os


def singleimgfile():
    """Return a list of a single image file (.png, .jpg, .tif)"""
    filename = filedialog.askopenfilename(
        filetypes=[(".png", "*.png"), (".jpg", "*.jpg"), (".tif", "*.tif")])

    # Change directory
    os.chdir(os.path.dirname(filename))

    return filename

def dirimgfile():
    """Return a sorted list of all image files (.png, .jpg, .tif) in a directory"""
    inputdirectory = filedialog.askdirectory()  # Select directory

    filelist_png = sorted(glob.glob(inputdirectory + "/*.png"))
    filelist_jpg = sorted(glob.glob(inputdirectory + "/*.jpg"))
    filelist_tif = sorted(glob.glob(inputdirectory + "/*.tif"))
    filelist = filelist_png + filelist_jpg + filelist_tif

    dirname = os.path.dirname(filelist[0])

    # Change directory
    os.chdir(inputdirectory)

    return dirname, filelist

def videofile():
    """Return a single video file (.avi)"""
    filename = filedialog.askopenfilename(
        filetypes=[(".avi", "*.avi")])

    # Change directory
    os.chdir(os.path.dirname(filename))

    return filename

def dirvideofile():
    """Return a directory of video files (.avi)"""
    inputdirectory = filedialog.askdirectory()  # Select directory

    filelist = glob.glob(inputdirectory + "/*.avi")

    dirname = os.path.dirname(filelist[0])

    # Change directory
    os.chdir(inputdirectory)

    return dirname, filelist

def anyfile():
    """Return a single file of any file type that iCLOTS accepts"""
    filename = filedialog.askopenfilename(
        filetypes=[(".png", "*.png"), (".jpg", "*.jpg"), (".tif", "*.tif"), (".avi", "*.avi")])

    # Change directory
    os.chdir(os.path.basename(filename))

    return filename  # Output


def diranyfile():
    """Return a directory of any file type that iCLOTS accepts"""
    inputdirectory = filedialog.askdirectory()  # Select directory

    filelist_png = glob.glob(inputdirectory + "/*.png")
    filelist_jpg = glob.glob(inputdirectory + "/*.jpg")
    filelist_tif = glob.glob(inputdirectory + "/*.tif")
    filelist_avi = glob.glob(inputdirectory + "/*.avi")
    filelist = filelist_png + filelist_jpg + filelist_tif + filelist_avi

    dirname = os.path.dirname(filelist[0])

    # Change directory
    os.chdir(inputdirectory)

    return dirname, filelist