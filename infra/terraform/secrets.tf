# Segredos gerenciados pelo Secret Manager. Os VALORES não são versionados:
# são definidos fora do Terraform (console/CLI/CI seguro).

resource "google_secret_manager_secret" "transparencia_api_key" {
  secret_id = "${local.name}-transparencia-api-key"

  replication {
    auto {}
  }

  labels = local.labels
}

resource "google_secret_manager_secret" "llm_api_key" {
  secret_id = "${local.name}-llm-api-key"

  replication {
    auto {}
  }

  labels = local.labels
}
