import sys
import pymysql
import csv
import connect as config

c_type = config.type
c_host = config.host
c_port = int(config.port)
c_user = config.user
c_passwd = config.passwd
c_charset = config.charset

if c_type != "mysql":
    print("Is not mysql")
else:
    conn = pymysql.connect(host=c_host, port=c_port, user=c_user,passwd=c_passwd, db='test', charset=c_charset )
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select t1, t2 from test"
    curs.execute(sql)

    rows=curs.fetchall()
    #print(rows)
    result=[]
    for row in rows:
        #print(row)       
        print("t1 : %s, t2 : %s" % (row['t1'],row['t2']))
        test = [row['t1'], row['t2']]
        if result is None:
            result = test
        else:
            result.append(test)
        
    f = open("test.csv","w")
    for line in result:
        input = "'" + line[0] + "'," + str(line[1]) + "\n"
        print(input)
        f.write(input)
    
    f.close()

    conn.close()

