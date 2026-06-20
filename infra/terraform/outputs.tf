output "service_url" {
  description = "URL pública do serviço de consulta."
  value       = google_cloud_run_v2_service.api.uri
}

output "corpus_bucket" {
  description = "Bucket de corpus e índices file-based."
  value       = google_storage_bucket.corpus.name
}

output "image_repository" {
  description = "Artifact Registry de imagens."
  value       = google_artifact_registry_repository.images.name
}
