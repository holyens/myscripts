#!/bin/bash
# function: 重置wlan0为managed模式

# 更改无线网卡模式
sudo ip link set wlan0 down
sudo iwconfig wlan0 mode managed
sudo ip link set wlan0 up
echo "down."
