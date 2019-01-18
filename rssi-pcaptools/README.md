## Linux Wifi Beacon抓包脚本和Beacon生成程序
#### 1. beacon.cpp
-   程序功能： 周期发送WiFi Beacon帧
-   运行参数： `./beacon [$ssid [$interval]]`
    -   $ssid (str): 指定beacon帧SSID字段，缺省值为testap-1
    -   $interval (int): beacon帧周期发送的间隔，单位ms, 缺省值为100
-   Examples:
    -   `./beacon`
    -   `./beacon testap-2`
    -   `./beacon testap-2 200`
-   注意： 程序使用网卡`wlan0`，
    
实验过程中发现实验室ThinkPad Linux系统的hostapd产生的beacon帧不是按照/etc/hostapd.conf中设置的beacon_int等时间间隔出现，而是时密时疏（不知道是否hostapd在所有系统下都是如此）。真实AP实测的Beacon interval基本上与beacon帧中的interval相同，且间隔固定。要探究Beacon interval对RSSI丢失率的影响，需要生成interval可控的beacon帧，并且应该与真实AP一样时间间隔是固定的，所以hostapd不符合实验要求。这是编写此程序的最初目的。

#### 2. Beacon抓包脚本
1. configWifi.sh
-   脚本功能
    -   更改无线网卡名称为`wlan0`
    -   更改无线网卡为monitor模式
    -   设置无线网卡的工作信道
-   运行参数： `./configWifi [$channel]`
    -   $channel (int)： 设置工作信道，范围1~13，缺省值为1
-   注意： 此脚本应该在其他脚本前运行
2. resetWifi.sh
-   脚本功能： 重置`wlan0`为managed模式
-   运行方式： `./resetWifi.sh`
3. runWiresharkGtk.sh
-   脚本功能： 运行界面版Wireshark,可指定信道
-   运行参数： `./runWiresharkGtk.sh [$channel]`
    -   channel (int)：要监听的信道, 缺省时保持当前信道不变
4. autoCapBeacon.sh
-   脚本功能: 使用`tshark`捕获WiFi数据包, 并且将结果保存到文件 `$(file_prefix)_$(duration)_$(channel).pcapng`
-   运行参数： `./autoCapBeacon.sh $file_prefix $duration [$manual_channel]`
    -   $file_prefix (str): 输出文件名前缀
    -   $duration (int): 程序在每个信道的捕获时长，单位为s
    -   $manual_channel (int): 如果被设置，则程序只在该信道捕获$duration秒数据；如果未被设置，程序将在1-13信道依次各捕获$duration秒数据
-   提示：捕获的文件可以使用WiresharkGtk打开查看
5. exportPcap2csv.sh
-   脚本功能: 将$1目录中的`.pcapng`文件导出为`.csv`文件。
-   运行参数： `./exportPcap2csv.sh $1 $2 [$3]`
    -   $1: 输入文件所在目录
    -   $2: 输入文件前缀 
    -   $3: 帧过滤器，如`wlan.fc.type_subtype==0x08`表示仅输出802.11 beacon帧
-   提示：可以指定输出到csv文件的帧的fields，可以使用tshark的`-e`选项设置
6. estenblishAP.sh
-   脚本功能： 将`./hostapd.conf`作为配置文件，使用hostapd建立AP
-   运行方式： `./estenblishAP.sh`
#### 3. 使用2中脚本进行Beacon抓包的过程
1. 图形界面方式
```bash
./configWifi 5			#设置网卡名为wlan0，工作模式为monitor，工作信道为5（可选）
./runWiresharkGtk.sh 6		#打开WiresharkGtk，并设置监听信道为6（可选）
./resetWifi.sh			#重置`wlan0`为managed模式，因为无线网卡在monitor模式无法上网

```
2. 命令行模式
```bash
./configWifi			#设置网卡名为wlan0，工作模式为monitor，工作信道为5（可选）
./autoCapBeacon.sh cap/wifibeacon_A1 20 5	#使用tshark在信道5抓包20s，并将结果保存到文件cap/wifibeacon_A1_20_5.pcapng
./autoCapBeacon.sh cap/wifibeacon_A2 20		#使用tshark在1-13信道依次抓包各20s，并将结果保存到文件cap/wifibeacon_A2_20_1.pcapng，cap/wifibeacon_A2_20_2.pcapng，...
./exportPcap2csv.sh cap/wifibeacon_A2 wlan.fc.type_subtype==0x08	#将上一命令的所有输出文件导出为同名的.csv文件，导出时只导出满足过滤条件的帧
./resetWifi.sh			#重置`wlan0`为managed模式，因为无线网卡在monitor模式无法上网

```



