variable "AWS_ACCESS_KEY_ID" {
    type = string
}
variable "AWS_SECRET_ACCESS_KEY_ID" {
    type = string
}
variable "DB_USER" {
    type = string
    default = "postgres"
}
variable "DB_PASS" {
    type = string
}
variable "DB_HOST" {
    type = string
}
variable "DB_NAME" {
    type = string
}
variable "DB_PORT" {
    type = number
}
variable "SCHEMA_NAME" {
    type = string 
}

variable "STORAGE_IMAGE_LOCATION" {
    type = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c10-late-devonian-storage:latest"
}



