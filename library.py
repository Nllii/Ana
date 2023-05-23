# this is used to handle all uncaught exceptions
# import multiStonk
# import distutils
import os
import datetime
import traceback
import settings
from colorama import Fore, Back, Style, init
import subprocess
import re
import sys
import warnings
init(autoreset=True)
__all__ = ['log_exception']

VERBOSE = [ sys.argv if '-v' in sys.argv else False][0]
ANA_ROOT = os.path.abspath(os.path.dirname(__file__))
UNIXSCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__) + '/unix-scripts')






class notification(object):
    def __init__(self,cell_number=None,f_args=None,launchctl_script=None,options=None):
        self.script = launchctl_script or f"{UNIXSCRIPT_ROOT}/launchctl_notification.sh"
        self.arg_options = options or "helloworld.py"
        self.f_args = f_args or "create_plist"
        self.number = cell_number or settings.phone_number
        
    def setup_launchctl(self):
        subprocess.call(['bash', self.script, self.f_args,self.arg_options])
   

    def send_message(self,message):
        if VERBOSE:
            print(Fore.GREEN + message + Fore.RESET)
        if message:
            # escaped_message = re.sub('"', '\\"', message)  # Escape double quotes in message
            command = ['osascript', '-e', f'tell application "Messages" to send "{message}" to buddy "{self.number}" of (service 1 whose service type is iMessage)']        
        subprocess.Popen(command)
        return {"message": "Message sent successfully."}
    
    def send_media(self, message=None, media_files=None):
        _DEPRECATION_MESSAGE = ("This method is deprecated. using send_alert instead...")
        if VERBOSE:
            print(Fore.RED + _DEPRECATION_MESSAGE + Fore.RESET)
        else:
            warnings.warn(_DEPRECATION_MESSAGE, DeprecationWarning, 2)
        return  self.send_message(message=message)
        """
        number = self.number
        if message:
            
            escaped_message = re.sub('"', '\\"', message)  # Escape double quotes in message
            command = [
                'osascript', '-e',
                f'tell application "Messages" to send "{escaped_message}" to buddy "{number}" of (service 1 whose service type is iMessage)'
            ]
            subprocess.Popen(command)

        if media_files:
            for file_path in media_files:
                if os.path.exists(file_path):
                    command = [
                        'osascript', '-e',
                        f'tell application "Messages" to send POSIX file "{file_path}" to buddy "{number}" of (service 1 whose service type is iMessage)'
                    ]
                    subprocess.Popen(command)
                else:
                    print(f"File not found: {file_path}")

        return "Message sent successfully."
        """
        
        
def log_exception(exctype, value, tb):
    """A function to log all unhandled exceptions to a file"""
    now = datetime.datetime.now()
    with open(f'{ANA_ROOT}/debug.log', 'a') as f:
        print(Fore.RED + f"Uncaught exception: {exctype} {value} ")
        f.write(f"{now}:\n")
        traceback.print_exception(exctype, value, tb, file=f)
        notification().send_message(f"Uncaught exception: {exctype} {value} ")

sys.excepthook = log_exception