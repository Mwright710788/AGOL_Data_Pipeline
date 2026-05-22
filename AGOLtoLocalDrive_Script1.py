import os
import json
import datetime
from arcgis.gis import GIS

##variables
jsonPath = "C:/YOUR/LOCAL/PATH/TO/DICTIONARY/projectDictionary.json"
timeStamp = datetime.datetime.now().strftime("%m%d%Y")

##connect to AGOL
print("Connecting using your ArcGIS Pro login credentials...")
gis = GIS(profile = "PROFILE_NAME")
print(f"Logged in as: {gis.users.me.username}\n")
        
##read json data file
with open(jsonPath, "r") as f:
    data = json.load(f)

##iterate through json data items
for item in data:
    featureLayerID = item["featureClass"]
    featureName = item["projectName"]
    localPath = item["absolutePath"]

    print(f"Processing name {featureName}")

##access the layer and export
    try:
        dataItem = gis.content.get(featureLayerID)

        ##if statement to catch instances of no feature class with that ID
        if dataItem is None:
            print(f"Could not find item  with ID {featureLayerID}, skipping...")
            continue
        
        ##create unique compressed ZIP file name with timeStamp
        exportTitle = f"Backup_{featureName}_{timeStamp}"
        print(f"Exporting {dataItem.title} as {exportTitle}...")

        exportItem = None

        try:
            ##create a temporary CSV item in your AGOL content
            exportItem = dataItem.export(title = exportTitle, export_format= "Shapefile")

            ##download the file locally
            downloadedFile = exportItem.download(save_path = localPath)
            print(f"File downloaded to: {localPath}")

            ##force specific filename format locally
            finalPath = os.path.join(localPath, exportTitle + ".zip")

            ##check if file exists before renaming to avoid errors
            if os.path.exists(finalPath):
                os.remove(finalPath)
            os.rename(downloadedFile, finalPath)

            print(f"Successfully saved to: {finalPath}\n")

        finally:
            ##delete the temp CSV item from AGOL
            if exportItem:
                exportItem.delete()
        
    except Exception as e:
        print(f"An error occurred: {e}")

print("Script has successfully executed!")
