resource "azurerm_service_plan" "backendServicePlan" {
  name                = "backendServicePlan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "ResumeRoastApi" {
  depends_on          = [azurerm_resource_group.rg, azurerm_service_plan.backendServicePlan]
  name                = "ResumeRoastApi"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.backendServicePlan.id

  site_config {
    health_check_path                 = "/healthz"
    health_check_eviction_time_in_min = 2
    application_stack {
      python_version = "3.10"
    }
    cors {
      allowed_origins     = ["*"]
      support_credentials = false
    }
  }
  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT"                       = "8080"
    "FLASK_APP"                           = "app"
  }
}


# resource "azurerm_app_service_source_control" "SourceControlFlaskBackend" {
#   app_id   = azurerm_linux_web_app.ResumeRoastApi.id
#   repo_url = "https://github.com/bskdany/ResumeRoastBackend.git"
#   branch   = "main"
# }
