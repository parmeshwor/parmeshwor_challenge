
resource "aws_instance" "ec2" {

    ami = "ami-07d9b9ddc6cd8dd30" # ubuntu
    instance_type = "t2.small"
    user_data = file("user-data.sh")

    key_name = aws_key_pair.ssh_key.id
    vpc_security_group_ids = [aws_security_group.sg_web_server.id]


    tags = {
      Name = var.instance_name
    }

}

resource "aws_key_pair" "ssh_key" {

    key_name = "pthapa-ec2-key-second"
    public_key = file("~/.ssh/d/pthapa_aws_ec2_second.pub")
  
}

resource "aws_security_group" "sg_web_server" {

    name = "http-ssh-access"
    description = "allow http from internet"

    dynamic "ingress" {
        iterator = port
        for_each = var.ingress_rules

        content {
          description = "http"
          from_port = port.value
          to_port = port.value
          protocol = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
          self = false
          ipv6_cidr_blocks = []
          prefix_list_ids = []
          security_groups = []
        }
    }


    dynamic "egress" {
        iterator = port
        for_each = var.egress_rules

        content {
          description = "http"
          from_port = port.value
          to_port = port.value
          protocol = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
          self = false
          ipv6_cidr_blocks = []
          prefix_list_ids = []
          security_groups = []
        }
    }

    tags = {
      Name = "sg-for-web-server"
    }
}



