from library import notification
import os
import sys



reset_server = [ sys.argv if '-reset' in sys.argv else False][0]
message = [ sys.argv if '-m' in sys.argv else False][0]
def launchctl_setup():
    notification().setup_launchctl()
    notification(f_args='remove_launchctl').setup_launchctl()
    notification(f_args='launch_daemons').setup_launchctl()
def test_notification():
    #.1 setup 
    launchctl_setup()
    #.2 send message    
    reponse = notification().send_message("test_notification notification().send_message")
    if reponse:
        notification().send_media("test_notification notification().send_media")
if reset_server:    
    test_notification()
    

if message:
    notification().relay_message([message[2] if message else "test_notification notification().relay_message"],endpoints='imessage',port=5020,local_server=True)






