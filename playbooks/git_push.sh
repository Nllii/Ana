#!bin/bash 

# uplaod to github
echo "$(pwd)"



git add .
read -p "Enter commit message: " commit
if [ -z "$commit" ]; then
    echo "Commit message is empty using default message called "update""
    commit="update"
fi

git commit -am "$commit"
git push 




