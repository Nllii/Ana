#!bin/bash 

# uplaod to github
echo "$(pwd)"



git add .
read -p "Enter commit message: " commit
if [ -z "$commit" ]; then
    commit="update"
fi

git commit -am "$commit"
git push 




