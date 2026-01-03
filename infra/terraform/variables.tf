variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo da instância"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Nome do Key Pair existente na AWS (EC2 > Key pairs)"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR permitido para SSH. Use seu IP/32 para mais segurança."
  type        = string
  default     = "0.0.0.0/0"
}
