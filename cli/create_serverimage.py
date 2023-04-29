import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import datetime

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

Instance_list=[] #동일한 서버 이미지 들어가면 에러 발생합니다. 
ServerImageName_list=[]
regionCode = 'KR'

def create_image():
	for image, name in zip (Instance_list, ServerImageName_list):

		#문자열 변환
		name = str(name)
		image = str(image)

		serverInstanceNo = image
		memberServerImageName = name + '-' + str_dt # 현재 날짜로 서버 이미지 네이밍


		# CREATE API URL
		create_api_url = "/vserver/v2/createMemberServerImageInstance"
		create_api_url = create_api_url +"?regionCode=" + regionCode + "&serverInstanceNo=" + serverInstanceNo + "&memberServerImageName=" + memberServerImageName 

		# hmac으로 암호화할 문자열 생성
		create_message = method + space + create_api_url + new_line + timestamp + new_line + ncloud_accesskey
		create_message = bytes(create_message, 'UTF-8')

		# hmac_sha256 암호화
		create_ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
		create_signingKey = base64.b64encode(hmac.new(create_ncloud_secretkey, create_message, digestmod=hashlib.sha256).digest())

		# http 호출 헤더값 설정
		create_http_header = {
			'x-ncp-apigw-timestamp': timestamp,
			'x-ncp-iam-access-key': ncloud_accesskey,
			'x-ncp-apigw-signature-v2': create_signingKey
		}
		create_response = requests.get(api_server + create_api_url, headers=create_http_header)
	
#함수 호출 
create_image()



