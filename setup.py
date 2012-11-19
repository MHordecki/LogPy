from setuptools import setup
from os.path import abspath, dirname, join

readme_fn = join(abspath(dirname(__file__)), 'README.rst')

setup(name='LogPy',
    version = '1.0',
    description = 'Unorthodox logging for python',
    long_description = open(readme_fn).read(),
    author = 'Michal Hordecki',
    author_email = 'mhordecki@gmail.com',
    url = 'http://github.com/MHordecki/LogPy',
    py_modules = ['logpy'],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ]
    )

