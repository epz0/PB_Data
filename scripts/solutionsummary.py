#%%
import pandas as pd
from pathlib import Path
import numpy as np
import json
import math

#%%

def solutions_summary(dir_data, saveExcel=True):

    #! finding solutions' save files
    pth = Path(dir_data)

    ls_solf = []

    for p in pth.rglob("*.json"):
        ls_solf.append([p.parent, p.stem])

    df_sols = pd.DataFrame(ls_solf, columns=['path', 'PT']).drop(columns=['path'])
    df_sols['PT'] = df_sols['PT'].str.replace('-0','-')

    #df_sols[['PT','IntID','SolID']] = df_sols['PT'].str.split('-',expand=True)
    #df_sols['SolID'] = df_sols['SolID'].astype(int)
    df_sols[['TLength','NSegm','NJoint']] = ''

    #! getting summary info from solutions' save files
    for n, sol in enumerate(ls_solf):
        #read file (layout json)
        df = pd.read_json(f'{sol[0]}/{sol[1]}.json')

        df_Anchor=df.iloc[0,10]
        df_Edge=df.iloc[1,10]
        df_Joints=df.iloc[2,10]
        df_Phase=df.iloc[3,10]

        df_Anchor= pd.json_normalize(df_Anchor)
        df_Joints=pd.json_normalize(df_Joints)
        df_Edge=pd.json_normalize(df_Edge)

        df_AncJon= pd.concat([df_Anchor,df_Joints],ignore_index=True)

        xDict = dict(zip(df_AncJon.loc[:,'m_Guid'], df_AncJon.loc[:,'m_Pos.x']))
        yDict = dict(zip(df_AncJon.loc[:,'m_Guid'], df_AncJon.loc[:,'m_Pos.y']))

        #initialise the columns
        df_Edge['nAx']=''
        df_Edge['nAy']=''
        df_Edge['nBx']=''
        df_Edge['nBy']=''
        df_Edge['EdgeSize']=''

        df_Edge['nAx']=df_Edge['m_NodeAGuid'].map(xDict)
        df_Edge['nAy']=df_Edge['m_NodeAGuid'].map(yDict)

        df_Edge['nBx']=df_Edge['m_NodeBGuid'].map(xDict)
        df_Edge['nBy']=df_Edge['m_NodeBGuid'].map(yDict)

        for i in range(len(df_Edge.index)):
            x0=df_Edge.iloc[i,6]
            y0=df_Edge.iloc[i,7]
            x1=df_Edge.iloc[i,8]
            y1=df_Edge.iloc[i,9]

            df_Edge.iloc[i,df_Edge.columns.get_loc('EdgeSize')]= math.sqrt((x0-x1)**2+(y0-y1)**2)

        df_MatSummary=df_Edge.groupby('m_MaterialType')['EdgeSize'].sum()
        df_MatSummary = pd.DataFrame(df_MatSummary)

        MatDict = { #id, name, line width, color
            '1':[200,'road',5,'rgb(139,69,19)'], #saddlebrown
            '2':[400,'reinforced road',5,'rgb(255,140,0 )'], #dark orange
            '3':[180, 'wood',3,'rgb(222,184,135)'], #burly wood
            '4':[450, 'steel',4,'rgb(178,34,34)'], #mediumvioletred
            '5':[220, 'rope',2,'rgb(218,165,32)'], #golden rod
            '6':[400, 'cable',1,'rgb(105,105,105)'], #dimgray
            '7':[450, 'hydro',4,'rgb(30,144,255)'], #dodgerblue
            '8':[330, 'spring',5,'rgb(255,215,0)'] #gold
        }

        df_MatSummary['MatType']=df_MatSummary.index
        df_MatSummary['CostTotal']= ''
        df_MatSummary['Materials']=''
        df_MatSummary['AvgSize']= df_Edge.groupby('m_MaterialType')['EdgeSize'].mean()
        df_MatSummary['NumSegments']= df_Edge.groupby('m_MaterialType')['EdgeSize'].count()

        #print(df_MatSummary.info())

        #print(df_MatSummary)

        for i in range(len(df_MatSummary.index)):
            matType=MatDict[str(df_MatSummary.iloc[i,1])][0]
            matLen=df_MatSummary.iloc[i,0]
            df_MatSummary.iloc[i,2]= matLen * matType
            df_MatSummary.iloc[i,3]= MatDict[str(df_MatSummary.iloc[i,1])][1]

        #! get values & add to df_sols
        total_length = df_MatSummary['EdgeSize'].sum()
        total_segments = df_MatSummary['NumSegments'].sum()
        total_joints = len(df_AncJon)

        df_sols.loc[n,'TLength'] = total_length
        df_sols.loc[n,'NSegm'] = total_segments
        df_sols.loc[n,'NJoint'] = total_joints

    if saveExcel == True:
        df_sols.to_excel(f'{dir_data}/solutions_sumary.xlsx')

    return df_sols


'''
## Sum total of... ##
#synBudgetAvail = df_Config.loc['m_Budget.m_Cash'][0]
synBudgetUsed = df_MatSummary['CostTotal'].sum()
synTotalLen = df_MatSummary['EdgeSize'].sum()

### find gap size ###
synGap = 0
for i in range(len(df_Anchor.index)-1):
    temp = abs(df_Anchor.iloc[i,3]-df_Anchor.iloc[i+1,3])
    if temp > synGap:
        synGap=temp
#print(synGap)

## Count number of... ##
synNumSegments = df_MatSummary['NumSegments'].sum()
synNumAnchors = len(df_Anchor.index)
synNumJoints = len(df_Joints.index)

#print(df_MatSummary)
### Reorder summary df
df_MatSummaryOrd = df_MatSummary[['Materials','MatType','NumSegments','EdgeSize','AvgSize','CostTotal']]
df_MatSummaryOrd['EdgeSize']=df_MatSummaryOrd[['EdgeSize']].astype(float).round(decimals=1)
df_MatSummaryOrd['AvgSize']=df_MatSummaryOrd[['AvgSize']].round(decimals=1)
df_MatSummaryOrd['CostTotal']=df_MatSummaryOrd[['CostTotal']].astype(float).round(decimals=1)
#print(df_MatSummaryOrd)
#print(df_AncJon)

'''


