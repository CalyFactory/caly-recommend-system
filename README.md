Caly Recommend Engine 
=========
![build status](https://travis-ci.org/CalyFactory/caly-recommend-system.svg)
[![Coverage Status](https://coveralls.io/repos/github/CalyFactory/caly-recommend-system/badge.svg?branch=master)](https://coveralls.io/github/CalyFactory/caly-recommend-system?branch=master)

testWeb
___
caly의 추천 엔진 그리고 이를 적용할수있는 web버전입니다. 
실제 일정을 입력해보고 추천을 받아볼 수 있습니다. 


```
python3 -m venv
source env/bin/activate
pip3 install -r requirements.txt
python3 webReco.py
```


Naming
* camel : only class
* snake : another all


***Analysis Event Module (NLP)***
---

# Need to next progress

[MeCab binding to python3.x](https://bitbucket.org/eunjeon/mecab-python-0.996)

Install flow

```
virtualenv calyenv
source calyenv/bin/activate
pip3 install -r requirements.txt
npm install
```

start command ( for Web view )

```
python3 app.py
```

Recommand Module
---

Install
```
pip3 install -r requirements.txt
```

Useage
```
from reco import Reco
recoModule = Reco(jsonData, userHashKey)

print(
    recoModule.getRecoList()
)
```



Coverage
---

Recommand Module

```

Name                         Stmts   Miss  Cover
------------------------------------------------
../common/db_manager.py         34     23    32%
../common/mongo_manager.py      13      9    31%
./reco.py                      236     44    81%
./test.py                      235     10    96%
------------------------------------------------
TOTAL                          518     86    83%
```
