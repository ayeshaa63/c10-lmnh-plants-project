
resource "aws_s3_bucket" "s3-test" {
  bucket = "late-devonian-tf-test-bucket"

  tags = {
    Name        = "late-devonian"
    Environment = "Dev"
  }
}

