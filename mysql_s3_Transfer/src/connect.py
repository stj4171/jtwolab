import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element,ElementTree,SubElement,dump
import base64

#config xml read
filepath = "config.xml"
tree = ET.parse(filepath)

#ET.dump(tree)

root = tree.getroot()

#Database config read
database = root.find("Database")

type = database.attrib["type"]
host = database.attrib["host"]
port = database.attrib["port"]
user = database.attrib["user"]

#passwd decode or passwd get
if 'passwd' in database.attrib:
    passwd = database.attrib["passwd"]
    #print("passwd : ", passwd)
else:
    passwd_enc = database.attrib["passwd_enc"]
    #print("passwd_enc : ", passwd_enc)
    dpasswd_enc = base64.b64decode(passwd_enc)
    passwd = dpasswd_enc.decode('ascii')
    #print(passwd)

charset = database.attrib["charset"]

#s3 config read
s3 = root.find("S3")

region_name = s3.attrib["region_name"]

aws_access_key_id_enc = s3.attrib["aws_access_key_id_enc"]
daws_access_key_id_enc = base64.b64decode(aws_access_key_id_enc)
aws_access_key_id = daws_access_key_id_enc.decode('ascii')

aws_secret_access_key_enc = s3.attrib["aws_secret_access_key_enc"]
daws_secret_access_key_enc = base64.b64decode(aws_secret_access_key_enc)
aws_secret_access_key = daws_secret_access_key_enc.decode('ascii')


#print("DB INFO - type : ", type)
#print("DB INFO - host : ", host)
#print("DB INFO - port : ", port)
#print("DB INFO - user : ", user)
#print("DB INFO - passwd : ", passwd)

#print("DB INFO - charset : ", charset)
