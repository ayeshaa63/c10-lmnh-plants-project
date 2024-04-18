resource "aws_lambda_function" "alpha-etl-lambda" {
  function_name = "alpha-etl-lambda"
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c10-late-devonian-etl:latest"
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
      AYESHA_EMAIL=var.AYESHA_EMAIL
      DANA_EMAIL=var.DANA_EMAIL
      HOWARD_EMAIL=var.HOWARD_EMAIL
      NATHAN_EMAIL=var.NATHAN_EMAIL
      REGION=var.REGION
    }
}
}

resource "aws_scheduler_schedule" "alpha_etl_schedule" {
    name = "alpha-etl-schedule"
    flexible_time_window {
    mode = "OFF"
    }
    schedule_expression = "cron(*/1 * * * ? *)"
    schedule_expression_timezone = "Europe/London"
    target {
    arn      = aws_lambda_function.alpha-etl-lambda.arn
    role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_1e67d5c529"
    }
}