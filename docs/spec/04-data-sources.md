# 04 — Fontes de Dados

> Fonte primária: **[API de Dados do Portal da Transparência do Governo Federal](https://portaldatransparencia.gov.br/api-de-dados)**.
> Todos os dados são públicos e abertos (ver [Constituição P2](00-constitution.md)).

## Catálogo de conjuntos (Executivo Federal)

A API expõe, entre outros, os seguintes conjuntos relevantes para gastos:

| Conjunto | Conteúdo | Uso na Lupa Pública |
| --- | --- | --- |
| **Despesas públicas** | Empenho, liquidação, pagamento por órgão/ação | Núcleo do gasto; agregações por órgão/período |
| **Contratos do Executivo Federal** | Contratos firmados, valores, vigência, fornecedor | Relações órgão↔fornecedor↔contrato |
| **Licitações do Executivo Federal** | Modalidade, objeto, valor, resultado | Vínculo contrato↔licitação; dispensas |
| **Convênios** | Transferências a entes/entidades, valores | Fluxo de recursos para terceiros |
| **Emendas parlamentares** | Autor, valor, destino | Rastreio de emendas a destinos |
| **Cartões de pagamento (CPGF/CPCC)** | Gastos com cartão corporativo | Pontos de atenção (gastos pulverizados) |
| **Servidores do Executivo Federal** | Vínculos e remuneração (dados públicos) | Contexto; **uso restrito** conforme P2 |

> A lista completa e oficial está em
> <https://portaldatransparencia.gov.br/api-de-dados> e na
> [origem dos dados](https://portaldatransparencia.gov.br/origem-dos-dados).

## Esquema (campos típicos a normalizar)

Por se tratar de fontes heterogêneas, a normalização (RF1) deve padronizar ao menos:

| Campo canônico | Descrição | Exemplo de origem |
| --- | --- | --- |
| `orgao_codigo`, `orgao_nome` | Órgão/unidade gestora | despesas, contratos |
| `fornecedor_cnpj`, `fornecedor_nome` | Fornecedor/credor | contratos, despesas |
| `valor` | Valor em R$ (numérico) | todos |
| `data` / `competencia` | Data do evento ou competência | todos |
| `documento_id` | Identificador único do registro | todos |
| `tipo` | Tipo do gasto (empenho, contrato, etc.) | derivado |
| `fonte_url` | Link para o registro oficial | construído na ingestão |

O campo `fonte_url` é **obrigatório** para satisfazer [Constituição P1](00-constitution.md)
(citação de fonte).

## Estratégia de coleta

- **Autenticação**: a API requer **chave/token de API** (cadastro no Portal). A
  chave é armazenada no **Secret Manager** (RNF5).
- **Paginação**: a maioria dos endpoints é paginada — coletar página a página com
  backoff em caso de erro.
- **Rate limits**: respeitar limites da API; coleta em modo *batch* agendado
  (Cloud Scheduler + Cloud Run Jobs).
- **Versionamento**: gravar cada coleta sob prefixo datado no Cloud Storage
  (ex.: `raw/2026-06/...`) para reprodutibilidade ([Constituição P5](00-constitution.md)).
- **Ingestão incremental**: priorizar coleta do delta (novos/alterados) para
  reduzir custo (RNF2).

## Licença e uso

Os dados do Portal da Transparência são públicos e de uso livre, respeitada a
indicação da fonte. A Lupa Pública sempre **cita a origem** e não reusa dados
pessoais sensíveis além do que já é público.

## Expansão futura

- **LexML** (legislação/jurisprudência) para enriquecer o contexto normativo dos gastos.
- **Portais estaduais/municipais** de transparência (escopo do [roadmap](06-roadmap-tasks.md)).
