#!/bin/bash
# function: use tshark to capture wlan data packages, and save the result to files "cap/$1_$2_$channel.pcapng".
# $1: Filename prefix
# $2: Capture time on all channel(2.4GHz)
# $3: Manual channel
# -f wlan[0]==0x80 (Not yet)

# Get the wireless device name
wldev=$(iwconfig |grep "^wl[[:alnum:]]*" -o)
# add a new monitor mode interface mon0 on wldev
sudo iw dev $wldev interface add mon0 type monitor
# delete the managed interface wldev, if not, the channel cannot be changed
sudo iw dev $wldev del
# enable mon0
sudo ifconfig mon0 up

if [ x"$3" = x ]; then
# Do capture on all channel
for ((i=1; i<=13; i++))
do	
    sudo iw dev mon0 set channel $i
    echo "channel-$i"
    sudo tshark -i mon0  -a duration:$2 -w cap/$1_$2_$i.pcapng -n
    if [ 1 == $i ]
    then
        :
    fi
done
else
# Do capture on the specified channel
    sudo iw dev mon0 set channel $3
    echo "channel-$3"
    sudo tshark -i mon0  -a duration:$2 -w cap/$1_$2_$3.pcapng -n
fi
