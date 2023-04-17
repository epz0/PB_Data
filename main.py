# accessing script with functions
from gallerydownload import *

# downloads data from the API and creates file
DownloadAPI('FullAPI_Download_5p',nPages=5) #first 5 pages only

# cleans the data downloaded from the API
CleanFullDump('C:\DSX_Vis\FullAPI_Download_5p.json', exportJson=True, exportExcel=True) # full filepath of the Downloaded file

