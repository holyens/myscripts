#!/bin/bash
# function: export .pcapng files to .csv files from directory $1
# $1: input files directory
# $2: input file name prefix 
# $3: Frame filter (e.g., "wlan.fc.type_subtype==0x08")

if [ x"$1" = x ] ; then
    echo "[Error-2]: Directory not specified"
    exit -2
fi
scnt=0
ttnt=0
for file in $1/$2*.pcapng
do
    outfile=${file/%.pcapng/.csv}
    if test -f $file
    then
        tshark -r $file -Y "$2" -n -T fields -E separator=, \
        -e frame.number \
        -e frame.time_relative \
        -e wlan_radio.channel \
        -e wlan.bssid \
        -e wlan_radio.signal_dbm \
        -e wlan_mgt.fixed.beacon \
        -e wlan_mgt.ssid \
        >$outfile
        let tcnt+=1
        if [ $? -eq 0 ];then
            let scnt+=1
            echo ">>>$file -> $outfile done."
        else
            echo ">>>$file -> $outfile failure!"
        fi
    fi
done
echo "$scnt/$tcnt done."
