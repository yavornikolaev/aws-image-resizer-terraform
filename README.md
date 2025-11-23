# Image-Resizer Project

This repository contains a serverless image-resizing pipeline using AWS S3 + AWS Lambda + Terraform.

## Architecture

1. Upload original images to the input S3 bucket.
2. S3 triggers a Lambda function which resizes the image.
3. The resized image is stored in the output S3 bucket.

## Setup

### Prerequisites
- AWS account with permission to create S3, Lambda, IAM roles.
- Terraform installed.
- AWS CLI configured.

### Steps
1. Go into `terraform/` folder.
2. Fill in `variables.tf` or provide a `terraform.tfvars` file with values.
3. Build the Lambda deployment package:
   ```bash
   cd lambda
   pip install --target ./package -r requirements.txt
   cd package && zip -r ../lambda_package.zip .
   cd .. && zip lambda_package.zip handler.py
   mv lambda_package.zip ../terraform/
