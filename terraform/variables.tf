variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "db_user" {
  type        = string
  description = "Usuário do banco"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Senha do banco"
}

variable "ssh_key_name" {
  type        = string
  description = "Nome do par de chaves EC2 (deve ser criado no console AWS)"
}

variable "docker_image" {
  type        = string
  description = "Imagem Docker da API (ex: docker.io/user/fastdelivery:latest)"
}

variable "database_url" {
  type        = string
  description = "URL de conexão com o banco PostgreSQL"
  sensitive   = true
}
