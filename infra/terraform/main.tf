provider "azurerm" { 
  features {}
  subscription_id = var.subscription_id
}

# Abrufen der bestehenden Ressourcengruppe
data "azurerm_resource_group" "teamlink_rg" {
  name = var.resource_group_name
}

# Erstellen eines virtuellen Netzwerks und Subnetzes
resource "azurerm_virtual_network" "example" {
  name                = "example-network"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = data.azurerm_resource_group.teamlink_rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Netzwerkschnittstelle für Jenkins VM
resource "azurerm_network_interface" "jenkins" {
  name                = "jenkins-nic"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                    = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Netzwerkschnittstelle für Docker Swarm Node VM
resource "azurerm_network_interface" "docker_swarm_node" {
  name                = "docker-swarm-node-nic"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                    = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Netzwerkschnittstelle für Docker Swarm Worker VM
resource "azurerm_network_interface" "docker_swarm_worker" {
  name                = "docker-swarm-worker-nic"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                    = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Zufällige ID für Disknamen (damit jeder Diskname einzigartig ist)
resource "random_id" "jenkins_id" {
  byte_length = 8
}

resource "random_id" "docker_swarm_node_id" {
  byte_length = 8
}

resource "random_id" "docker_swarm_worker_id" {
  byte_length = 8
}

# Erstellen der Jenkins-VM
resource "azurerm_virtual_machine" "jenkins" {
  name                  = "Jenkins"
  resource_group_name   = data.azurerm_resource_group.teamlink_rg.name
  location              = data.azurerm_resource_group.teamlink_rg.location
  vm_size               = "Standard_B2ms"
  network_interface_ids = [azurerm_network_interface.jenkins.id]

  storage_os_disk {
    name              = "jenkins-os-disk-${random_id.jenkins_id.hex}"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  os_profile {
    computer_name  = "jenkins-vm"
    admin_username = var.admin_username  # Dies sollte in deiner `variables.tf` definiert sein
    admin_password = var.admin_password  # Dies sollte in deiner `variables.tf` definiert sein
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  tags = {
    environment = "teamlink"
  }
}

# Erstellen der Docker Swarm Node-VM
resource "azurerm_virtual_machine" "docker_swarm_node" {
  name                  = "DockerSwarmNode"
  resource_group_name   = data.azurerm_resource_group.teamlink_rg.name
  location              = data.azurerm_resource_group.teamlink_rg.location
  vm_size               = "Standard_B2ms"
  network_interface_ids = [azurerm_network_interface.docker_swarm_node.id]

  storage_os_disk {
    name              = "docker-swarm-node-os-disk-${random_id.docker_swarm_node_id.hex}"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  os_profile {
    computer_name  = "docker-swarm-node-vm"
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  tags = {
    environment = "teamlink"
  }
}

# Erstellen der Docker Swarm Worker-VM
resource "azurerm_virtual_machine" "docker_swarm_worker" {
  name                  = "DockerSwarmWorker"
  resource_group_name   = data.azurerm_resource_group.teamlink_rg.name
  location              = data.azurerm_resource_group.teamlink_rg.location
  vm_size               = "Standard_B2ms"
  network_interface_ids = [azurerm_network_interface.docker_swarm_worker.id]

  storage_os_disk {
    name              = "docker-swarm-worker-os-disk-${random_id.docker_swarm_worker_id.hex}"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  os_profile {
    computer_name  = "docker-swarm-worker-vm"
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  tags = {
    environment = "teamlink"
  }
}

output "jenkins_vm_id" {
  value = azurerm_virtual_machine.jenkins.id
}

output "docker_swarm_node_vm_id" {
  value = azurerm_virtual_machine.docker_swarm_node.id
}

output "docker_swarm_worker_vm_id" {
  value = azurerm_virtual_machine.docker_swarm_worker.id
}
