# AGOLtoSharePoint

Python scripts for automating data exports from ArcGIS Online (AGOL) to local storage and SharePoint, with optional integration into Smartsheet.

---

## What This Does

This repo contains two pipeline scripts that handle automated data movement from AGOL project layers:

**Script 1 — Shapefile Downloader   -- AUTOMATED ARCHIVE SYSTEM**
Reads a JSON project dictionary and downloads shapefiles for each active project from AGOL, saving zipped exports to local project folders.

**Script 2 — CSV Exporter (in refactor)  -- EXPORT FEATURE CLASS TABLE DATE TO SHAREDRIVE TO BE DATA SHUTTLED TO SMARTSHEET**
Reads the same JSON project dictionary and exports feature class data as CSVs from AGOL, saving them to their respective SharePoint project folders; this data will ultimately be fed into Smartsheet via Data Shuttle. A project name column is appended to each CSV to enable filtering in Smartsheet.

---

## Requirements

- Python 3.x
- ArcGIS Pro (for authenticated AGOL profile)
- `arcgis` Python API (`pip install arcgis`)
- Access to target AGOL organization and layers
- SharePoint drive access (Script 2)
- Smartsheet access (Script 2)

---

## Configuration

Scripts are driven by a JSON project dictionary (`projects.json`). Each entry follows this structure:

```json
[
  {
    "projectName": "YOUR_PROJECT_NAME",
    "featureClass": "YOUR_AGOL_FEATURE_CLASS_ID",
    "localPath": "YOUR_LOCAL_FOLDER_PATH",
    "sharedPath": "YOUR_SHAREPOINT_FOLDER_PATH"
  }
]
```

- `projectName` — human-readable project label (e.g. `fannin_p2z2`)
- `featureClass` — AGOL feature layer item ID
- `localPath` — absolute path for local shapefile storage (Script 1)
- `sharedPath` — SharePoint path for CSV storage (Script 2)

> **Note:** Do not commit a populated `projects.json` to version control. See `.gitignore`.

---

## Usage

### Script 1 — Download Shapefiles

```bash
python download_shapefiles.py
```

Iterates through `projects.json`, connects to AGOL using your saved Pro profile, and downloads each project's shapefile as a zip to `localPath`.

### Script 2 — Export CSVs to SharePoint

```bash
python export_csvs.py
```

*(Under active refactor)* Iterates through `projects.json`, exports each project's feature class data as CSVs from AGOL, appends a `projectName` column to each CSV, and saves to `sharedPath` for Smartsheet ingestion.

---

## Architecture

```
projects.json
     |
     |---> download_shapefiles.py --> localPath (zipped shapefiles)
     |
     '---> export_csvs.py ----------> sharedPath (CSVs w/ projectName column)
                                           |
                                           '--> Smartsheet
```

---

## Refactor Roadmap

- [x] Establish single-project proof of concept (original script)
- [x] Commit original to version control
- [x] Rename `absolutePath` to `localPath` in JSON and Script 1
- [x] Add `sharedPath` key to JSON
- [x] Refactor Script 2 to read from JSON dictionary
- [x] Refactor Script 2 to iterate over all projects
- [x] Add `projectName` column to each exported CSV
- [x] End-to-end test across all active projects

---

## Security Notes

- AGOL credentials are handled via saved ArcGIS Pro profile (`GIS(profile="...")`) — no credentials are stored in scripts or config files
- `projects.json` contains internal file paths and AGOL layer IDs — excluded from version control via `.gitignore`
- Replace all placeholder values before running in your environment

---

## Author

Marc Wright — GIS Supervisor, Trans-Tel Central

