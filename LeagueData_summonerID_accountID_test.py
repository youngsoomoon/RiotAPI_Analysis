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

# summonerID 가져오기

import requests
import json
import pandas as pd
import numpy as np
import pymongo

from pymongo import MongoClient
client = MongoClient()
db = client.RiotAPI
iron2_user_collection = db.league_iron2_user

# # 몽고디비에서 아이언2티어 유저 데이터 가져오기

for i in iron2_user_collection.find():
    print(i)

# # collection에 저장된 데이터 중 summonerId만 가져오기

s_id = list(iron2_user_collection.find({}, {'_id' : 0, 'summonerId' : 1}))[0]
s_id

a = list(s_id.values())
a[0]

# # summonerId입력해서 accountId 받아오기

api_key = 'RGAPI-47b2b136-2721-49ac-ae73-80bbab633e46'

SUM_accountId = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"+a[0]+"?api_key="+api_key
r_accountId  = requests.get(SUM_accountId)
r_accountId.json()['accountId']

# # accountId 입력해서 gameId(=matchId) 받아오기

MAT_matchId = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+r_accountId.json()['accountId']+'?api_key='+api_key
r_matchId = requests.get(MAT_matchId)
r_matchId.json()

# ## json 형식은 파이썬에서 dict로 인식
# ## json으로 변환하고싶다면 json.dumps()함수 이용

m_id = json.dumps(r_matchId.json())
m_id
