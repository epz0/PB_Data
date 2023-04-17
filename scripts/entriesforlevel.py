# script with function to filter and export .xlsx file with
# all entries for a particular level, from the clean data .json

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# function to filter data to level of interest only
# filePath is the full path for the clean data .json
# levelName is the name of the level of interest
def AllEntriesForLevel(filePath, levelName):
    fileDir = Path.cwd().parents[0]

    #read clean .json file
    df = pd.read_json(filePath)
    df_data = pd.DataFrame(df).T

    # filter data based on the levelName
    df_filtered = df_data[df_data['title'] == levelName].reset_index()

    # check if export folder already exists and creates it if not
    exportfolder = Path(f"{fileDir}/export/")
    if not exportfolder.exists():
        exportfolder.mkdir()

    # save .xlsx file with all entries for the selected level
    df_filtered.to_excel(f"{exportfolder}/{levelName.replace(' ', '')}_Clean.xlsx")
    print(f"Excel file saved in {exportfolder} at {datetime.now()}")

    return df_filtered
