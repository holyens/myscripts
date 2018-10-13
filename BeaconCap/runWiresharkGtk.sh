#!/bin/bash
# $1: channel, Opt, default: 1

#获取无线网卡名称
wldev=$(iwconfig |grep "^wl[[:alnum:]]*" -o)

# 以monitor模式在dev上新建接口mon0
sudo iw dev $wldev interface add mon0 type monitor
# 删除网卡原来的managed模式接口，避免与monitor产生冲突
sudo iw dev $wldev del

# 设置要监听的无线信道
if [ x$1 = x ]; then
  sudo iw dev mon0 channel 1
else
  sudo iw dev mon0 channel $1
fi
# 使能接口mon0接口
sudo ifconfig mon0 up

# 运行wireshark-gtk
sudo wireshark-gtk
