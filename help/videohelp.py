"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-03 for version 1.0b1

Video editing menu window display shows help data for all video editing applications

"""

import tkinter as tk
import tkinter.scrolledtext as st


class HelpDisplay(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Widgets
        self.title(name + " help")

        # Widgets
        namelabel = tk.Label(self, text="Using video editing tools")
        namelabel.grid(row=0, column=0, pady=10, padx=10)

        # Text box
        self.helptext = st.ScrolledText(self,
                                        width=100,
                                        height=20,
                                        font=("Arial",
                                              10))
        self.helptext.grid(row=1, column=0, pady=10, padx=10)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=2, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Inserting Text which is read only

        # Making the text read only
        self.helptext.insert(tk.INSERT, u"""\
        iCLOTS provides a suite of video and image file editing tools to help users format their data for iCLOTS analysis. 
        Briefly, users select a single file or a folder of .png, .jpg, .tif, and/or .avi files for modification. 
        Users may need to perform some operation or edit indicated parameters, 
        some image processing step is applied, and all edited files are returned in a new directory within the original folder. 

       Resize file(s)
        --This application resizes image(s) or video(s) using a resize factor, 
        ---a constant that a frame's dimensions are multiplied by during the resize process.
        ----For input parameter resize factor, <1 indicates reducing resolution, 
        ----->1 indicates "increasing" resolution.
        --Decreasing resolution can help speed computational analysis of large files.
        ----In applications quantifying movement of cells, sometimes lower resolution is sufficient. 
        ----In applications quantifying changes in morphology or size, maintain the highest resolution possible.
        --Artificially increasing resolution in post-processing oftentimes isn't useful. 
        ----It is not possible to add information that the microscopy did not provide. 
        ----In may lead to bias in morphological results by increasing changes in dimension.
        
        Rotate file(s)
        --This application rotates image(s) or video(s) using a specified angle input parameter. 
        ----All files are rotated to the same degree. 
        ----Angle value units are degrees. 
        ------An angle value >0 rotates the file counterclockwise and an angle value <0 rotates clockwise. 
        --This application is specially designed to maintain the original aspect ratio of the file 
        ---such that the same µm-to-pixel ratio can be used during analysis.
        --Rotating videos or images such that microfluidic channels are horizontal is crucial 
        ---for applications that rely on left-right indexing, such as microchannel occlusion 
        ---or velocity profiles. 
        ----It is suggested for one-directional movement quantification, such as the specialized deformability application.
        --Rotating images has no affect on morphology measurements.
        
        Edit the contrast of files
        --This application edits the contrast of file(s) using a two point process: 
        ----Multiplication followed by addition with a constant.
        --Input variables include:
        ----alpha, the constant each pixel's intensity value is multiplied by.
        ----beta, the constant added (or subtracted) from each pixel's intensity value.
        --Alpha is oftentimes called gain, and should be >1. 
        ----This value controls contrast. 
        ----High values of alpha cause the relatively bright pixels to become even brighter. 
        ----Any value of alpha leaves black pixels as black (value 0).
        --Beta is oftentimes called bias. 
        ----<0 decreases the overall brightness of the file.
        ---->0 increases the overall brightness of the image.
        --Editing contrast can be useful in applications detecting movement. 
        ----Features of interest, like a cell, and more easily distinguished from background, like channels.
        --Take care in interpreting pixel intensity values after editing contrast.
        ----It may lead to bias in fluorescence-based results.
        ----It can be hard to detect a strong signal from fluorescently stained but moving cells.
        ------If you adjust contrast of those videos to better detect cells, return original fl. int. values by:
        --------Fl. int = (Fl. int - beta)/alpha
        
        Choose a region of interest (ROI)
        --This application is designed to crop file(s) to a region of interest. 
        --After file(s) upload, a window displaying the file will appear, and a draggable rectangle 
        ---allows the user to select an area they are interested in analyzing further.
        --In assays using microfluidics, small defects in microfluidic walls are often detected as cells 
        ---or patterns of cells. The iCLOTS team suggests cropping all data taken using microfluidic systems 
        ---to the channel area only.
        --This application allows user to select a custom ROI for each file.
        ---If you are interested in cropping a series of images to a specific ROI, convert to video, crop,
        ----then convert back to images for version 1.0b1. Additional functionality coming in later iCLOTS versions.

        Crop a video to a specified frame range
        --This application is designed to shorten a video to a specifed start:finish frame range.
        --Input variables include the start frame number and the end frame number. 
        ----If multiple files are selected, all will be cropped to the same range.
        --This script is most useful for removing portions of a video clearly affected by changes 
        ---in microscopy acquisition settings such as changes in illumination or laser power, 
        ---or for shortening videos to reduce computational analysis time.
        --To start and end at roughly a given time, multiply that time (in seconds) 
        ---by the frames per second (FPS) imaging rate, a microscope acquisition setting you should be able to reference.

        Convert an image sequence to a video
        --May be useful depending on the timecourse outputs of your microscopy software. 
        --Single cell tracking, specialized deformability, and velocity applications require an .avi video input.
        --One single video is made from all images within the selected file folder.
        ----All images must have the same dimensions.
        ----Images must be named in the proper alphabetical/numerical order.
        ----If image names contain numbers, use preceding zeros to order properly.
        ------i.e. 01, 02, ... 10 vs. 1, 2, ... 10
        --The video uses the file folder name as a filename - please avoid spaces or punctuation within this name.
        --Inputs include a frames per second rate, the rate at which you would like your created video to play. 
        ----This parameter does not affect later analysis. 
        --If your completed video will not play, check that all image frames were the same dimension.

        Convert a video to an image sequence
        --Application converts a single video to a sequence of images. 
        --This script is useful for .avi files that must be presented to iCLOTS as a time series, 
        ---like the accumulation/occlusion applications. 
        --Images are returned named with the video name plus a frame number.
        --Up to five preceding zeros are used to number the frames sequentially. 
        ----This will not work on files >99,999 frames, 
        -----but iCLOTS cannot realistically handle that many images anyways.
        --Images are saved as .png files to avoid unnecessary compression.
        
        Normalize range of pixel intensity values
        --All images are scaled such that the lowest pixel value is 0 (black) and the highest pixel value is 255 (white). 
        ----This can be useful for standardizing images taken during different experiments, etc.
        --This application is for use with image files only. 
        ----If you need to normalize frames from a video, you could split into images, normalize, and combine again.
        ----All channels (red, green, blue) are normalized to the same range. 
        ----Later iterations of iCLOTS will include options for normalizing all frames of a video file 
        -----and for normalizing certain color channels only.
        --Use caution normalizing images to the same range. 
        ----Normalizing can remove bias that comes from different laser power, gain, etc. settings, 
        -----but can also introduce bias. 
        ----It's almost always ideal to compare images taken during the same experiment. 
        --Ideally the initial image pixel values are within a (0, 254) range. 
        ----"Maxed out" pixel values (255, the highest possible value) cause loss of information. 
        ------A range of intensities may have existed beyond the 255 value.
        --This application uses the following method of normalization:
        ----new value = (original layer) - minimum value of the layer / 
        -----(maximum value of the layer - minimum value of the layer) * 255

        iCLOTS is under continuous development:
        --Feel free to contact the authors:
        ----Using the form at iCLOTS.org/contact
        ----By emailing lamlabcomputational@gmail.com
        ------If your question is about use with a particular set of data, please attach a sample file
        ------Data will not be shared outside of the iCLOTS development team
        --For those users who also code, please feel free to submit a pull request:
        ----github.com/iCLOTS
        ----You can also find analysis methods-only at github.com/LamLabEmory
        --Issues with software, requests for help troubleshooting, new application ideas, and general comments, suggestions, 
        ---and concerns are all welcome
        --The authors hope this will become a field-wide effort to improve quantitative data analysis precision 
        for common cell microscopy-based assays, particularly microfluidic assays

        Thanks for being an iCLOTS user!"""
                             )

        self.helptext.configure(state='disabled')