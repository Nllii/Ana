#!/bin/bash

# Path to the 50-cloud file
NETPLAN_FILE="/etc/netplan/50-cloud-init.yaml"

# Function to apply netplan configuration
apply_netplan() {
    echo "Applying netplan configuration..."
    sudo netplan apply
}

# Function to test the netplan configuration
test_netplan() {
    echo "Testing netplan configuration..."
    sudo netplan --debug try
    if [ $? -eq 0 ]; then
        echo "Netplan test passed. Proceeding with applying the configuration."
        apply_netplan
    else
        echo "Netplan test failed. Please review the configuration and try again."
    fi
}

# Function to reboot the system
reboot_system() {
    echo "Rebooting the system..."
    sudo reboot
}

# Validate the input arguments
if [[ $# -lt 2 ]]; then
    echo "Invalid number of arguments. Please provide at least two arguments: [action] [file]"
    exit 1
fi

# Get the action and file path from input arguments
action=$1
file=$2


# Check if the specified file exists
if [ ! -f "$file" ]; then
    echo "File not found: $file"
    exit 1
fi
echo "updated: (netconfig.sh)"
echo "Action: $action"
echo "File: $file"



# backup the current netplan configuration if there is an error swap back to the original
if [ -f "$NETPLAN_FILE" ]; then
    echo "Backing up the current netplan configuration..."
    sudo cp "$NETPLAN_FILE" "$NETPLAN_FILE.bak"
fi


# Copy the file to the netplan directory
sudo cp "$file" "$NETPLAN_FILE"
echo "Copied $file to $NETPLAN_FILE"
echo "backup: $NETPLAN_FILE.bak"
echo "sudo cat $NETPLAN_FILE"
echo "to apply: sudo systemctl restart systemd-networkd "


# Perform the specified netplan action
# case "$action" in
#     "test")
#         echo "Action: Test netplan configuration"
#         test_netplan
#         ;;
#     "apply")
#         echo "Action: Apply netplan configuration"
#         apply_netplan
#         ;;
#     "reboot")
#         echo "Action: Reboot the system"
#         reboot_system
#         ;;
#     *)
#         echo "Invalid action: $action. Please choose from: test, apply, reboot"
#         exit 1
#         ;;
# esac

# # Swap back to the original netplan configuration if there is an error
# if [ -f "$NETPLAN_FILE.bak" ]; then
#     echo "reverting back to the original netplan configuration... $NETPLAN_FILE.bak -> $NETPLAN_FILE"
#     echo "why? script was suppose to exit code: $?"
#     cat "$NETPLAN_FILE.bak"
#     sudo cp "$NETPLAN_FILE.bak" "$NETPLAN_FILE"
# fi


# "${@:1}" "${@:3}"
