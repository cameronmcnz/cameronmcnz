# HTML to S3 Upload Script

This script uploads all HTML files from the current directory and subdirectories to an S3 bucket.

## Prerequisites

- Python 3.6 or higher
- boto3 library (`pip install boto3`)
- AWS credentials configured (via AWS CLI or environment variables)

## Usage

Set the `BUCKET` environment variable to your S3 bucket name and run the script:

```bash
export BUCKET=your-bucket-name
python3 upload_html_to_s3.py
```

Or in a single command:

```bash
BUCKET=your-bucket-name python3 upload_html_to_s3.py
```

## What it does

1. Scans the current directory and all subdirectories for `.html` files
2. Uploads each HTML file to the specified S3 bucket
3. Preserves the directory structure in S3 (relative paths become S3 keys)
4. Sets the correct `Content-Type: text/html` for all uploaded files
5. Provides progress feedback during upload
6. Reports a summary of successful and failed uploads

## AWS Credentials

The script uses boto3, which automatically looks for credentials in:
- Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- AWS credentials file (`~/.aws/credentials`)
- AWS config file (`~/.aws/config`)
- IAM role (if running on EC2)

Make sure your AWS credentials have permission to upload objects to the specified S3 bucket.

## Example Output

```
Scanning for HTML files...
Found 971 HTML files.
Uploading index.html to s3://my-bucket/index.html... ✓
Uploading about.html to s3://my-bucket/about.html... ✓
Uploading videos/youtube/example.html to s3://my-bucket/videos/youtube/example.html... ✓
...

Upload complete:
  Successfully uploaded: 971
  Failed: 0
```

## Error Handling

- If the `BUCKET` environment variable is not set, the script exits with an error
- If AWS credentials are not found, the script exits with an error
- Individual file upload failures are reported but don't stop the entire process
- The script exits with code 1 if any uploads fail, code 0 if all succeed
