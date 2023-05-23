#!/bin/bash

# Set the server URL and DNS IP address
SERVER_URL=$(cat $(pwd)/.server_url.txt | head -n 1)
DNS_IP="8.8.8.8"
LOG_FILE=$(pwd)/.internet_connection.log

alert(){
    alert_message=$@
    PAYLOAD="message=$alert_message"
    RESPONSE=$(curl -s -w "%{http_code}" -d "$PAYLOAD" "$SERVER_URL/imessage")
    # Get the HTTP status code from the response
    HTTP_STATUS="${RESPONSE:(-3)}"
    # Get the response body from the response
    RESPONSE_BODY="${RESPONSE:0:${#RESPONSE}-3}"
    if [ "$HTTP_STATUS" -eq 200 ]; then
        # Command executed successfully. Output:
        echo "$RESPONSE_BODY" >> $LOG_FILE
    else
        # Error executing command. Server response:
        echo "$RESPONSE_BODY" >> $LOG_FILE
    fi
}

"${@:1}" "${@:3}"
