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

# 📌 Bestehende Public IPs aus Azure abrufen
data "azurerm_public_ip" "jenkins_ip" {
  name                = var.jenkins_public_ip_name
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
}

data "azurerm_public_ip" "docker_swarm_node_ip" {
  name                = var.docker_swarm_node_public_ip_name
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
}

data "azurerm_public_ip" "docker_swarm_worker_ip" {
  name                = var.docker_swarm_worker_public_ip_name
  resource_group_name = data.azurerm_resource_group.teamlink_rg.name
}

# 📌 Netzwerksicherheitsgruppe für Jenkins
resource "azurerm_network_security_group" "jenkins_nsg" {
  name                = "jenkins-nsg"
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
    name                       = "AllowJenkins"
    priority                   = 1010
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8080"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# 📌 Netzwerksicherheitsgruppe für Docker Swarm VMs
resource "azurerm_network_security_group" "docker_swarm_nsg" {
  name                = "docker-swarm-nsg"
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
    name                       = "AllowDockerSwarm"
    priority                   = 1020
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
    public_ip_address_id          = data.azurerm_public_ip.jenkins_ip.id
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
    public_ip_address_id          = data.azurerm_public_ip.docker_swarm_node_ip.id
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
    public_ip_address_id          = data.azurerm_public_ip.docker_swarm_worker_ip.id
  }
}

# 📌 NSG mit den Netzwerkschnittstellen verknüpfen
resource "azurerm_network_interface_security_group_association" "jenkins_nsg_assoc" {
  network_interface_id      = azurerm_network_interface.jenkins.id
  network_security_group_id = azurerm_network_security_group.jenkins_nsg.id
}

resource "azurerm_network_interface_security_group_association" "docker_swarm_node_nsg_assoc" {
  network_interface_id      = azurerm_network_interface.docker_swarm_node.id
  network_security_group_id = azurerm_network_security_group.docker_swarm_nsg.id
}

resource "azurerm_network_interface_security_group_association" "docker_swarm_worker_nsg_assoc" {
  network_interface_id      = azurerm_network_interface.docker_swarm_worker.id
  network_security_group_id = azurerm_network_security_group.docker_swarm_nsg.id
}

# 📌 Outputs für Public IPs
output "jenkins_public_ip" {
  value = data.azurerm_public_ip.jenkins_ip.ip_address
}

output "docker_swarm_node_public_ip" {
  value = data.azurerm_public_ip.docker_swarm_node_ip.ip_address
}

output "docker_swarm_worker_public_ip" {
  value = data.azurerm_public_ip.docker_swarm_worker_ip.ip_address
}
