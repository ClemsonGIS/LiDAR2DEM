#process_laz_files.py
 
import os
import subprocess
import arcpy
from glob import glob
#from split import lastoolsPath
 
ext = "*.laz"

currDir = os.getcwd()

shapeCursor = "test.shp"

arcpy.CreateFeatureclass_management(currDir, shapeCursor, "POLYGON", "", "DISABLED", "DISABLED")

arcpy.AddField_management(shapeCursor,"Name","TEXT")

# set paths to LAStools
#lastoolsPath = "C:\\arcgis\\LAStools\\bin"

cursor = arcpy.da.InsertCursor(shapeCursor,["Name","SHAPE@"])

# set up paths
lasinfo = os.path.join(lastoolsPath, "lasinfo")
# set up the commands for LAStools
lasInfoCommand = lasinfo + " " + ext + " -otxt -cores 12 -odix _info -nmm"
lasInfoCommandList = lasInfoCommand.split()
        
# Run all the tools
proc = subprocess.Popen(lasInfoCommandList, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
proc.communicate()

gotProj = False
proj = ""
###
for f in glob("*_info.txt"):
        maxFound, minFound = False, False
        x1,y1,z1,x2,y2,z2 = 0,0,0,0,0,0
        if not gotProj:
                ### Prompt user for EPSG code of the LAZ files. 
                epsgKnown = raw_input('Do you know the EPSG code for the projection of your LAZ files? [yes/no] ')
                if epsgKnown == 'yes':
                        epsg = raw_input('Type the EPSG code: ')
                        print ("Using EPSG Code "+ epsg +". ")
                        gotProj = True
                        spatial_ref = arcpy.SpatialReference(int(epsg))
                        arcpy.DefineProjection_management(shapeCursor,spatial_ref)
                else:
                        print("Scanning for prjection key within the info files......")
        if not gotProj:
                infoFile = open(f,"r")
                for line in infoFile:
                        if "ProjectedCSTypeGeoKey" in line:
                                proj = line.split()[7]
                                if proj < 32767 and proj > 0:
                                        print ("ProjectedCSTypeGeoKey: "+ proj +" found!")
                                        spatial_ref = arcpy.SpatialReference(int(proj))
                                        arcpy.DefineProjection_management(shapeCursor,spatial_ref)
                                        gotProj = True
                                else:
                                        print("ProjectedCSTypeGeoKey: " + proj + " not valid.")
                infoFile.close()
        if not gotProj:
                infoFile = open(f,"r")
                for line in infoFile:
                        if "GeographicTypeGeoKey" in line:
                                proj = line.split()[7]
                                print ("GeographicTypeGeoKey: "+ proj +" found!")
                                spatial_ref = arcpy.SpatialReference(int(proj))
                                arcpy.DefineProjection_management(shapeCursor,spatial_ref)
                                gotProj = True
                infoFile.close()
        if not gotProj:
                print("Projection not found. Exiting......")
                sys.exit()
        infoFile = open(f,"r")
        for line in infoFile:
                if "max" in line:
                        x1,y1,z1 = line[30:-1].split()
                        maxFound = True
                        print x1,y1,z1
                elif "min" in line and "minor" not in line:
                        x2,y2,z2 = line[30:-1].split()
                        minFound = True
                        print x2,y2,z2
                if maxFound and minFound:
                        array = arcpy.Array([arcpy.Point(x1,y2),
                                             arcpy.Point(x1,y1),
                                             arcpy.Point(x2,y1),
                                             arcpy.Point(x2,y2)])
                        polygon = arcpy.Polygon(array)
                        cursor.insertRow([f[:-9]+".laz",polygon])
                        
                        maxFound, minFound = False, False
        infoFile.close()
        os.unlink(f)
del cursor
print ("Check the above extents to make sure they are within the coordinate system.")
print ("If the extents do not look correct, please review the data and manually enter a coordinate system")
