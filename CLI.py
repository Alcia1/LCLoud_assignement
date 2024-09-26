import os
import boto3
import re

#set up aws client using environment variables
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

#list all files in an s3 bucket
def list_files(bucket_name, prefix=''):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        #return an array of obj keys, used later in list_files_regex
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append(obj['Key'])
        else:
            print("No files found.")

        return files
    except Exception as e:
        print(f"Error listing files: {e}")

#upload a local file to a defined location in the bucket 
def upload_local_file(file_path, bucket_name, destination_key):
    try:
        s3_client.upload_file(file_path, bucket_name, destination_key)
        print(f"File '{file_path}' uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")

#list an AWS buckets files that match a "filter" regex
def list_files_regex(bucket_name, prefix='', pattern=''):
    files = list_files(bucket_name, prefix)
    regex = re.compile(pattern)

    #print all mtching keys
    if files:
        for obj in files:
            if regex.match(obj):
                print(obj)
    else:
        print("No files found.")

#delete all files matching a regex from a bucket
def delete_files_regex(bucket_name, prefix='', pattern=''):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    regex = re.compile(pattern)

    if 'Contents' in response:
        #add all keys objects matching regex to dict
        delete = {
            'Objects': [
                {'Key': obj['Key']}
                for obj in response['Contents'] if regex.match(obj['Key'])
            ]
        }
        if delete['Objects']:
            try:
                s3_client.delete_objects(Bucket=bucket_name, Delete=delete)
                print(f"Deleted files: {[obj['Key'] for obj in delete['Objects']]}")
            except Exception as e:
                print(f"Error deleting file: {e}")
        else:
            print("No files match the pattern.")
    else:
        print("No files found.")


#main 
if __name__ == '__main__':
    bucket_name = 'developer-task'
    prefix = 'x-wing'
    print("list all files in bucket:")
    for file in list_files(bucket_name, prefix):
        print(file)

    file_path = 'test.txt' #the file is in the same directory as the script
    destination_key = 'x-wing/test.txt'
    print("\nupload a local file to bucket:")
    upload_local_file(file_path, bucket_name, destination_key)
    
    pattern = r'.*\.(...)$'
    print("\nfind file matching a regex pattern (this one looks for all files ending with three letters after a dot):")
    list_files_regex(bucket_name, prefix, pattern)

    pattern = r'.*\.txt$'
    print("\ndelete files matching a regex pattern (this one deletes all .txt files):")
    delete_files_regex(bucket_name, prefix, pattern)
