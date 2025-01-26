resource "azurerm_storage_account" "blobStorageAccount" {
  name                     = "blobaccount"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
resource "azurerm_storage_container" "blobStorageContainer" {
  name                  = "user-pdf-submission"
  storage_account_id    = azurerm_storage_account.blobStorageAccount.id
  container_access_type = "container"
}

