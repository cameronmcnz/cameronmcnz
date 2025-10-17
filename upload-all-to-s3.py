import os
import sys
import boto3
from mimetypes import guess_type
from botocore.exceptions import ClientError

# ----------- Configuration -------------
BUCKET_NAME = 'windsafe.org'
S3_PREFIX = ''  # e.g., 'dev-site/' if you want a subfolder; leave '' for root
REGION = 'us-east-1'  # bucket region

# Use the current working directory
LOCAL_DIRECTORY = os.getcwd()

# ----------- S3 Client -----------------
s3_client = boto3.client('s3', region_name=REGION)

# ----------- Upload Logic --------------
NO_CACHE_VALUE = 'no-cache, no-store, must-revalidate'

def upload_file(file_path: str, s3_key: str) -> None:
    content_type, _ = guess_type(file_path)
    extra_args = {
        'CacheControl': NO_CACHE_VALUE
    }
    if content_type:
        extra_args['ContentType'] = content_type

    try:
        s3_client.upload_file(file_path, BUCKET_NAME, s3_key, ExtraArgs=extra_args)
        print(f'Uploaded: {file_path} --> s3://{BUCKET_NAME}/{s3_key}')
        print(f'  Headers: {extra_args}')
    except ClientError as e:
        print(f'ERROR uploading {file_path} -> {s3_key}: {e}', file=sys.stderr)

def upload_directory(local_dir: str, s3_prefix: str = '') -> None:
    for root, _, files in os.walk(local_dir):
        for file in files:
            full_path = os.path.join(root, file)
            # Path relative to the base directory
            relative_path = os.path.relpath(full_path, local_dir)
            # Normalize to S3-style forward slashes
            s3_key = os.path.join(s3_prefix, relative_path).replace('\\', '/')
            upload_file(full_path, s3_key)

# ---------- Run Upload -----------------
if __name__ == '__main__':
    print(f"Uploading files from {LOCAL_DIRECTORY} to s3://{BUCKET_NAME}/{S3_PREFIX}")
    upload_directory(LOCAL_DIRECTORY, S3_PREFIX)
    print("✅ Upload complete.")
