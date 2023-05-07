
import os
import sys
import configparser
import datetime
from playbooks.backend import extras
import argparse
import subprocess


DEBUG = [True if '-d' in sys.argv else False][0]
CURRENT_WORKING_DIR = os.getcwd()
__version__ = '0.0.1'

def management():
    parser = argparse.ArgumentParser(description=f'v{__version__} Ana an assistant to help with the management of projects and tasks')
    parser.add_argument('-p','--path', action='store_true', help='show the path of the ana directory')
    parser.add_argument('-cd','--change_dir', action='store_true', help='show the path of the ana config file')
    parser.add_argument('-d','--null', action='store_true', help='show the version of ana')
    parser.add_argument('-push','--push', action='store_true', help='show the version of ana')


    args = parser.parse_args()
    if args.path:
        if DEBUG:
            print(extras.output(f'{extras.main_directory}', color='white'))
            print(extras.output(f'calling from current working directory: {CURRENT_WORKING_DIR}', color='yellow'))
        if args.change_dir:
            subprocess.call(f'bash {extras.main_directory}/playbooks/scripts/change_dir.sh {extras.main_directory}', shell=True)
        sys.exit(0)
    if args.push:
        subprocess.call(f'bash {extras.main_directory}/playbooks/scripts/git_push.sh {extras.main_directory}', shell=True)
        sys.exit(0)
    
        
        


    if not len(sys.argv) > 1:
        parser.print_help()
        print('\n -d for debug mode \n -vvv for verbose mode')    
        sys.exit(1)
        
    

    