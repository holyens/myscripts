#!/bin/bash
# function: use tshark to capture wlan data packages, and save the result to files "cap/$1_$2_$channel.pcapng".
# $1: Filename prefix
# $2: Capture time on all channel(2.4GHz)
# $3: Manual channel
# -f wlan[0]==0x80 (Not yet)

# enable wlan0
sudo ifconfig wlan0 up

if [ x"$3" = x ]; then
# Do capture on all channel
for ((i=1; i<=13; i++))
do	
    sudo iw dev wlan0 set channel $i
    echo "channel-$i"
    sudo tshark -i wlan0  -a duration:$2 -w cap/$1_$2_$i.pcapng -n
    if [ 1 == $i ]
    then
        :
    fi
done
else
# Do capture on the specified channel
    sudo iw dev wlan0 set channel $3
    echo "channel-$3"
    sudo tshark -i wlan0  -a duration:$2 -w cap/$1_$2_$3.pcapng -n
fi
