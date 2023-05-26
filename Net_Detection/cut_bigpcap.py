# 将大文件仅提取tcp/udp
from scapy.all import *

writers = PcapWriter('udp_or_tcp_from_input.pcap')

i = 0

with PcapReader('testbed-13jun.pcap') as pcap_reader:

    for pkt in pcap_reader:
        if 'UDP' in pkt:
            print(repr(pkt))
            writers.write(pkt=pkt)
            print(i)
            i = i + 1

        if 'TCP' in pkt:
            print(repr(pkt))
            writers.write(pkt=pkt)
            print(i)
            i = i + 1


writers.close()
