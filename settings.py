"""This is used to handle all uncaught exceptions and send notifications to the user flask server if requested
uses imessage.

"""
from library import VERBOSE, notification,network_management,archive,find_servers
import os
import sys
from colorama import Fore, Back, Style, init
import subprocess
init(autoreset=True)

# remove phone number from environment variables
reset_server = [ sys.argv if '-reset' in sys.argv else False][0]
message = [ sys.argv if '-m' in sys.argv else False][0]
delete_phone_number = [ sys.argv if '-remove' in sys.argv else False][0]
send_files = [ sys.argv if '-send' in sys.argv else False][0]
UNIXSCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__) + '/unix-scripts')
DEVICE_SETUP = [ sys.argv if '-setup' in sys.argv else False][0]
SCAN_NETWORK = [ sys.argv if '-scan' in sys.argv else False][0]


# check the for .ana_variables file in the home directory
def create_varibale_file():    
    varibale_file= os.path.expanduser('~/.ana_variables')
    if os.path.exists(varibale_file):
        with open(varibale_file,'r') as f:
            for line in f.readlines():
                if 'phone_number' in line:
                    os.environ['phone_number'] = line.split('=')[1].strip()
                    break
    else:
        print("environment variables not found. creating environment variables")
        os.environ['phone_number'] = input("enter phone number: ")
        with open(varibale_file,'w') as f:
            f.write('phone_number='+os.environ['phone_number'])
    return varibale_file

# check the os if linux or mac
if sys.platform.lower() == 'darwin':
    varibale_file = create_varibale_file()
    if varibale_file and os.environ.get('phone_number'):
        pass
    else:
        print(Fore.RED + "phone number not found in environment variables $ export phone_number=""0000000""\n" +"Add this to your .bash_profile or .bashrc file or path for permanent changes not just session")
        os.remove(varibale_file)
        sys.exit()


    if delete_phone_number:
        os.unsetenv('phone_number')
        os.remove(varibale_file)
        try:
            ask_ = input("close the terminal or restart the shell to see the changes. close the terminal? y/n: ")
            if ask_ == 'y':
                os.system('killall Terminal')
        except:
            # used for windows and linux systems... not tested
            raise Exception ("close the terminal or restart the shell to see the changes")
        sys.exit()
    

def launchctl_setup():
    notification().setup_launchctl()
    notification(f_args='remove_launchctl').setup_launchctl()
    notification(f_args='launch_daemons').setup_launchctl()
    
    
    
def test_notification():
    """setup launchctl and send a message to the user via imessage from the flask server if requested
    """
    launchctl_setup()
    reponse = notification().send_message("it works!")
    if reponse:
        notification().send_media("send_media function is deprecated. use send_alert instead.")


if reset_server and reset_server[1] == '-reset':  # reset server. 
    print("resetting server")  
    test_notification()
elif message:
    
    notification().relay_message([message[2] if message else ""],endpoints='imessage',port=5020,local_server=True)

    


if send_files and send_files[1] == '-send':    
    if send_files[send_files.index('-r') + 1]:
        remote = send_files[send_files.index('-r') + 1]
    else:
        remote = None
        
    if send_files[send_files.index('-local') + 1]:
        local = send_files[send_files.index('-local') + 1]
    else:
        local = None
    hostname = send_files[send_files.index('-device') + 1]
    find_by_IP = [ send_files if '-ip' in send_files else None][0]
    # get all the ip addresses of the devices for flag -ip if there are multiple devices
    if find_by_IP:
        ip_addresses = [ find_by_IP[find_by_IP.index('-ip') + 1:]]
        network_management(hostname=f"{send_files[send_files.index('-device') + 1]}",remote=remote,local=local,IP=ip_addresses)    
        sys.exit() # stop here. no need to continue
    else:
        network_management(hostname=f"{send_files[send_files.index('-device') + 1]}",remote=remote,local=local)    
        sys.exit() # stop here. no need to continue


        
            
