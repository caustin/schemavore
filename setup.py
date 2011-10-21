from unittest import TestLoader
from pkg_resources import resource_exists
from pkg_resources import resource_listdir
from setuptools import setup, find_packages

setup(
    name='schemavore',
    package=find_packages('schemavore'),
    package_dir={'':'schemavore'},
    version = '0.0.1',
    licensse = 'LGPL',
    install_requires = [
        'setuptools',
        'lxml',
        'ordereddict',
    ]

)