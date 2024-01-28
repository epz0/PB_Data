# accessing script with functions
from gallerydata import *

# download entries' video and thumbnail
# originalBudget is the level budget
# levelName is the name of the level on the API
# these info can be retrieved from \support\LevelsInfo-master.xlsx
DownloadEntriesVid(r'C:/Py/DSX_Vis/export/2023-05-24_FullClean.json', originalBudget=10000,
                   levelName='Sandbox')