if DEVICE_SETUP and DEVICE_SETUP[1] == '-setup':
    # make sure it running linux 
    deviceIs = sys.platform.lower() 
    overide = [ True if '-overide' in DEVICE_SETUP else False][0]
    IP = [ DEVICE_SETUP if '-ip' in DEVICE_SETUP else None][0]
    user = [ DEVICE_SETUP if '-user' in DEVICE_SETUP else None][0]
    password = [ DEVICE_SETUP if '-pass' in DEVICE_SETUP else None][0]
    device_password = [ DEVICE_SETUP if '-pass' in DEVICE_SETUP else None][0]
    if IP:
        addresses = [ DEVICE_SETUP[DEVICE_SETUP.index('-ip') + 1:]]
    else:
        addresses = None
    # options = [ DEVICE_SETUP if '-passless' in DEVICE_SETUP else None][0]
    if '-passless' in DEVICE_SETUP:    
        if deviceIs == 'linux' or  overide:
            if user:
                username = [ DEVICE_SETUP[DEVICE_SETUP.index('-user') + 1:]][0]
            else:
                username = None
            if password:
                password = [DEVICE_SETUP[DEVICE_SETUP.index('-pass') + 1:]][0]
            else:
                password = None
            if VERBOSE:    
                print(Fore.GREEN + "setting up devices" + Fore.RESET)
                print(f"addresses: {addresses} username: {username} password: {password}")
            network_management(hostname=None,IP=addresses,disable_login_password=True, username=username,password=password)
        else:
            print(Fore.RED + "This is recommend on linux  pass -overide flag to continue with your task" + Fore.RESET)
            sys.exit()
    elif '-dev_install' in DEVICE_SETUP:
        if deviceIs == 'linux' or  overide:
            response  = subprocess.call(['bash',UNIXSCRIPT_ROOT+'/setup+linux-devices.sh' ,'install_all'],shell=True,executable='/bin/bash',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            print(response)
            print(Fore.GREEN + "setup complete" + Fore.RESET)
            sys.exit()
        else:
            print(Fore.RED + "This is recommend on linux  pass -overide flag to continue with your task" + Fore.RESET)
            sys.exit()
    elif '-ios' in DEVICE_SETUP:
        attachments = archive()
        if attachments:
            if VERBOSE:
                print(attachments)
        if '-i' in DEVICE_SETUP:
            print('installing required packages')
            attachments.install_required_packages()
        elif '-create' in DEVICE_SETUP:
            print('creating session')
            attachments.create_session
        elif '-archive' in DEVICE_SETUP:
            print('archiving session files please wait')
            attachments.archive
        elif '-clean' in DEVICE_SETUP:
            attachments.close_session()
            print('cleaning up session')
if '-scan' in sys.argv:
    print("scanning network")
    print(find_servers().servers())
    sys.exit()
    # subprocess.call(['bash',UNIXSCRIPT_ROOT+'/setup+linux-devices.sh' ,'install_all'],shell=True,executable='/bin/bash',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # sys.exit()     



#TODO: collect all the todo and write the code.


help_meun = """
-reset: reset the server
-m: send a message to the user
-remove: remove the phone number from the environment variables
-send: send files to the user
    * example: python3 settings.py -send -device "iPhone" -r "/Users/username/Desktop" -local "/Users/username/Desktop file.txt"
    * ana -send -device "iPhone" -r "/Users/username/Desktop" -local "/Users/username/Desktop file.txt"
        ana -send -r /home/ubuntu -local  ana  -device "ubuntu" 
-device: the device name to send files to
-r: remote file path
-local: local file path
- setup: setup devices
    ana  -setup -passless -overide -pass "password" -user "username" -ip " "
- dock -setup -dev_install

"""


docker_meun = """
-docker: entry to this script
-reset: reset the server


docker = [ sys.argv if '-docker' in sys.argv else False][0]
if docker:
    no_args = [ sys.argv if len(sys.argv) == 1 else False][0]
    if no_args:
        print(help_meun)
        
tools = [ sys.argv if '-tools' in sys.argv else False][0]
=========================    
developer_setup
preventSudo
install_conda
install_docker
install_portainer
libreddit
install_node_and_npm
cockpit
install_neofetch
install_java
install_golang

"""



def _entry_point():
    """cli entrypoint"""
    flags_provided = False
    for i in sys.argv:
        if i.startswith("-"):
            flags_provided = True
            break
    if flags_provided:
        docker = [ sys.argv if '-dock' in sys.argv else False][0]
        if docker:
            print(docker_meun)
        pass
    elif flags_provided == False:
        print(help_meun)
        
