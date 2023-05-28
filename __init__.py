__version__ = '0.0.1'
__author__ = 'Nii Golightly'
ana_man = """
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

-docker: entry to this script
-reset: reset the server


docker = [ sys.argv if '-docker' in sys.argv else False][0]
if docker:
    no_args = [ sys.argv if len(sys.argv) == 1 else False][0]
    if no_args:
        print(help_meun)
        
# TODO: add tools to the cli

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
