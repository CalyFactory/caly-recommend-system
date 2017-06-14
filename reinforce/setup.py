from distutils.core import setup
 
setup(
    name = "reinforce",
    version = "1.0.0",
    author = "reionforce",
    author_email = "kkk1140@naver.common",
    py_modules=[
        'reinforce', 
        'common/db_manager',
        'common/mongo_manager',
        'common/util/utils'
    ],
    description = "caly reinforce lib",
)