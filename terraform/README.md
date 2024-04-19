# Terraforming

## Setup
### Environment variables

The following `.tfvars` variables must be accessible to the script:
```sh
DB_HOST
DB_NAME
DB_USER
DB_PASS
DB_PORT
SCHEMA_NAME

BUCKET_NAME
STORAGE_IMAGE_LOCATION
REGION

AYESHA_EMAIL
DANA_EMAIL
HOWARD_EMAIL
NATHAN_EMAIL
```

### AWS roles and ECRs

*This terraform script does not create new IAM roles or ECR repositories, but instead references currently active ones. This is something that may be reworked in the future!*

## Usage

To start up the ETL and storage pipelines, run
```sh
terraform init
terraform plan
terraform apply
```

## Terraform files

### main_etl.tf

Sets up an AWS EventBridge schedule to run every 1 minute.
Also sets up an AWS lambda function, which, when triggered by the EventBridge schedule, runs the ETL pipeline from an image in an ECR repository.

### main_storage.tf

Sets up an AWS EventBridge schedule to run every 1 hour.
Also sets up an AWS lambda function, which, when triggered by the EventBridge schedule, runs the long-term-storage pipeline from an image in an ECR repository.

### provider.tf

Connects to AWS using access keys and a specified region.

### variables.tf

For gathering relevant variables to be used in main terraform files.

### output.tf

When `terraform apply` is run, the name of the S3 bucket will be printed in the terminal
