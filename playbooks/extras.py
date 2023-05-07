import os
import sys
import argparse
import configparser
import datetime
import traceback
import subprocess



__version__  = '0.0.1'
__last_modification__ = '05-06-2023'
__author__ = 'Christian Nii Lantey Golightly'

project_directory = os.path.abspath(os.path.dirname(__file__))
main_directory = os.path.dirname(project_directory)




def output(st, color, background=False, bright=False): 
    """
    use a print() function to print colored text to the terminal:
    Args:
        color ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        background (bool, optional): Defaults to False.
        bright (bool, optional): Defaults to False.
    Returns:    
    - ref: https://github.com/geohot/tinygrad/blob/d26345595d8359c8e0f49fa5645c33f2b9a6b12d/tinygrad/helpers.py#L9
    """
    # print(f"\u001b[{10*background+60*bright+30+['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color)}m{st}\u001b[0m")
    return f"\u001b[{10*background+60*bright+30+['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color)}m{st}\u001b[0m"  # replace the termcolor library with one line


def log_exception(exctype, value, tb):
    """A function to log all unhandled exceptions to a file"""
    now = datetime.datetime.now()
    # if not os.path.exists(f'{main_directory}/debug.log'):
    #     with open(f'{main_directory}/debug.log', 'w') as f:
    #         f.write(f"{now}:\n")
    #         traceback.print_exception(exctype, value, tb, file=f)
            
    with open(f'{main_directory}/debug.log', 'a') as f:
        print(output(f"Uncaught exception: {exctype} {value}", color='red', bright=True))
        f.write(f"{now}:\n")
        traceback.print_exception(exctype, value, tb, file=f)



sys.excepthook = log_exception
