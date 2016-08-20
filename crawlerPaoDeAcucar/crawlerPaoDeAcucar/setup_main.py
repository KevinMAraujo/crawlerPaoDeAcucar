from distutils.core import setup
import scrapy
import py2exe
#from lxml import _elementhpath as _dummy

includes = ['scrapy', 'os', 'twisted', 'gzip',
             'test', 'zope', 'zope.interface', 'pkgutil', 'lxml','lxml.etree', 'lxml._elementpath',
            'multipart', 'email.mime.multipart', 'email.mime.text',
 ]
#excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
#            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
#            'Tkconstants', 'Tkinter']
excludes = []
packages = ['os', 'twisted',  'test', 'zope', 'zope.interface', 'pkgutil', 'lxml',
                         'lxml.etree', 'lxml._elementpath', 'multipart', 'email.mime.multipart', 'email.mime.text',
            #'scrapy',
                         ]
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']

setup(
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    windows=['main.py']
)