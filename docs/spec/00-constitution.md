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
**cobram por uso**; evite serviços gerenciados caros (ex.: Cloud SQL, Spanner
Graph, Vertex AI Vector Search) quando alternativas de baixo custo (ex.: backends
file-based do LightRAG no Cloud Storage; ou Postgres + pgvector em VM free-tier)
atendem ao requisito. A solução deve permanecer **portável** e barata de operar.

## P7 — Acessibilidade

A interface e as respostas devem ser compreensíveis para um cidadão **sem
formação técnica ou jurídica**. Jargão de finanças públicas deve ser explicado
(ver [Glossário](07-glossary.md)).

## P8 — Infraestrutura como Código

Toda a infraestrutura na GCP é provisionada via **Terraform**, versionada no
repositório. Nada de cliques manuais no console: a infra deve ser reprodutível,
revisável em pull request e destruível/recriável de forma determinística. O
deploy (build, push de imagem, apply) é automatizado por **CI/CD com GitHub
Actions** (ver [08-infra-cicd.md](08-infra-cicd.md)).

## P9 — Testar localmente antes de implantar

Nenhuma infraestrutura sobe para a GCP sem antes passar por um **teste local no
sandbox**. O pipeline (ingestão → indexação → consulta) deve rodar
**offline**, com um provedor *fake* de LLM/embeddings, validando o fluxo
ponta a ponta sem custo e sem credenciais. Só após o teste local verde é que se
aplica o Terraform e se faz o deploy na nuvem.
