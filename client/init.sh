#!/bin/bash

#sudo yum -y install docker jq git &>/dev/null
#sudo yum -u update
sudo yum -y install python38 jq git &>/dev/null
#sudo yum -y install python-pip
#sudo pip-3.8 install --upgrade pip
#sudo python -m pip install -U git+https://github.com/coin-or/pulp
#sudo yum makecache
#sudo yum -y install glpk-utils

#sudo service docker start
sudo git clone https://github.com/cd-athena/wondershaper.git /home/ec2-user/wondershaper
#sudo yum -y install gcc  # Prerequisite for ITU-T package
#sudo yum -y install gcc-c++  # Prerequisite for ITU-T package
#sudo pip-3.8 install Cython  # Prerequisite for ITU-T package
#sudo git clone https://github.com/itu-p1203/itu-p1203.git /home/ec2-user/itu-t
#sudo pip-3.8 install /home/ec2-user/itu-t/
#sudo git clone https://github.com/Telecommunication-Telemedia-Assessment/itu-p1203-codecextension.git /home/ec2-user/itu-t-extension
#sudo pip-3.8 install /home/ec2-user/itu-t-extension

#config=$(cat /home/ec2-user/config.json)
#player=$(echo "$config" | jq -r '.player')

#sudo docker pull babakt/ppt-client:cadvise &>/dev/null
#sudo docker run --rm -d --name "ppt-client-$player" -p 5900:5900 -v /dev/shm:/dev/shm babakt/ppt-client:cadvise

#sudo docker cp /home/ec2-user/config.json "ppt-client-$player:/home/seluser/ppt/config.json"
#sudo docker exec -d "ppt-client-$player" sudo pm2 start index.js

exit 0
