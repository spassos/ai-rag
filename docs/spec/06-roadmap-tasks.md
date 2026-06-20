# 06 — Roadmap e Tarefas

> Backlog acionável para a implementação futura. As tarefas referenciam os
> requisitos de [02-requirements.md](02-requirements.md). Marque `[x]` ao concluir.

## Fase 1 — PoC de ingestão + LightRAG local

Objetivo: provar o fluxo ponta a ponta localmente, com um subconjunto de dados.

- [ ] Definir escopo do subconjunto (ex.: contratos de 1 ministério, 1 ano).
- [ ] Implementar conector da API do Portal da Transparência (paginação, chave) — RF1.
- [ ] Normalizar registros para o esquema canônico de [04-data-sources.md](04-data-sources.md) — RF1.
- [ ] Rodar LightRAG localmente (storage de arquivo) e indexar o subconjunto — RF2.
- [ ] Validar consultas básicas em linguagem natural com citação de fonte — RF3, RF4.
- [ ] Definir camada de abstração de LLM/embeddings (Vertex AI ↔ Claude ↔ **fake offline**) — ADR-004.
- [ ] **Smoke test offline no sandbox** (`scripts/local_smoke.sh`) rodando o pipeline com provedor fake — [P9](00-constitution.md).

## Fase 2 — Knowledge graph + consulta com citações

Objetivo: qualidade de retrieval e fundamentação.

- [ ] Implementar criação **determinística** de arestas na ingestão — [05](05-knowledge-graph.md).
- [ ] Normalizar fornecedores por CNPJ; tratar entidades incompletas — [05](05-knowledge-graph.md).
- [ ] Confirmar backends **file-based** do LightRAG (NanoVectorDB + NetworkX + JSON) — ADR-001.
- [ ] Implementar filtros estruturados (órgão, período, fornecedor, valor) — RF5.
- [ ] Garantir formato de resposta com lista de fontes e fallback "não sei" — RF4, EARS-4.2.
- [ ] Esboçar detecção de **pontos de atenção** (sem juízo de valor) — RF6, P4.

## Fase 3 — Infra como código + CI/CD

Objetivo: automatizar build/deploy de forma reprodutível ([P8](00-constitution.md)).

- [ ] Escrever a infra GCP em **Terraform** (`infra/terraform/`) — [08](08-infra-cicd.md), ADR-005.
- [ ] Workflow **`ci.yml`**: lint + pytest + **smoke offline** + `terraform validate` — ADR-006, [P9](00-constitution.md).
- [ ] Workflow **`cd.yml`**: build + push + `terraform apply` + deploy Cloud Run (Workload Identity Federation) — ADR-006.
- [ ] `Dockerfile` do serviço de consulta e do job de ingestão.

## Fase 4 — Deploy em GCP (baixo custo)

> ⚠️ **Gate [P9](00-constitution.md)**: só executar esta fase **após** o smoke
> test local/offline passar no sandbox e no CI.

Objetivo: colocar em produção respeitando [Constituição P6](00-constitution.md).

- [ ] Corpus bruto/versionado no **Cloud Storage** — RNF7.
- [ ] Persistir backends **file-based** do LightRAG no **Cloud Storage** (gcsfuse) — ADR-001.
- [ ] Serviço de consulta em contêiner no **Cloud Run** (escala a zero) — ADR-003.
- [ ] Ingestão agendada via **Cloud Scheduler + Cloud Run Jobs** — RNF2.
- [ ] Segredos no **Secret Manager** — RNF5.
- [ ] Observabilidade/logs de auditoria de ingestão e respostas — RNF6.

## Fase 5 — UX, avaliação e expansão

Objetivo: usabilidade para leigos e qualidade mensurável.

- [ ] Interface de consulta acessível a leigos — RNF4.
- [ ] Exportação de evidências (markdown/PDF com fontes) — RF7.
- [ ] Suite de avaliação de qualidade (perguntas-padrão, taxa de fundamentação,
      detecção de alucinação) — P1.
- [ ] Medir latência (p95) e custo por consulta; otimizar — RNF1, RNF3.
- [ ] Expansão de fontes: LexML e portais estaduais/municipais — [04](04-data-sources.md).

## Marcos (milestones)

| Marco | Critério de "pronto" |
| --- | --- |
| M1 — PoC local | Pipeline ponta a ponta + **smoke test offline** verde no sandbox |
| M2 — Grafo+citações | Consultas de relação funcionam; respostas sempre fundamentadas |
| M3 — IaC + CI/CD | Terraform validado e Actions com smoke offline obrigatório |
| M4 — Produção GCP | Serviço público no Cloud Run com custo monitorado |
| M5 — Avaliado | Métricas de qualidade/latência/custo em painel |
