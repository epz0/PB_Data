# accessing script with functions
from gallerydownload import *
from entriesforlevel import *

# downloads data from the API and creates file
#DownloadAPI('FullAPI_Download_5p',nPages=5) #first 5 pages only

# cleans the data downloaded from the API
#CleanFullDump('C:\DSX_Vis\FullAPI_Download_5p.json', exportJson=True, exportExcel=True) # full filepath of the Downloaded file

# download entries' video amd thumbnail
# originalBudget is the level budget
# levelName is the name of the level on the API
# these info can be retrieved from \support\LevelsInfo-master.xlsx
#DownloadEntriesVid(r'C:\DSX_Vis\2023-04-17_FullClean.json', originalBudget=10000,
#                    levelName='Sandbox')

# filter and export clean data based on levelName
AllEntriesForLevel(r'C:\DSX_Vis\2023-04-17_FullClean.json', 'Sandbox')