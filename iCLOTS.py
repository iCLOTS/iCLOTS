"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2022-09-06 for version 1.0b1

"""
from menu import mainmenu
# import os
# import sys

class iCLOTS():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainmenu()

    # def resource_path(self, relative_path):
    #     """ Get absolute path to resource, needed to display logo in .app"""
    #     try:
    #         # PyInstaller creates a temp folder and stores path in _MEIPASS
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #
    #     return os.path.join(base_path, relative_path)


