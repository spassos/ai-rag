# 00 — Constituição do Projeto

> A constituição define os **princípios inegociáveis** da Lupa Pública. Toda
> decisão de produto, arquitetura ou implementação futura deve estar em
> conformidade com estes princípios. Quando houver conflito entre conveniência
> técnica e um princípio, o princípio prevalece.

## P1 — Fundamentação obrigatória (anti-alucinação)

Nenhuma resposta pode ser gerada sem **citar a fonte**: o documento/registro de
origem e, sempre que possível, um link direto para o dado oficial. Se o sistema
não encontrar evidência suficiente no corpus, deve declarar que **não sabe** em
vez de inferir. A fundamentação é um requisito de primeira classe, não um
recurso opcional.

## P2 — Apenas dados públicos

O sistema consome **exclusivamente** fontes oficiais e abertas. Não se coletam,
armazenam ou inferem dados pessoais sensíveis além do que a legislação de
transparência (e a LGPD, no que se aplica a dados já públicos) torna público.

## P3 — Rastreabilidade e auditabilidade

Todo o pipeline — da ingestão de um dado bruto até a resposta final ao usuário —
deve ser auditável: é preciso conseguir reconstruir **de onde veio** cada
afirmação e **quando** o dado foi coletado.

## P4 — Neutralidade

A Lupa Pública apresenta **fatos e fontes**, não emite juízo de irregularidade.
Padrões atípicos são sinalizados como **"pontos de atenção"** para investigação
humana, nunca como acusação de ilícito. A interpretação cabe ao usuário.

## P5 — Reprodutibilidade e versionamento

O corpus é versionado. Uma mesma pergunta sobre uma mesma versão do corpus deve
produzir respostas consistentes. Mudanças nos dados de origem são registradas.

## P6 — Eficiência de custo

Custo é um requisito de primeira classe. Prefira serviços que **escalam a zero** e
**cobram por uso**; evite serviços gerenciados caros (ex.: Spanner Graph, Vertex
AI Vector Search) quando alternativas de baixo custo (ex.: PostgreSQL + pgvector)
atendem ao requisito. A solução deve permanecer **portável** e barata de operar.

## P7 — Acessibilidade

A interface e as respostas devem ser compreensíveis para um cidadão **sem
formação técnica ou jurídica**. Jargão de finanças públicas deve ser explicado
(ver [Glossário](07-glossary.md)).
