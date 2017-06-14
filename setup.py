from distutils.core import setup

# extractor 
setup(
    name = "extractor",
    version = "1.0.0",
    author = "refgjin",
    author_email = "refgjin@gmail.com",
    py_modules=[
        'extractor/event_extractor', 
        'extractor/common/db_manager'
    ],
    package_data = [('key', ['key/extract_conf.json'])],
    description = "caly extractor lib",
)

# reinforce
setup(
    name = "reinforce",
    version = "1.0.0",
    author = "reionforce",
    author_email = "kkk1140@naver.common",
    py_modules=[
        'reinforce/reinforce', 
        'reinforce/common/db_manager',
        'reinforce/common/mongo_manager',
        'reinforce/common/util/utils'
    ],
    description = "caly reinforce lib",
)

# reco 
setup(
    name = "reco",
    version = "1.0.0",
    author = "jspiner",
    author_email = "jspiner@naver.com",
    py_modules=[
        'reco/reco', 
        'reco/common/db_manager',
        'reco/common/mongo_manager',
        'reco/common/util/utils'
    ],
    description = "caly reco lib",
)