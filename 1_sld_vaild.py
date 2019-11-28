import dpkt
import dns.message
import socket
import struct
import os
import sys
import threading
from dns import resolver
import time

SERVER = ["101.7.8.9"]


PORT = 53
domains = []
filename = sys.argv[1]

file = open(filename, "r")


for eachline in file:
    eachline=eachline.strip()
    domains.append(eachline)

lock = threading.Lock()
c_index = 0

flag_dict={0:"NOERROR",1:"Formaterror",2:"Serverfailure",3:"NXDOMAIN",4:"NotImplemented",5:"Refused"}


def domain2ns():
    global c_index
    while True:
        lock.acquire()
        if c_index >= len(domains):
            lock.release()
            break  # End of list
        domain = domains[c_index]
        #print "---testing:" + domain+"\n"
        c_index += 1
        if (c_index % 1000 ==0 ):
            print str(c_index)+" domain done!"
        lock.release()
        try:
            dns_query = dns.message.make_query(domain, "ns")
            ans = dns.query.udp(dns_query, "101.7.8.9", port=PORT,timeout=5)
           # print(ans.flags & 0x0F)
            if (ans.flags & 0x0F ==0):
                with open(filename.strip(".txt") + '_vaild.txt', 'a') as f:
                    f.write(domain+ "\n")
            elif(ans.flags & 0x0F ==5):
                with open(filename.strip(".txt") + '_nxdomain.txt', 'a') as f:
                    f.write(domain+ "\n")
            time.sleep(5)
        except Exception as e:
            #print e
            continue



threads = []
for i in range(1000):
    t = threading.Thread(target=domain2ns)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

file.close()
print '******************All Done!******************'