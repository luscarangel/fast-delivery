# Definição da task ECS (container da API)
resource "aws_ecs_task_definition" "api" {
  family                   = "fastdelivery-api"
  requires_compatibilities = ["EC2"]
  network_mode             = "bridge"
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "fastdelivery"
      image     = var.docker_image
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      environment = [
        {
          name  = "ENV"
          value = "production"
        },
        {
          name  = "DATABASE_URL"
          value = var.database_url
        }
      ]
    }
  ])
}

# Serviço ECS que mantém a task rodando
resource "aws_ecs_service" "api_service" {
  name            = "fastdelivery-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1
  launch_type     = "EC2"

  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
