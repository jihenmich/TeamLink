provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# 📌 Abrufen der bestehenden Ressourcengruppe
data "azurerm_resource_group" "teamlink_rg" {
  name = var.resource_group_name
}

# 📌 Virtuelles Netzwerk
resource "azurerm_virtual_network" "teamlink_vnet" {
  name                = "teamlink-network"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
  address_space       = ["10.0.0.0/16"]
}

# 📌 Subnetz
resource "azurerm_subnet" "teamlink_subnet" {
  name                 = "teamlink-subnet"
  resource_group_name  = data.azurerm_resource_group.teamlink_rg.name
  virtual_network_name = azurerm_virtual_network.teamlink_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# 📌 Statische Public IPs für die VMs
resource "azurerm_public_ip" "jenkins_ip" {
  name                = "jenkins-public-ip"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip" "docker_swarm_node_ip" {
  name                = "docker-swarm-node-public-ip"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip" "docker_swarm_worker_ip" {
  name                = "docker-swarm-worker-public-ip"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# 📌 Netzwerksicherheitsgruppe (NSG) für alle VMs
resource "azurerm_network_security_group" "teamlink_nsg" {
  name                = "teamlink-nsg"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  security_rule {
    name                       = "AllowSSH"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowHTTP"
    priority                   = 1010
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowJenkins"
    priority                   = 1020
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8080"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowDockerSwarm"
    priority                   = 1030
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_ranges    = ["2377", "7946", "4789"]
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# 📌 Netzwerkschnittstellen für VMs
resource "azurerm_network_interface" "jenkins" {
  name                = "jenkins-nic"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  ip_configuration {
    name                          = "jenkins-ipconfig"
    subnet_id                     = azurerm_subnet.teamlink_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.jenkins_ip.id
  }
}

resource "azurerm_network_interface" "docker_swarm_node" {
  name                = "docker-swarm-node-nic"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  ip_configuration {
    name                          = "docker-swarm-node-ipconfig"
    subnet_id                     = azurerm_subnet.teamlink_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.docker_swarm_node_ip.id
  }
}

resource "azurerm_network_interface" "docker_swarm_worker" {
  name                = "docker-swarm-worker-nic"
  location            = data.azurerm_resource_group.teamlink_rg.location
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name

  ip_configuration {
    name                          = "docker-swarm-worker-ipconfig"
    subnet_id                     = azurerm_subnet.teamlink_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.docker_swarm_worker_ip.id
  }
}

# 📌 VMs erstellen
resource "azurerm_virtual_machine" "jenkins" {
  name                  = "Jenkins"
  resource_group_name   = data.azurerm_resource_group.teamlink_rg.name
  location              = data.azurerm_resource_group.teamlink_rg.location
  vm_size               = "Standard_B2ms"
  network_interface_ids = [azurerm_network_interface.jenkins.id]

  storage_os_disk {
    name              = "jenkins-os-disk"
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
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

resource "azurerm_virtual_machine" "docker_swarm_node" {
  name                  = "DockerSwarmNode"
  resource_group_name   = data.azurerm_resource_group.teamlink_rg.name
  location              = data.azurerm_resource_group.teamlink_rg.location
  vm_size               = "Standard_B2ms"
  network_interface_ids = [azurerm_network_interface.docker_swarm_node.id]

  storage_os_disk {
    name              = "docker-swarm-node-os-disk"
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
}

resource "azurerm_virtual_machine" "docker_swarm_worker" {
  name                  = "DockerSwarmWorker"
  resource_group_name   = data.azurerm_resource_group.teamlink_rg.name
  location              = data.azurerm_resource_group.teamlink_rg.location
  vm_size               = "Standard_B2ms"
  network_interface_ids = [azurerm_network_interface.docker_swarm_worker.id]

  storage_os_disk {
    name              = "docker-swarm-worker-os-disk"
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
}
