import sys
from setuptools import setup

if sys.version_info < (2, 7):
    raise NotImplementedError("Sorry, you need at least Python 2.7 or Python 3.6+ to use bottle.")

import phuse

setup(name='phuse',
      version=phuse.__version__,
      description='Fast and simple WSGI-framework for small web-applications.',
      long_description=phuse.__doc__,
      long_description_content_type="text/markdown",
      author=phuse.__author__,
      author_email='rayan.m.haddad@proton.me',
      py_modules=['phuse'],
      scripts=['phuse.py'],
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   ],
      )