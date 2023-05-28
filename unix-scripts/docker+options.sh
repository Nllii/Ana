#!/bin/bash

RED='\033[0;31m'
White="\[\033[0;37m\]"
END='\033[0m' 
Yellow="\033[0;93m[x]"
project_path=$(pwd)


build_container(){


    # echo project_name: $project_name
    if ! [ -f $project_path/"Dockerfile" ]; then
        echo -e "${RED}No Dockerfile found.${END}"
        exit 1
    fi
    project_name=$(git config --get remote.origin.url | sed 's/.*\/\(.*\)\.git/\1/')
    echo -e "${Yellow_task}Building docker image ${project_name}${END}"
    read -p "Dockerfile name or leave blank: " dockerfile_name
    if [ -z "$dockerfile_name" ]; then
        if [ "$project_name" != "$(echo $project_name | tr '[:upper:]' '[:lower:]')" ]; then
            echo -e "${RED}Project name must be lowercase.${END}"
            project_name=$(echo $project_name | tr '[:upper:]' '[:lower:]')
            echo -e "${Yellow_task}Project name changed to ${project_name}${END}"
            sudo docker build --tag $project_name .
            sudo docker run -d $project_name
        else
            echo "looks like this project doesn't have a git repository or its owned by you"
            read -p "give me the  project name?: " project_name
            echo -e "${Yellow_task}Building project: $project_name${END}"
            sudo docker build --tag $project_name .
            sudo docker run -d $project_name
        fi
    else
        echo -e "${Yellow_task}Building project: $project_name with Dockrfile! error in else statement :$dockerfile_name${END}"
        sudo docker build --tag $project_name:$dockerfile_name .
        sudo docker run -d $project_name:$dockerfile_name
    fi
}

    

compose_build()
{

# project_name=$(git config --get remote.origin.url | sed 's/.*\/\(.*\)\.git/\1/')
if ! [ -f $project_path/"docker-compose.yml" ]; then
    echo -e "${RED}No docker-compose.yml found.${END}"
    exit 1
fi
echo -e "${RED}using --no-cache build  ${project_name}${END}"
sudo docker-compose build --no-cache --force-rm
sudo docker-compose up -d --force-recreate
#docker-compose build --no-cache && sudo docker-compose up -d 
}


update_containers(){
    # updates to always run.
    echo -e "${RED}setting all containers to always run${END}"
    docker update --restart always $(docker ps -q)
}


stop_containers(){
    # stops all containers
    echo -e "${RED}stopping all containers${END}"
    docker stop $(docker ps -q)
}


remove_containers(){
    # removes all containers
    echo -e "${RED}removing all containers${END}"
    docker rm $(docker ps -a -q)
}


remove_images(){
    # removes all images
    echo -e "${RED}removing all images${END}"
    docker rmi $(docker images -q)
}

restart_containers(){
    # restarts all containers
    container_name=$(docker ps -a -q)
    echo -e "${RED}restarting all containers${END}"

    for i in $container_name; do
        echo -e "${RED}restarting container: $i${END}"
        docker restart $i
    done



    # # sudo docker restart portainer

    # echo -e "${RED}restarting all containers${END}"
    # docker restart $(docker ps -q)
}

"${@:1}" "${@:3}"


# docker-compose up -d --force-recreate
# docker-compose build --no-cache && sudo docker-compose up -d
# docker-compose build --no-cache && sudo docker-compose up -d --force-recreate
# docker-compose build --no-cache && sudo docker-compose up -d --force-recreate --remove-orphans
# docker-compose build --no-cache && sudo docker-compose up -d --force-recreate --remove-orphans --build