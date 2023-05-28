import os
from re import sub 
import sys
from datetime import datetime
import subprocess
from library import notification


class archive:
    def __init__(self, drive,src=None, dst=None):
        self.mounted_drive = os.path.join(os.getcwd(), drive) 
        self.logs = os.path.join(self.mounted_drive, 'archive.log')
        locations = [self.mounted_drive, self.logs]
        for location in locations:
            if location.endswith('.log'):
                continue
            if not os.path.exists(location):
                os.makedirs(location,exist_ok=True)
        self.src = src
        self.dst = dst
    @property
    def create_session(self):
        # use the subprocess module to create a session between the local machine and the remote machine using the bash script provided setup+device.sh
        response =  subprocess.run(['bash', 'setup+devices.sh','create_session'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        
    @property
    def archive(self):
        """use the bash script instead
        Args:
            src (str): local path to the file to be archived
            dst (str): remote path to the file to be archived
        """
        # use the subprocess module to create a session between the local machine and the remote machine using the bash script provided setup+device.sh
        response =  subprocess.run(['bash', 'setup+devices.sh','archive'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        # write the response to the log file
        self.log = open(self.logs, 'a')
        self.log.write(response.stdout.decode('utf-8'))
        self.log.write("\n")
        self.log.close()

    def clean(self):
        response =  subprocess.run(['bash', 'setup+devices.sh','terminate_session'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(response.stdout.decode('utf-8'))
        # write the response to the log file
        self.log = open(self.logs, 'a')
        self.log.write(response.stdout.decode('utf-8'))
        self.log.write("terminated session and cleaning up the session")
        self.log.write("\n")
        self.log.close()

        




attachments = archive("archive")
attachments.create_session
attachments.archive
attachments.clean()




