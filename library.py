# this is used to handle all uncaught exceptions
import os
import datetime
import re
import traceback
from colorama import Fore, Back, Style, init
import subprocess
import sys
import warnings
from backend import connection
import requests



init(autoreset=True)
# __all__ = ['log_exception','notification','network_management','archive','find_servers']


VERBOSE = [True if '-v' in sys.argv else False][0]
ANA_ROOT = os.path.abspath(os.path.dirname(__file__))
UNIXSCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__) + '/unix-scripts')




class find_servers():
    """finds servers on the network"""
    def __init__(self,hostname=None):
        if hostname is None:
            self.devices_name = ['mac','linux','windows','raspberry','Raspberry Pi','ubuntu','debian','Apple']
        else:
            self.devices_name = hostname
            
            
            
            
    def servers(self,verbose=False,IP=None):
        """returns a list of servers on the network

        Returns:
            str: list
        """
        verbose = verbose or VERBOSE
        if IP is None:
            print(Fore.GREEN + "- finding servers on the network this may take a while" + Fore.RESET)
        else:
            return IP
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
                                if verbose:
                                    print(f"found {names} with ip address {device_address}")
                                break
                        except:
                            pass
        if verbose:    
            devices = list(set(found_devices))
            print(f"found {len(devices)} devices on the network with the following ip addresses: ") 
            print(devices,'\n',sep='\n') 
            print()    
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
        if sys.platform.lower() == 'linux':
            if VERBOSE:
                print(Fore.RED + "This method is not supported on linux using flask: try to call this directly next time" + Fore.RESET)
            return self.relay_message(message=message)
        
        if disable_verbose is False:
            pass
        elif VERBOSE:
            print(Fore.GREEN + f"Sending message to {self.number} ({message})" + Fore.RESET)
        else:
            pass

        if message:
            # escaped_message = re.sub('"', '\\"', message)  # Escape double quotes in message
            command = ['osascript', '-e', f'tell application "Messages" to send "{message}" to buddy "{self.number}" of (service 1 whose service type is iMessage)']        
        subprocess.Popen(command)
        return {"message": "Message sent successfully."}
    
    def send_media(self, message=None, media_files=None):
        _DEPRECATION_MESSAGE = "This method is deprecated. using send_message instead... can't send media files yet."
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
        
    def relay_message(self,message,endpoints='imessage',port=5020,local_server=None):
        
        """ sends a message to a server on the network.
        Example:
        notification().relay_message([message[2] if message else "test_notification notification().relay_message"],endpoints='imessage',port=5020,local_server=True)
        
        Args:
            message (str): "a message to send"
            endpoints (str, optional): if you have a different endpoint to use for your message. Defaults to 'imessage'.
            port (int, optional): what port is your server using for messaging. Defaults to 5020.
            local_server (str, optional): if False, it scans LAN and sends out the message to every endpoint on your network. Defaults to True.

        Returns:
            payload = {'message': message}  # Data to be sent in the request's form data
            requests.post(url, data=payload)  # Send POST request
        """
        if sys.platform.lower() == 'linux':
            # set the local_server to false if you are using linux or the user has specified a local server
            local_server = False
        
        relay_url = []
        if (local_server==True): #LOL python is weird awesome; 
            conn = connection.cluster()
            local_address = conn.local_address()
            url = f'http://{local_address}:{port}/{endpoints}'  # Replace with the appropriate URL where your Flask server is running
            relay_url.append(url)
        elif (local_server is False): # only python will allow this type of syntax!
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
                '''  
                # Python code to be executed on the server
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
        
        
        

class network_management(find_servers):
    """using rsync  to send files."""
    def __init__(self,hostname,remote=None,local=None,IP=None,disable_login_password=False,password=None,username=None):
        self.local_path = local
        self.remote_path = remote
        self.name = hostname or None
        self.username = username or 'ubuntu'
        self.password = password or 'ubuntu'
        if IP is None:
            self.IP = None
        else:
            self.IP = IP[0] if isinstance(IP,list) else IP
        super().__init__()
        if disable_login_password is True:
            print(Fore.RED + "disabling password login" + Fore.RESET)
            # print the username and password
            print(Fore.GREEN + f"username: {self.username} password: {password}" + Fore.RESET)
            self.disable_password_login(hostname_address=hostname,username=self.username ,password=password)
            return None # return None to stop the script:
        # else:
        self._send_()
    
    def _send_(self):   
        # use rsync to send files
        # if self.local_path is None or self.local_path == '.':
        #     self.local_path = os.getcwd()
        if self.remote_path is None:
            raise Exception ("- specify a remote path.")
        if self.name is None:
            raise Exception ("- specify a hostname.")
        
        for server in self.servers(IP=self.IP):
            try:
                notification().send_message(f" sending files to  server {server}   {self.name} from {self.local_path} to {self.remote_path}",disable_verbose=True)
                files_ = subprocess.Popen(['rsync', '-avz', self.local_path, f'{self.name}@{server}:{self.remote_path}'], stdout=subprocess.PIPE)
                files_.communicate() # Wait for the process to finish
                
                notification().send_message(f" files sent to  server {server}   {self.name} from {self.local_path} to {self.remote_path}",disable_verbose=True)
                print(Fore.YELLOW + f"files sent to  server {server}   {self.name} from {self.local_path} to {self.remote_path}" + Fore.RESET)
                
                
            except Exception as e:
                # print(e)
                continue
    # i don't think this makes sense to have here.
    
    def disable_password_login(self,hostname_address=None,username='ubuntu',password=None):
        """
        disables password login on a server.
    
        Args:
            hostname_address (str): the hostname or IP address of the server.
            username (str, optional): the username to use. Defaults to 'ubuntu'.
            password (str, optional): the password to use. Defaults to ''.
        """
        self.hostname = []
        if hostname_address is None:
            for server in self.servers(IP=self.IP):
                self.hostname.append(server)

        # print(Fore.YELLOW + f"disabling sudo on {hostname_address}" + Fore.RESET)
        self.password = password[0] if isinstance(password,list) else password

        remove_sudo = connection.cluster()
        if self.IP is None:
            hostname_address = self.hostname
        for hostname_address in self.hostname:
            print(Fore.YELLOW + f"disabling sudo on {hostname_address} with username '{username}' and password {self.password}" + Fore.RESET)
            response = remove_sudo.config_ssh_keygen(hostname_address,username,self.password)
            if response == True:
                print(Fore.GREEN + f"sudo disabled on {hostname_address}" + Fore.RESET)
                notification().send_message(f"sudo disabled on {hostname_address}",disable_verbose=True)
            

            
            
            


class archive:
    def __init__(self, drive= None,src=None, dst=None):
        """archive files to a mounted drive. 

        Args:
            drive (str, optional): the name of the mounted drive. Defaults to '$HOME/ios_archive'.
            src 
            dst (_type_, optional): _description_. Defaults to None.
        """
        self.drive = drive or f"{os.environ['HOME']}/ios_archive"
        
        # check to make sure its the full path
        if not self.drive.startswith('/'):
            self.drive = os.path.join(os.getcwd(), self.drive)
        if not os.path.exists(self.drive):
            print(Fore.YELLOW + f"creating directory {self.drive}" + Fore.RESET)
            os.makedirs(self.drive,exist_ok=True)
        else:
            pass
            # print(Fore.YELLOW + f"directory {self.drive} already exists" + Fore.RESET)        
        self.mounted_drive = os.path.join(os.getcwd(), self.drive) 
        self.logs = os.path.join(self.mounted_drive, 'archive.log')
        locations = [self.mounted_drive, self.logs]
        for location in locations:
            if location.endswith('.log'):
                continue
            if not os.path.exists(location):
                os.makedirs(location,exist_ok=True)
        self.src = src
        self.dst = dst
    def __repr__(self):
        # just return something for verbose
        return f"archive(drive='{self.drive}',src='{self.src}',dst='{self.dst}')"    
    
    
    def install_required_packages(self):
        response =  subprocess.run(['bash', f'{UNIXSCRIPT_ROOT}/setup+ios-devices.sh','packages',f'{self.drive}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        return response
    
    @property
    def create_session(self):
        # use the subprocess module to create a session between the local machine and the remote machine using the bash script provided setup+device.sh
        response =  subprocess.run(['bash', f'{UNIXSCRIPT_ROOT}/setup+ios-devices.sh','create_session',f'{self.drive}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        
    @property
    def archive(self):
        """use the bash script instead
        Args:
            src (str): local path to the file to be archived
            dst (str): remote path to the file to be archived
        """
        # use the subprocess module to create a session between the local machine and the remote machine using the bash script provided setup+device.sh
        response =  subprocess.run(['bash', f'{UNIXSCRIPT_ROOT}/setup+ios-devices.sh','archive',f'{self.drive}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        # write the response to the log file
        self.log = open(self.logs, 'a')
        self.log.write(response.stdout.decode('utf-8'))
        self.log.write("\n")
        self.log.close()

    def close_session(self):
        response =  subprocess.run(['bash',  f'{UNIXSCRIPT_ROOT}/setup+ios-devices.sh','terminate_session'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        # write the response to the log file
        self.log = open(self.logs, 'a')
        self.log.write(response.stdout.decode('utf-8'))
        self.log.write("terminated session and cleaning up the session")
        self.log.write("\n")
        self.log.close()

        



def log_exception(exctype, value, tb):
    """A function to log all unhandled exceptions to a file"""
    now = datetime.datetime.now()
    with open(f'{ANA_ROOT}/debug.log', 'a') as f:
        print(Fore.RED + f"Uncaught exception: {exctype} {value} ")
        f.write(f"{now}:\n")
        traceback.print_exception(exctype, value, tb, file=f)
        notification().send_message(f"Uncaught exception: {exctype} {value} ")
        traceback.print_tb(tb)

sys.excepthook = log_exception