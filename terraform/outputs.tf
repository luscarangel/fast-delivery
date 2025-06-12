# ID da VPC principal usada na infraestrutura
output "vpc_id" {
  value = aws_vpc.main.id
}

# IDs das subnets públicas onde instâncias EC2 podem ser lançadas
output "public_subnets" {
  value = aws_subnet.public[*].id
}

# ID do Security Group usado pelo cluster ECS/EC2
output "security_group_id" {
  value = aws_security_group.ecs_sg.id
}

# Endpoint público do banco de dados PostgreSQL (RDS)
output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

# IPs públicos das instâncias EC2 gerenciadas pelo Auto Scaling Group do ECS
output "ec2_public_ips" {
  value       = data.aws_instances.ecs_nodes.public_ips
  description = "Endereços IP públicos das instâncias ECS"
}
