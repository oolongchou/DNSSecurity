# encoding=gbk

import threading
import os
import re

urls = []

fobj = open('attack/updatecheck.txt')

for eachline in fobj.readlines():
    urls.append(eachline)

lock = threading.Lock()
c_index = 0


def test_DNS_Servers():
    global c_index
    while True:
        lock.acquire()

        if c_index >= len(urls):
            lock.release()
            break  # End of list
        domain = urls[c_index].strip()

        c_index += 1
        if(c_index%1000==0):
            print(c_index)
        lock.release()
        list=domain.split("\t")
        cmd = str(list[0])

        ip=str(list[1])
        #print(cmd)
        #print(ip)




        cmd_res = os.popen(cmd).read()


        if cmd_res.find(ip) > 0:

            print '*' * 10 + ' Vulnerable update dns server found:', cmd, '*' * 10

            with open('vulnerable_update_hosts.txt', 'a') as f:
                f.write(cmd+"\n")
            with open(cmd + '.txt', 'w') as f:
                f.write(cmd_res+"\n")


threads = []
for i in range(100):
    t = threading.Thread(target=test_DNS_Servers)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print 'All Done!'