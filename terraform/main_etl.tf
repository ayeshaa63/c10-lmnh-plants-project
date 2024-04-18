provider "aws" {
    region = "eu-west-2"
    access_key = var.AWS_ACCESS_KEY_ID
    secret_key = var.AWS_SECRET_ACCESS_KEY_ID
}

resource "aws_scheduler_schedule" "alpha_etl_schedule" {
    name = "alpha_etl_schedule"
    flexible_time_window {
    mode = "OFF"
    }
    schedule_expression = "cron(* * * * ? *)"
    target {
    arn      = aws_lambda_function.alpha-etl-lambda.arn
    role_arn = "role arn"
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
      identifiers = ["???"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lam.json
}

resource "aws_iam_role" "iam_for_eventbridge" {
  name               = "iam_for_eventbridge"
  assume_role_policy = data.aws_iam_policy_document.assume_role_event.json
}

resource "aws_ecr_repository" "alpha_etl_image" {
  name                 = "alpha_etl_image"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
resource "aws_lambda_function" "alpha-etl-lambda" {
  function_name = "alpha-etl-lambda"
  image_uri     = "${aws_ecr_repository.alpha_etl_image.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.lambda.arn
}