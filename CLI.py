import os
import boto3

#set up aws client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

#list all files in an s3 bucket
def list_files(bucket_name, prefix=''):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print("No files found.")

#upload a local file to a defined location in the bucket 
def upload_local_file(file_path, bucket_name, destination_key):
    try:
        s3_client.upload_file(file_path, bucket_name, destination_key)
        print(f"File '{file_path}' uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")

#main 
if __name__ == '__main__':
    bucket_name = 'developer-task'
    prefix = 'x-wing'
    list_files(bucket_name, prefix)

    file_path = 'test.txt' #the file is in the same directory as the script
    destination_key = 'x-wing/file.txt'
    upload_local_file(file_path, bucket_name, destination_key)
