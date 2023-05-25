#!/usr/bin/env bash
# https://github.com/tensorflow/tensorflow/blob/master/tools/tf_env_collect.sh
# https://www.launchd.info
# use this or the python version in the settings.py

set -u  # Check for undefined variables
set -e
set -x

s_number() {

cat <<EOF > $HOME/.ana_variables
# created by ana $(date) $(whoami) $(pwd)

# export phone_number=$@

EOF

}

"${@:1}" "${@:3}"
