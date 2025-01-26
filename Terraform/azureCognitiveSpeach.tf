resource "azurerm_cognitive_account" "cognitive_account_resume_roast" {
  name                = "resume-roast-cognitive-account"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "SpeechServices"
  sku_name            = "S0"
}
