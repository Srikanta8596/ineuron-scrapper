import os
#SAVE PDF FILES DIRECTORY
PDF_DIRECTORY="/pdf_files"


#MONGODB
MONGO_DB_CONNECTION_STRING=os.environ('MONGO_DB_CONNECTION_STRING')
MONGO_DATA_BASE_NAME =os.environ('MONGO_DATA_BASE_NAME')
MONGO_COLLECTION_NAME= os.environ('MONGO_COLLECTION_NAME')

#SQL
SQL_HOST='localhost'
SQL_DATABASE_NAME='ineuron_courses'
SQL_TABLE_NAME= 'course_name_description'
SQL_USER_NAME='root'
SQL_PASSWORD='srikanta'
SQL_AUTH_PLUGIN='mysql_native_password'
AUTO_COMMIT=True

#AWS ACCESS KEY
AWS_ACCESS_KEY_ID = os.environ('AWS_ACCESS_KEY_ID ')
AWS_SECRET_ACCESS_KEY= os.environ('AWS_SECRET_ACCESS_KEY')

#S3 BUCKET NAME
S3_BUCKET_NAME =  os.environ('S3_BUCKET_NAME')
#SAVE PDF FILES DIRECTORY

PDF_DIRECTORY="/pdf_files"
