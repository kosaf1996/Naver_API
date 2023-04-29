import time
import requests

###################################################################
###                       Token 생성                            ###
###################################################################
class works_token :
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self):
        self.client_id= ""
        self.client_secret = ""
        self.sevice_account = ""
        self.scope = "calendar,calendar.read"
        self.timestamp = time.time() * 1000

    #########################################
    ##            Token Create             ##
    #########################################
    def works_token(self, jwt):
        header = {
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
        }
        # 고정값

        params = {
            "assertion" : jwt,
            "grant_type" : "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "scope" : self.scope
        }
        # signed_jwt 는 위 단계에서 만든 JWT

        url = "https://auth.worksmobile.com/oauth2/v2.0/token"

        r = requests.post(url, params=params, headers=header).json()
        return r["access_token"]