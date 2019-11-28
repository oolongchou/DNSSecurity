import mysql.mysql as mysql
import sys




def usage():

    print("Usage: "+sys.argv[0]+" domain_txts")





def main():
    global DB, CURSOR

    if len(sys.argv) == 1:
        usage()
        sys.exit()

    domain_txt = sys.argv[1]

    DB, CURSOR = mysql.connect()

    file = open(domain_txt,"r")
    for line in file:
        line = line.strip()
        domain = line.split("\t")[0]
        ns = line.split("\t")[1]
        ns_a = line.split("\t")[2]
        sql_cmd="INSERT INTO domain2019(domain,category,ns,ns_ip) VALUES ('" + str(domain) + "',4,'" + str(ns) + "','" + str(ns_a) + "')"
        mysql.do_sql(DB, CURSOR,sql_cmd)


    mysql.disconnect(DB)

if __name__ == '__main__':
    main()