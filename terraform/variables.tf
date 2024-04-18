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
    type = string
}
variable "SCHEMA_NAME" {
    type = string 
}

variable "ecr_name" {
  description = "The list of ecr names to create"
  type        = list(string)
  default     = null
}
variable "tags" {
  description = "The key-value maps for tagging"
  type        = map(string)
  default     = {}
}
variable "image_mutability" {
  description = "Provide image mutability"
  type        = string
  default     = "MUTABLE"
}

variable "encrypt_type" {
  description = "Provide type of encryption here"
  type        = string
  default     = "KMS"
}

