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
import seaborn as sns

# +
from pymongo import MongoClient
client = MongoClient()
db = client.RiotAPI

challenger_user_collection = db.league_challenger_user
challenger_accId_collection = db.challenger_accId
challenger_gameId_collection = db.challenger_gameId
challenger_gameData_collection = db.challenger_gameData
# -

api_key = 'RGAPI-534e0591-7946-48b2-bf84-51cdc11d5cba'

Challenger_API = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"+"?api_key="+api_key
r_Challenger_API = requests.get(Challenger_API)
r_Challenger_API.json()

# # 챌린저 데이터 mongoDB에 저장

challenger_user_collection.insert_many(r_Challenger_API.json()['entries'])

r_Challenger_API.json()['entries']

Challlenger_sumId = []
for i in r_Challenger_API.json()['entries']:
    Challlenger_sumId.append(i['summonerId'])
Challlenger_sumId

len(Challlenger_sumId)

# # sumId입력을 통해 accId 받아오기
#

accId_list = []
for i in range(len(Challlenger_sumId)):
    accountId_API = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"+Challlenger_sumId[i]+"?api_key="+api_key
    r_accountId_API = requests.get(accountId_API)
    accId_list.append(r_accountId_API.json()['accountId'])
    time.sleep(1.5)
accId_list

accId_list

gameId_list = []
for g in accId_list:
    gameId_API = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+g+'?api_key='+api_key
    r_gameId_API = requests.get(gameId_API)
    challenger_gameId_collection.insert_one(r_gameId_API.json())
    gameId_list.append(list(gameId_dict.values())[1])
    time.sleep(1.3)
gameId_list

matches_list = []
for i in list(challenger_gameId_collection.find({},{'_id' : 0,'matches':1})):
    matches_list.append(i)
matches_list[0]

matches_list[0]

challenger_gameId = []
for i in matches_list:
    for j in range(len(list(i.values())[0])):
        challenger_gameId.append(list(i.values())[0][j]['gameId'])
challenger_gameId 

len(challenger_gameId)


# # challenger 의 유저당 100개의 게임데이터를 가져와서 mongoDB에 저장했지만 중복되는 게임데이터가 많음

for i in challenger_gameId:
    gameData_API = "https://kr.api.riotgames.com/lol/match/v4/matches/"+ str(i) +'?api_key='+api_key
    r_gameData = requests.get(gameData_API)
    challenger_gameData_collection.insert_one(r_gameData.json())
    print(challenger_gameId.index(i),'/',len(challenger_gameId))
    time.sleep(1.5)

chal_league_df = pd.DataFrame(challenger_gameData_collection.find())
chal_league_df

chal_league_df.info()

chal_league_df.isnull().sum()

chal_league_df = chal_league_df.drop(columns=['status'],axis=1)
chal_league_df.info()

chal_league_df = chal_league_df.dropna()
chal_league_df.info()

# # 중복된 데이터 제거하기

# gameId 컬럼의 중복되지 않은 값의 갯수
chal_league_df['gameId'].nunique()

chal_league_df.duplicated(["gameId"])

# gameId의 중복 
chal_league_df = chal_league_df.drop_duplicates(['gameId'])

chal_league_df.info()

chal_teams_df = pd.DataFrame(dict(chal_league_df['teams'])).T
chal_teams_df

chal_teams_df = pd.concat([chal_league_df, chal_teams_df[0]], axis=1)

chal_teams_df

chal_teams_df = pd.DataFrame(dict(chal_teams_df[0])).T
chal_teams_df

# 경기 데이터의 전체 승/패 차트
chal_teams_df['win'].value_counts().plot.barh()

# 게임데이터 전체 승률
(len(win)/(len(win)+len(lose)))*100

win = chal_teams_df[ chal_teams_df["win"] == "Win" ]
win_firstBlood = win[win["firstBlood"] == True]
win_firstBlood

lose = chal_teams_df[ chal_teams_df["win"] == "Fail" ]
lose_firstBlood = lose[lose["firstBlood"] == True]
lose_firstBlood

# # 퍼스트블러드에 따른 승/패 여부

# seaborn 을 이용한 시각화
# firstBlood에 따른 승/패 여부
sns.countplot(x="firstBlood", data =chal_teams_df, hue = 'win')

#퍼블따고 이길 확률
len(win_firstBlood)/len(chal_teams_df)*100

#퍼블따고 질 확률
len(lose_firstBlood)/len(chal_teams_df)*100

# # 첫 타워 처치에 따른 승/패 여부

win_firstTower = win[win["firstTower"] == True]
lose_firstTower = lose[lose["firstTower"] == True]

# firstTower에 따른 승/패 여부
sns.countplot(x="firstTower", data =chal_teams_df, hue = 'win')

#퍼스트타워따고 이길 확률
len(win_firstTower)/len(chal_teams_df)*100

#퍼스트타워따고 질 확률
len(lose_firstTower)/len(chal_teams_df)*100

# # 첫 억제기 처치에 따른 승/패 여부

win_firstInhibitor = win[win["firstInhibitor"] == True]
lose_firstInhibitor = lose[lose["firstInhibitor"] == True]

# firstInhibitor에 따른 승/패 여부
sns.countplot(x="firstInhibitor", data =chal_teams_df, hue = 'win')

#퍼스트억제기따고 이길 확률
len(win_firstInhibitor)/len(chal_teams_df)*100

