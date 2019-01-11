#include <stdio.h>
#include <string.h>
typedef unsigned char uint8;
const char *crc5_polynomial = "101001";
const char *crc5_preset = "01001";

char *crc_n(const char *data, char *crc, const char *polynomial)
{
	for(int i=0;data[i];i++){
        if(data[i]!='0'&&data[i]!=1)
            continue;
		if(crc[0]=='1'){
		    // XOR
			for(int j=0;crc[j];j++)
				crc[j] = (crc[j]==polynomial[j]?'0':'1');
		}
		//Left shift
		int j;
		for(j=1;crc[j];j++)
			crc[j-1]=crc[j];
		crc[j-1]=data[i];
	}
	return crc;
}
int main()
{
	char data[100]="1000000000000000010000";
	char crc[6]="01001";
	char *p = crc_n(data, crc, crc5_polynomial);
	printf("%s\n", p);
	return 0;
}
