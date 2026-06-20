# 01 — Visão

## Problema

Os dados de gastos públicos do governo federal **já são abertos** e publicados no
[Portal da Transparência](https://portaldatransparencia.gov.br/). Na prática,
porém, eles permanecem **inacessíveis ao cidadão comum**: estão distribuídos em
dezenas de conjuntos de dados, planilhas volumosas e APIs que exigem conhecimento
técnico. Para responder a uma pergunta simples ("este contrato é caro?", "quem é
este fornecedor?") é preciso cruzar várias fontes manualmente.

O resultado é um **déficit de controle social**: a transparência existe no papel,
mas o esforço para exercê-la é alto demais para a maioria das pessoas.

## Proposta de valor

A Lupa Pública reduz esse esforço a uma **pergunta em linguagem natural**. Ela
recupera os registros relevantes, conecta entidades relacionadas (órgão,
fornecedor, contrato, licitação) através de um **knowledge graph** e responde de
forma compreensível, **sempre citando a fonte oficial**.

## Personas

| Persona | Necessidade | Exemplo de uso |
| --- | --- | --- |
| **Cidadão** | Entender para onde vai o dinheiro público sem jargão | "Quanto a prefeitura gastou com merenda escolar este ano?" |
| **Jornalista investigativo** | Achar pistas e cruzar dados rapidamente | "Quais fornecedores receberam contratos sem licitação acima de R$ 1 mi?" |
| **Servidor de órgão de controle** | Triagem de pontos de atenção para auditoria | "Liste contratos com aditivos que dobraram o valor original" |
| **Pesquisador / acadêmico** | Extrair séries e padrões para estudos | "Evolução do gasto com diárias por ministério de 2020 a 2025" |

## Casos de uso de alto nível

1. **Consulta direta**: somar/filtrar gastos por órgão, período, fornecedor ou valor.
2. **Exploração de relações**: a partir de um fornecedor, ver todos os órgãos,
   contratos e licitações conectados.
3. **Pontos de atenção**: sinalizar padrões atípicos (ex.: dispensa de licitação
   recorrente, valores fora da curva) — sempre como hipótese a investigar, nunca
   como acusação (ver [Constituição P4](00-constitution.md)).
4. **Exportação de evidências**: gerar um dossiê com as fontes citadas para
   auditoria ou reportagem.

## Prior art e diferencial

- **Portal da Transparência**: é a fonte de dados, mas exige navegação manual e
  não responde perguntas em linguagem natural.
- **Operação Serenata de Amor / Rosie** (Open Knowledge Brasil): provou o valor de
  IA sobre gastos públicos (análise de reembolsos da Cota Parlamentar), porém com
  regras/modelos específicos, sem interface conversacional aberta.

**Diferencial da Lupa Pública**: combinar (a) **busca conversacional** acessível a
leigos, (b) um **knowledge graph** que captura as relações entre entidades de
gasto, e (c) **fundamentação verificável** com citação de fonte em toda resposta.

## Não-objetivos (nesta concepção)

- Não substitui auditoria oficial nem emite parecer jurídico.
- Não afirma a ocorrência de irregularidade — apenas apresenta dados e pontos de atenção.
- Não cobre, inicialmente, dados estaduais/municipais (foco no Executivo Federal;
  expansão prevista no [roadmap](06-roadmap-tasks.md)).
