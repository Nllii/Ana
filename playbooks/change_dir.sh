#!/usr/bin/env bash

cd "$1"
echo "Changed directory to $(pwd)"
# if linux use bash if mac use zsh
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  exec bash
elif [[ "$OSTYPE" == "darwin"* ]]; then
  exec zsh
fi
