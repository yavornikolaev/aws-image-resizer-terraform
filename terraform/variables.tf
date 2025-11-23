variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "input_bucket_name" {
  description = "Name of the S3 bucket for originals"
  type        = string
}

variable "output_bucket_name" {
  description = "Name of the S3 bucket for resized output"
  type        = string
}
