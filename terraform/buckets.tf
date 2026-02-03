provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "input_bucket" {
  bucket        = var.input_bucket_name
  force_destroy = true
}

resource "aws_s3_bucket" "output_bucket" {
  bucket        = var.output_bucket_name
  force_destroy = true
}