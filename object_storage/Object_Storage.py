import hashlib
import hmac
import datetime
import requests
import urllib

###################################################################
###                    인증 & 서명                               ###
###################################################################
def get_hash(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def create_signed_headers(headers):
    signed_headers = []

    for k in sorted(headers):
        signed_headers.append('%s;' % k)

    return ''.join(signed_headers)[:-1]


def create_standardized_headers(headers):
    signed_headers = []

    for k in sorted(headers):
        signed_headers.append('%s:%s\n' % (k, headers[k]))

    return ''.join(signed_headers)


def create_standardized_query_parameters(request_parameters):
    standardized_query_parameters = []

    if request_parameters:
        for k in sorted(request_parameters):
            standardized_query_parameters.append('%s=%s' % (k, urllib.quote(request_parameters[k], safe='')))

        return '&'.join(standardized_query_parameters)
    else:
        return ''


###################################################################
###                   Storage Class                             ###
###################################################################
class ObjectStorage:
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self):
        self.region = 'kr-standard'
        self.endpoint = 'https://kr.object.ncloudstorage.com'
        self.host = 'kr.object.ncloudstorage.com'
        self.access_key = ''
        self.secret_key = ''

        self.payload_hash = 'UNSIGNED-PAYLOAD'
        self.hashing_algorithm = 'AWS4-HMAC-SHA256'
        self.service_name = 's3'
        self.request_type = 'aws4_request'

        self.time_format = '%Y%m%dT%H%M%SZ'
        self.date_format = '%Y%m%d'

    #########################################
    ##            인증 & 서명               ##
    #########################################
    def _create_credential_scope(self, date_stamp):
        return date_stamp + '/' + self.region + '/' + self.service_name + '/' + self.request_type

    def _create_canonical_request(self, http_method, request_path, request_parameters, headers):
        standardized_query_parameters = create_standardized_query_parameters(request_parameters)
        standardized_headers = create_standardized_headers(headers)
        signed_headers = create_signed_headers(headers)

        canonical_request = (http_method + '\n' +
                             request_path + '\n' +
                             standardized_query_parameters + '\n' +
                             standardized_headers + '\n' +
                             signed_headers + '\n' +
                             self.payload_hash)

        print('canonical_request:\n%s\n' % canonical_request)
        return canonical_request

    def _create_string_to_sign(self, time_stamp, credential_scope, canonical_request):
        string_to_sign = (self.hashing_algorithm + '\n' +
                          time_stamp + '\n' +
                          credential_scope + '\n' +
                          hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())

        print('string_to_sign:\n%s\n' % string_to_sign)
        return string_to_sign

    def _create_signature_key(self, date_stamp):
        key_date = get_hash(('AWS4' + self.secret_key).encode('utf-8'), date_stamp)
        key_string = get_hash(key_date, self.region)
        key_service = get_hash(key_string, self.service_name)
        key_signing = get_hash(key_service, self.request_type)
        return key_signing

    def _create_authorization_header(self, headers, signature_key, string_to_sign, credential_scope):
        signed_headers = create_signed_headers(headers)
        signature = hmac.new(signature_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        return (self.hashing_algorithm + ' ' +
                'Credential=' + self.access_key + '/' + credential_scope + ', ' +
                'SignedHeaders=' + signed_headers + ', ' +
                'Signature=' + signature)

    def _sign(self, http_method, request_path, headers, time, request_parameters=None):
        time_stamp = time.strftime(self.time_format)
        date_stamp = time.strftime(self.date_format)

        credential_scope = self._create_credential_scope(date_stamp)
        canonical_request = self._create_canonical_request(http_method, request_path, request_parameters, headers)
        string_to_sign = self._create_string_to_sign(time_stamp, credential_scope, canonical_request)
        signature_key = self._create_signature_key(date_stamp)

        headers['authorization'] = self._create_authorization_header(headers, signature_key, string_to_sign, credential_scope)

    #########################################
    ##          Bucket List 조회            ##
    #########################################  
    def list_bucket(self, request_parameters=None) :
        http_method = 'GET'

        time = datetime.datetime.utcnow()
        time_stamp = time.strftime(self.time_format)

        headers = {'x-amz-date': time_stamp,
                   'x-amz-content-sha256': self.payload_hash,
                   'host': self.host}
        
        request_path = '/' 
        
        self._sign(http_method, request_path, headers, time, request_parameters)
        request_url = self.endpoint + request_path
        r = requests.get(request_url, headers=headers, params=request_parameters, stream=True)
        print('Response code: %d' % r.status_code)
        print(r.text)

    #########################################
    ##          Object List 조회            ##
    #########################################  
    def list_object(self, bucket_name, request_parameters=None) :
        http_method = 'GET'

        time = datetime.datetime.utcnow()
        time_stamp = time.strftime(self.time_format)

        headers = {'x-amz-date': time_stamp,
                   'x-amz-content-sha256': self.payload_hash,
                   'host': self.host}
        
        request_path = '/%s' % (bucket_name)
        
        self._sign(http_method, request_path, headers, time, request_parameters)
        request_url = self.endpoint + request_path
        r = requests.get(request_url, headers=headers, params=request_parameters, stream=True)
        print('Response code: %d' % r.status_code)
        print(r.text)

    #########################################
    ##             Object 삭제             ##
    #########################################  
    def delete_object(self, bucket_name, object, request_parameters=None) :
        http_method = 'DELETE'

        time = datetime.datetime.utcnow()
        time_stamp = time.strftime(self.time_format)

        headers = {'x-amz-date': time_stamp,
                   'x-amz-content-sha256': self.payload_hash,
                   'host': self.host}


        request_path = '/%s/%s' % (bucket_name, object)
        
        self._sign(http_method, request_path, headers, time, request_parameters)
        request_url = self.endpoint + request_path
        r = requests.delete(request_url, headers=headers, params=request_parameters, stream=True)
        print('Response code: %d' % r.status_code)
        print(r.text)


    #########################################
    ##              메인 함수               ##
    #########################################  
if __name__ == '__main__':
    storage = ObjectStorage()
    #storage.list_bucket()
    #storage.list_object('Bucket') #버킷명 
    storage.delete_object('gm-test', 'testdir/test/NCP.pdf') #버킷명 파일명 

