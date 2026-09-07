variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "evidence_bucket_name" {
  type        = string
  description = "Globally unique bucket name for compliance evidence."
}
