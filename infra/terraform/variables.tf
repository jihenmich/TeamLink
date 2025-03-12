variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}


variable "resource_group_name" {
  description = "Name der bestehenden Ressourcengruppe"
  type        = string
}

variable "admin_username" {
  description = "Der Administrator-Benutzername"
  type        = string
}

variable "admin_password" {
  description = "Das Administrator-Passwort"
  type        = string
  sensitive   = true
}

variable "jenkins_public_ip_name" {
  description = "Der Name der bestehenden statischen Public IP für Jenkins"
  type        = string
}

variable "docker_swarm_node_public_ip_name" {
  description = "Der Name der bestehenden statischen Public IP für Docker Swarm Node"
  type        = string
}

variable "docker_swarm_worker_public_ip_name" {
  description = "Der Name der bestehenden statischen Public IP für Docker Swarm Worker"
  type        = string
}

