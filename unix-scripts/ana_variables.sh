#!/usr/bin/env bash
# https://github.com/tensorflow/tensorflow/blob/master/tools/tf_env_collect.sh
# https://www.launchd.info
# use this or the python version in the settings.py

set -u  # Check for undefined variables
set -e
set -x

# same as the python version
s_number() {
cat <<EOF > $HOME/.ana_variables
phone_number=$@
# created by ana $(date) $(whoami) $(pwd)
EOF
}

"${@:1}" "${@:3}"
