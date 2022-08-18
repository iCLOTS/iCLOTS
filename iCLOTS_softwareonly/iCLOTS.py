"""iCLOTS is a free software created for the analysis of common hematology workflow image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-06 for version 1.0b1

"""
from menu import mainmenu

class iCLOTS():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainmenu()