# Lupa Pública

> **Status:** 🟡 Fase de especificação (Spec-Driven Development). Nenhum código de
> aplicação foi implementado ainda — este repositório contém **a documentação base**
> que guiará a construção.

**Lupa Pública** é um sistema **RAG (Retrieval-Augmented Generation)** sobre
**gastos públicos** do governo brasileiro. O objetivo é permitir que qualquer
pessoa — cidadão, jornalista, servidor de órgão de controle ou pesquisador —
faça perguntas em **linguagem natural** ("Quanto o Ministério X gastou com o
fornecedor Y em 2025?") e receba respostas **fundamentadas e com citação da
fonte oficial**.

Os dados já são públicos, mas hoje estão presos em planilhas e portais de difícil
navegação. A Lupa Pública democratiza esse acesso, transformando dados abertos em
respostas compreensíveis — sempre rastreáveis até o registro oficial.

## Por que é útil para a sociedade

- **Controle social acessível**: traduz dados orçamentários complexos para
  qualquer cidadão.
- **Apoio ao jornalismo investigativo e aos órgãos de controle**.
- **Transparência com rastreabilidade**: toda resposta cita a fonte; o sistema
  apresenta fatos, não acusações.

## Stack planejada (ainda **não** implementada)

| Camada | Tecnologia |
| --- | --- |
| Linguagem | **Python** |
| Motor RAG | **LightRAG** (knowledge graph + retrieval dual-level) |
| Nuvem | **Google Cloud Platform** (foco em baixo custo / pay-per-use) |
| Armazenamento de corpus | Cloud Storage |
| Vetores + grafo | Cloud SQL (PostgreSQL + `pgvector`) |
| Serviço de consulta | Cloud Run (escala a zero) |
| Embeddings / LLM | Vertex AI ou API Claude |

> Serviços gerenciados caros (Spanner Graph, Vertex AI Vector Search) foram
> **deliberadamente evitados** — ver [ADRs em `03-architecture.md`](docs/spec/03-architecture.md).

## Como navegar a especificação

A documentação segue a convenção **Spec-Driven Development**
(constitution → vision → requirements → design → tasks). Leia nesta ordem:

| # | Documento | O que cobre |
| --- | --- | --- |
| 00 | [Constituição](docs/spec/00-constitution.md) | Princípios inegociáveis do projeto |
| 01 | [Visão](docs/spec/01-vision.md) | Problema, personas, valor social, prior art |
| 02 | [Requisitos](docs/spec/02-requirements.md) | Requisitos funcionais/não-funcionais e user stories (EARS) |
| 03 | [Arquitetura](docs/spec/03-architecture.md) | Design técnico GCP + LightRAG + Python, fluxos e ADRs |
| 04 | [Fontes de Dados](docs/spec/04-data-sources.md) | Catálogo de dados abertos, esquemas, ingestão |
| 05 | [Knowledge Graph](docs/spec/05-knowledge-graph.md) | Ontologia do domínio: entidades e relações |
| 06 | [Roadmap e Tarefas](docs/spec/06-roadmap-tasks.md) | Fases e backlog para implementação |
| 07 | [Glossário](docs/spec/07-glossary.md) | Termos de finanças públicas |

## Licença e dados

O projeto consome exclusivamente **dados públicos abertos** de fontes oficiais
(ver [Fontes de Dados](docs/spec/04-data-sources.md)). Nenhum dado pessoal
sensível além do que a legislação de transparência já torna público é coletado.
