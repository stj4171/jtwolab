import sys
import pymysql
import boto3
import datetime as dt
import connect as config

#mysql connect
def mysql_connection():
    try:
        
        g_host = config.host
        g_port = int(config.port)
        g_user = config.user
        g_passwd = config.passwd
        g_charset = config.charset
        
        mysql_conn = pymysql.connect(host=g_host,
                               port=g_port,
                               user=g_user,
                               passwd=g_passwd,
                               db='test',
                               charset=g_charset )

    except Exception as e:
        print(e)
    else:
        print("mysql connect")
        return mysql_conn

#aws s3 connect
def s3_connection():
    try:
        g_region_name = config.region_name
        g_aws_access_key_id = config.aws_access_key_id
        g_aws_secret_access_key = config.aws_secret_access_key

        s3 = boto3.client(
            service_name = "s3",
            region_name = g_region_name,
            aws_access_key_id = g_aws_access_key_id,
            aws_secret_access_key = g_aws_secret_access_key
        )
    except Exception as e:
        print(e)
    else:
        print("s3 buket connect")
        return s3

g_type = config.type

#file name make
now_dt = dt.datetime.now()
file_name = str(now_dt.year) + str(now_dt.month) + str(now_dt.day) + "_test.csv"
now_dt_str = str(now_dt.year) + str(now_dt.month) + str(now_dt.day)

#get mysql data
if g_type != "mysql":
    print("Is not mysql")
else:
    conn = mysql_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select t1, t2 from test"
    curs.execute(sql)

    rows=curs.fetchall()
    #print(rows)
    result=[]

    #get sql data
    for row in rows:
        #print(row)       
        #print("t1 : %s, t2 : %s" % (row['t1'],row['t2']))
        test = [row['t1'], row['t2']]
        if result is None:
            result = test
        else:
            result.append(test)
    
    #make csv
    f = open(file_name,"w")
    for line in result:
        input = "'" + line[0] + "'," + str(line[1]) + "\n"
        #print(input)
        f.write(input)
    
    f.close()

    conn.close()

#print(type(result))


#input csv to s3 
if len(result) :
    s3 = s3_connection()
    response = s3.list_buckets()
    #print(response)

    #bucket check
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    #print("bucket name : %s" % buckets)

    obj_list = s3.list_objects(Bucket="teststj")
    print("obj : %s" % obj_list)
    contents_list = obj_list['Contents']
    print("contents : %s" % contents_list)

    file_list=[]
    check_exist_file = False

    for content in contents_list:
        #print("content : %s" % content)
        key = content['Key']
        file_list.append(key)


    #bucket file check
    for file in file_list:
        #print("file : %s" % file)
        if file == now_dt_str + "/" + file_name:        
            check_exist_file = True
            break
        else:
            check_exist_file = False

    if check_exist_file == True:
        print("file exist")
    else:
        print("file not exist")
        s3.upload_file(file_name, "teststj", now_dt_str + "/" + file_name)