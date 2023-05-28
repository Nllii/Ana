#!/usr/bin/env bash
# https://github.com/tensorflow/tensorflow/blob/master/tools/tf_env_collect.sh
# https://www.launchd.info

set -u  # Check for undefined variables
set -e
set -x

die() {
    echo $@
    exit 1
}
python_bin_path=$(which python || which python3 || die "Cannot find Python binary")
directory=$(pwd)
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: $directory/launchctl_notification.sh [create_plist|setup_launchctl|remove_launchctl|link_python] [path_to_python_script]"
    exit 1
fi

run_file=$(pwd)/launchctl_notification_macosx/app.py
launchctl_name=ana

create_plist() {
cat <<EOF > launchctl_notification_macosx/com.$launchctl_name.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.$launchctl_name</string>
    <key>ProgramArguments</key>
    <array>

        <string>bash</string>
        <string>-c</string>
        <string>lsof -P | grep ':5020' | awk '{print \$2}' | xargs kill -9; $python_bin_path $run_file</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$directory</string>
    <key>StandardOutPath</key>
    <string>/var/log/$launchctl_name.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/$launchctl_name.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>

</plist>
EOF

}





launch_daemons() {
    echo "Copying com.$launchctl_name.plist to /Library/LaunchDaemons/  and starting service"
    sudo cp launchctl_notification_macosx/com.$launchctl_name.plist /Library/LaunchDaemons/
    # sudo launchctl unload /Library/LaunchDaemons/com.$launchctl_name.plist
    sudo launchctl load -w /Library/LaunchDaemons/com.$launchctl_name.plist
    sudo launchctl start com.$launchctl_name
    cat /var/log/$launchctl_name.log
}

remove_launchctl() {
    echo "Stopping com.$launchctl_name.plist to /Library/LaunchDaemons/  and removing service"
    
    sudo launchctl stop com.$launchctl_name
    sudo launchctl unload /Library/LaunchDaemons/com.$launchctl_name.plist
    # remove the file
    sudo rm /Library/LaunchDaemons/com.$launchctl_name.plist
    # remove the log file
    sudo rm /var/log/$launchctl_name.log

}




"${@:1}" "${@:3}"
