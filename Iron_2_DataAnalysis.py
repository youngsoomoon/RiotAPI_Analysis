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
import matplotlib.pyplot as plt

# +
from pymongo import MongoClient
client = MongoClient()
db = client.RiotAPI

iron2_user_collection = db.league_iron2_user
iron2_accId_collection = db.iron2_accId
iron2_gameId_collection = db.iron2_gameId
iron2_gameData_collection = db.iron2_gameData
# -

api_key = 'RGAPI-2bfa9053-b8e6-4fed-928e-8cf4892b96d2'

# # mongoDB에서 summonerID 가져오기

for i in iron2_user_collection.find():
    print(i)

iron2_sumId_list = list(iron2_user_collection.find({}, {'_id' : 0, 'summonerId' : 1}))
iron2_sumId = []
for i in iron2_sumId_list:
    iron2_sumId.append(list(i.values())[0])

# # 아이언 2티어 accountID를 mongoDB에 저장하기

for i in range(len(iron2_sumId)):
    accountId_API = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"+iron2_sumId[i]+"?api_key="+api_key
    r_accountId_API = requests.get(accountId_API)
    iron2_accId_collection.insert_one(r_accountId_API.json())
    time.sleep(1.5)

for i in iron2_accID_collection.find():
    print(i)

iron2_accID_list = list(iron2_accId_collection.find({},{'_id' : 0, 'accountId' : 1} ))
iron2_accID_list

iron2_accID = []
for i in iron2_accID_list:
    iron2_accID.append(list(i.values())[0])

print(iron2_accID[0])

# # mongoDB에 matches 데이터 저장하기

iron2_gameID_list = []
for g in iron2_accID:
    gameId_API = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+g+'?api_key='+api_key
    r_gameId_API = requests.get(gameId_API)
    iron2_gameId_collection.insert_one(r_gameId_API.json())
    print(r_gameId_API.json())
    time.sleep(1.5)

# # matches 데이터에서 gameID만 가져오기

matches_list = []
for i in list(iron2_gameId_collection.find({},{'_id' : 0,'matches':1})):
    matches_list.append(i)
matches_list[0]

iron2_gameId = []
for i in matches_list:
    for j in range(len(list(i.values())[0])):
        iron2_gameId.append(list(i.values())[0][j]['gameId'])
iron2_gameId #gameId 추출성공!!!!!!!!

# # mongoDB에 gameData 저장하기 

# ### 20500개의 게임데이터 1.5초에 1개씩 저장
# ### 20500*1.5/60 = 약 512분(8.5시간) 소요예정

for i in iron2_gameId:
    gameData_API = "https://kr.api.riotgames.com/lol/match/v4/matches/"+ str(i) +'?api_key='+api_key
    r_gameData = requests.get(gameData_API)
    iron2_gameData_collection.insert_one(r_gameData.json())
    print(iron2_gameId.index(i),'/',len(iron2_gameId))
    time.sleep(1.5)

# # gameData 불러와서 DataFrame으로 만들기

iron_league_df = pd.DataFrame(iron2_gameData_collection.find())

iron_league_df

iron_league_df.isnull().sum()

iron_league_df['status']

# # status값이 출력된 컬럼 삭제

iron_league_df = iron_league_df.drop(columns=['status'],axis=1)

iron_league_df.info()

# NaN값을 가진 행 모두 삭제
iron_league_df = iron_league_df.dropna()

iron_league_df.info()

# # teams 컬럼만 가져와서 새로운 컬럼 만들기

iron_teams_df = pd.DataFrame(dict(iron_league_df['teams'])).T
iron_teams_df

# # 동일한 형태의 데이터프레임 합치기 pd.concat()
# ## iron_league_df에 iron_teams_df 열로 추가하기

iron_teams_df = pd.concat([iron_league_df, iron_teams_df], axis=1)
iron_teams_df

# # iron_teams_df의 0 컬럼을 딕셔너리형태로 바꾸고 데이터프레임으로 생성

df1 = pd.DataFrame(dict(iron_teams_df[0])).T
df1

# 경기 데이터의 전체 승/패 차트
df1['win'].value_counts().plot.barh()

win = df1[ df1["win"] == "Win" ]
win

win_firstBlood = win[win["firstBlood"] == True]
win_firstBlood

lose = df1[ df1["win"] == "Fail" ]
lose

lose_firstBlood = lose[lose["firstBlood"] == True]
lose_firstBlood

labels = ['Win & FirstBlood', 'Lose & FirstBlood']
sizes = [len(win_firstBlood),len(lose_firstBlood)]
plt.bar(labels,sizes, width=0.3, color = ['green','red'])

#퍼블따고 이길 확률
(len(win_firstBlood)/(len(win_firstBlood)+len(lose_firstBlood)))*100

#퍼블따고 질 확률
(len(lose_firstBlood)/(len(win_firstBlood)+len(lose_firstBlood)))*100


