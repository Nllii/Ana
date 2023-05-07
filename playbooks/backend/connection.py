from paramiko import SSHClient, AutoAddPolicy
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

# import time
import os
import re
# from fabric2 import Connection, Config
# from invoke import Responder
import subprocess
from playbooks.backend import extras
import configparser
import platform
import socket
import nmap
import random
import json
import sys

class cluster(object):
    def __init__(self,inventory=''):
        self.ssh_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        self.project_dir = extras.main_directory
        self.found_mothership = self.inventory(file=inventory,username='mothership')
        
        
        



    def get_mac_address(self):
        if sys.platform == "darwin" or "Darwin":
            # macOS
            output = subprocess.check_output(["ifconfig", "en0"])
            mac_address_search = re.search(r'ether (\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', output.decode())
            if mac_address_search:
                mac_address = mac_address_search.group(1).encode()
            else:
                mac_address = None
        else:
            # Linux
            output = subprocess.check_output(["ip", "link", "show", "eth0"])
            mac_address_search = re.search(r'ether (\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', output.decode())
            if mac_address_search:
                mac_address = mac_address_search.group(1).encode()
            else:
                mac_address = None
        return mac_address


        
    def local_address(self):
        if platform.system() == "Linux":
            result = subprocess.run("ip addr show | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}' | cut -f1 -d'/'", shell=True, capture_output=True, text=True)
            ip = result.stdout.strip()
        elif platform.system() == "Darwin":
            result = subprocess.run("ifconfig | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -v 127.0.0.1 | head -1 | awk '{ print $2 }'", shell=True, capture_output=True, text=True)
            ip = result.stdout.strip()
        else:
            ip = None
        return ip


    def assign_server_name(self):
        with open('/usr/share/dict/words', 'r') as f:
            word_list = [word.strip() for word in f.readlines()]
        # Create a random name for the server
        server_name = random.choice(word_list)    
        return server_name


    def scan_network(self,get_host='ubuntu',host_range='192.168.1.0/24'):
        """scan the network and find the ip address of the server
        * get_host as an argument to find the ip address of the server
        Default is ubuntu
        """
        UBUNTU_LOCAL_IP = []
        try:
            nm = nmap.PortScanner()
        except nmap.PortScannerError:
            print('Nmap not found', sys.exc_info()[0])
            if platform.system() == "Linux":
                print("Please install nmap using 'sudo apt-get install nmap'")
            elif platform.system() == "Darwin":
                print("Please install nmap using 'brew install nmap'")
                sys.exit(1)
                
        nm.scan(hosts=host_range, arguments='-n -sP -PE -PA21,23,80,3389')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        count = 0
        for host, status in hosts_list:
            count += 1
            try:
                name = socket.gethostbyaddr(host)[0]
            except socket.herror:
                name = ''
            if get_host in name:
                UBUNTU_LOCAL_IP.append(host)
            if count == 5:
                break
            print('{0}:{1}:{2}'.format(host, status, name))
            
        if UBUNTU_LOCAL_IP == []:
            print(extras.output(f"No server found on the network with the name {get_host} and the host range {host_range},please manually config them in your inventory file",color='red'))
            return False
        return UBUNTU_LOCAL_IP
    
        
        # connected = self.clusters()


    def clusters(self,update_cluster=False,hosts='ubuntu'):
        """
        This function will search for the following servers on the network:
        - Defualt hosts is called ubuntu
        - Mothership Server (Main Master Server) manually configure this server: 
        - Master Server (Master Server)
        - Slave Server (Slave Server)
        """

        print(extras.output(f"Searching for the mothership server on the network",color='red'))
        ping = self.scan_network(get_host=hosts)
        if ping == False:
            return False
    
    
        
    def inventory(self,ansible_user='ubuntu',username=None,password='ubuntu',read_inventory=False,file=''):    
        is_address = self.get_mac_address().decode()
        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=[file])
        host = inventory.get_host(username)
        disabled = host.vars['disable']
        mac_address = host.vars['mac_address']
        if mac_address != is_address:
            print(extras.output(f"Your mac address is {is_address} and the mac address in the inventory file is {mac_address},please manually config them in your inventory file",color='red'))
            return False
        if disabled:
            print(extras.output(f"{username} is disabled:",color='red'))
        self.clusters()
        
        
    

    def config_ssh_keygen(self,hostname_address,username,password):
        """Add SSH key to remote server to allow passwordless login"""
        # Generate an SSH key pair on the local machine
        ssh_keygen_cmd =  ['ssh-keygen', '-t', 'rsa', '-N', '', '-f', f'{os.path.expanduser("~")}/.ssh/id_rsa']
        # subprocess.run(ssh_keygen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(ssh_keygen_cmd)
        # Copy the public key to the remote server
        public_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        with open(public_key_path, "r") as f:
            public_key = f.read()
        # copy the public key to the remote server without using ssh-copy-id
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            ssh.connect(hostname=hostname_address, username=username, password=password,timeout=10)
        except:
            print(f"Unable to connect to remote server. Please check the IP address {hostname_address} and try again.")
            return hostname_address
        
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'mkdir -p ~/.ssh && echo "{public_key}" >> ~/.ssh/authorized_keys')
        ssh_stdin.channel.shutdown_write()
        ssh_stdin.channel.recv_exit_status()
        print("SSH key added to remote server.")
        
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo nano /etc/ssh/sshd_config')
        ssh_stdin.write('PasswordAuthentication no\n')
        ssh_stdin.flush()
        ssh_stdin.channel.shutdown_write()
        ssh_stdin.channel.recv_exit_status()
        ssh.close()
        print("SSH key added and password-based authentication disabled on remote server.")

    def ansible(self,playbook=None,script=None):
        if script != None:
            print(extras.output(f"Running tasks {script} ",color='red'))
            subprocess.call(['bash', f'{self.project_dir}/playbooks/scripts/{script}.sh'])
            return True
            
        # ansible-playbook -i  server playbooks/send_script.yml -e 'ansible_become_password=ch1ris23' -K -vvv
        subprocess.run(['ansible-playbook', '-i', 'server.ini', f'playbooks/{playbook}.yml', '-e', 'ansible_become_password=ch1ris23', '-K', '-vvv'])
        
        
            
    

