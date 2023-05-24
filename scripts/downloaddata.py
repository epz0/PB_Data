from pathlib import Path
import argparse

# accessing script with functions
from gallerydata import *

#argument parser
parser = argparse.ArgumentParser(description='file name & num pages')
parser.add_argument('-out', help='file name to create')
parser.add_argument('-pg', help='number of pages. if not passed, download all pages.', type=int)

args = parser.parse_args()
filename = args.out
nPages = args.pg

# downloads data from the API and creates file
savedfile = DownloadAPI(filename, nPages)

# cleans the data downloaded from the API
CleanFullDump(savedfile, exportJson=True, exportExcel=True) # full filepath of the Downloaded file
