import PyInstaller.__main__

PyInstaller.__main__.run([
    'iCLOTS.py',  # Script you're starting from, should call other scripts
    '--onefile',  # One piece of software
    '--windowed',  # Indicates there are several windows, you might not need this

    '--icon=/Users/meredithfay/Documents/PycharmProjects/iCLOTS_softwareonly/iCLOTS.ico'  # Add .ico file - not working?
])