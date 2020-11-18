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
payload = "{\n  \"username\" : \"admin\",\n  \"password\" : \"Beanie01!\"\n}"
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
#print("epoch_var: ", epoch_var, "\n")

#Parse JSON
vrops_auth = data.decode("utf-8")
auth_dict = json.loads(vrops_auth)
#print("All JSON: ", auth_dict, "\n")
#print("Just token: ", auth_dict['token'], "\n")
token_var = auth_dict['token']
#print("token_var: ", token_var, "\n")

# OK, we now have the auth token, let's push some data
#auth_var = "'vRealizeOpsToken " + token_var + "'"
#print("auth_var: ", auth_var, "\n")

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
#print('Firmware Revision:\t{}'.format(hex(pimon.getFWRev())))
#print('Board Model:\t\t{}'.format(pimon.getBoardModel()))
#print('Board Revision:\t\t{}'.format(hex(pimon.getBoardRev())))
#print('Board MAC Address:\t{}'.format(boardMACStr))
#print('Board Serial:\t\t{0:#0{1}x}'.format(pimon.getBoardSerial(), 16))
#print('Temp:\t\t\t{} (deg. C)'.format(pimon.getTemp()))
#print('Temp : ', pimon.getTemp())
temp_var=pimon.getTemp()
#print('temp_var : ', temp_var, '\n')

conn = http.client.HTTPSConnection("vrops.fios-router.home")

#payload = "{\n  \"property-content\" : [ \n      {\n    \"statKey\" : \"CustomProps|CPUTemp\",\n    \"timestamps\" : [ 1605487211384 ],\n    \"data\" : [ 50 ],\n    \"others\" : [ ],\n    \"otherAttributes\" : { }\n     } \n  ]\n}"
#build the payload line with updated epoch time.
payload = "{\n  \"property-content\" : [ \n      {\n    \"statKey\" : \"CustomProps|CPUTemp\",\n    \"timestamps\" : [ " + str(epoch_var) + " ],\n    \"data\" : [ " + str(temp_var) + " ],\n    \"others\" : [ ],\n    \"otherAttributes\" : { }\n     } \n  ]\n}"
print("payload: ", payload, "\n")

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'vRealizeOpsToken ac97277c-b93c-4f1a-a2a0-45e9b5241037::7f382880-f3bd-4eec-88e5-0f1106fedc5c',
  'Accept': 'application/json'
}

#Update the Authorization token
headers["Authorization"] = "vRealizeOpsToken " + token_var
#print("headers: ", headers, "\n")

conn.request("POST", "/suite-api/api/resources/85965d5f-de89-4f79-9131-8552d007d0a7/properties", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
