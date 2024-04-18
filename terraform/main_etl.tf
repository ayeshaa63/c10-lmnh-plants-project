
resource "aws_scheduler_schedule" "alpha_etl_schedule" {
    name = "alpha-etl-schedule"
    flexible_time_window {
    mode = "OFF"
    }
    schedule_expression = "cron(* * * * ? *)"
    target {
    arn      = aws_lambda_function.alpha-etl-lambda.arn
    role_arn = aws_iam_role.iam_for_eventbridge.arn
    }
}

data "aws_iam_policy_document" "assume_role_lam" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}
data "aws_iam_policy_document" "assume_role_event" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam-for-lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lam.json
}

resource "aws_iam_role" "iam_for_eventbridge" {
  name               = "iam-for-eventbridge"
  assume_role_policy = data.aws_iam_policy_document.assume_role_event.json
}

resource "aws_lambda_function" "alpha-etl-lambda" {
  function_name = "alpha-etl-lambda"
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c10-late-devonian-storage:latest"
  package_type  = "Image"
  role          = aws_iam_role.iam_for_lambda.arn
  environment {
    variables = {
      DB_HOST=var.DB_HOST
      DB_NAME=var.DB_NAME
      SCHEMA_NAME=var.SCHEMA_NAME
      DB_USER=var.DB_USER
      DB_PASS=var.DB_PASS
      DB_PORT=var.DB_PORT
    }
}
}