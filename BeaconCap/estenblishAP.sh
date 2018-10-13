sudo nmcli radio wifi off
sudo rfkill unblock wlan

sudo ifconfig wlx8cbebe05496a 10.15.0.1/24 up
#sleep 1
sudo service isc-dhcp-server restart
sudo service hostapd restart
sudo hostapd ./hostapd.conf
