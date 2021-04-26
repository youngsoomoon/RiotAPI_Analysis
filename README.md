# :mag:RiotAPI를 이용한 League Of Legend 게임 데이터 분석
RiotApi로부터 각 리그당 (아이언 ~ 챌린저) 2만여개의 데이터를 가져와 mongoDB에 저장 후,
게임 데이터를 분석한다.
* 'firstBlood를 따면 패배한다'라는 속설을 검증
* firstBlood, firstTower, firstInhibitor, firstDragon 이라는 4가지 요소로 승/패 데이터 분석
* 챌린저 리그 챔피언 밴 데이터 분석

## 개발환경

```
🔶 Jupyter
    🍃 Pymongo
    🐼  Pandas
    🧮  Numpy
    📊  matplotlib
    📊  seaborn
    🌏  Requests
🍃 mongoDB
📤 Riot API
```

## :eyes: Riot Developer Potal에 접속하여 RiotAPI에 접근
* [:earth_asia: 라이엇 개발자 포털](https://developer.riotgames.com/)
![image](https://user-images.githubusercontent.com/74235867/115826093-59ba1c80-a445-11eb-813b-3c37f40fb274.png)

## :leaves: RiotAPI로부터 받아온 데이터를 mongoDB에 저장
![image](https://user-images.githubusercontent.com/74235867/115830595-7d806100-a44b-11eb-8e66-5f375fd87ce8.png)

## :open_file_folder: 게임 데이터 접근
![image](https://user-images.githubusercontent.com/74235867/115831289-5bd3a980-a44c-11eb-8ad9-9e6e2bc5a21b.png)

## :mag: '퍼스트 블러드를 따면 패배한다' 가설 검증
![image](https://user-images.githubusercontent.com/74235867/115831716-f03e0c00-a44c-11eb-9471-3ca9e41a1520.png)

## :bar_chart: 챌린저 게임데이터 4가지 요소로 분석
![image](https://user-images.githubusercontent.com/74235867/115831842-1663ac00-a44d-11eb-89a3-988d3ef2b142.png)

## :mag: 챌린저 챔피언 밴 분석
![image](https://user-images.githubusercontent.com/74235867/115831941-37c49800-a44d-11eb-9720-5f1cd0e8b860.png)
![image](https://user-images.githubusercontent.com/74235867/115831967-414e0000-a44d-11eb-8536-5c782d2f4c06.png)

