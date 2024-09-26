import os
import boto3
import re

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

#list an AWS buckets files that match a "filter" regex
def list_files_with_regex(bucket_name, prefix='', pattern=''):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    regex = re.compile(pattern)
    if 'Contents' in response:
        for obj in response['Contents']:
            if regex.match(obj['Key']):
                print(obj['Key'])
    else:
        print("No files found.")

#main 
if __name__ == '__main__':
    bucket_name = 'developer-task'
    prefix = 'x-wing'
    print("list all files in bucket:")
    list_files(bucket_name, prefix)

    file_path = 'test.txt' #the file is in the same directory as the script
    destination_key = 'x-wing/test.txt'
    print("\nupload a local file to bucket:")
    upload_local_file(file_path, bucket_name, destination_key)
    
    pattern = r'.*\.(...)$'
    print("\nfind file with regex pattern (this one looks for all files ending with three letters after a dot):")
    list_files_with_regex(bucket_name, prefix, pattern)
