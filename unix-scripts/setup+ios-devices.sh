#!bin/bash 
set -e
# TESTED ON ubuntu 22.x on raspberry pi 4 LTS
# TESTED ON ubuntu 23.x on raspberry pi 4 
packages(){
    # these instructions are for raspberry pi 4
    sudo apt-get -y install usbmuxd libimobiledevice-utils libimobiledevice6 openssh-server
    sudo apt-get install -y libusbmuxd-tools
    sudo systemctl start usbmuxd
}


# create a tmux session to run the a background process::
create_session(){
    drive_location=$@
    tmux new -s "ios" -d
    # run this command iproxy 2222 22
    # append to log file called archive/archive.log "try ssh root@localhost -p 2222 to connect to device"""  
    tmux send-keys -t "ios" "echo 'try ssh root@localhost -p 2222 to connect to device' >> $drive_location/archive.log" C-m
    # run this command idevicepair pair
    tmux send-keys -t "ios" "idevicepair pair " C-m
    # run this command idevicepair validate
    tmux send-keys -t "ios" "idevicepair validate" C-m
    # run this command ideviceinfo
    tmux send-keys -t "ios" "ideviceinfo" C-m
    tmux send-keys -t "ios" "iproxy 2222 22" C-m

 

}

terminate_session(){
    tmux kill-session -t "ios"
}


# Mount the drive
mount_drive(){

    # Check if the drive is mounted
    if ! mountpoint -q /mnt/T7; then
        # Mount the drive
        sudo mount /dev/sda1 /mnt/T7
        if [ $? -eq 0 ]; then
            echo "Drive mounted successfully."
        else
            echo "Failed to mount the drive."
        fi
    else
        echo "Drive is already mounted."
    fi


}

# Unmount the drive
unmount_drive(){

    # Check if the drive is mounted
    if mountpoint -q /mnt/T7; then
        # Unmount the drive
        sudo umount /mnt/T7
        if [ $? -eq 0 ]; then
            echo "Drive unmounted successfully."
        else
            echo "Failed to unmount the drive."
        fi
    else
        echo "Drive is already unmounted."
    fi

}

# TODO: add make this verbose when running from python let python get the stdout
archive()
{   echo "find the file setup+ios-devices.sh and fix the archive function"
    # TODO: set the drive location and source location from the command line; if not set then use the default values, the issue is we need to map the correct arguments to the correct variables
    exit 1
    source=$@ #
    destination=$@
    echo "archiving files to $drive_location from $source"
    rsync -avz -e "ssh -p 2222" root@localhost:"$source" "$destination"

}




# setup all the things
install_all(){
    packages
    create_session
    # mount_drive
    # archive
    # unmount_drive
    # terminate_session
}


# https://stackoverflow.com/questions/255898/how-to-iterate-over-arguments-in-a-bash-script
"${@:1}" "${@:3}"

