from distutils.core import setup
 
setup(
    name = "reco",
    version = "1.0.0",
    author = "reco",
    author_email = "jspiner@naver.com",
    py_modules=[
        'reco', 
        'common/db_manager',
        'common/mongo_manager',
        'common/util/utils'
    ],
    description = "caly reco lib",
)