#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os.path
import warnings
import sys

try:
    from setuptools import setup, Command
    setuptools_available = True
except ImportError:
    from distutils.core import setup, Command
    setuptools_available = False
from distutils.spawn import spawn

try:
    # This will create an exe that needs Microsoft Visual C++ 2008
    # Redistributable Package
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print('Cannot import py2exe', file=sys.stderr)
        exit(1)

py2exe_options = {
    'bundle_files': 1,
    'compressed': 1,
    'optimize': 2,
    'dist_dir': './bin_win32',
    'dll_excludes': ['w9xpopen.exe', 'crypt32.dll'],
}

# Get the version from yt_dlp/version.py without importing the package
exec(compile(open('yt_dlp/version.py').read(),
             'yt_dlp/version.py', 'exec'))

DESCRIPTION = 'YouTube video downloader'
LONG_DESCRIPTION = 'Command-line program to download videos from YouTube.com and other video sites'

py2exe_console = [{
    'script': './yt_dlp/__main__.py',
    'dest_base': 'yt-dlp',
    'version': __version__,
    'description': DESCRIPTION,
    'comments': LONG_DESCRIPTION,
    'product_name': 'yt-dlp',
    'product_version': __version__,
}]

py2exe_params = {
    'console': py2exe_console,
    'options': {'py2exe': py2exe_options},
    'zipfile': None
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    params = py2exe_params
else:
    files_spec = [
        ('etc/bash_completion.d', ['yt-dlp.bash-completion']),
        ('etc/fish/completions', ['yt-dlp.fish']),
        ('share/doc/yt_dlp', ['README.txt']),
        ('share/man/man1', ['yt-dlp.1'])
    ]
    root = os.path.dirname(os.path.abspath(__file__))
    data_files = []
    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn('Skipping file %s since it is not present. Type  make  to build all automatically generated files.' % fn)
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {
        'data_files': data_files,
    }
    if setuptools_available:
        params['entry_points'] = {'console_scripts': ['yt-dlp = yt_dlp:main']}
    else:
        params['scripts'] = ['bin/yt-dlp']

class build_lazy_extractors(Command):
    description = 'Build the extractor lazy loading module'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        spawn(
            [sys.executable, 'devscripts/make_lazy_extractors.py', 'yt_dlp/extractor/lazy_extractors.py'],
            dry_run=self.dry_run,
        )

setup(
    name='yt_dlp',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/ytdl-org/yt-dlp',
    author='Ricardo Garcia',
    author_email='ytdl@yt-dl.org',
    maintainer='Sergey M.',
    maintainer_email='dstftw@gmail.com',
    license='Unlicense',
    packages=[
        'yt_dlp',
        'yt_dlp.extractor', 'yt_dlp.downloader',
        'yt_dlp.postprocessor'],

    # Provokes warning on most systems (why?!)
    # test_suite = 'nose.collector',
    # test_requires = ['nosetest'],

    classifiers=[
        'Topic :: Multimedia :: Video',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    cmdclass={'build_lazy_extractors': build_lazy_extractors},
    **params
)
