import time
import json
import base64
import jwt
from datetime import datetime, timedelta

###################################################################
###                   works_jwt Class                           ###
###################################################################
class works_jwt:
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self):
        self.client_id = ""
        self.client_secret = ""
        self.sevice_account = ""

        self.timestamp = int(time.time() * 1000)
        self.timestamp_exp = int((time.time() * 1000) + 360000 )
        self.header = {
            "alg": "RS256",
            "typ":"JWT"
        }

        self.payload = {
            "iss":self.client_id,
            "sub":self.sevice_account,
            "iat":self.timestamp,
            "exp":self.timestamp + 3600
            }
        self.key ="""-----BEGIN PRIVATE KEY----- 

-----END PRIVATE KEY-----"""

    #########################################
    ##             JWT Heade               ##
    #########################################
    def jwt_header(self):
        header_byte = json.dumps(self.header)
        header_byte = base64.b64encode(header_byte.encode('utf-8'))
        #print(header_byte)

        return header_byte

    #########################################
    ##             JWT Payload             ##
    #########################################
    def jwt_payload(self):
        payload_byte = json.dumps(self.payload)
        payload_byte = base64.b64encode(payload_byte.encode('utf-8'))
        
        return payload_byte
 
    #########################################
    ##             JWT Create              ##
    #########################################
    def jwt_works(self): 
        # jwt_header = bytes(works.jwt_header())
        # jwt_payload = bytes(works.jwt_payload())
        jwt_header = works_jwt.jwt_header(self)
        jwt_payload = works_jwt.jwt_payload(self)
        #print( jwt_header)
        #print(jwt_payload)
        #private_key = str(self.key)
        #print(self.key)

        signed_jwt = jwt.encode(payload=self.payload, key=self.key, headers=self.header,algorithm='RS256')

        #print(signed_jwt)
        #token = works.token(signed_jwt)
        return signed_jwt