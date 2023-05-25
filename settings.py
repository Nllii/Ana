"""This is used to handle all uncaught exceptions and send notifications to the user flask server if requested
uses imessage.

"""
from library import notification,send_data
import os
import sys
from colorama import Fore, Back, Style, init
init(autoreset=True)

# remove phone number from environment variables
reset_server = [ sys.argv if '-reset' in sys.argv else False][0]
message = [ sys.argv if '-m' in sys.argv else False][0]
delete_phone_number = [ sys.argv if '-remove' in sys.argv else False][0]
send_files = [ sys.argv if '-send' in sys.argv else False][0]

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
    send_data(hostname=f"{send_files[send_files.index('-device') + 1]}",remote=remote,local=local)    
            
    



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
"""



def _entry_point():
    """cli entrypoint
    
    """
    flags_provided = False
    for i in sys.argv:
        if i.startswith("-"):
            flags_provided = True
            break
    if flags_provided:
        pass
    elif flags_provided == False:
        print(help_meun)
