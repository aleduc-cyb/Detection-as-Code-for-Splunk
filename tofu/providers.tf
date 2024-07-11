terraform {
  required_providers {
    splunk = {
      source  = "splunk/splunk"
      version = "~> 1.4.0"
    }
  }
}

provider "splunk" {
  url                  = var.splunk_url
  username             = var.splunk_username
  password             = var.splunk_password
  insecure_skip_verify = true
}