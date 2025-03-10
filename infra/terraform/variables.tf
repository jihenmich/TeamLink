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
