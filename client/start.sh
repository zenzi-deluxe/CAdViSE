#!/bin/bash

config=$(cat /home/ec2-user/config.json)
#id=$(echo "$config" | jq -r '.id')
#alk=$(echo "$config" | jq -r '.alk')
#duration=$(($(echo "$config" | jq -r '.experimentDuration')))
#title=$(echo "$config" | jq -r '.title')
player=$(echo "$config" | jq -r '.player')
serverIp=$(echo "$config" | jq -r '.serverIp')
title="tos_5min"
net_trace="4G"
abr="basic"
buff_size=40
#
#sudo docker exec -d "ppt-client-$player" python3 /home/seluser/ppt/ppt.py "http://localhost/player/$player?id=$id&title=$title&alk=$alk" "$duration"
#
#durations=($(echo "$config" | jq -r '.shapes[].duration'))
#ingresses=($(echo "$config" | jq -r '.shapes[].clientIngress'))
#egresses=($(echo "$config" | jq -r '.shapes[].clientEgress'))
#latencies=($(echo "$config" | jq -r '.shapes[].clientLatency'))
#
#shaperIndex=0
#while [ $shaperIndex -lt "${#durations[@]}" ]; do
#
#  sudo /home/ec2-user/wondershaper/wondershaper -a eth0 -c
#
#  if [[ ${ingresses[$shaperIndex]} -gt 0 ]] && [[ ${egresses[$shaperIndex]} -gt 0 ]]; then
#    sudo /home/ec2-user/wondershaper/wondershaper -a eth0 -d "${ingresses[$shaperIndex]}" -u "${egresses[$shaperIndex]}"
#  elif [[ ${ingresses[$shaperIndex]} -gt 0 ]]; then
#    sudo /home/ec2-user/wondershaper/wondershaper -a eth0 -d "${ingresses[$shaperIndex]}"
#  elif [[ ${egresses[$shaperIndex]} -gt 0 ]]; then
#    sudo /home/ec2-user/wondershaper/wondershaper -a eth0 -u "${egresses[$shaperIndex]}"
#  elif [[ ${latencies[$shaperIndex]} -gt 0 ]]; then
#    sudo tc qdisc replace dev eth0 root netem delay "${latencies[$shaperIndex]}ms"
#  fi
#
#  sleep $((durations[shaperIndex]))
#  ((shaperIndex++))
#done

# As input to the AStream script
while getopts a:z:t:n:b: flag
do
    case "${flag}" in
        a) abr=${OPTARG};;  # name of the abr
        z) medusa=${OPTARG};;  # 0 or 1
        t) title=${OPTARG};;  # title of the video
        n) net_trace=${OPTARG};;  # network trace
        b) buff_size=${OPTARG};;  # Buffer size
    esac
done

if [ ${net_trace} == "4G" ]; then
    source /home/ec2-user/"4G_trace_wondershaper.sh"&
elif [ ${net_trace} == "cascade" ]; then
    source /home/ec2-user/"cascade_wondershaper.sh"&
elif [ ${net_trace} == "FCC" ]; then
    # source /home/ec2-user/"amzonfcc.sh"&
    source /home/ec2-user/"FCC$player.sh"&
elif [ ${net_trace} == "competition" ]; then
    source /home/ec2-user/"competition.sh"&
fi
#source /home/ec2-user/"network_trace.sh"&
# source /home/ec2-user/"4G_trace_wondershaper.sh"&
#source /home/ec2-user/"bus57_1_tc_wondershaper.sh"&

manifest="https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/tos_5min/4s/manifest_new.mpd"

if [ ${title} == "tos_5min" ]; then
    manifest="https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/tos_5min/4s/manifest_new.mpd"
    # manifest="http://18.156.198.140/Dash/tos_5min/4s/manifest_new.mpd"
elif [ ${title} == "tos_5min_end" ]; then
    manifest="https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/tos_5min_end/4s/manifest_new.mpd"
elif [ ${title} == "gameplay" ]; then
    manifest="https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/gameplay_24fps_5min/4s/manifest_new.mpd"
elif [ ${title} == "rally" ]; then
    manifest="https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/Rally_4k_5min_24fps/4s/manifest_new.mpd"
fi

#
# ToS: https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/tos_5min/4s/manifest_new.mpd
# ToS_End: https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/tos_5min_end/4s/manifest_new.mpd
# Rally: https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/Rally_4k_5min_24fps/4s/manifest_new.mpd
# Gameplay: https://daniele-mcom.s3.eu-central-1.amazonaws.com/Dash/gameplay_24fps_5min/4s/manifest_new.mpd
#

python /home/ec2-user/AStream/dist/client/dash_client.py -m $manifest -p $abr -z $medusa -b $buff_size > /home/ec2-user/temp_log.log &

exit 0
