import http.client
import mimetypes

#Epoch time
import time

#Parse JSON
import json

#thebel1 GPIO
import sys
from pimonLib import *



#fix SSL cert issues
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context

conn = http.client.HTTPSConnection("vrops.fios-router.home")
payload = "{\n  \"username\" : \"admin\",\n  \"password\" : \"Password01!\"\n}"
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
conn.request("POST", "/suite-api/api/auth/token/acquire", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

#Epoch Time
epoch_var = int(time.time())

#Parse JSON
vrops_auth = data.decode("utf-8")
auth_dict = json.loads(vrops_auth)
token_var = auth_dict['token']

# OK, we now have the auth token, let's push some data

#Get the CPU Temp using code from https://github.com/thebel1/thpimon/blob/main/pyUtil/pimon_util.py
pimon = PiMon()
boardMACBytes = pimon.getBoardMAC().to_bytes(6, 'little')
boardMACArr = []
boardMACStr = 'NONE'
for i in range(len(boardMACBytes)):
    byteStr = '{:x}'.format(int.from_bytes(boardMACBytes[i:i+1], 'little'))
    boardMACArr.append(byteStr)
if boardMACArr is not None:
    boardMACStr = ':'.join(boardMACArr)
temp_var=pimon.getTemp()

conn = http.client.HTTPSConnection("vrops.fios-router.home")

#build the payload line with updated epoch time.
payload = "{\n  \"property-content\" : [ \n      {\n    \"statKey\" : \"CustomProps|CPUTemp\",\n    \"timestamps\" : [ " + str(epoch_var) + " ],\n    \"data\" : [ " + str(temp_var) + " ],\n    \"others\" : [ ],\n    \"otherAttributes\" : { }\n     } \n  ]\n}"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'vRealizeOpsToken ac97277c-b93c-4f1a-a2a0-45e9b5241037::7f382880-f3bd-4eec-88e5-0f1106fedc5c',
  'Accept': 'application/json'
}

#Update the Authorization token
headers["Authorization"] = "vRealizeOpsToken " + token_var

conn.request("POST", "/suite-api/api/resources/85965d5f-de89-4f79-9131-8552d007d0a7/properties", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
