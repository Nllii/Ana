# this is used to handle all uncaught exceptions
# import multiStonk
# import distutils
import os
import datetime
import traceback
# import settings
from colorama import Fore, Back, Style, init
import subprocess
import re
import sys
import warnings
from backend import connection
import requests

init(autoreset=True)
__all__ = ['log_exception','notification']


VERBOSE = [True if '-v' in sys.argv else False][0]
ANA_ROOT = os.path.abspath(os.path.dirname(__file__))
UNIXSCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__) + '/unix-scripts')




class find_servers():
    """finds servers on the network"""
    def __init__(self,device_name=None):
        if device_name is None:
            self.devices_name = ['mac','linux','windows','raspberry','Raspberry Pi','ubuntu','debian','Apple']
        else:
            self.devices_name = device_name
            
    def servers(self):
        """returns a list of servers on the network

        Returns:
            str: list
        """
        conn = connection.cluster()
        devices = conn.scan_network()
        found_devices = []
        for information in devices:
            for mac_address, vendor in information['vendor'].items():
                for names in self.devices_name:
                    if names in vendor:
                        try:
                            network_address = information['addresses']
                            for version in network_address:
                                device_address = network_address[version]
                                found_devices.append(device_address)
                                break
                        except:
                            pass
        return found_devices
    




class notification(object):
    def __init__(self,cell_number=None,f_args=None,launchctl_script=None,options=None):
        self.script = launchctl_script or f"{UNIXSCRIPT_ROOT}/launchctl_notification.sh"
        self.arg_options = options or "helloworld.py"
        self.f_args = f_args or "create_plist"
        # read the phone number from the environment variable
        self.number = cell_number or os.environ.get('phone_number')
        # self.number = cell_number or settings.phone_number
        
    def setup_launchctl(self):
        subprocess.call(['bash', self.script, self.f_args,self.arg_options])
   

    def send_message(self,message=None,disable_verbose=False):
        if disable_verbose is False:
            pass
        elif VERBOSE:
            print(Fore.RED + f"Sending message to {self.number} ({message})" + Fore.RESET)
        else:
            pass

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
        
    def relay_message(self,message,endpoints='imessage',port=5020,local_server=True):
        
        """ sends a message to a server on the network.
        Example:
        notification().relay_message([message[2] if message else "test_notification notification().relay_message"],endpoints='imessage',port=5020,local_server=True)
        
        Args:
            message (str): "a message to send"
            endpoints (str, optional): if you have a different endpoint to use for your message. Defaults to 'imessage'.
            port (int, optional): what port is your server using for messaging. Defaults to 5020.
            local_server (str, optional): if False, it scans LAN and sends out the message to every endpoint on your network. Defaults to True.

        Returns:
            _type_: _description_
        """
        
        # list_servers = find_servers()
        relay_url = []
        if (local_server==True): #LOL python is weird awesome; 
            conn = connection.cluster()
            local_address = conn.local_address()
            url = f'http://{local_address}:{port}/{endpoints}'  # Replace with the appropriate URL where your Flask server is running
            relay_url.append(url)
        elif (local_server is False):
            servers = find_servers()
            listed_servers = [found_server for found_server in servers.servers()]
            for server in listed_servers:    
                url = f'http://{server}:{port}/{endpoints}'
                relay_url.append(url)
        for message_url in relay_url:
            try: 
                code = '''
                def multiply(a, b):
                    return a * b

                result = multiply(5, 10)
                print(result)
                '''  # Python code to be executed on the server
                # command = 'ls -l'  # Command to be executed on the server
                # payload = {'code': code}  # Data to be sent in the request's form data
                payload = {'message': message}  # Data to be sent in the request's form data
                response = requests.post(message_url, data=payload)
                if response.status_code == 200:
                    print(Fore.GREEN + "Message sent successfully." + Fore.RESET)
                else:
                    print(Fore.RED + "Error executing command. Server response:" + Fore.RESET)
            except Exception as e:
                continue
        
        
        

class send_data(find_servers):
    """using rsync  to send files."""
    def __init__(self,hostname,remote=None,local=None):
        self.local_path = local
        self.remote_path = remote
        self.name = hostname or None
        super().__init__()
        self._send_()
    
    def _send_(self):   
        # use rsync to send files
        # if self.local_path is None or self.local_path == '.':
        #     self.local_path = os.getcwd()
        if self.remote_path is None:
            raise Exception ("- specify a remote path.")
        if self.name is None:
            raise Exception ("- specify a hostname.")
        print(self.local_path)
        
        for server in self.servers():
            try:
                notification().send_message(f" sending files to  server {server}   {self.name} from {self.local_path} to {self.remote_path}",disable_verbose=True)
                files_ = subprocess.Popen(['rsync', '-avz', self.local_path, f'{self.name}@{server}:{self.remote_path}'], stdout=subprocess.PIPE)
                files_.communicate() # Wait for the process to finish
                
                notification().send_message(f" files sent to  server {server}   {self.name} from {self.local_path} to {self.remote_path}",disable_verbose=True)
                
                
            except Exception as e:
                # print(e)
                continue











def log_exception(exctype, value, tb):
    """A function to log all unhandled exceptions to a file"""
    now = datetime.datetime.now()
    with open(f'{ANA_ROOT}/debug.log', 'a') as f:
        print(Fore.RED + f"Uncaught exception: {exctype} {value} ")
        f.write(f"{now}:\n")
        traceback.print_exception(exctype, value, tb, file=f)
        notification().send_message(f"Uncaught exception: {exctype} {value} ")

sys.excepthook = log_exception