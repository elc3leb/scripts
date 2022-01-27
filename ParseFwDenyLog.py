#!/usr/bin/python3

# Author : elc3leb
# Desc : Check iptables DENY logs & summ IT

import os
import sys
from datetime import datetime

source=None
destination=None
destination_port=None
logfile = '/var/log/messages'
logline=[]
date = datetime.today().strftime('%b %d')

with open(logfile) as f:
    for line in f:
        if date in line:
            if 'FIREWALL' in line:
                #Jan 26 17:32:38 p3svc01 kernel: [FIREWALL DENY]IN=ib0 OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:08:00:00:00 SRC=172.19.0.152 DST=172.19.0.15 LEN=52 TOS=0x00 PREC=0x00 TTL=64 ID=21835 DF PROTO=TCP SPT=443 DPT=38237 WINDOW=868 RES=0x00 ACK URGP=0
                for w in line.split():
                    if 'SRC=' in w :
                        source = w.split('=')[1]
                    if 'DST=' in w :
                        destination = w.split('=')[1]
                    if 'DPT=' in w :
                        destination_port = w.split('=')[1]
                    if source and destination and destination_port:
                        if int(destination_port) < 5000:
                            logline.append("[SRC:{} DST:{} DPT:{}]".format(source,destination,destination_port))
words = {}
for e in logline:
    if e not in words:
        words[e] = 1
    else:
        words.update({e: words.get(e) + 1})

for key, value in sorted(words.items(), key = lambda kv: kv[1], reverse = True):
    print(key, value)


