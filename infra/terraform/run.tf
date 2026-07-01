# Serviço de consulta (escala a zero — ADR-003) e job de ingestão (RNF2).

resource "google_cloud_run_v2_service" "api" {
  name     = "${local.name}-api"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.api.email

    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }

    containers {
      image = var.image

      env {
        name  = "LUPA_PROVIDER"
        value = "vertex"
      }
      env {
        name  = "LUPA_WORKING_DIR"
        value = "/data/rag"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
    }
  }

  labels = local.labels
}

resource "google_cloud_run_v2_job" "ingest" {
  name     = "${local.name}-ingest"
  location = var.region

  template {
    template {
      service_account = google_service_account.ingest.email

      containers {
        image   = var.image
        command = ["python", "-m", "lupa_publica.cli", "smoke"]
      }
    }
  }

  labels = local.labels
}
