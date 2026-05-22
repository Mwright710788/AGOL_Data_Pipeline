import json
import sys
import os
import pandas as pd
from arcgis.gis import GIS
import zipfile

##variables
jsonPath = "C:/Users/MWright/Desktop/projectDictionary.json"

##print Python environment path and version
print(f"Path: {sys.executable}")
print(f"Version: {sys.version}")

##connect to AGOL
print("Connecting using your ArcGIS Pro login credentials...")
gis = GIS(profile = "trans_tel")
print(f"Logged in as: {gis.users.me.username}")

print("\n")

##read json data file
with open(jsonPath, "r") as f:
    data = json.load(f)

##iterate through json data items
for item in data:
    featureLayerID = item["featureClass"]
    featureName = item["projectName"]
    sharedPath = item["sharedPath"]

    print(f"Processing name {featureName}")

    try:
        ##create folder directory if it does not already exist
        if not os.path.exists(sharedPath):
            os.makedirs(sharedPath)

        ##access the layer and export
        dataItem = gis.content.get(featureLayerID)
        print(f"Exporting {dataItem.title} to CSV...")

        ##create a temporary CSV item in your AGOL content
        exportItem = dataItem.export(title= "Temp_Export_For_SP", export_format= "CSV")

        ##download the file locally
        downloadedFile = exportItem.download(save_path = sharedPath)
        print(f"File downloaded to: {downloadedFile}")

        ##delete the temp CSV item from AGOL
        exportItem.delete()
        print(f"Deleting temporary zip file from ArcGIS Online: {downloadedFile}")        

        ##unzip the zip file and save individual CSVs to unzippedPath
        with zipfile.ZipFile(os.path.join(sharedPath, "Temp_Export_For_SP.zip"), "r") as zip_ref:
            zip_ref.extractall(sharedPath)

        ##delete zip files from sharedPath
        os.remove(downloadedFile)
        print(f"Deleting temporary zip file from SharePoint drive: {downloadedFile}")

        print("\n")

        files = [f for f in os.listdir(sharedPath) if f.endswith(".csv")]
        for file in files:
            print(f"Adding 'project' column to: {file}") 
            df = pd.read_csv(os.path.join(sharedPath, file))
            df["project"] = featureName
            print(f"Populating 'project' column with: {featureName}")
            print("\n")
            df.to_csv(os.path.join(sharedPath, file), index = False)


    except Exception as e:
        print(f"An error occurred: {e}")


print("Script has successfully executed!")
