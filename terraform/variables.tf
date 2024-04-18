variable "ACCESS_KEY_ID" {
    type = string
}

variable "SECRET_ACCESS_KEY" {
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
    type = string
}

variable "BUCKET_NAME" {
    type = string
}

variable "AYESHA_EMAIL" {
    type = string 
}
variable "DANA_EMAIL" {
    type = string 
}
variable "HOWARD_EMAIL" {
    type = string 
}
variable "NATHAN_EMAIL" {
    type = string 
}
variable "REGION" {
    type = string 
}


