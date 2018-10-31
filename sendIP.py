import requests,struct,socket,re
s = requests.Session()

def get_ips():
    reg = re.compile(r'^172\.')
    addrs = socket.getaddrinfo(socket.gethostname(),None)
    ipsl = [ip[4][0] for ip in addrs if reg.match(ip[4][0])]
    for i,ip in enumerate(ipsl):
        int_ip = struct.unpack('!I', socket.inet_aton(ip))[0]
        ipsl[i] = str(int_ip)
    if ipsl:
        return '-'.join(ipsl)
    else:
        return ''
    
def post_ip():
    ips = get_ips()
    param = {'token': 'qaz', 'ips': ips}
    url = 'https://api.iotfan.net/other/recip.php'
    res = s.post(url, data=param)
    return res.content

def main():
    print(post_ip())

if __name__ == "__main__":
    main()
