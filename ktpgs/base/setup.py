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
    version = "0.9.35",
    license = "GPL3",
    description = "A thicket and pegs game using the curses",
    long_description = "README",
    url = "http://github.com/cdede/ketpegs/",
    platforms = 'POSIX',
    packages = ['ktpgs' , 
        'ktpgs.base',
        'ktpgs.other',
        'ktpgs.tests',
        ],
    data_files = [  ('share/doc/ketpegs', ['README', 'COPYING']),
        ('share/ketpegs',['config.json', ]) ,
        ],
    scripts = ['ketpegs']
)
