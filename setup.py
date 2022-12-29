#!/usr/bin/env python3
from pathlib import Path
from setuptools import setup

with open(Path(__file__).parent / 'README.md', 'r') as stream:
    long_description = stream.read()

about={}
with open('apyllo/__version__.py', 'r') as stream:
    exec(stream.read(), about)

setup(
    name = 'apyllo',
    version = about['__version__'],
    author = 'about['__author__'],
    license='GPLv3',
    description=('A Discord bot for displaying status of a game server.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/Kexanone/apyllo',
    keywords='discord bot game server status query',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8'
    ],
    packages=['apyllo'],
    python_requires=">=3.8.*"
)
