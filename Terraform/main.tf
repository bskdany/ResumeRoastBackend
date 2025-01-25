resource "azurerm_resource_group" "rg" {
  name     = "resume-roast-rg"
  location = var.resource_group_location
}