from library import notification
# TODO: fix this.

def launchctl_setup():
    notification().setup_launchctl()
    notification(f_args='remove_launchctl').setup_launchctl()
    notification(f_args='launch_daemons').setup_launchctl()
    # notification(f_args='load_launchctl').setup_launchctl()
def test_notification():
    #.1 setup 
    launchctl_setup()
    #.2 send message    
    reponse = notification().send_message("test_notification notification().send_message")
    if reponse:
        notification().send_media("test_notification notification().send_media")
    


# test_notification()



