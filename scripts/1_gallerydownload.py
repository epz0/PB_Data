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
    dirMain = Path(r'C:\DSX_Vis\support') # your path for SelfLevelsIDs.csv file
    df_IDsExc = pd.read_csv(f'{dirMain}/SelfLevelsIDs.csv')
    idsList = df_IDsExc['ID'].values.tolist()
    df_CleanFull = df_nodup[~df_nodup['id'].isin(idsList)]

    # Final DF with Clean values from the json passed
    df_CleanFull = df_CleanFull.reset_index(drop=True)

    # exporting results
    # exporting as json
    if exportJson:
        with open(f'{dirMain}/export/{datetime.now().date()}_FullClean.json', 'w') as outfile:
            json.dump(df_CleanFull.T.to_dict(),outfile,indent=4)
        df = pd.read_json(f'{dirMain}/{datetime.now().date()}_FullClean.json')
        print(f"json file saved in {dirMain}/export/ at {datetime.now()}")

    # exporting as excel
    if exportExcel:
        df_CleanFull.to_excel(f'{dirMain}/export/{datetime.now().date()}_FullClean.xlsx')
        print(f"Excel file saved in {dirMain}/export/ at {datetime.now()}")

    return df_CleanFull


# Function to download entries' videos and thumbnails of a particular level
# fileFullPath is the full path of the clean data (.json)

def DownloadEntriesVid(fileFullPath, originalBudget, levelName=None):

    # folder to save the videos and thumbnails
    desktopfolder = Path(f"{Path.cwd()}/video-thumb/{levelName.replace(' ', '')}/")  # desktopfolder = Path('/'+ levelName.replace(' ', '') + '/')

    # check if folder already exists and creates it if not
    if not desktopfolder.exists():
        desktopfolder.mkdir()

    # get the data from the clean data json file
    df = pd.read_json(fileFullPath)
    df_data = pd.DataFrame(df).T

    # filter data to focus on the selected level
    if levelName:
        df_data = df_data[df_data['title'] == levelName]

    # check if there is data in this filtered df
    # if yes, then goes through each row (entries) and downloads the video & thumbnail
    # the file name for the video & thumbnail follows the following convention:
    # ID-Result-MaxStress-Budgetused-BudgetPercent (e.g. ABCD1-R_win-MS_98.7-B_12345-Bp_78.9.dat)
    if len(df_data) > 0:
        for i, row in df_data.iterrows():

            vidLink = str(row['video'])
            URLOpen = urllib.request.urlopen(vidLink).read()
            open(f"{desktopfolder}/{row['id']}-R_{row['result']}-MS_{row['maxStress']}-B_{row['budgetUsed']}-Bp_{row['budgetUsed']*100/originalBudget:.1f}.dat",
             'wb+').write(URLOpen)

            prevLink = str(row['videoPreview'])
            URLOpen = urllib.request.urlopen(prevLink).read()
            open(f"{desktopfolder}/{row['id']}-R_{row['result']}-MS_{row['maxStress']}-B_{row['budgetUsed']}-Bp_{row['budgetUsed']*100/originalBudget:.1f}.png",
                 'wb+').write(URLOpen)

            time.sleep(1) #to not overload the server

    #if there is no data in the filtered df, the levelName is wrong or level does not exist
    else:
        print(f" {levelName} does not exist!")

    print(f"Download conclude at {datetime.now()} and files saved in {desktopfolder}")