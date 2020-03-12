#!/bin/bash

sudo yum -y install docker jq
sudo service docker start
sudo docker network create ppt-net

config=$(cat /home/ec2-user/config.json)

mode=$(echo "$config" | jq -r '.mode')
player=$(echo "$config" | jq -r '.player')
bandwidths=($(echo "$config" | jq -r '.shapes[].availableBandwidth'))
delays=($(echo "$config" | jq -r '.shapes[].latency'))
packetLosses=($(echo "$config" | jq -r '.shapes[].packetLoss'))
packetDuplicates=($(echo "$config" | jq -r '.shapes[].packetDuplicate'))
packetCorruptions=($(echo "$config" | jq -r '.shapes[].packetCorruption'))

sudo docker pull lukaszlach/docker-tc:latest && sudo docker run -d --name docker-tc --network \
  host --cap-add NET_ADMIN -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/docker-tc:/tmp/docker-tc lukaszlach/docker-tc

sudo docker pull babakt/ppt-"$mode":latest && sudo docker run --rm -d --name "ppt-$mode-$player" --net ppt-net -p 5900:5900 \
  --label "com.docker-tc.enabled=1" \
  --label "com.docker-tc.limit=${bandwidths[0]}kbit" \
  --label "com.docker-tc.delay=${delays[0]}ms" \
  --label "com.docker-tc.loss=${packetLosses[0]}%" \
  --label "com.docker-tc.duplicate=${packetDuplicates[0]}%" \
  --label "com.docker-tc.corrupt=${packetCorruptions[0]}%" \
  -v /dev/shm:/dev/shm babakt/ppt-"$mode"
