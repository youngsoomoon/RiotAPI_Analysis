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

# +
from pymongo import MongoClient
client = MongoClient()
db = client.RiotAPI

iron2_user_collection = db.league_iron2_user
iron2_accId_collection = db.iron2_accId
iron2_gameId_collection = db.iron2_gameId
iron2_gameData_collection = db.iron2_gameData
# -

api_key = 'RGAPI-8e41ee52-29f8-4a01-8a37-9cef4cea3522'

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


