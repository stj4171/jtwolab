import sys
import os
import boto3
import connect as config

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

s3 = s3_connection()
response = s3.list_buckets()
print(response)

buckets = [bucket['Name'] for bucket in response['Buckets']]
print("bucket name : %s" % buckets)

obj_list = s3.list_objects(Bucket="teststj", Prefix="test")
print("obj : %s" % obj_list)
contents_list = obj_list['Contents']
print("contents : %s" % contents_list)

file_list=[]
check_exist_file = False

for content in contents_list:
    print("content : %s" % content)
    key = content['Key']
    file_list.append(key)



for file in file_list:
    print("file : %s" % file)
    if file == "test/test.jpg":        
        check_exist_file = True
        break
    else:
        check_exist_file = False

if check_exist_file == True:
    print("file exist")
else:
    print("file not exist")
    s3.upload_file("img/test.jpg", "teststj", "test/test.jpg")