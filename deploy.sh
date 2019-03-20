#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/CI/deploytravis
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop portofolio
sudo docker rm portofolio
sudo docker rmi mohazril/portofolio
sudo docker run -d --name portofolio -p 5000:5000 -t mohazril/portofolio:latest
