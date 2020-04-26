#!/bin/bash

echo "Installing Ubuntu docker and docker-compose"

#Docker

sudo apt-get update

sudo apt-get install     apt-transport-https     ca-certificates     curl     gnupg-agent     software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) test"

sudo apt-get update

sudo docker run hello-world


#Docker compose
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
