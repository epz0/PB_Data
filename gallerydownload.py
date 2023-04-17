import json
import requests
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.response

# function to download gallery info. number of pages optional.
def DownloadAPI(fileNameJson,nPages=None):

    # if nPages is specified
    if nPages:

        # api address
        url2 = (
            "http://pb2-authed-api.drycactus.com/v1/public/gallery/entries/read/all?page={}"
        )

        all_data = []

        # navigate through the api pages
        for page in range(1, nPages + 1):
            codefull = requests.get(url2.format(page))

            # if page does not load, retry
            if codefull.status_code == 500:
                while (True):
                    codefull = requests.get(url2.format(page))
                    if codefull.status_code != 500:
                        data = codefull.json() # gets the data from the page
                        all_data.extend(data["data"])
                        break
                    time.sleep(1) # to not overload the server
            else:
                data = codefull.json() # gets the data from the page
                all_data.extend(data["data"])
            time.sleep(1) # to not overload the server

        # save json file
        with open(fileNameJson + '.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

    else: # nPages not specified --> gets all the data available on the API
        # getting metada to figure out number of pages
        url1 = ("http://pb2-authed-api.drycactus.com/v1/public/gallery/entries/read/all")
        allAPI = requests.get(url1)
        dataAPI = allAPI.json()
        numPages = dataAPI["meta"]['last_page']

        # navigating through all pages and dumping to .json file
        url2 = (
            "http://pb2-authed-api.drycactus.com/v1/public/gallery/entries/read/all?page={}"
        )

        all_data = []
        for page in range(1, numPages+1):
            codefull = requests.get(url2.format(page)) # gets the data from the page

            # if page does not load, retry
            if codefull.status_code == 500:
                while (True):
                    codefull = requests.get(url2.format(page))
                    if codefull.status_code!=500:
                        data = codefull.json()
                        all_data.extend(data["data"])
                        break
                    time.sleep(1) # to not overload the server
            else:
                data = codefull.json() # gets the data from the page
                all_data.extend(data["data"])
            time.sleep(1) # to not overload the server

        # save json file
        with open(f'{fileNameJson}_{datetime.now().date()}' + '.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

    # print outcome
    print(f"Downloaded {fileNameJson} at {datetime.now()} saved in {Path.cwd()}")




# function to clear data dumped & export .json & .xlsx
def CleanFullDump(filedir, exportJson=None, exportExcel=None):

    # read full dump from API
    # filedir must be the full filepath
    df = pd.read_json(filedir)
    df_data = pd.DataFrame(df)

    # remove entries with empty values for video and videopreview
    df_data = df_data[~df_data['video'].isnull()]
    df_data = df_data[~df_data['videoPreview'].isnull()]

    # remove duplicated values
    df_nodup = df_data[~df_data.duplicated()]

    # remove self/test ids created when developing the method
    dirMain = Path('C:\DSX_Vis') # your path for SelfLevelsIDs.csv file
    df_IDsExc = pd.read_csv(f'{dirMain}/SelfLevelsIDs.csv')
    idsList = df_IDsExc['ID'].values.tolist()
    df_CleanFull = df_nodup[~df_nodup['id'].isin(idsList)]

    # Final DF with Clean values from the json passed
    df_CleanFull = df_CleanFull.reset_index(drop=True)

    # exporting results
    # exporting as json
    if exportJson:
        with open(f'{dirMain}/{datetime.now().date()}_FullClean.json', 'w') as outfile:
            json.dump(df_CleanFull.T.to_dict(),outfile,indent=4)
        df = pd.read_json(f'{dirMain}/{datetime.now().date()}_FullClean.json')
        print(f"json file saved in {dirMain} at {datetime.now()}")

    # exporting as excel
    if exportExcel:
        df_CleanFull.to_excel(f'{dirMain}/{datetime.now().date()}_FullClean.xlsx')
        print(f"Excel file saved in {dirMain} at {datetime.now()}")

    return df_CleanFull

