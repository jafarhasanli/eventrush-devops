
# Security Group for EventRush EC2

resource "aws_security_group" "eventrush" {
  name_prefix = "eventrush-dev-"
  description = "Security group for EventRush application"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "eventrush-dev-sg"
  }
}

# Allow outbound HTTP
resource "aws_vpc_security_group_egress_rule" "http" {
  security_group_id = aws_security_group.eventrush.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "tcp"
  from_port   = 80
  to_port     = 80

  description = "Allow outbound HTTP"
}

# Allow outbound HTTPS
resource "aws_vpc_security_group_egress_rule" "https" {
  security_group_id = aws_security_group.eventrush.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "tcp"
  from_port   = 443
  to_port     = 443

  description = "Allow outbound HTTPS"
}
