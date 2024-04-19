
resource "aws_s3_bucket" "s3-test" {
  bucket = var.BUCKET_NAME

  tags = {
    Name        = "late-devonian"
    Environment = "Dev"
  }
}

resource "aws_lambda_function" "alpha-storage-lambda" {
  function_name = "alpha-storage-lambda"
  image_uri     = var.STORAGE_IMAGE_LOCATION
  package_type  = "Image"
  role          = "arn:aws:iam::129033205317:role/service-role/c10-late-devonian-etl-lambda-role-ne686ivv"
  timeout = 60
  environment {
    variables = {
      DB_HOST=var.DB_HOST
      DB_NAME=var.DB_NAME
      SCHEMA_NAME=var.SCHEMA_NAME
      DB_USER=var.DB_USER
      DB_PASS=var.DB_PASS
      DB_PORT=var.DB_PORT
      BUCKET_STORAGE_NAME=var.BUCKET_NAME
      ACCESS_KEY_ID=var.ACCESS_KEY_ID
      SECRET_ACCESS_KEY=var.SECRET_ACCESS_KEY

    }
}
}

resource "aws_scheduler_schedule" "alpha_storage_schedule" {
    name = "alpha-storage-schedule"
    flexible_time_window {
    mode = "OFF"
    }
    schedule_expression = "cron(0 * * * ? *)"
    schedule_expression_timezone = "Europe/London"
    target {
    arn      = aws_lambda_function.alpha-storage-lambda.arn
    role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_1e67d5c529"
    }
}
