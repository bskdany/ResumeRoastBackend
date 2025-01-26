resource "azurerm_static_web_app" "example" {
  name                = "resume-roast-webapp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = "centralus"
  sku_tier            = "Free"
  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT"                       = "4200"
    "WEBSITES_NODE_DEFAULT_VERSION"       = "~20"
    "WEBSITES_WEBDEPLOY_USE_SCM"          = "false"
  }
}
