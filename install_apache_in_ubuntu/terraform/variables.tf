variable "region"{
    type = string
    default = "us-east-1"
}

variable "instance_name"{
    type = string
    default = "Apache_Web_Server"
}

variable "ingress_rules" {
  type = list(number)
  default = [80,443,22]  # http; https; ssh
}

variable "egress_rules" {
  type = list(number)
  default = [ 80,443,22]
}

