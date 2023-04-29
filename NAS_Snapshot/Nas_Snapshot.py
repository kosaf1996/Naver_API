import sys
import os
import hashlib
import hmac
import base64
import requests
import time
from datetime import datetime, timedelta
import re

###Global
class Nas_Snapshot:
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self):

        timestamp = int(time.time() * 1000)
        self.timestamp = str(timestamp)

        self.ncloud_accesskey = ""
        self.ncloud_secretkey = ""


        self.space = " "
        self.new_line = "\n"

        self.log_path = "/api/logs"

        self.api_server = "https://ncloud.apigw.ntruss.com"

        self.regionCode = 'KR'
        
        self.nasvolume = ''

    #########################################
    ##          Create SnapShot            ##
    #########################################
    def create_snapshot(self):
        method = "GET"

        create_api_url = "/vnas/v2/createNasVolumeSnapshot"
        create_api_url = create_api_url +"?regionCode=" + self.regionCode + "&nasVolumeInstanceNo=" + self.nasvolume 

        create_message = method + self.space + create_api_url + self.new_line + self.timestamp + self.new_line + self.ncloud_accesskey
        create_message = bytes(create_message, 'UTF-8')

        create_ncloud_secretkey = bytes(self.ncloud_secretkey, 'UTF-8')
        create_signingKey = base64.b64encode(hmac.new(create_ncloud_secretkey, create_message, digestmod=hashlib.sha256).digest())

        create_http_header = {
            'x-ncp-apigw-timestamp': self.timestamp,
            'x-ncp-iam-access-key': self.ncloud_accesskey,
            'x-ncp-apigw-signature-v2': create_signingKey
        }
        create_response = requests.get(self.api_server + create_api_url, headers=create_http_header)


    #########################################
    ##           SnapShot list             ##
    #########################################
    def snapshot_list(self, delete_day):
        method = "GET"

        list_api_url = "/vnas/v2/getNasVolumeSnapshotList"
        list_api_url = list_api_url +"?regionCode=" + self.regionCode + "&nasVolumeInstanceNo=" + self.nasvolume 

        list_message = method + self.space + list_api_url + self.new_line + self.timestamp + self.new_line + self.ncloud_accesskey
        list_message = bytes(list_message, 'UTF-8')

        list_ncloud_secretkey = bytes(self.ncloud_secretkey, 'UTF-8')
        list_signingKey = base64.b64encode(hmac.new(list_ncloud_secretkey, list_message, digestmod=hashlib.sha256).digest())

        list_http_header = {
            'x-ncp-apigw-timestamp': self.timestamp,
            'x-ncp-iam-access-key': self.ncloud_accesskey,
            'x-ncp-apigw-signature-v2': list_signingKey
        }
        list_response = requests.get(self.api_server + list_api_url, headers=list_http_header)

        #XML 파싱
        response_txt = re.sub("\<|\>|\/", "", list_response.text)
        response_txt = list(response_txt.split())

        rs_key = []
        key = 'nasVolumeSnapshotName'

        for word in response_txt:
            if key in word:
                rs_key.append(word)

        str_rs_key = ' '.join(s for s in rs_key) 

        returnMessage = str_rs_key.replace('nasVolumeSnapshotName', '')

        snapshot_name = returnMessage.split(' ')
        
        for i in snapshot_name :
            if delete_day in i  :
                Nas_Snapshot.snapshot_delete(self,i)
            else : 
                pass
    
    def snapshot_delete(self,snapshot_target):
        method = "GET"

        delete_api_url = "/vnas/v2/deleteNasVolumeSnapshot"
        delete_api_url = delete_api_url +"?regionCode=" + self.regionCode + "&nasVolumeInstanceNo=" + self.nasvolume + "&nasVolumeSnapshotName=" + snapshot_target

        delete_message = method + self.space + delete_api_url + self.new_line + self.timestamp + self.new_line + self.ncloud_accesskey
        delete_message = bytes(delete_message, 'UTF-8')

        delete_ncloud_secretkey = bytes(self.ncloud_secretkey, 'UTF-8')
        delete_signingKey = base64.b64encode(hmac.new(delete_ncloud_secretkey, delete_message, digestmod=hashlib.sha256).digest())

        delete_http_header = {
            'x-ncp-apigw-timestamp': self.timestamp,
            'x-ncp-iam-access-key': self.ncloud_accesskey,
            'x-ncp-apigw-signature-v2': delete_signingKey
        }
        delete_response = requests.get(self.api_server + delete_api_url, headers=delete_http_header)
    

#########################################
##             메인  함수               ##
#########################################
if __name__ == '__main__':
    dt = datetime.now()
    dt = dt - timedelta(days=56) ##날짜 계산 
    format = "%Y%m%d"
    delete_dt = datetime.strftime(dt,format)
    
    nas = Nas_Snapshot()
    nas.create_snapshot()
    nas.snapshot_list(delete_dt)