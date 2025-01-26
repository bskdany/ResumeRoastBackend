resource "azurerm_linux_web_app" "ResumeRoastWebAppService" {
  depends_on          = [azurerm_resource_group.rg, azurerm_service_plan.backendServicePlan]
  name                = "resume-roast-webapp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.backendServicePlan.id

  site_config {
    application_stack {
      node_version = "20-lts"
    }

  }
  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT"                       = "4200"
    "WEBSITES_NODE_DEFAULT_VERSION"       = "~20"
  }
}
resource "azurerm_app_service_source_control" "SourceControlByteRelayWebAppGithub" {
  app_id   = azurerm_linux_web_app.ResumeRoastWebAppService.id
  repo_url = "https://github.com/bskdany/ResumeRoast"
  branch   = "main"
}
