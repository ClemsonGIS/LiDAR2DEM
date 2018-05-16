import os
import arcpy
from shutil import move
from glob import glob
from zipfile import ZipFile

# set our workspace to the current working directory
arcpy.env.workspace = os.getcwd()
currDir = os.getcwd()

# get the county name
countyName = raw_input("Enter name for area of interest: ")
outDir = raw_input("Enter directory for final rasters: ")

# use the same projection we used in the processing script
projfile = arcpy.SpatialReference(26917)

# make a folder to store the processed zip files
processedData = os.getcwd() +'\processed_data' 
if not os.path.exists(processedData):
    os.makedirs(processedData)
mosaicDataSource = os.getcwd() +'\mosaic_data_source' 
if not os.path.exists(mosaicDataSource):
    os.makedirs(mosaicDataSource)
zips = glob("*.zip")
for z in zips:
    ZipFile(z).extractall()
    move(z, ".\processed_data")

unzipped = glob("DTM*") + glob("DSM*") + glob("intensity*")
for tiles in unzipped:
    move(tiles, ".\mosaic_data_source")

# create names for the new mosaic datasets
DTM = countyName + "_DTM"
DSM = countyName + "_DSM"
intensity = countyName + "_intensity"

# create a geodatabase to store the mosaic datasets
arcpy.CreateFileGDB_management(os.getcwd(), countyName)

# create a mosaic dataset for the DTM and the DSM
arcpy.CreateMosaicDataset_management(os.path.abspath(countyName + ".gdb"), DTM, projfile)
arcpy.CreateMosaicDataset_management(os.path.abspath(countyName + ".gdb"), DSM, projfile)
arcpy.CreateMosaicDataset_management(os.path.abspath(countyName + ".gdb"), intensity, projfile)


DTMList = []
DSMList = []
intensityList = []

# make 3 lists containing the path of all DTM tif files, all DSM tif files, and all intensity raster files
os.chdir(mosaicDataSource)
for tif in glob("DTM_" + countyName + "*.tif"):
    #print ("Found DTM: "+tif)
    DTMList.append(os.path.abspath(tif))
for tif in glob("DSM_" + countyName + "*.tif"):
    #print ("Found DSM: "+tif)
    DSMList.append(os.path.abspath(tif))
for tif in glob("intensity_" + countyName + "*.tif"):
    #print ("Found intensity: "+tif)
    intensityList.append(os.path.abspath(tif))
os.chdir(currDir)

DTMInputs = ";".join(DTMList[0:])
DSMInputs = ";".join(DSMList[0:])
intensityInputs = ";".join(intensityList[0:])

# add all the .tif rasters to the mosaic dataset
arcpy.AddRastersToMosaicDataset_management(os.path.abspath(countyName + ".gdb") + "\\" + DTM, "Raster Dataset", DTMInputs)
arcpy.AddRastersToMosaicDataset_management(os.path.abspath(countyName + ".gdb") + "\\" + DSM, "Raster Dataset", DSMInputs)
arcpy.AddRastersToMosaicDataset_management(os.path.abspath(countyName + ".gdb") + "\\" + intensity, "Raster Dataset", intensityInputs)

# copy the raster dataset to one large tif file to obtain one final raster
arcpy.CopyRaster_management(os.path.abspath(countyName + ".gdb") + "\\" + DTM, outDir + countyName + "_DTM.tif")
arcpy.CopyRaster_management(os.path.abspath(countyName + ".gdb") + "\\" + DSM, outDir + countyName + "_DSM.tif")
arcpy.CopyRaster_management(os.path.abspath(countyName + ".gdb") + "\\" + intensity, outDir + countyName + "_intensity.tif")

# delete the old DTM and DSM pieces
'''
for f in glob("DTM*") + glob("DSM*") + glob("intensity*"):
    os.unlink(f)
'''
