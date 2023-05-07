#!bin/bash 
# check if python is installed via conda
if ! [ -x "$(command -v conda)" ]; then
  echo 'Error: conda is not installed.' >&2
  exit 1
fi


