import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import re
import socket

###############################
##           GLOBAL          ##
###############################
timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

ncloud_accesskey = "accesskey"
ncloud_secretkey = "secretkey"

method = "GET"
space = " "
new_line = "\n"

api_server = "https://ncloud.apigw.ntruss.com"

regionCode = 'KR'

#vpc ID 
vpc = VPC_ID
vpc = str(vpc)

#타겟그룹 
targetGroupNo = Target_Group_ID
targetGroupNo = str(targetGroupNo)

###############################
##    GET_SERVER_HOSTNAME    ##
###############################
def get_hostname():
	hostname = socket.gethostname()

	return hostname 

###############################
##    GET_SERVER_IP          ##
###############################
def get_ip():
	ip = socket.gethostbyname(socket.gethostname())

	return ip 

###############################
##     GET_SERVER_NUMBER     ##
###############################
def get_servernumber():
	hostname = get_hostname()
	ip = get_ip()

	get_server_api_url = "/vserver/v2/getServerInstanceList"
      
	#get_server_api_url = get_server_api_url +"?regionCode=" + regionCode + "&vpcNo=" + vpc +"&serverInstanceStatusCode=RUN" + "&serverName=" + hostname 
	get_server_api_url = get_server_api_url +"?regionCode=" + regionCode + "&vpcNo=" + vpc +"&serverInstanceStatusCode=RUN" + "&serverName=" + hostname + "&ip=" + ip

	get_server_message = method + space + get_server_api_url + new_line + timestamp + new_line + ncloud_accesskey
	get_server_message = bytes(get_server_message, 'UTF-8')

	get_server_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
	get_server_signingKey = base64.b64encode(hmac.new(get_server_ncloud_secretkey, get_server_message, digestmod=hashlib.sha256).digest())

	get_server_http_header = {
		'x-ncp-apigw-timestamp': timestamp,
		'x-ncp-iam-access-key': ncloud_accesskey,
		'x-ncp-apigw-signature-v2': get_server_signingKey
	}

	get_server_response = requests.get(api_server + get_server_api_url, headers=get_server_http_header)
	print(api_server)
	print(get_server_api_url)
	response_txt = re.sub("\<|\>|\/", "", get_server_response.text)
	response_txt = list(response_txt.split())

	rs_key = []
	key = 'serverInstanceNo'

	for word in response_txt:
		if key in word:
			rs_key.append(word)

	str_rs_key = ' '.join(s for s in rs_key) 

	serverInstanceNo = str_rs_key.replace('serverInstanceNo', '')

	return(serverInstanceNo)

###############################
##     GET_TARGET_NUMBER     ##
###############################
def get_target():
	get_api_url = "/vloadbalancer/v2/getTargetList"
	get_api_url = get_api_url +"?regionCode=" + regionCode + "&targetGroupNo=" + targetGroupNo 

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

	totalRows =[]
	rs_key = []
	key = 'totalRows'

	for word in response_txt:
		if key in word:
			rs_key.append(word)

	str_rs_key = ' '.join(s for s in rs_key) 

	totalRows = str_rs_key.replace('totalRows', '')
	totalRows =(int(totalRows))
	totalRows = totalRows + 1 
	totalRows = (str(totalRows))

	return(totalRows)

###############################
##            ADD            ##
###############################
def add_target():
	#함수 호출 
	totalRows = get_target()
	print(totalRows)
	servernumber = get_servernumber()
	print(servernumber)

	add_api_url = "/vloadbalancer/v2/addTarget"
	add_api_url = add_api_url +"?regionCode=" + regionCode + "&targetGroupNo=" + targetGroupNo + "&targetNoList." + totalRows + "=" + servernumber

	add_message = method + space + add_api_url + new_line + timestamp + new_line + ncloud_accesskey
	add_message = bytes(add_message, 'UTF-8')

	add_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
	add_signingKey = base64.b64encode(hmac.new(add_ncloud_secretkey, add_message, digestmod=hashlib.sha256).digest())

	add_http_header = {
		'x-ncp-apigw-timestamp': timestamp,
		'x-ncp-iam-access-key': ncloud_accesskey,
		'x-ncp-apigw-signature-v2': add_signingKey
	}

	add_response = requests.get(api_server + add_api_url, headers=add_http_header)


add_target()
