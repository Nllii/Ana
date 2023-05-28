from paramiko import SSHClient, AutoAddPolicy
import os
import re
import subprocess
from colorama import Fore, Back, Style, init
import platform
import nmap
import random
import sys



project_directory = os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.dirname(project_directory)
sys.path.append(parent_directory)
found_devices = list()

class cluster(object):
    def __init__(self,inventory=None):
        self.ssh_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        self.file = inventory
        self.project_dir = parent_directory
        self.hosts = None
        

    def get_mac_address(self):
        if sys.platform == "darwin":
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


    #TODO: save the ip address of the server to file nvm... just request it everytime
    def local_address(self):
        if platform.system().lower() == "linux":
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

    # @property #TODO: enable this property or remove it in the future
    def scan_network(self,get_host='ubuntu',host_range=False):
        """scan the network and find the ip address of the server
        *  get_host as an argument to find the ip address of the server names : ubuntu is the default host name
        """
        try:
            nm = nmap.PortScanner()
        except Exception as e:
            print('Nmap not found', sys.exc_info()[0])
            if platform.system() == "Linux":
                print("Please install nmap using 'sudo apt-get install nmap -y'")
            elif platform.system() == "Darwin":
                print("Please install nmap using 'brew install nmap'")
                sys.exit(1)
            else:
                print("Please install nmap")
                sys.exit(1)
        
        if host_range == True:
            nm.scan(hosts=f'{self.local_address()}/24', arguments='-n -sP -PE -PA21,23,80,3389',sudo=True)
        else:
            nm.scan(hosts=f'{self.local_address()[:-1]}0-10', arguments='-n -sP -PE -PA21,23,80,3389',sudo=True)
            
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for host, status in hosts_list:
            try:
                found_devices.append(nm[host])
            except Exception as e:
                continue
        if found_devices == {} or found_devices == []:
            print(Fore.RED + f"No server found on the network with the name {get_host} and the host range {host_range}" + Fore.RESET)
            if host_range == False:
                print(Fore.RED + f"Trying again.." + Fore.RESET)
                self.scan_network(get_host=get_host,host_range=True)

            else:
                print(Fore.RED + f"could not figure out the host...  check the host range and manually set it" + Fore.RESET)
                sys.exit(1)
        return found_devices
    '''
    TODO: OLD CODE from ansible library. Delete this code in the future. 
    def save_inventory(self,inventory_file, group_name, host_vars):
        with open(inventory_file, 'a') as f:
            f.write(f'\n[{group_name}:children]\n')
            f.write(f'{host_vars["name"]} ansible_host={host_vars["ansible_host"]}')
            for key in host_vars:
                if key == 'ansible_host' or key == 'name':
                    continue
                f.write(f' {key}={host_vars[key]}')
            f.write('\n')
        return True

    def get_host_vars(self,inventory_file, group_name, address,user='ubuntu',password=None):
        with open(inventory_file, 'r') as f:
            host_vars = {}
            found_group = False
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    group = line[1:-1]
                    if group == group_name:
                        found_group = True
                        continue
                    if group == f"{group_name}:children":
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith('['):
                                # end of group or start of another group, exit loop
                                break
                            # check for comments and skip that line
                            if line.startswith('#') or line.startswith(';'):
                                # print(line)
                                continue
                            
                            for item in line.split():
                                if '=' not in item:
                                    continue                            
                                key, value = item.split('=')
                                if key == 'ansible_host' and value == address:
                                    host_vars['ansible_host'] = value
                                    continue
                                if key == 'ansible_user' and value == user:
                                    host_vars['ansible_user'] = value
                                    continue
                                if key == 'ansible_password' and value == password:
                                    host_vars['ansible_password'] = value
                                    continue
                                if key == 'name':
                                    host_vars['name'] = value
                                    continue
                                if key == 'group_name' and value == group_name:
                                    host_vars['group_name'] = value
                                    continue
                                host_vars[key] = value
                            
                            return host_vars
                                    

            if found_group == False:
                print("group not found check inventory file and create it")
                return False

            host_vars['name'] = self.assign_server_name()
            host_vars['ansible_host'] = address
            host_vars['ansible_user'] = user
            host_vars['ansible_password'] = password
            host_vars['group_name'] = group_name
            self.save_inventory(inventory_file, group_name, host_vars)            
            return host_vars
    def inventory(self,ansible_host,ansible_user='ubuntu',password='ubuntu',groups=None):   
        if groups == None:
            return False
        # device_vendor = self.get_mac_address().decode()
        # def get_host_vars(self,inventory_file, group_name, address,user='ubuntu',password=None):
        host_var = self.get_host_vars(self.file, groups, ansible_host, ansible_user, password)
        return host_var
        
        '''


    def perform_scans(self,hosts='ubuntu',verbose=False):
        """
        This function will search for the following servers on the network and display them
        - Defualt hosts is called ubuntu
        - Master Server (Master Server)
        - Slave Server (Slave Server)
        """
        print(Fore.GREEN + "Searching devices on the network on the network" + Fore.RESET)
        ping = self.scan_network(get_host=hosts)
        if ping == False:
            return False
        else:
            if verbose:
                print(Fore.GREEN + "Found the following devices on the network" + Fore.RESET)
        for device in ping:
            print(Fore.GREEN + f"Device: {device['hostname']} IP Address: {device['addresses']['ipv4']}" + Fore.RESET)
        return ping

    
    

    # THIS IS AN IMPORTANT FUNCTION
    def config_ssh_keygen(self,hostname_address,username,password):
        """Add SSH key to remote server to allow passwordless login"""
        # Generate an SSH key pair on the local machine
        ssh_keygen_cmd =  ['ssh-keygen', '-t', 'rsa', '-N', '', '-f', f'{os.path.expanduser("~")}/.ssh/id_rsa']
        # subprocess.run(ssh_keygen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # check if password is set or list and if not set then generate ssh key
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
            print(f"Unable to connect to remote server. Please check the IP address {hostname_address} {username} {password} and try again.")
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
        return True
