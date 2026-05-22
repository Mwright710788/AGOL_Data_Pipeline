import sys
import os
from arcgis.gis import GIS
import zipfile

##configure environments and variables
featureLayerID = "AGOL_FEATURE_CLASS_ID_HERE"
localPath = "C:/YOUR/TEMP/LOCAL/FOLDER/PATH/HERE/"
unzippedPath = "C:/MICROSOFT/SHAREPOINT/PATH/HERE/"

##create folder directory if it does not already exist
if not os.path.exists(localPath):
    os.makedirs(localPath)

##print Python environment path and version
print(f"Path: {sys.executable}")
print(f"Version: {sys.version}")

##connect to AGOL
print("Connecting using your ArcGIS Pro login credentials...")
gis = GIS(profile = "trans_tel")
print(f"Logged in as: {gis.users.me.username}")
        

##access the layer and export
try:
    dataItem = gis.content.get(featureLayerID)
    print(f"Exporting {dataItem.title} to CSV...")

    ##create a temporary CSV item in your AGOL content
    exportItem = dataItem.export(title= "Temp_Export_For_SP", export_format= "CSV")

    ##download the file locally
    downloadedFile = exportItem.download(save_path = localPath)
    print(f"File downloaded to: {downloadedFile}")

    ##delete the temp CSV item from AGOL
    exportItem.delete()
except Exception as e:
    print(f"An error occurred: {e}")

##unzip the zip file and save individual CSVs to unzippedPath
with zipfile.ZipFile(f"{localPath}Temp_Export_For_SP.zip", "r") as zip_ref:
    zip_ref.extractall(unzippedPath)

print("Script has successfully executed!")
