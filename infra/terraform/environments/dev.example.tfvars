# Exemplo de variáveis para o ambiente dev. Copie para dev.tfvars (não versionado)
# e ajuste. Segredos NÃO vão aqui — vão para o Secret Manager.
project_id  = "seu-projeto-gcp"
region      = "southamerica-east1"
environment = "dev"
image       = "southamerica-east1-docker.pkg.dev/seu-projeto-gcp/lupa-publica-dev/api:latest"
