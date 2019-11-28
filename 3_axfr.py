# encoding=gbk

import threading
import os
import sys


def checkpath(result_path):
    isExists = os.path.exists(result_path)
    if not isExists:
        os.makedirs(result_path)

urls = []


domain_txt = sys.argv[1]



fobj = open(domain_txt)
for eachline in fobj.readlines():
    urls.append(eachline)

lock = threading.Lock()
c_index = 0

checkpath("axfr/")
checkpath("dnsaxfr/")


def test_DNS_Servers():
    global c_index
    while True:
        lock.acquire()
        if c_index >= len(urls):
            lock.release()
            break  # End of list
        cmd = urls[c_index]
        server = cmd.split(' ')[2]
        NS=cmd.split(' ')[3]

        #print "---testing:" + cmd

        c_index += 1
        lock.release()
        cmd_res = os.popen(cmd).read()
        if cmd_res.find('Transfer failed.') > 0:

            with open('axfr/Transfer_faild_hosts.txt', 'a') as f:
                f.write(cmd)

        elif cmd_res.find('connection timed out') > 0:
            with open('axfr/time_out_hosts.txt', 'a') as f:
                f.write(cmd)

        if cmd_res.find('Transfer failed.') < 0 and cmd_res.find('connection timed out') < 0 and cmd_res.find(
                'XFR size') > 0:
            lock.acquire()
            print '*' * 10 + ' Vulnerable dns server found:', cmd, '*' * 10
            lock.release()
            with open('axfr_vulnerable_hosts.txt', 'a') as f:
                f.write(cmd)
            with open('dnsaxfr/' + server + NS+ '.txt', 'w') as f:
                f.write(cmd_res)

threads = []
for i in range(1000):
    t = threading.Thread(target=test_DNS_Servers)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print 'All Done!'