#퍼스트억제기따고 질 확률
len(lose_firstInhibitor)/len(chal_teams_df)*100

#퍼스트억제기밀리고 질 확률
lose_firstInhibitor_F = lose[lose["firstInhibitor"] == False]
len(lose_firstInhibitor_F)/len(chal_teams_df)*100

# # 첫 용 처치에 따른 승/패 여부

sns.countplot(x="firstDragon", data =chal_teams_df, hue = 'win')

win_firstDragon = win[win["firstDragon"] == True]
lose_firstDragon = lose[lose["firstDragon"] == True]

#퍼스트 용 먹고 이길 확률
len(win_firstDragon)/len(chal_teams_df)*100

#퍼스트 용 먹고 질 확률
len(lose_firstDragon)/len(chal_teams_df)*100

sns.countplot(x="towerKills", data =chal_teams_df, hue = 'win')

# # 히스토그램

chal_teams_df

h = chal_teams_df.iloc[:,8].hist(figsize=(12,12))

sns.scatterplot(data=chal_teams_df, x = "towerKills", y = 'dragonKills',hue='win')

# --------------------------------------------------------------------------------------------------

# # FirstBlood , First Tower , First Inhibitor, First Dragon 에 따른 승률

# ## FirstBlood & FirstTower

chal_teams_df

# ### firstBlood 와 firstTower 가 모두 True

df_FB_FT_TT = chal_teams_df[
    (chal_teams_df["firstBlood"] == True) &
    (chal_teams_df["firstTower"] == True)]
df_FB_FT_TT

chal_teams_df.groupby(["firstBlood","firstTower","firstDragon","firstInhibitor"])["win"].count()



chal_teams_df.groupby(["firstBlood","firstTower","firstDragon","firstInhibitor"])["win"].count().plot.bar()

chal_teams_df['BTDI'] = chal_teams_df[]

if chal_teams_df[(chal_teams_df["firstBlood"] == True) &
    (chal_teams_df["firstTower"] == True)]

chal_teams_df['firstBlood'].value_counts().plot.bar()









# --------------------------------------------------------------------------------------------------

# # 챌린저데이터에서 밴 챔피언ID 가져오기

chal_teams_df['bans']

chal_bans = chal_teams_df[['bans']]
chal_bans

df1 = pd.DataFrame(list(chal_teams_df['bans']))
df1

df1.isnull().sum()

chal_bansChamp = df1.dropna()
chal_bansChamp

chal_bansChamp1 = chal_bansChamp
chal_bansChamp1

len(chal_bansChamp.index)

chal_bansChamp.iloc[1][2]['championId']

# # championID만 가져오기

for i in range(len(chal_bansChamp.index)):
    for j in range(len(chal_bansChamp.columns)):
        chal_bansChamp1.iloc[i][j] = chal_bansChamp.iloc[i][j]['championId']
chal_bansChamp1

# # stack()을 이용하여 1게임당 5개의 밴 챔피언을 하나의 열로 압축시키고 value_counts()로 빈도 수 파악

chal_bansChamp1.stack().value_counts().head(10)

chal_bansChamp1.stack().value_counts().tail(10)

chal_bans_se = chal_bansChamp1.stack().value_counts()
chal_bans_se

chal_bans_se.head(10).plot.barh()

# # ChampionID를 실제 챔피언 이름으로 변경하기
# ## mongoDB에서 Champion Data 가져오기

Champ_API = 'http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/champion.json'
r_Champ_API = requests.get(Champ_API)
r_Champ_API.json()

champ_df = pd.DataFrame(r_Champ_API.json()['data'])
champ_df

champ_se = champ_df.loc['key']
champ_se

champ_se.index

# # 밸류값을 오름차순으로 정렬하기위해 모든 밸류값을 int형으로 바꿔준다

for i in range(len(champ_se.values)):
    champ_se.values[i] = int(champ_se.values[i])
champ_se.values

champ_se =champ_se.sort_values()
champ_se

champ_se_list = list(champ_se.index)
champ_se_list

ban = list(chal_bans_se.index)
ban

name = list(champ_se.values)
name

name.insert(0,-1)

name.remove(887)
name

name.remove(21)

print(len(ban), len(name))

# ## ban 챔피언 목록에는 전체 챔피언중 없는것이 1개 존재하는데 다음 소스를 통해 21번 챔피언이 없는것을 확인

for i in range(len(ban)):
    if ban[i] == name[i]:
        print(ban[i])
    else:
        print('error')

name.remove(21)

print(len(ban), len(name))

# # Index 수정을 위해 오름차순으로 정렬

chal_bans_se = chal_bans_se.sort_index()
chal_bans_se

# ## -1은 밴을 선택하지 않을것을 의미하므로 인덱스리스트에 추가

champ_se_list.insert(0,"None")
champ_se_list

# ## 그웬과 미스포춘은 밴 목록에 해당하지 않아서 삭제

champ_se_list.remove('Gwen')

champ_se_list.remove('MissFortune')

# ## ChampionID 와 챔피언 이름 리스트가 일치하는것을 확인 후 인덱스 변경

len(champ_se_list)

chal_bans_se.index = champ_se_list

chal_bans_se

# # 챔피언 이름으로 인덱스를 바꿔준 챔피언 밴 시리즈를 내림차순으로 저장

chal_bans_se = chal_bans_se.sort_values(ascending=False)

chal_bans_se.head(10).plot.barh()
