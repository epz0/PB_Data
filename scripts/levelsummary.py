# accessing script with functions
from gallerydata import *
from solutionsummary import *

# filter and export clean data based on levelName
AllEntriesForLevel(r'C:\DSX_Vis\export\2023-05-24_FullClean.json', 'Sandbox')

my_dir = 'C:\Py\DSX_Vis\SaveFiles'

df_s = solutions_summary(my_dir, saveExcel=True)
#print(df_s)