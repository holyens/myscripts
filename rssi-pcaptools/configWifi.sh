#!/bin/bash
# function: 为了程序方便，统一将无线网卡名字改为wlan0，并改为monitor模式
# $1: channel, Opt, default: 1

# 获取无线网卡名称
wldev=`ls /sys/class/net|grep 'wl[[:alnum:]]\+' -o`
echo "rename $wldev as wlan0 "

# 更改无线网卡名称及模式
sudo ip link set $wldev down
sudo ip link set $wldev name wlan0
sudo iwconfig wlan0 mode monitor
sudo ip link set wlan0 up

# 设置要监听的无线信道
if [ x$1 = x ]; then
  sudo iw dev wlan0 set channel 1
else
  sudo iw dev wlan0 set channel $1
fi
echo "done."

