# Uma service account por componente (menor privilégio — RNF5).

resource "google_service_account" "api" {
  account_id   = "${local.name}-api"
  display_name = "Lupa Pública - serviço de consulta"
}

resource "google_service_account" "ingest" {
  account_id   = "${local.name}-ingest"
  display_name = "Lupa Pública - job de ingestão"
}

# Acesso ao bucket de corpus/índices.
resource "google_storage_bucket_iam_member" "api_corpus_read" {
  bucket = google_storage_bucket.corpus.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.api.email}"
}

resource "google_storage_bucket_iam_member" "ingest_corpus_write" {
  bucket = google_storage_bucket.corpus.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.ingest.email}"
}

# Leitura de segredos em runtime.
resource "google_secret_manager_secret_iam_member" "api_secret" {
  secret_id = google_secret_manager_secret.transparencia_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.ingest.email}"
}
