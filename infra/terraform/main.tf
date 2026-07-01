# Infraestrutura da Lupa Pública na GCP (ADR-005).
# State remoto em bucket GCS (criar o bucket manualmente uma única vez, ou via
# bootstrap separado). Nada além disto é criado fora do Terraform (P8).

terraform {
  required_version = ">= 1.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    # bucket e prefix informados via -backend-config no CI/CD.
    # bucket = "lupa-publica-tfstate"
    # prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name = "lupa-publica-${var.environment}"
  labels = {
    app         = "lupa-publica"
    environment = var.environment
    managed_by  = "terraform"
  }
}
