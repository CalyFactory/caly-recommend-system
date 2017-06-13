Caly Recommend Engine 
=========
![build status](https://travis-ci.org/CalyFactory/caly-recommend-system.svg)
[![Coverage Status](https://coveralls.io/repos/github/CalyFactory/caly-recommend-system/badge.svg?branch=recommender)](https://coveralls.io/github/CalyFactory/caly-recommend-system?branch=recommender)


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
Name      Stmts   Miss  Cover
-----------------------------
reco.py     261     98    62%
test.py     110      8    93%
-----------------------------
TOTAL       371    106    71%
```