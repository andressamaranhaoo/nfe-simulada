output "ec2_public_ip" {
  value = aws_instance.api.public_ip
}

output "ssh_command" {
  value = "ssh -i <sua-chave.pem> ubuntu@${aws_instance.api.public_ip}"
}
