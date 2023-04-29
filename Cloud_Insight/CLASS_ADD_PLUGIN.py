import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json
def main():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    access_key = ''
    secret_key = ''
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    regionCode = 'KR'

    api_server = "https://cw.apigw.gov-ntruss.com"
    uri = "/cw_server/real/api/plugin/process/add"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    http_header = {
            'x-ncp-apigw-signature-v2': signingKey,
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': access_key,
            'x-ncp-dmn_cd': 'GOV',
            'x-ncp-region_code': regionCode

            }
    payload = {
        #"prodKey": class_cw_key,
        "configList": [

        ],
        "instanceNo": "",
        "type": "ClassicServer"
    }
    response = requests.post(api_server + uri, headers=http_header, json=payload)
    print(response.text)
main()

