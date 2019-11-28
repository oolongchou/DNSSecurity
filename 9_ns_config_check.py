import mysql.mysql as mysql
import sys


def main():
    global DB, CURSOR
    count = 0

    DB, CURSOR = mysql.connect()

    sql_cmd="select distinct(domain) from domain2019 where category=4 ;"

    domain_list=mysql.query_sql(DB, CURSOR,sql_cmd)
    for domain in domain_list:
        domain_Str=str(domain).lstrip("(u'").strip("',)")
        #print domain_Str
        sql_cmd_1 = "select ns_ip from domain2019 where domain = '"+ domain_Str +"' ;"

        ns_list = mysql.query_sql(DB, CURSOR,sql_cmd_1)

        if len(ns_list)<2:
            count =count +1
            with open('gov_ns_misconfig.txt', 'a') as f:
                f.write(domain_Str+"\n")
        elif len(ns_list)==2:
            if str(ns_list[0]).split(".")[0:2]==str(ns_list[1]).split(".")[0:2]:
                count = count + 1
                with open('gov_ns_misconfig.txt', 'a') as f:
                    f.write(domain_Str + "\n")

    mysql.disconnect(DB)
    print(count)
if __name__ == '__main__':
    main()