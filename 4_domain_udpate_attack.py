# encoding=gbk

import threading
import os
import re

urls = []

# fobj = open('attack/updatelist.txt')


fobj = open('attack/updatelist.txt')
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
        server = urls[c_index][:-1]

        #server = urls[c_index]
        #cmd = "nsupdate update/"+server+".txt"

        #cmd = "nsupdate update/"+server+".txt 2>> updateerror/"+server+"_error.txt"
        cmd = "nsupdate update/" + server + ".txt"


        #print "---testing:" + urls[c_index]

        c_index += 1
        lock.release()
        cmd_res = os.popen(cmd).read()
        if "update failed: REFUSED" in str(cmd_res):

            with open('update_refused_hosts.txt', 'a') as f:
                f.write(cmd + "\n")
        elif "update failed: NOTIMP" in cmd_res:

            with open('update_notimp_hosts.txt', 'a') as f:
                f.write(cmd + "\n")
        elif "update failed: NOTAUTH" in cmd_res:

            with open('update_notauth_hosts.txt', 'a') as f:
                f.write(cmd + "\n")
        elif "couldn't get address" in cmd_res:

            with open('update_noaddr_hosts.txt', 'a') as f:
                f.write(cmd + "\n")
        elif "timed out" in cmd_res:

            with open('update_timed_out_hosts.txt', 'a') as f:
                f.write(cmd + "\n")
        else:
            with open('other_hosts.txt', 'a') as f:
                f.write(cmd + "\n")
                f.write(str(cmd_res) + "\n")


threads = []
for i in range(100):
    t = threading.Thread(target=test_DNS_Servers)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print 'All Done!'






