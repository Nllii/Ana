#!/bin/bash
set -x
set -e
cd $HOME # everything in this script is relative to the home directory make sure you are in the home directory
# TODO: clean up this script so that it is more modular and ssh executable
# check if we are in the home directory
if [ ! -d "$HOME" ]; then
    echo "You are not in the home directory"
    exit 1
fi

developer_setup(){
    sudo apt-get update -y
    sudo apt-get upgrade -y
    sudo apt-get install -y build-essential
    sudo apt-get install clang -y


}

preventSudo() {
    disable_sudo_username=$(whoami)
    sudo cp /etc/sudoers /etc/sudoers.bak
    sudo bash -c "echo '$disable_sudo_username ALL=(ALL) NOPASSWD: ALL' | (EDITOR='tee -a' visudo)"
}

install_golang()
{
    sudo apt install golang -y

}
#!/bin/bash

install_docker() {
    if ! command -v docker &>/dev/null; then
        # Remove any existing Docker installations
        sudo apt-get remove docker docker-engine docker.io containerd runc

        # Install dependencies
        sudo apt-get update
        sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

        # Add Docker GPG key
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

        # Add Docker repository
        echo "deb [arch=arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        # Install Docker
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io

        # Add user to docker group
        sudo usermod -aG docker $USER

        echo "Docker installed successfully."
    else
        echo "Docker is already installed."
    fi

    if ! command -v docker-compose &>/dev/null; then
        # Install Docker Compose
        sudo apt-get install -y curl
        sudo curl -sSL https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose

        echo "Docker Compose installed successfully."
    else
        echo "Docker Compose is already installed."
    fi
}



install_portainer(){
    if [[ "$(sudo docker image ls -q portainer/portainer-ce)" ]]; then
        echo "Portainer is installed"
    else
        echo "Portainer is not installed"
        sudo docker volume create portainer_data
        sudo docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
    fi

}





install_node_and_npm(){
    # check if node command exists
    if [ ! -x "$(command -v node)" ]; then
        echo "installing node"
        sudo apt install nodejs -y
    else
        echo "node is already installed"
    fi
    # check if npm command exists
    if [ ! -x "$(command -v npm)" ]; then
        echo "installing npm"
        sudo apt install npm -y
    else
        echo "npm is already installed"
    fi

}





mount_ssd(){
    # find the ssd device and mount it, do not change ownership: https://askubuntu.com/questions/113733/how-do-i-correctly-mount-a-ntfs-partition-in-etc-fstab
    # device=$(lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT | grep -i sda1 | awk '{print $1}')

    if [ ! -d "$HOME/extenal_drive" ]; then
        echo "mounting ssd"
        mkdir $HOME/extenal_drive
        sudo mount /dev/sda1 $HOME/extenal_drive
    else
        echo "ssd is already mounted"
    fi
}

libreddit(){
    # https://github.com/libreddit/libreddit
    device=$(uname -m)
    # docker pull libreddit/libreddit
    # docker run -d --name libreddit -p 80:8080 libreddit/libreddit
    # sudo docker stop libreddit
    # sudo docker rm -v libreddit


    # To deploy on arm64 platforms, simply replace libreddit/libreddit in the commands above with libreddit/libreddit:arm.
    # To deploy on armv7 platforms, simply replace libreddit/libreddit in the commands above with libreddit/libreddit:armv7.
    if [[ $device == "aarch64" ]]; then
        echo "installing libreddit for $device"
        sudo docker pull libreddit/libreddit:arm
        sudo docker run -d --name libreddit -p 8050:8080 --expose 8050-8090 libreddit/libreddit:arm
    elif [[ $device == "armv7l" ]]; then
        echo "installing libreddit for $device"
        sudo docker pull libreddit/libreddit:armv7
        sudo docker run -d --name libredditlibreddit -p 8050:8080 --expose 8050-8090 libreddit/libreddit:armv7
    else
        echo "installing libreddit for $device"
        sudo docker run -d --name libreddit libreddit -p 8050:8080 --expose 8050-8090  libreddit/libreddit
    fi
    # ask if they want to stop and remove the container
    read -p "Do you want to stop and remove the container? " -n 1 -r
    echo # move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo docker stop libreddit
        sudo docker rm -v libreddit
    fi

}

install_java(){
    sudo apt update && sudo apt upgrade -y
    sudo apt autoremove -y
    sudo apt install default-jdk -y
}

install_neofetch()
{
    sudo apt install neofetch -y

}


cockpit()
{

    sudo apt install --fix-missing  cockpit -y 
    sudo systemctl start cockpit
    sudo ufw allow 9090/tcp
    sudo apt install  --fix-missing cockpit-machines -y

}

install_conda(){
    echo "Installing Conda for python management"
    cd ~/
    # check if Mambaforge-$(uname)-$(uname -m).sh  exists
    if [ ! -f "Mambaforge-$(uname)-$(uname -m).sh" ]; then
        echo "Downloading Mambaforge-$(uname)-$(uname -m).sh"
        curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
    fi
    # check if folder exists
    if [ ! -d "$HOME/miniforge3" ]; then
        echo "Installing Mambaforge-$(uname)-$(uname -m).sh"
        bash Mambaforge-$(uname)-$(uname -m).sh  -b -p $HOME/miniforge3 
    else
        echo "Mambaforge-$(uname)-$(uname -m).sh is already installed"
    fi

    # bash Mambaforge-$(uname)-$(uname -m).sh  -b -p $HOME/miniforge3 
    
    # rm Mambaforge-$(uname)-$(uname -m).sh
    echo "export PATH=$HOME/miniforge3/bin:$PATH" >> ~/.bashrc
    source ~/.bashrc
    # conda init 
    # conda init zsh
    # conda update -n base -c defaults conda -y
    # conda config --set auto_activate_base true

    
}



install_all() {
    
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
sudo apt-get install nmap -y # used for network discovery in the local network python script library
sudo apt-get install net-tools -y # used for network discovery in the local network python script library
}

"${@:1}" "${@:3}"
# $ curl -sfL https://get.k3s.io | K3S_URL=https://http://192.168.1.156:6443 K3S_TOKEN=K10095cb1e5ffbf1b985c8a23243ade3911a40b9f9523a1181e01353b29b765d23e::server:e2c69b129bf644e4401e4a38e0737113 sh -
