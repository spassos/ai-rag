# Bucket único para corpus bruto e índices file-based do LightRAG (ADR-001).
resource "google_storage_bucket" "corpus" {
  name                        = "${local.name}-corpus"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Delete"
    }
  }

  labels = local.labels
}

# Repositório de imagens de contêiner.
resource "google_artifact_registry_repository" "images" {
  repository_id = local.name
  location      = var.region
  format        = "DOCKER"
  labels        = local.labels
}
