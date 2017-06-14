from distutils.core import setup
 
setup(
    name = "extractor",
    version = "1.0.0",
    author = "refgjin",
    author_email = "refgjin@gmail.com",
    py_modules=[
        'extractor', 
        'common/db_manager'
    ],
    description = "caly extractor lib",
)