terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.14.0"
    }
    azuread = {
      source = "hashicorp/azuread"
    }
  }
}

provider "azurerm" {
  subscription_id = "61704dc3-d019-4cad-b064-21d8e83be1a0"
  features {}
}