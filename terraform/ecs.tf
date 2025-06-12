# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "fastdelivery-cluster"
}

# IAM Role para EC2 (ECS Instance Role)
resource "aws_iam_role" "ecs_instance_role" {
  name = "ecsInstanceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_instance_attach" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecs-instance-profile"
  role = aws_iam_role.ecs_instance_role.name
}

# Launch Template com Amazon ECS-optimized AMI
data "aws_ssm_parameter" "ecs_ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
}

resource "aws_launch_template" "ecs_lt" {
  name_prefix   = "ecs-lt-"
  image_id      = data.aws_ssm_parameter.ecs_ami.value
  instance_type = "t2.micro"
  key_name      = var.ssh_key_name # precisa ser criada no console
  iam_instance_profile {
    name = aws_iam_instance_profile.ecs_instance_profile.name
  }

  user_data = base64encode(<<EOF
#!/bin/bash
echo ECS_CLUSTER=${aws_ecs_cluster.main.name} >> /etc/ecs/ecs.config
EOF
  )

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.ecs_sg.id]
  }
}

# Auto Scaling Group com 1 instância EC2
resource "aws_autoscaling_group" "ecs_asg" {
  name                = "ecs-asg"
  max_size            = 1
  min_size            = 1
  desired_capacity    = 1
  vpc_zone_identifier = aws_subnet.public[*].id
  launch_template {
    id      = aws_launch_template.ecs_lt.id
    version = "$Latest"
  }
  lifecycle {
    create_before_destroy = true
  }
  tag {
    key                 = "Name"
    value               = "fastdelivery-ecs-node"
    propagate_at_launch = true
  }
}

# Data source para obter instâncias EC2 criadas pelo ASG
data "aws_instances" "ecs_nodes" {
  filter {
    name   = "tag:Name"
    values = ["fastdelivery-ecs-node"]
  }

  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

