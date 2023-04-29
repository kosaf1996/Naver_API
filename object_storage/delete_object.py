import boto3

####################################################
####                 Global                      ###
####################################################

services_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = ''
secret_key = ''

####################################################
####              Storage Class                  ###
####################################################
class Storage():

    def __init__(self):
        s3 = boto3.client(services_name, 
                          endpoint_url=endpoint_url, 
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)

    def create_bucket(self, bname):
        bucket_name = bname 
        self.s3.create_bucket(Bucket=bucket_name)

        
    def get_bucket_list(self):
        response = self.s3.ListBuckets()
        for b in response.get('Buckets', []): print(b.get('Name'))



        
def main():
    storage = Storage()
    storage.get_bucket_list()
    #storage.create_bucket('test')
    # storage.obj_upload('office_test', 'sample_folder/')

####################################################
####                   Main                      ###
####################################################
if __name__ == "__main__":
    main()
