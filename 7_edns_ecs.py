#!/usr/bin/python
# coding: utf-8

# parse the captured packets
import dpkt
import socket
import sys
import os
import sys
import threading


result = {}
#client = "10.0.0.5"       # where is the request sent from?

filename = sys.argv[1]
bufsize= sys.argv[2]
ecs_support=sys.argv[3]
file = open(filename, "r")
domains=[]

for eachline in file:
    eachline=eachline.strip()
    domains.append(eachline)


lock = threading.Lock()
c_index = 0




def process_thread():
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
        qdomain=domain.split("\t")[0]
        ns = domain.split("\t")[-1]
        if (ecs_support==1):
            cmd = "dig +subnet=10.0.0.1/16 +edns +bufsize="+bufsize+" @" + ns + " " + qdomain
            try:
                cmd_res = os.popen(cmd).read()
                if cmd_res.find('status: NOERROR') > 0 and cmd_res.find('; CLIENT-SUBNET:') > 0:
                    with open(filename.strip(".pcap") + '_ecs_vaild.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('status: FORMERR') > 0 and cmd_res.find('; CLIENT-SUBNET:') > 0:
                    with open(filename.strip(".pcap") + '_ecs_FORMERR.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('status: REFUSED') and cmd_res.find('; CLIENT-SUBNET:') > 0:
                    with open(filename.strip(".pcap") + '_ecs_REFUSED.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('status: NOTIMP') and cmd_res.find('; CLIENT-SUBNET:') > 0:
                    with open(filename.strip(".pcap") + '_ecs_NOTIMP.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('status: BADVERS') and cmd_res.find('; CLIENT-SUBNET:') > 0:
                    with open(filename.strip(".pcap") + '_ecs_BADVERS.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('status: SERVFAIL') and cmd_res.find('; CLIENT-SUBNET:') > 0:
                    with open(filename.strip(".pcap") + '_ecs_SERVFAIL.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('; CLIENT-SUBNET:') == 0:
                    with open(filename.strip(".pcap") + '_no_ecs.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                if cmd_res.find('; EDNS: version: 0') > 0:
                    with open(filename.strip(".pcap") + '_edns.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('connection timed out;') > 0:
                    with open(filename.strip(".pcap") + '_time_out.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif len(cmd_res) == 0:
                    with open(filename.strip(".pcap") + '_invaild_ns.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                else:
                    with open(filename.strip(".pcap") + '_no_edns.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
            except Exception as e:
                print e
                with open(filename.strip(".pcap") + '_error.txt', 'a') as f:
                    f.write(qdomain + "," + ns + "\n")
                continue
        else:
            cmd = "dig +edns +bufsize="+bufsize+" @" + ns + " " + qdomain
            try:
                cmd_res = os.popen(cmd).read()
                if cmd_res.find('; EDNS: version: 0') > 0:
                    with open(filename.strip(".txt") + '_edns.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif len(cmd_res) == 0:
                    with open(filename.strip(".txt") + '_invaild_ns.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                elif cmd_res.find('connection timed out;') > 0:
                    with open(filename.strip(".txt") + '_time_out.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
                else:
                    with open(filename.strip(".txt") + '_no_edns.txt', 'a') as f:
                        f.write(qdomain + "," + ns + "\n")
            except Exception as e:
                print e
                with open(filename.strip(".txt") + '_error.txt', 'a') as f:
                    f.write(qdomain + "," + ns + "\n")
                continue

threads = []
for i in range(100):
    t = threading.Thread(target=process_thread)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

file.close()
print '******************All Done!******************'