#!/bin/bash
# function: 重置wlan0为managed模式

# 更改无线网卡模式
ip link set wlan0 down
iwconfig wlan0 mode managed
ip link set wlan0 up
