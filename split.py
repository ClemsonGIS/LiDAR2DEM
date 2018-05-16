# las_tiles.py

import os
import shutil
import arcpy
from zipfile import ZipFile

# set directory with files
workdir = ""

# toolbox path
lastoolsPath = raw_input('Enter the path to your LAStools binary folder: ')
if not lastoolsPath:
    print ("Using default...\n")
    lastoolsPath = ("C:\\arcgis\\LAStools\\bin")

#while not os.path.isdir(os.path.join(os.getcwd(), workdir)) or not workdir:
while not os.path.isdir(os.path.join(os.getcwd(), workdir)) or not workdir:
    workdir = raw_input('Enter the name of the directory where your .laz files are kept: ')

# set the directory with shapefile and laz files
workdir = os.path.join(os.getcwd(), workdir)
print(workdir)
currDir = os.getcwd()

# make a folder to store the split zip files
newpath = currDir +'\split_data' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

shapefileExist = raw_input('Does the data include a shapefile? [yes/no] ')
	
# get shapefile name
if shapefileExist == 'yes':
    shapefile = raw_input('Enter the name of the shapefile: ')
else:
    shutil.copy(currDir+"\\GenerateShapefile.py",workdir+"\\GenerateShapefile.py")
    os.chdir(workdir)
    execfile("GenerateShapefile.py")
    shapefile = "test.shp"
    os.chdir(currDir)  

# make shapefile into full path
shapefile = os.path.join(workdir, shapefile)

# generate Neighbors table
if not os.path.isfile(os.path.join(workdir, "neighborTable.dbf")):
    arcpy.PolygonNeighbors_analysis (shapefile, os.path.join(workdir, "neighborTable.dbf"), ["FID", "Name"], "AREA_OVERLAP", "BOTH_SIDES", "1 FOOT", "", "")


with arcpy.da.SearchCursor(os.path.join(workdir, "neighborTable.dbf"), ['src_FID', 'nbr_Name', 'src_Name']) as cursor:
    for row in cursor:
        fid = str(row[0])
        zip_name = ZipFile(newpath + '\\tile_' + fid + ".zip", 'a',allowZip64=True)
        # put the neighbor laz file in the zipfile
        zip_name.write(os.path.join(workdir, row[1]),row[1])
        zip_name.close()
del cursor

# for each polygon in original shapefile
with arcpy.da.SearchCursor(shapefile, ['FID','Name']) as cursor:
    for row in cursor:
        fid = str(row[0])
        zip_name = ZipFile(newpath + '\\tile_' + fid + ".zip", 'a',allowZip64=True)
        #put center laz file in the zipfile
        zip_name.write(os.path.join(workdir, row[1]),"center_"+row[1])
        zip_name.close()
del cursor
