# Subnet Group + RDS PostgreSQL
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "fastdelivery-db-subnet-group"
  subnet_ids = aws_subnet.public[*].id
  tags = {
    Name = "rds-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier             = "fastdelivery-db"
  allocated_storage      = 20
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  username               = var.db_user
  password               = var.db_password
  publicly_accessible    = true
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id] # ← atualizado
  skip_final_snapshot    = true
  deletion_protection    = false
  apply_immediately      = true
  tags = {
    Name = "fastdelivery-postgres"
  }
}
