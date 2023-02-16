from database.configuration import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import logging
class s3Operation:
    def __init__(self) -> None:
        self.AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY =AWS_SECRET_ACCESS_KEY
        self.S3_BUCKET_NAME= S3_BUCKET_NAME
    
    def insert(self,file_name,key):
        session = boto3.Session(
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                )
        s3 = session.resource('s3')
        # Filename - File to upload
        # Bucket - Bucket to upload to (the top level directory under AWS S3)
        # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
        try:
            response=s3.meta.client.upload_file(file_name, S3_BUCKET_NAME,key)
            return response
        except ClientError as e:
            logging.error(e)
            return False
        except FileNotFoundError:
            logging.info("The file was not found")
            return False
        except NoCredentialsError:
            logging.info("Credential is not available")
            return False

    def insert_s3(self,file,pdf_object):
        session = boto3.Session(
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                )
        s3 = session.resource('s3')
        #s3.Bucket(self.S3_BUCKET_NAME).put_object(Key=dir+'/'+file, Body=pdf.output(file, 'S').encode('latin-1'))
        dir='PDF-FILES'
        s3.Bucket(self.S3_BUCKET_NAME).put_object(Key=dir+'/'+file, Body=pdf_object)


    

        
        




