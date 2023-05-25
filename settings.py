"""This is used to handle all uncaught exceptions and send notifications to the user flask server if requested
uses imessage.

"""
from library import notification
import os
import sys
from colorama import Fore, Back, Style, init
init(autoreset=True)

# remove phone number from environment variables
reset_server = [ sys.argv if '-reset' in sys.argv else False][0]
message = [ sys.argv if '-m' in sys.argv else False][0]
delete_phone_number = [ sys.argv if '-remove' in sys.argv else False][0]

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

    





def _entry_point():
    """cli entrypoint
    """
    pass