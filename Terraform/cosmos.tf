resource "azurerm_cosmosdb_account" "cosmosDbAccountService" {

  name                = "resume-roast"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  capabilities {
    name = "EnableServerless"
  }
  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
  consistency_policy {
    consistency_level = "Session"
  }
  depends_on = [
    azurerm_resource_group.rg
  ]
}
resource "azurerm_cosmosdb_sql_database" "ResumeRoastDB" {
  name                = "ResumeRoastDb"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmosDbAccountService.name
}
resource "azurerm_cosmosdb_sql_container" "userSubmissionContainer" {
  name                  = "userSubmissionContainer"
  resource_group_name   = azurerm_resource_group.rg.name
  account_name          = azurerm_cosmosdb_account.cosmosDbAccountService.name
  database_name         = azurerm_cosmosdb_sql_database.ResumeRoastDB.name
  partition_key_paths   = ["/id"]
  partition_key_version = 1

  indexing_policy {
    indexing_mode = "consistent"
  }

  unique_key {
    paths = ["/idlong", "/idshort"]
  }
}

