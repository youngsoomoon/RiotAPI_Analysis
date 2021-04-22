# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import requests
import json
import pandas as pd
import pymongo
import time
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# %matplotlib inline

# +
from pymongo import MongoClient
client = MongoClient()
db = client.RiotAPI

challenger_user_collection = db.league_challenger_user
challenger_accId_collection = db.challenger_accId
challenger_gameId_collection = db.challenger_gameId
challenger_gameData_collection = db.challenger_gameData
# -

plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)

# %config InlineBackend.figure_format = 'retina'

chal_league_df = pd.DataFrame(challenger_gameData_collection.find())
chal_league_df

chal_league_df.isnull().sum()
chal_league_df = chal_league_df.drop(columns=['status'],axis=1)
chal_league_df = chal_league_df.dropna()
chal_league_df = chal_league_df.drop_duplicates(['gameId'])
chal_teams_df = pd.DataFrame(dict(chal_league_df['teams'])).T
chal_teams_df = pd.concat([chal_league_df, chal_teams_df[0]], axis=1)
chal_teams_df = pd.DataFrame(dict(chal_teams_df[0])).T
chal_teams_df['win'].value_counts().plot.barh()

chal_teams_df

# # 분석에 필요한 컬럼들만 남겨둔다.

chal_teams_df1 = chal_teams_df.drop(['teamId', 'towerKills', 'inhibitorKills', 'baronKills', 'dragonKills', 'vilemawKills', 'riftHeraldKills','dominionVictoryScore', 'bans' ],axis = 1)

chal_teams_df1 = chal_teams_df1.drop(['firstBaron', 'firstRiftHerald'],axis = 1)

chal_teams_df1

# # 'BTID' 컬럼에 각 요소 별 True값에 따라 유형 분류

chal_teams_df1['BTID'] = ''

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == False) , 'B',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == False) , 'T',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == False) , 'I',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == True) , 'D',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == False) , 'BT',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == False) , 'BI',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == True) , 'BD',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == False) , 'TI',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == True) , 'TD',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == True) , 'ID',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == False) , 'BTI',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == True) , 'BTD',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == True) , 'BID',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == True) , 'TID',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == True) & 
    (chal_teams_df1['firstTower'] == True) &
    (chal_teams_df1['firstInhibitor'] == True) &
    (chal_teams_df1['firstDragon'] == True) , 'BTID',chal_teams_df1['BTID'])

chal_teams_df1['BTID'] = np.where(
    (chal_teams_df1['firstBlood'] == False) & 
    (chal_teams_df1['firstTower'] == False) &
    (chal_teams_df1['firstInhibitor'] == False) &
    (chal_teams_df1['firstDragon'] == False) , 'FFFF',chal_teams_df1['BTID'])

chal_teams_df1.isnull().sum()

# # 각 유형별 승/패 데이터 그래프(수정 전)

sns.countplot(data=chal_teams_df1, x="BTID", hue="win")

# # BTID 컬럼 글자 수 기준 오름차순으로 정렬

chal_teams_df2 = chal_teams_df1.sort_values(by=["BTID"],key=lambda x:x.str.len())
chal_teams_df2

xlabels = list(chal_teams_df2['BTID'].unique())



# # 각 유형별 승/패 데이터 그래프(수정 후)

# +
chart1 = plt.subplots(figsize=(8,4))
chart1 = sns.countplot(data=chal_teams_df2, x="BTID", hue="win")

chart1.set_title('각 요소 선취에 따른 승/패 그래프')
chart1.set_xlabel('B = Blood , T = Tower , I = Inhibitor , D = Dragon')
chart1.set_ylabel('경기 수')
chart1.set_xticklabels(labels = xlabels, rotation=45)

plt.show()
# -

# ## 크기 순서대로 나열

xlabels_value = list(chal_teams_df1['BTID'].value_counts().index)

# +
chart1 = plt.subplots(figsize=(8,4))
chart1 = sns.countplot(data=chal_teams_df2, x="BTID", hue="win",order =xlabels_value )

chart1.set_title('각 요소 선취에 따른 승/패 그래프')
chart1.set_xlabel('B = Blood , T = Tower , I = Inhibitor , D = Dragon')
chart1.set_ylabel('경기 수')
chart1.set_xticklabels(labels = xlabels_value, rotation=45)

plt.show()
# -

# # 각 유형 별 승리 데이터 그래프

# ## BTI ( firstBlood + Tower + Inhibitor) 를 얻은 게임이 가장 승리가 많음
# ## BTID ( 선취점+ 타워 +억제기 +용) 모두 얻은 팀의 승리가 가장 많을 것이라 예측했으나 다른 결과

chal_teams_win_df = chal_teams_df2[chal_teams_df2['win'] == 'Win']
chal_teams_win_df

chal_teams_win_df = chal_teams_win_df.sort_values(by=["BTID"],key=lambda x:x.str.len())
chal_teams_win_df['BTID'].unique()

xlabels_win1 = list(chal_teams_win_df['BTID'].unique())

# +
chart2 = plt.subplots(figsize=(8,4))
chart2 = sns.countplot(data=chal_teams_win_df, x="BTID")

chart2.set_title('각 요소 선취에 따른 승리 그래프')
chart2.set_xlabel('B = Blood , T = Tower , I = Inhibitor , D = Dragon')
chart2.set_ylabel('경기 수')
chart2.set_xticklabels(labels = xlabels_win1, rotation=45)
plt.show()
# -

# ## 크기순서대로 나열

chal_teams_win_df['BTID'].value_counts().index

chal_teams_win_df['BTID'].value_counts()

xlabels_win = list(chal_teams_win_df['BTID'].value_counts().index)
xlabels_win

# +
chart2 = plt.subplots(figsize=(8,4))
chart2 = sns.countplot(data=chal_teams_win_df, x="BTID",order = xlabels_win)

chart2.set_title('각 요소 선취에 따른 승리 그래프')
chart2.set_xlabel('B = Blood , T = Tower , I = Inhibitor , D = Dragon')
chart2.set_ylabel('경기 수')
chart2.set_xticklabels(labels = xlabels_win, rotation=45)
plt.show()
# -

# # 각 유형 별 패배 데이터 그래프

chal_teams_lose_df = chal_teams_df2[chal_teams_df2['win'] == 'Fail']
chal_teams_lose_df

xlabels3 = list(chal_teams_lose_df['BTID'].unique())

# +
chart3 = plt.subplots(figsize=(8,4))
chart3 = sns.countplot(data=chal_teams_lose_df, x="BTID")

chart3.set_title('각 요소 선취에 따른 패배 그래프')
chart3.set_xlabel('B = Blood , T = Tower , I = Inhibitor , D = Dragon')
chart3.set_ylabel('경기 수')
chart3.set_xticklabels(labels = xlabels3, rotation=45)
plt.show()
# -

# ## 크기순서대로 나열

xlabel_lose = list(chal_teams_lose_df['BTID'].value_counts().index)

# +
chart3 = plt.subplots(figsize=(8,4))
chart3 = sns.countplot(data=chal_teams_lose_df, x="BTID",order =xlabel_lose)

chart3.set_title('각 요소 선취에 따른 패배 그래프')
chart3.set_xlabel('B = Blood , T = Tower , I = Inhibitor , D = Dragon')
chart3.set_ylabel('경기 수')
chart3.set_xticklabels(labels = xlabel_lose, rotation=45)
plt.show()
