# Dispara o job de ingestão periodicamente (RNF2).
resource "google_cloud_scheduler_job" "ingest" {
  name      = "${local.name}-ingest-trigger"
  region    = var.region
  schedule  = var.ingest_schedule
  time_zone = "America/Sao_Paulo"

  http_target {
    http_method = "POST"
    uri = format(
      "https://%s-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/%s/jobs/%s:run",
      var.region, var.project_id, google_cloud_run_v2_job.ingest.name
    )

    oauth_token {
      service_account_email = google_service_account.ingest.email
    }
  }
}
