# iCLOTS_software
iCLOTS software source code

Standalone software v0.1.0 is available now at https://www.iCLOTS.org/software
We are in the processing of submitting a manuscript describing iCLOTS for peer review, look out for a publication soon! In the meantime...


iCLOTS is a free software created for the analysis of common life sciences, e.g. hematology, and/or microfluidic workflow image data. 

### Basis for software

 - The Lam lab and associated collaborators have identified a need for easy-to-use software-based tools to analyze the information-rich imaging data obtained with ever-improving novel in vitro microscopy-based assays, including microfluidic assays.
 - Computational methods capable of processing/interpreting large amounts of imaging data efficiently represent a solution. However, application requires a level of computational expertise impractical for most researchers. 
 - We present a user-adaptable toolkit packaged into the open-source, standalone Interactive Cellular assay Labeled Observation and Tracking Software (iCLOTS).
 - iCLOTS has been designed to bring advanced image processing and data science approaches to all researchers and clinicians, regardless of computational experience.

### Software availibility and source code
 - iCLOTS source code is available here. For users with computational expertise, standalone methods are also available at github.com/LamLabEmory. 
 - All code is licensed under the Apache License 2.0, a standard open-source license. 
 - This repository also includes a code of conduct and contributing information, files standard to open-source projects.
 - Standalone software is available at iCLOTS.org/software. As iCLOTS continues to grow, all versions of iCLOTS will be maintained here.

### Software installation guide
 - An iCLOTS .app file has been developed on Mac OS Monterrey version 12.5.1, but has been tested on other Mac OS, including Catalina. 
 - iCLOTS .exe file has been developed on Windows version 11, but has been tested on other Windows versions, including Windows version 10.
 - iCLOTS is written in Python 3.7 and packaged natively using the open-source library Pyinstaller version 5.6.2. 
 - iCLOTS has been designed as a standalone software to reach the widest range of users possible and for potential use in clinical environments. As such, no supporting software or software dependencies are required. No additional resources are needed to run the program.

 - iCLOTS is installed simply by downloading the appropriate files. On Mac OS, users click the tar.gz distribution file to open, then click the .app file to start the software. On windows, users can click on the .exe file directly.

 - The iCLOTS software is approximately ~150 MB, so may take 1-10 minutes to download, depending on internet speed. iCLOTS will take a 1-5 minutes to open, particularly for first time use. On Mac OS, when opening, the icon will appear and "bounce" in the dock, disappear, and reappear when the software has loaded. 

 - The development team has taken the necessary steps to identify ourselves as legitimate developers to Mac and Windows OS. Upon opening for the first time, you may receive some messages:
 -On Mac OS, you may be alerted that this is a software downloaded from the internet. This is common to most open-source projects, including other bioimage analysis software like Ilastik and CellProfiler. You may also be alerted that we are a new team of developers, and asked if you trust the source of this software. The source of the software is attributed to Meredith Fay, manuscript first author and iCLOTS lead developer. 
 - On Windows OS, you may be alerted that this is a new piece of software. There is an option to click "continue" or "advanced" and open the software from the message window. The source of the software may also be attributed to Meredith Fay. 
 - During testing, all software users received and accepted these messages, with no negative effect to their computers.
 - Over time, as more users download and use iCLOTS, we will build a positive reputation with Apple and Windows, and messages alerting users to the source of the software will no longer be present.

### Data availibility
 - A limited set of test data for every application is available at github.com/LamLabEmory and at iCLOTS.org/software (located under software files).  -   - This set of test data is designed to demonstrate software capabilities using real-world data. Use with your own data is also encouraged.
 - All data used within this manuscript is also available without restriction upon request to corresponding author Wilbur Lam, MD, PhD (email: wilbur.lam@emory.edu).
 - Detailed experimental protocols and microfluidic device mask files are also available upon request.

### General software use
 - iCLOTS is a large piece of software with many applications. A "Tutorial" button on each application and in the main window provides help with use, including: algorithms adapted for use with cells and cell suspensions, inputs, parameters to edit, outputs, experimental suggestions, computational suggestions, and how to contact the development team should a user encounter an error. All tutorial information is also available at iCLOTS.org/documentation.

 - iCLOTS is interactive: as users change parameter values, results are updated in real-time in the analysis window. As such, in particularly large files, changes in parameters may take a few seconds. Parameters can also be edited by typing in a value and clicking up or down to signal changes should take affect.

### Reporting software errors and bugs
 - iCLOTS version 0.1.0 is presented as a large scale test of a software designed for feedback from a wide group. While we have extensively tested iCLOTS on several machines, as with any software, operational errors ("bugs") may still be present. 
 - Users can contact us for prompt resolution by (1) filling out the contact form at iCLOTS.org/contact, (2) emailing the development team directly at lamlabcomputational@gmail.com, or (3) raising an issue in GitHub, which is particularly useful for users with computational experience. 
 - This process is shared in the tutorials, the manuscript supplement, on the website, and on our GitHub accounts. The development team is dedicated to resolving any issues promptly.

### iCLOTS applications available
 - iCLOTS is comprised of four categories of image processing applications, a machine learning application, and a suite of video editing tools to help users format data properly.
 - Image processing capabilities are divided into four main categories: (1) adhesion, (2) single cell tracking, (3) multi-scale microfluidic accumulation, and (4) velocity time course/profile analysis.
 - iCLOTS-generated Excel files (or any files following formatting guides) may be used in iCLOTS' machine learning clustering algorithms. iCLOTS implements Kmeans algorithms to detect and mathematically characterize natural groupings and patterns within clinical data sets.

 - iCLOTS does require specific data formats, e.g. image, image series, or video, depending on application. Users may want to shorten, rotate, crop, or normalize images for most ideal use. A series of video processing tools assists users in preparing their data for successful analysis.

 - Each application takes approximately 30 seconds-3 minutes to run on a "normal" computer on the test data provided. Larger files will take additional time.

### Quality of results
 - As with all computational analysis, quality of results depends on quality of data. In microfluidic data in particular, debris or small defects in the channel can affect results.
 - For results describing individual cells, iCLOTS has been designed to label every cell with an index so that users can check numerical data against imaging data to ensure quality.  Users may find that correcting computationally produced results is less time-consuming than manual analysis. 
 - Not all cells will be counted due to measures designed to ensure high-quality data points.
 - In some tracking applications where cells are located as Gaussian distributions of pixel intensity, cells with a heterogenous appearance (such as white blood cells) may be difficult to detect. Area measurements may be based on a small portion of the cell.
 - For these and related reasons, the "tutorial" button located in each application provides application-specific tips and tricks are included to help users troubleshoot poor analysis. 

### Contacting the iCLOTS development team
 - iCLOTS is under continuous development. We feel that while microscopy and microfluidic technologies have significantly advanced over the last several decades, there has not been concurrent development of widely-accessible techniques to analyze the resultant data, resulting in lost resolution and missed opportunities for innovative metrics. Over time, we hope that using feedback from researchers, clinicians, and other developers, our software will continue to grow in order to benefit the widest range of users. We have shared contact information in the manuscript, supplement, on our GitHub accounts, within the software, and on our website. All requests for troubleshooting, new application ideas, and general comments, suggestions, and concerns are welcome.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
