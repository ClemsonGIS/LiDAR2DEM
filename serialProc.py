#Script to loop and serially process LiDAR data in the event that it continually fails over Condor.

import os
import shutil
import subprocess
from glob import glob

# Set inputs to the process_laz_files_buff.py script
countyName = "gvl"
bufferSize = "200"

# Set paths
currDir = os.getcwd()
zipDir = os.path.join(currDir, "zip\\")
outputDir = os.path.join(currDir, "output\\")
pythonPath = "C:\Python27\ArcGIS10.5\python.exe"
if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
procArray = []

# Loop through all files
os.chdir(zipDir)
for zip in glob("*.zip"):
    prefix = zip + ".tmp"
    print("Starting processing on " + zip + "\n")
    procDir = os.path.join(currDir, prefix)
    if os.path.isdir(procDir):
        print("Removing prior processing\n")
        shutil.rmtree(procDir)
    os.mkdir(procDir)
    print("copying file " + zip + " to processing directory\n")
    shutil.copy(zip, procDir)
    shutil.copy(currDir+"\\process_laz_files_buff.py",procDir+"\\process_laz_files_buff.py")
    print("Starting processing script\n")
    os.chdir(procDir)
    subprocess.call([pythonPath,procDir + "\\process_laz_files_buff.py",countyName,bufferSize])
    for f in glob(procDir + "\\*.zip"):
        print("moving completed file to output directory: " + f +"\n")
        shutil.move(f,outputDir)
    print("Cleaning up\n")
    print("Finished processing " + zip + "\n")
    os.chdir(zipDir)
    shutil.rmtree(procDir)

print("Cleaning up all temporary directories\n")
for dir in glob(currDir + "\\*.zip*"):
    shutil.rmtree(dir)
print("Successful completion\n")
