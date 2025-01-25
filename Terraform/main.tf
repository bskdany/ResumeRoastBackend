resource "azurerm_resource_group" "rg" {
  name     = "rg-byte-relay"
  location = var.resource_group_location
}