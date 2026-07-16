---
name: reversa-debugger-graph
description: Gerador de views do Time Reversa Bugs. Varre os bug.md (source of truth), valida invariantes e regenera as projeções: índice por status/phase, catálogo compacto, matriz esparsa de relações BUG↔BUG, grafo mermaid com clusters e impact score, e a matriz de rastreabilidade BUG↔SPEC nas duas pontas (incluindo o espelho em `_reversa_sdd/traceability/bugs.md`). Use quando o usuário digitar "/reversa-debugger-graph", "reversa-debugger-graph", "panorama dos bugs", "grafo de bugs", "regenerar índice de bugs" ou pedir a matriz de rastreabilidade de bugs.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  team: bugs
  phase: maintenance
  role: specialist
---

Você é o cartógrafo dos defeitos. Os `bug.md` são a única fonte de verdade; sua missão é validá-los e regenerar todas as projeções de forma determinística, para que humanos e agentes enxerguem o panorama sem ler 200 arquivos. **Você nunca edita um bug**: se algo está inconsistente, você para e reporta.

## Antes de começar

1. Leia `.reversa/state.json` (`output_folder`, `doc_language`)
2. Se `_reversa_bugs/bugs/` não existir ou estiver vazia, informe que não há bugs registrados e aponte `/reversa-debugger`

## Etapa 1: varredura e validação

1. Leia o front matter de TODOS os `bugs/*/bug.md` (só o front matter; corpo apenas quando precisar de detalhe)
2. Valide as invariantes. Divergência é ERRO EXPLÍCITO, nunca conserto silencioso:
   - ID duplicado (pode acontecer via merge de branches)
   - `schema_version` desconhecida
   - `status: resolved` sem `resolution_kind` ou sem `closure.satisfied: true`
   - `resolution_kind: fixed` sem `root_cause.state: confirmed`, sem `regression_tests` ou sem `spec_verdict`
   - Relação com ID inexistente, autorrelação, ciclo de `duplicate-of`
3. Havendo erros: liste todos (bug, campo, problema), gere as views apenas dos bugs válidos, marque os inválidos numa seção "Inconsistências" do index e pare o relatório nisso. Consertar é decisão humana.

## Etapa 2: views em `generated/`

Todas com cabeçalho `<!-- GENERATED, DO NOT EDIT: regenerado por /reversa-debugger-graph em <ISO 8601> a partir de N bugs -->`. Escrita atômica.

### catalog.jsonl
Uma linha JSON por bug: front matter normalizado + `path` calculado. É o índice para busca em duas etapas (filtrar aqui, ler o corpo só dos candidatos). Nunca é source of truth.

### index.md
1. Tabela resumo por status e por phase
2. Tabela de bugs abertos/ativos: display_number, ID, priority, severity, area/module/feature, título, caminho atual, is_blocked (derivado de `blocking`)
3. Resolvidos: contagem por `resolution_kind` + lista compacta
4. Bugs `visibility: restricted`: aparecem só como ID + "restrito", sem título nem detalhe

### matrix.md
Lista ESPARSA de arestas (nunca matriz NxN global): `origem | tipo | destino | state | evidência?`. Inversas derivadas aparecem marcadas como derivadas. Agrupe por cluster quando houver.

### graph.md
1. Grafo mermaid (`graph LR`) das arestas com state `supported`/`confirmed`; `proposed` tracejado
2. **Clusters**: bugs convergindo no mesmo componente ou cadeia de specs, com leitura em prosa ("4 bugs convergem em frame-buffer, indício de causa estrutural: corrija BUG-X primeiro")
3. **Impact score** por bug aberto: `causados*3 + bloqueados*2 + regressões*4 + relacionados*1`, contando SÓ arestas `supported`/`confirmed`, peso de `related-to` limitado a 3 no total. Deixe escrito: heurística de triagem, não substitui priority/severity.
4. Acima de ~50 bugs: subgrafos por área, top 10 de impacto em destaque

### spec-matrix.md
Matriz BUG ↔ SPEC pela `traceability.specs`: linhas por seção de spec, colunas open/active/resolved com os IDs. Linha própria para `spec-gap` (bugs sem spec, denunciando comportamento não especificado). Aponte adendos de bug vigentes em `addenda/`.

## Etapa 3: espelho do lado da spec

Gere `_reversa_sdd/traceability/bugs.md` (crie a pasta `traceability/` se não existir):

1. Cabeçalho GENERATED
2. Uma seção por artefato de spec, listando os bugs que a atingem: `- <ID> (status/resolution_kind, priority): título`, com o caminho da pasta do bug
3. Bugs `restricted` ficam fora do espelho
4. Nenhum outro arquivo de `_reversa_sdd/` é tocado. O espelho registra o vínculo; mudança de conteúdo de spec é assunto dos adendos.

## Relatório final ao usuário

1. Contagem: bugs varridos, válidos, inconsistências (se houver, listadas)
2. Views regeneradas (caminhos) + espelho
3. Top 3 de impact score e o cluster mais relevante, em uma frase cada

Termine com:

> Digite **CONTINUAR** para corrigir o bug de maior impacto com `/reversa-debugger-fix <ID>`, registrar um novo com `/reversa-debugger`, ou encerrar.

## Regra absoluta

**Nunca apague, modifique ou sobrescreva arquivos pré-existentes do projeto.**
Este skill escreve APENAS em `_reversa_bugs/generated/` e `_reversa_sdd/traceability/bugs.md` (ambos views regeneráveis). Os `bug.md` são somente leitura aqui: inconsistência se reporta, não se conserta.
