import os
from setuptools import setup
import configparser
directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

__version__ = '0.0.1'

setup(
    name='Ana',
    version=__version__,
    description='Ana is an assistant for managing raspberry pi and other devices using [Linux]',
    long_description=long_description,
    keywords='assistant', 
    author='Nii Golightly',
    py_modules=['ana'],
    entry_points={
        'console_scripts': [
            'ana=settings.py',

        ],
        
    },
    
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools']


)