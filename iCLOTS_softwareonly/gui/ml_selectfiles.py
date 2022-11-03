"""iCLOTS is a free software created for the analysis of common hematology and/or microfluidic workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-10-26 for version 1.0b1

Portion of machine learning application, window to assist user in selecting files for analysis

"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from tkinter import filedialog
import os
import glob
import pandas as pd
import openpyxl
from help import mlhelp as hp
from accessoryfn import error
from gui import ml_selectfeatures as sf
import datetime

class SelectExcel(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # App details, subject to change
        name = 'iCLOTS'

        # Fonts
        boldfont = font.Font(weight="bold")
        smallfont = font.Font(size=8)

        self.df = []
        self.dirname = []

        # Widgets
        self.title(name + " machine learning")

        # Application title
        menutitle = tk.Label(self, text="Select Excel file(s) for machine learning")
        menutitle["font"] = boldfont
        menutitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Instructions label
        instructionslabel = tk.Label(self, text="Please select a single file folder including all datasets.\n"
                                                "Each data set should be represented by a single Excel file.\n"
                                                "Avoid spaces or punctuation in Excel sheet names.\n"
                                                "Each Excel file should contain one sheet only.\nEach line of the sheet should "
                                                "describe one data point with multiple metrics.")
        instructionslabel.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Input folder of files button
        folder_button = tk.Button(self, text="Select folder of Excel file(s)", command=self.choose_folder)
        folder_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Help button
        help_button = tk.Button(self, text="Tutorial", command=self.help)
        help_button.grid(row=3, column=0, padx=5, pady=5)

        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=3, column=1, padx=5, pady=5)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Tkinter protocol for x close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Choose single video, convert to avi
    def choose_folder(self):
        """Convert a list of excel files representing separate datasets into one big dataframe for further analysis."""

        inputdirectory = filedialog.askdirectory()  # Select directory

        filelist = glob.glob(inputdirectory + "/*.xlsx")

        # Create results file, change to directory directory
        now = datetime.datetime.now()
        output_folder = os.path.join(inputdirectory, 'Results, ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
        os.mkdir(output_folder)
        os.chdir(output_folder)

        if len(filelist) >= 1:

            self.df = pd.DataFrame()  # Initial holder
            self.dirname = os.path.basename(inputdirectory)

            # Combine data from all sheets into a single dataframe
            for filename in filelist:

                trigger_error = False  # Keep next window from opening if too many sheets included
                # Check number of sheet names
                xl = openpyxl.load_workbook(filename)
                if len(xl.sheetnames) != 1:
                    error.ErrorWindow(message='Too many or two few sheets included in:\n' + filename)
                    trigger_error = True
                else:
                    # Read excel
                    sheet = pd.read_excel(filename, engine='openpyxl')

                    samplename = os.path.basename(filename).split('.')[0]  # Sample name: name of excel sheet (remove .xlsx)
                    sheet['Sample'] = samplename  # Add as column
                    self.df = self.df.append(sheet, ignore_index=True)

            if trigger_error is False:
                # Call next window: correlation matrix/variable selection
                # print(output_folder)
                # sf.SelectFeatures(self.df, self.dirname, output_folder)  # Raise graph window
                sf.SelectFeatures(self.df, self.dirname)

        else:
            error.ErrorWindow(message='No excel sheets included')

    # Open help window
    def help(self):
        """All applications have a button to reference help documentation"""

        # Display specified help file
        hp.HelpDisplay()

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # Clear variables
            xl = None
            sheet = None
            filelist = None

