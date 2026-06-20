# 02 — Requisitos

> Notação: **RF** = Requisito Funcional, **RNF** = Requisito Não-Funcional.
> Critérios de aceitação seguem a notação **EARS** (Easy Approach to Requirements
> Syntax): *"Quando &lt;gatilho&gt;, o sistema deve &lt;resposta&gt;."*

## Requisitos Funcionais

### RF1 — Ingestão de dados abertos
O sistema deve coletar dados da API do Portal da Transparência (despesas,
contratos, licitações, convênios, emendas, cartões de pagamento) e armazená-los
como corpus bruto versionado. Detalhes em [04-data-sources.md](04-data-sources.md).

### RF2 — Indexação no knowledge graph
O sistema deve extrair entidades e relações dos dados ingeridos e populá-las no
grafo de conhecimento + índice vetorial do LightRAG. Ontologia em
[05-knowledge-graph.md](05-knowledge-graph.md).

### RF3 — Consulta em linguagem natural
O sistema deve aceitar perguntas em português e recuperar os registros relevantes
usando o retrieval dual-level (local + global) do LightRAG.

### RF4 — Resposta com citações
Toda resposta deve incluir as **fontes** que a fundamentam (registro de origem +
link oficial quando disponível). Sem fonte suficiente, o sistema declara que não sabe.

### RF5 — Filtros estruturados
O sistema deve permitir refinar consultas por **órgão**, **período**, **fornecedor
(CNPJ/nome)**, **faixa de valor** e **tipo de gasto**.

### RF6 — Pontos de atenção
O sistema deve poder sinalizar padrões atípicos como hipóteses a investigar,
**sem** afirmar irregularidade (ver [Constituição P4](00-constitution.md)).

### RF7 — Exportação de evidências
O sistema deve permitir exportar a resposta com a lista de fontes citadas (ex.:
markdown/PDF) para uso em auditoria ou reportagem.

## Requisitos Não-Funcionais

### RNF1 — Custo
A operação deve priorizar serviços que escalam a zero e cobram por uso. O custo de
indexação e consulta deve ser mensurado e mantido baixo (ver [Constituição P6](00-constitution.md)).

### RNF2 — Atualização do corpus
O corpus deve poder ser atualizado periodicamente (ex.: ingestão incremental
mensal) sem reindexação total quando evitável.

### RNF3 — Latência
Consultas interativas devem responder em tempo aceitável para uso conversacional
(meta inicial: p95 < 10s; refinar após PoC).

### RNF4 — Acessibilidade
Respostas devem ser compreensíveis para leigos; termos técnicos remetem ao
[Glossário](07-glossary.md).

### RNF5 — Segurança e privacidade
Apenas dados públicos; sem coleta de dados pessoais sensíveis. Chaves de API e
credenciais GCP geridas via secret manager.

### RNF6 — Observabilidade e auditabilidade
Ingestão, indexação e respostas devem ser logadas de forma a permitir reconstruir
a origem de cada afirmação (ver [Constituição P3](00-constitution.md)).

### RNF7 — Reprodutibilidade
A mesma pergunta sobre a mesma versão do corpus deve gerar resultados consistentes.

## User Stories e critérios de aceitação (EARS)

### US1 — Consulta de gasto por fornecedor
> Como **jornalista**, quero saber quanto um órgão pagou a um fornecedor em um
> período, para investigar concentração de contratos.

- **EARS-1.1**: *Quando* o usuário pergunta o total pago por um órgão a um
  fornecedor em um período, *o sistema deve* responder com o valor agregado e
  **citar** os registros (contratos/despesas) que o compõem.
- **EARS-1.2**: *Quando* não houver registros para o filtro informado, *o sistema
  deve* declarar que não encontrou dados, sem inventar valores.

### US2 — Exploração de relações no grafo
> Como **servidor de controle**, quero ver todas as entidades conectadas a um
> fornecedor, para triagem.

- **EARS-2.1**: *Quando* o usuário pede as conexões de um fornecedor, *o sistema
  deve* listar órgãos, contratos e licitações relacionados, com fonte de cada um.

### US3 — Ponto de atenção
> Como **cidadão**, quero saber se um contrato tem algo atípico.

- **EARS-3.1**: *Quando* o usuário pergunta sobre um contrato, *o sistema deve*
  apresentar os dados e, **se** houver padrão atípico, sinalizá-lo como "ponto de
  atenção a investigar", *sem* afirmar irregularidade.

### US4 — Resposta sempre fundamentada
> Como qualquer usuário, quero confiar na resposta.

- **EARS-4.1**: *Enquanto* houver geração de resposta, *o sistema deve* anexar a
  lista de fontes usadas.
- **EARS-4.2**: *Se* a confiança/evidência for insuficiente, *o sistema deve*
  responder explicitamente "não há dados suficientes" em vez de especular.

## Rastreabilidade Constituição → Requisitos

| Princípio | Requisitos relacionados |
| --- | --- |
| P1 Fundamentação | RF4, RNF6, EARS-4.1, EARS-4.2 |
| P2 Dados públicos | RF1, RNF5 |
| P3 Rastreabilidade | RNF6, RF7 |
| P4 Neutralidade | RF6, EARS-3.1 |
| P5 Reprodutibilidade | RNF7, RNF2 |
| P6 Custo | RNF1 |
| P7 Acessibilidade | RNF4 |
