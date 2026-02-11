#!/usr/bin/env python3
"""
Script to upload all HTML files from the current directory and subdirectories to an S3 bucket.
The S3 bucket name is specified via the BUCKET environment variable.
AWS credentials should be configured via AWS CLI or environment variables.
"""

import os
import sys
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def find_html_files(root_dir='.'):
    """
    Recursively find all HTML files in the given directory and subdirectories.
    
    Args:
        root_dir: Root directory to search from (default: current directory)
        
    Returns:
        List of Path objects for all HTML files found
    """
    html_files = []
    root_path = Path(root_dir).resolve()
    
    for html_file in root_path.rglob('*.html'):
        if html_file.is_file():
            html_files.append(html_file)
    
    return html_files


def upload_file_to_s3(s3_client, file_path, bucket_name, s3_key):
    """
    Upload a single file to S3.
    
    Args:
        s3_client: Boto3 S3 client instance
        file_path: Path to the file to upload
        bucket_name: Name of the S3 bucket
        s3_key: Key (path) to use in S3
        
    Returns:
        True if upload was successful, False otherwise
    """
    try:
        # Set content type for HTML files
        s3_client.upload_file(
            str(file_path),
            bucket_name,
            s3_key,
            ExtraArgs={'ContentType': 'text/html'}
        )
        return True
    except NoCredentialsError:
        print("\nError: AWS credentials not found. Please configure AWS CLI or set credentials.", file=sys.stderr)
        sys.exit(1)
    except ClientError as e:
        print(f"Error uploading {file_path} to S3: {e}", file=sys.stderr)
        return False


def main():
    """
    Main function to find and upload all HTML files to S3.
    """
    # Get bucket name from environment variable
    bucket_name = os.environ.get('BUCKET')
    
    if not bucket_name:
        print("Error: BUCKET environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    
    # Find all HTML files
    print("Scanning for HTML files...")
    html_files = find_html_files()
    
    if not html_files:
        print("No HTML files found.")
        return
    
    print(f"Found {len(html_files)} HTML files.")
    
    # Initialize S3 client once for all uploads
    s3_client = boto3.client('s3')
    
    # Get the root directory for relative path calculation
    root_path = Path('.').resolve()
    
    # Upload each file
    success_count = 0
    failure_count = 0
    
    for html_file in html_files:
        # Calculate relative path from root directory
        relative_path = html_file.relative_to(root_path)
        s3_key = str(relative_path).replace('\\', '/')  # Ensure forward slashes for S3
        
        print(f"Uploading {relative_path} to s3://{bucket_name}/{s3_key}...", end=' ')
        
        if upload_file_to_s3(s3_client, html_file, bucket_name, s3_key):
            print("✓")
            success_count += 1
        else:
            print("✗")
            failure_count += 1
    
    # Print summary
    print(f"\nUpload complete:")
    print(f"  Successfully uploaded: {success_count}")
    print(f"  Failed: {failure_count}")
    
    if failure_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
