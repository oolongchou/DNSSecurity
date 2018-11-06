#!/usr/bin/env python
#

from __future__ import print_function

"""
Lookup an NS record and printout all the hostnames and associated IP
addresses of the listed nameservers.
zone transfer check for each nameserver 
"""
import os
import getdns, pprint, sys,time

extensions = { "return_both_v4_and_v6" : getdns.EXTENSION_TRUE }


def usage():
    print("""Usage: AFXR.py <zone>

where <zone> is a DNS zone (domain).
""")
    sys.exit(1)


def get_ip(ctx, qname):
    iplist = []
    try:
        results = ctx.address(name=qname, extensions=extensions)
    except getdns.error as e:
        print(str(e))
        sys.exit(1)

    if results.status == getdns.RESPSTATUS_GOOD:
        for addr in results.just_address_answers:
            iplist.append(addr['address_data'])
    else:
        print("getdns.address() returned an error: {0}".format(results['status']))
    return iplist


if __name__ == '__main__':

    if len(sys.argv) != 2:
        usage()

    qname = sys.argv[1]

    ctx = getdns.Context()
    try:
        results = ctx.general(name=qname, request_type=getdns.RRTYPE_NS)
    except getdns.error as e:
        print(str(e))
        pass
    status = results.status

    hostlist = []
    if status == getdns.RESPSTATUS_GOOD:
        for reply in results.replies_tree:
            answers = reply['answer']
            for answer in answers:
                if answer['type'] == getdns.RRTYPE_NS:
                    iplist = get_ip(ctx, answer['rdata']['nsdname'])
                    for ip in iplist:
                        try:
                            hostlist.append( (answer['rdata']['nsdname'], ip) )
                        except:
                            pass

    elif status == getdns.RESPSTATUS_NO_NAME:
        print("{0}: no such DNS zone".format(qname))
    elif status == getdns.RESPSTATUS_ALL_TIMEOUT:
        print("{0}, NS: query timed out".format(qname))
    else:
        print("{0}, NS: unknown return code: {1}".format(qname, results["status"]))

    # Print out each NS server name and IP address
    for (nsdname, addr) in sorted(hostlist):



        try:
            outfile = open("DNS_Update_Record/" + nsdname + ".txt", "w")
            outfile.writelines("server " + addr + "\n" + "update add thutest." + qname
             + " 86400 IN A 9.9.9.9" + "\n" + "send \n")
        except:
            pass


        nsupdatecmd=("server " + addr + "\n" + "update add thutest." + qname
             + " 86400 IN A 9.9.9.9" + "\n" + "send \n")
        cmd = "nsupdate DNS_Update_Record/"+nsdname+".txt 2>> DNS_Update_Error/"+nsdname+"_error.txt"

       # print(cmd)
        cmd_res = os.popen(cmd).read()
        if cmd_res.find('REFUSED')>0:
            print("Congratulations! \n DNS_Vulnerable_Update_REFUSED_By_Server.\n ")
            exit(0)
        else:
            print("Waiting for update to take effect...\n ")
            time.sleep(10)

            cmd = ("dig @" + addr + " thutest." + qname + "\n")
            cmd_res = os.popen(cmd).read()
            # print(cmd_res)
            if cmd_res.find('NXDOMAIN') > 0:
                print("Congratulations! \n DNS_Vulnerable_Update_Free\n ")
            if cmd_res.find('9.9.9.9') > 0:
                print('*' * 10 + ' Vulnerable update dns server found:', nsdname, +":::" + addr, '*' * 10)

                with open('DNSSercurityWeakness/DNS_Vulnerable_Update.txt', 'a') as f:
                    f.write(qname + "_" + nsdname + "_" + addr + "\n")
                with open('DNS_Vulnerable_Update/' + cmd + '.txt', 'w') as f:
                    f.write(cmd_res + "\n")

        #print(cmd_res)
