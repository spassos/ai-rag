variable "project_id" {
  type        = string
  description = "ID do projeto GCP."
}

variable "region" {
  type        = string
  description = "Região GCP (ex.: southamerica-east1)."
  default     = "southamerica-east1"
}

variable "environment" {
  type        = string
  description = "Ambiente lógico (dev, prod)."
  default     = "dev"
}

variable "image" {
  type        = string
  description = "Imagem de contêiner do serviço/job (Artifact Registry)."
}

variable "ingest_schedule" {
  type        = string
  description = "Cron da ingestão periódica (Cloud Scheduler)."
  default     = "0 4 * * 1" # toda segunda às 04:00
}
