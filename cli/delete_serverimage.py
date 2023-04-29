import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import datetime
import re

# 현재 시간 정보
dt = datetime.datetime.now()
format = "%Y-%m-%d"
str_dt = datetime.datetime.strftime(dt,format)

# unix timestamp 설정
timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

# Ncloud API Key 설정
ncloud_accesskey = ""
ncloud_secretkey = ""

# 암호화 문자열 생성을 위한 기본값 설정
method = "GET"
space = " "
new_line = "\n"

# API 서버 정보
api_server = "https://ncloud.apigw.ntruss.com"

#Server InstenceNo List 15058826
Instance_list=[] #동일한 서버 이미지 들어가면 에러 발생합니다. 
ServerImageName_list=['test1', 'test2']
regionCode = 'KR'

def delete_image():
	for image, name in zip (Instance_list, ServerImageName_list):
		#문자열 변환
		name = str(name)
		image = str(image)

		serverInstanceNo = image
		memberServerImageName = name + '-' + str_dt # 현재 날짜로 서버 이미지 네이밍
		# GET API URL
		get_api_url = "/vserver/v2/getMemberServerImageInstanceList"
		get_api_url = get_api_url +"?regionCode=" + regionCode + "&memberServerImageName=" + memberServerImageName

		# hmac으로 암호화할 문자열 생성
		get_message = method + space + get_api_url + new_line + timestamp + new_line + ncloud_accesskey
		get_message = bytes(get_message, 'UTF-8')

		# hmac_sha256 암호화
		get_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
		get_signingKey = base64.b64encode(hmac.new(get_ncloud_secretkey, get_message, digestmod=hashlib.sha256).digest())

		# http 호출 헤더값 설정
		get_http_header = {
			'x-ncp-apigw-timestamp': timestamp,
			'x-ncp-iam-access-key': ncloud_accesskey,
			'x-ncp-apigw-signature-v2': get_signingKey
		}

		# GET api 호출
		get_response = requests.get(api_server + get_api_url, headers=get_http_header)
		#print(get_response.text)

		### ServerInstanceNo 검출 [Start]###
		response_txt = re.sub("\<|\>|\/", "", get_response.text)
		response_txt = list(response_txt.split())

		rs_key = []
		key = 'memberServerImageInstanceNo'

		# ServerInstanceNo 추출 반복문 - List형
		for word in response_txt:
			if key in word:
				rs_key.append(word)

		str_rs_key = ' '.join(s for s in rs_key) # List to String 형 변환
		memberServerImageInstanceNo = str_rs_key.strip(key) # ServerInstanceNo 추출 - String형

		### ---------- GET IMAGE Configure END ------------ ###


		### ---------- DELETE IMAGE Configure START ------------ ####

		# API URL
		delete_api_url = "/vserver/v2/deleteMemberServerImageInstances"
		delete_api_url = delete_api_url +"?regionCode=" + regionCode + "&memberServerImageInstanceNoList.1=" + memberServerImageInstanceNo

		# hmac으로 암호화할 문자열 생성
		delete_message = method + space + delete_api_url + new_line + timestamp + new_line + ncloud_accesskey
		delete_message = bytes(delete_message, 'UTF-8')

		# hmac_sha256 암호화
		delete_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
		signingKey = base64.b64encode(hmac.new(delete_ncloud_secretkey, delete_message, digestmod=hashlib.sha256).digest())

		# http 호출 헤더값 설정
		delete_headers = {
			'x-ncp-apigw-timestamp': timestamp,
			'x-ncp-iam-access-key': ncloud_accesskey,
			'x-ncp-apigw-signature-v2': signingKey
		}

		response = requests.get(api_server + delete_api_url, headers=delete_headers)
		
#함수 호출 
delete_image()