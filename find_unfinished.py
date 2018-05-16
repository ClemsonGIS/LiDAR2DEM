# find_unfinished.py
# This script will identify unfinished tiles and move the appropriate .zip (containing all LAZ files) to the proper directory.

import os
from glob import glob
import shutil

currDir = os.getcwd()
countyName = "Saluda"
lazFolder = "Saluda_County_2010"
lasDirectory = os.path.join(currDir, lazFolder)

#sourceDir = os.path.join(currDir, "split_backup\\")
#targetDir = os.path.join(currDir, "split_data\\")

#directory that contains all tiles w/ corresponding ID's as numbers appearing at the end of the file name ex: Tile_0
allTileDir = os.path.join(currDir, "split_data\\")
backUpDir = os.path.join(currDir, "split_backup\\")
if not os.path.exists(backUpDir):
    print ("No directory found, creating new directory...")
    os.mkdir(backUpDir)

# Find all complete DSMs,DTMs, and intensity rasters backed-up tile ZIPs and add to lists
returnedDsmList = [ tile for tile in glob("DSM" + "*.zip") ]
returnedDtmList = [ tile for tile in glob("DTM" + "*.zip") ]
returnedIntensityList = [ tile for tile in glob("intensity" + "*.zip") ]

returnedDsmIDs = []
for dsm in returnedDsmList:
    ID = filter(str.isdigit, dsm)
    returnedDsmIDs.append(ID)

returnedDtmIDs = []
for dtm in returnedDtmList:
    ID = filter(str.isdigit, dtm)
    returnedDtmIDs.append(ID)

returnedIntensityIDs = []
for intensity in returnedIntensityList:
    ID = filter(str.isdigit, intensity)
    returnedIntensityIDs.append(ID)

returnedIDs = []
for ID in returnedDsmIDs:
    if ID in returnedDtmIDs and ID in returnedIntensityIDs:
        returnedIDs.append(ID)

for tile in returnedIDs:
            old_file = os.path.join(allTileDir + "tile_" + tile + ".zip")
            new_file = os.path.join(backUpDir + "tile_" + tile + ".zip")
            if(os.path.exists(old_file)):
                print("Moving " + allTileDir + "tile_" + tile + ".zip", backUpDir + "tile_" + tile + ".zip")
                os.rename(old_file, new_file)
            #shutil.copy(old_file,new_file)

