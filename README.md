# _Poly Bridge 2_ data retrieval 
This repository contains code to help researchers and players to download information from the _Poly Bridge 2_ solutions gallery. You can download both the entries' information (win/fail, budget, etc.) and the video/thumbnail.

## Running the code ##
The main libraries required include `pandas`, `urllib`, `pathlib`, `datetime`. 

You can run the code from the terminal with the following command:
`python downloaddata.py -out test -pg 5` 

This will download the entries for the first five pages of the gallery, saving a json file named "test".


## Support information ##
A reference key between in-game level names and gallery level names (yes, they are different) is [provided](https://github.com/epz0/PB_Data/blob/master/support/LevelsInfo-master.xlsx).

For convenience, levels' json files have also [been added](https://github.com/epz0/PB_Data/tree/master/support/level-layouts).

## Obs. ##
This code was generated to support a research project looking at design creativity using computer games. Users are requested to be mindful of the game developers' resources to not overload their servers with download requests. 

The number of entries summarised in the LevelsInfo file was retrieved in December 2022. 





