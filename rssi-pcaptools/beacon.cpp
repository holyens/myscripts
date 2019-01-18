#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <netpacket/packet.h>
#include <linux/if_ether.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <net/if.h>

//typedef unsigned char bool;
typedef signed char int8;
typedef unsigned char uint8;
typedef signed short int16;
typedef unsigned short uint16;
typedef signed int int32;
typedef unsigned int uint32;
typedef signed long long int64;
typedef unsigned long long uint64;

#define AP_COUNT 4

struct MAC_BEACON_BODY_TAGGED{
    uint8 tag_num;
    uint8 tag_len;
    uint8 *tag_data;
};

struct AP{
    uint8 bssid[6];
    char  essid[32];
    uint8 essid_len;
    uint8  enable_probe_rep;
    //uint16 seq_id;
    uint16 beacon_interval;
    uint16 capa_info;   //0x0001;    
};
#define xmemcpy(dest,src,num) memcpy(dest,src,num); dest += num
uint32 create_beacon_frame(uint8 *buf, uint32 n, struct AP ap)
{   
    static uint16 seq_id = 1024;
    uint8 *pbuf = buf;
    // radiotap header
    xmemcpy(pbuf, "\x00\x00\x0d\x00\x04\x80\x02\x00\x02\x00\x00\x00\x00", 13); 
    // header
    xmemcpy(pbuf, "\x80\x00", 2);        //version[2]:type[2]:subtype[4]:other[8] bits
    xmemcpy(pbuf, "\x00\x00", 2);        //duration/id[2] byte
    xmemcpy(pbuf, "\xff\xff\xff\xff\xff\xff", 6);      //addr1[6]
    xmemcpy(pbuf, ap.bssid, 6);      //addr2
    xmemcpy(pbuf, ap.bssid, 6);      //addr3
    xmemcpy(pbuf, (uint8*)&seq_id, 2);
    seq_id += 0x10;
    // fixed
    struct timeval t_time;
    gettimeofday(&t_time,0);
    uint64 timestamp = ((uint64)t_time.tv_sec)*1000000+t_time.tv_usec;
    xmemcpy(pbuf, (uint8*)&timestamp, 8);
    xmemcpy(pbuf, (uint8*)&ap.beacon_interval, 2);
    xmemcpy(pbuf, (uint8*)&ap.capa_info, 2);
    // tagged
    xmemcpy(pbuf, "\x00", 1);
    xmemcpy(pbuf, &ap.essid_len, 1);
    xmemcpy(pbuf, ap.essid, ap.essid_len);

    return (uint32)(pbuf-buf);
}
int32 create_raw_socket(const char* p_iface);
// sizeof(str)>=18
char *bssid2str(char *str, uint8 bssid[])
{
    const char *hex_tb="0123456789abcdef";
    int32 j=0;
    for(int32 i=0;i<6;i++){
        str[j++]=hex_tb[(bssid[i]>>4)&0x0f];
        str[j++]=hex_tb[bssid[i]&0x0f];
        str[j++]=':';
    }
    str[j-1]='\0';
    return str;
}
int32 main(int argc, char *argv[])
{
    struct AP ap;    
    const char *ssid = "testap-1";
    memcpy(ap.bssid, "\xEC\x17\x2F\x2D\xB6\xB0", 6);
    if(argc>1)
        ssid = argv[1];
    ap.essid_len = strlen(ssid);
    memcpy(ap.essid, ssid, ap.essid_len);
    
    ap.enable_probe_rep = 0;
    if(argc>2)
        ap.beacon_interval = (uint16)atoi(argv[2]);
    else
        ap.beacon_interval = 100;
    ap.capa_info = 0x0001;
    char *str=(char *)malloc(6*3*sizeof(uint8));
    str = bssid2str(str, ap.bssid);
    printf("bssid=%s ssid=%s\nbeacon interval=%d\n",str, ssid,\
         ap.beacon_interval);
    int32 t_socket=create_raw_socket("wlan0");
    while(1)
    {
        uint8 t_buffer[4096];
        uint32 t_len=create_beacon_frame(t_buffer, 4096, ap);
        int32 t_size=write(t_socket, t_buffer, t_len);
        if(t_size<0)
        {
            perror("<send_80211_frame> write() failed!");
        }
        printf("%d ", t_size);
        usleep(ap.beacon_interval*1000);
    }
    return 0;
}

int32 create_raw_socket(const char* p_iface)
{
    /* new raw socket */
    int32 t_socket=socket(PF_PACKET,SOCK_RAW,htons(ETH_P_ALL));
    if(t_socket<0)
    {
        perror("<create_raw_socket> socket(PF_PACKET,SOCK_RAW,htons(ETH_P_ALL)) failed!");
        return -1;
    }
    /* get the index of the interface */
    struct ifreq t_ifr;
    memset(&t_ifr,0,sizeof(t_ifr));
    strncpy(t_ifr.ifr_name,p_iface,sizeof(t_ifr.ifr_name)-1);
    if(ioctl(t_socket,SIOCGIFINDEX,&t_ifr)<0)
    {
        perror("<create_raw_socket> ioctl(SIOCGIFINDEX) failed!");
        return -1;
    }
    /* bind the raw socket to the interface */
    struct sockaddr_ll t_sll;
    memset(&t_sll,0,sizeof(t_sll));
    t_sll.sll_family=AF_PACKET;
    t_sll.sll_ifindex=t_ifr.ifr_ifindex;
    t_sll.sll_protocol=htons(ETH_P_ALL);
    if(bind(t_socket,(struct sockaddr*)&t_sll,sizeof(t_sll))<0)
    {
        perror("<create_raw_socket> bind(ETH_P_ALL) failed!");
        return -1;
    }
    /* open promisc */
    struct packet_mreq t_mr;
    memset(&t_mr,0,sizeof(t_mr));
    t_mr.mr_ifindex=t_sll.sll_ifindex;
    t_mr.mr_type=PACKET_MR_PROMISC;
    if(setsockopt(t_socket,SOL_PACKET,PACKET_ADD_MEMBERSHIP,&t_mr,sizeof(t_mr))<0)
    {
        perror("<create_raw_socket> setsockopt(PACKET_MR_PROMISC) failed!");
        return -1;
    }
    return t_socket;
}
