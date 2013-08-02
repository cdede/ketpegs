import sys

from distutils import sysconfig
from distutils.core import setup

try:
    import os
except:
    print ('')
    sys.exit(0)

setup(
    name = "ketpegs",
    author = "",
    author_email = "",
    version = "0.8.94",
    license = "GPL3",
    description = "A pegs game using the curses library",
    long_description = "README",
    url = "http://github.com/cdede/ketpegs/",
    platforms = 'POSIX',
    packages = ['ktpgs' , 'ktpgs.base' ],
    data_files = [  ('share/doc/ketpegs', ['README', 'COPYING']),
        ('share/ketpegs',['config.json','test_1.py' ]) ,
        ],
    scripts = ['ketpegs']
)
