import os
from setuptools import setup
import configparser
directory = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


config.read(os.path.join(directory, 'account.ini'))
VERSION = config['development']['version']

setup(
    name='Ana',
    version=VERSION,
    description='Ana is an assistant for managing raspberry pi and other devices using [Linux]',
    long_description=long_description,
    keywords='assistant', 
    author='Nii Golightly',
    py_modules=['ana'],
    entry_points={
        'console_scripts': [
            'ana=ana:management',

        ],
        
    },
    
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: assistant :: management',
    ]


)