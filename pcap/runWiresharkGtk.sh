#!/bin/bash
# function: 运行界面版Wireshark,可指定信道
# $1: channel, Opt, default: unchanging

# 设置要监听的无线信道
if [ x$1 = x ]; then
  #sudo iw dev wlan0 channel 1
else
  sudo iw dev wlan0 channel $1
fi
# 使能接口mon0接口
sudo ifconfig wlan0 up

# 运行wireshark-gtk
sudo wireshark-gtk
