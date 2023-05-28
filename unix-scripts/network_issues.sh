#!bin/bash 
# lsof -P | grep ':3000' | awk '{print $2}' | xargs kill -9


SERVER_URL="http://localhost:5020"  # Replace with your server's URL #
# get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG_FILE="$DIR/logs/sever-pings.log"  # Path to the log file
TIMEOUT=5  # Timeout in seconds

# Function to restart the server
restart_server() {
    echo "** Restarting server..."
    # lsof -P | grep ':5020' | awk '{print $2}' | xargs kill -9
    # /Users/admin/miniconda3/bin/python /Users/admin/Desktop/fucked/libtools/launchctl_notification_macosx/app.py 
}

# Function to ping the server and check for response
ping_server() {
    echo "** Pinging server..."
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT $SERVER_URL)
    if [[ $response -ne 200 ]]; then
        echo "Server is not responding (HTTP code: $response)"
        restart_server
    else
        echo "Server is responding (HTTP code: $response)"
    fi
}

# Perform server ping and logging
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
ping_server >> $LOG_FILE 2>&1
echo "Ping performed at: $timestamp" >> $LOG_FILE
echo "" >> $LOG_FILE
