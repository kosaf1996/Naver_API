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
ncloud_secretkey = "ncloud_accesskey"

method = "GET"
space = " "
new_line = "\n"

api_server = "https://ncloud.apigw.gov-ntruss.com"

ServerImageName_list=['test1', 'test2', 'test3', 'test4' ]
regionCode = 'KR'

serverImage_Number = []
return_code = []

###Delete Image Function
def delete_image():
	#for image, name in zip (Instance_list, ServerImageName_list):
	for name in ServerImageName_list:

		name = str(name)
		#image = str(image)

		#serverInstanceNo = image
		memberServerImageName = name + '-' + str_dt 

		get_api_url = "/vserver/v2/getMemberServerImageInstanceList"
		get_api_url = get_api_url +"?regionCode=" + regionCode + "&memberServerImageName=" + memberServerImageName

		get_message = method + space + get_api_url + new_line + timestamp + new_line + ncloud_accesskey
		get_message = bytes(get_message, 'UTF-8')

		get_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
		get_signingKey = base64.b64encode(hmac.new(get_ncloud_secretkey, get_message, digestmod=hashlib.sha256).digest())

		get_http_header = {
			'x-ncp-apigw-timestamp': timestamp,
			'x-ncp-iam-access-key': ncloud_accesskey,
			'x-ncp-apigw-signature-v2': get_signingKey
		}

		get_response = requests.get(api_server + get_api_url, headers=get_http_header)

		response_txt = re.sub("\<|\>|\/", "", get_response.text)
		response_txt = list(response_txt.split())

		rs_key = []
		key = 'memberServerImageInstanceNo'

		for word in response_txt:
			if key in word:
				rs_key.append(word)

		str_rs_key = ' '.join(s for s in rs_key) 
		memberServerImageInstanceNo = str_rs_key.strip(key) 
	
		serverImage_Number.append(memberServerImageInstanceNo)

		delete_api_url = "/vserver/v2/deleteMemberServerImageInstances"
		delete_api_url = delete_api_url +"?regionCode=" + regionCode + "&memberServerImageInstanceNoList.1=" + memberServerImageInstanceNo

		delete_message = method + space + delete_api_url + new_line + timestamp + new_line + ncloud_accesskey
		delete_message = bytes(delete_message, 'UTF-8')

		delete_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
		signingKey = base64.b64encode(hmac.new(delete_ncloud_secretkey, delete_message, digestmod=hashlib.sha256).digest())

		delete_headers = {
			'x-ncp-apigw-timestamp': timestamp,
			'x-ncp-iam-access-key': ncloud_accesskey,
			'x-ncp-apigw-signature-v2': signingKey
		}

		delete_response = requests.get(api_server + delete_api_url, headers=delete_headers)
		
		response_txt = re.sub("\<|\>|\/", "", delete_response.text)
		response_txt = list(response_txt.split())

		rs_key = []
		key = 'returnMessage'

		for word in response_txt:
			if key in word:
				rs_key.append(word)

		str_rs_key = ' '.join(s for s in rs_key) 

		returnMessage = str_rs_key.replace('returnMessage', '')

		return_code.append(returnMessage)

###Delete Log Function 
def return_status():
	f =open(f'logs/{str_dt}_delete.log', 'w')
	for image, name, status in zip (serverImage_Number, ServerImageName_list, return_code):
		f.write(f'{dt}   ServerImageName : {name}   Image_Instance_Number : {image}  Status : {status} \n')
	
	f.close()

###Log Delete Function
def log_delete():
	path_target =  ('logs')
	days_elapsed = 30 #로그 30일 보관 
	for f in os.listdir(path_target):
		f = os.path.join(path_target, f)
		if os.path.isfile(f): 
			timestamp_now = datetime.now().timestamp() 
			is_old = os.stat(f).st_mtime < timestamp_now - (days_elapsed * 24 * 60 * 60)
			if is_old:
				try:
					os.remove(f) 
				except OSError: 
					print('can not delete') 

###Function Call 
delete_image()
return_status()
log_delete()
