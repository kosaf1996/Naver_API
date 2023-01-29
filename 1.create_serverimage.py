import sys
import os
import hashlib
import hmac
import base64
import requests
import time
from datetime import datetime
import re

###Global
dt = datetime.now()
format = "%Y-%m-%d"
str_dt = datetime.strftime(dt,format)

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

ncloud_accesskey = "ncloud_accesskey"
ncloud_secretkey = "ncloud_secretkey"

method = "GET"
space = " "
new_line = "\n"

log_path = "/api/logs"

api_server = "https://ncloud.apigw.gov-ntruss.com"

Instance_list=[인스턴스ID, 인스턴스ID, 인스턴스ID, 인스턴스ID] #동일한 서버 이미지 들어가면 에러 발생합니다. 
ServerImageName_list=['test1', 'test2', 'test3', 'test4' ]
regionCode = 'KR'

return_code = []

###Image Create Function
def create_image():
	for image, name in zip (Instance_list, ServerImageName_list):

		name = str(name)
		image = str(image)

		serverInstanceNo = image
		memberServerImageName = name + '-' + str_dt 

		create_api_url = "/vserver/v2/createMemberServerImageInstance"
		create_api_url = create_api_url +"?regionCode=" + regionCode + "&serverInstanceNo=" + serverInstanceNo + "&memberServerImageName=" + memberServerImageName 

		create_message = method + space + create_api_url + new_line + timestamp + new_line + ncloud_accesskey
		create_message = bytes(create_message, 'UTF-8')

		create_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
		create_signingKey = base64.b64encode(hmac.new(create_ncloud_secretkey, create_message, digestmod=hashlib.sha256).digest())

		create_http_header = {
			'x-ncp-apigw-timestamp': timestamp,
			'x-ncp-iam-access-key': ncloud_accesskey,
			'x-ncp-apigw-signature-v2': create_signingKey
		}
		create_response = requests.get(api_server + create_api_url, headers=create_http_header)

		response_txt = re.sub("\<|\>|\/", "", create_response.text)
		response_txt = list(response_txt.split())

		rs_key = []
		key = 'returnMessage'

		for word in response_txt:
			if key in word:
				rs_key.append(word)

		str_rs_key = ' '.join(s for s in rs_key) 

		returnMessage = str_rs_key.replace('returnMessage', '')

		return_code.append(returnMessage)


###Create Log 
def return_status():
	f =open(f'{log_path}/{str_dt}_create.log', 'w')
	for image, name, status in zip (Instance_list, ServerImageName_list, return_code):
		f.write(f'{dt}   ServerImageName : {name}   Server_Instance_Number : {image}  Status : {status} \n')
	
	f.close()

###Function Call
create_image()
return_status()
