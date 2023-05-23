#!bin/bash

# commit project
git add .
read -p "Enter commit message: " commit_message
git commit -am "$commit_message"
git push 