# Registro de Bugs (Reversa Bugs)

> Gerado pelo Reversa em {{DATA}}. Este arquivo é o contrato do registro de bugs deste projeto.
> Source of truth: cada `bugs/<ID>/bug.md`. Tudo em `generated/` é projeção regenerável.

## Configuração do projeto

```yaml
closure_policy: {{CLOSURE_POLICY}}   # local-software | package | production-service
control_mode: gated                  # supervised | gated | autonomous
```

- `closure_policy` define o que "resolvido" exige:
  - `local-software`: testes de regressão passando + veredito de spec
  - `package`: anterior + merge + versão corrigida publicada (+ backports requeridos)
  - `production-service`: anterior + entrega + janela de observação sem recorrência
- `control_mode: gated` (padrão): leitura, reprodução isolada e diagnóstico fluem sem aprovação;
  gate obrigatório para aplicar testes, aplicar change set, alterar spec efetiva, usar harness
  externo com acesso ao projeto e qualquer operação destrutiva.

## Estrutura

```text
_reversa_bugs/
├── README.md                    este contrato
├── taxonomy.yaml                vocabulário controlado de area/module/feature
├── bugs/BUG-<data>-<sufixo>-<slug>/   pasta única do bug (endereço IMUTÁVEL, nunca se move)
│   ├── bug.md                   registro canônico
│   ├── evidence/  ├── debate/  └── fix/
├── inspections/<feature>/       relatórios do pente-fino
└── generated/                   views regeneradas pelo /reversa-debugger-graph (não editar à mão)
```

## Ciclo de vida

`status`: `open` → `active` → `resolved`. `phase` detalha a etapa dentro de `active`
(mitigating, reproducing, diagnosing, testing, patching, delivering, observing, awaiting-human).
Bloqueio é condição (`blocking:`), nunca status. Todo fechamento tem `resolution_kind`.

## Regra de rastreabilidade

Todo bug DEVE identificar:

1. A seção de spec que define o comportamento esperado (spec efetiva = original + adendos vigentes).
   Sem spec, o bug carrega o label `spec-gap` e a lacuna é tratada antes da resolução.
2. O código afetado (onde aparece) e, após investigação, a causa raiz (onde nasceu), com estado
   epistemológico e evidências.
3. Os testes de reprodução e de regressão.

Um bug NÃO pode ser `resolved: fixed` com `traceability.specs`, `root_cause` (confirmed) ou
`regression_tests` vazios.

## Protocolo dos agentes

1. Registrar (`/reversa-debugger`) NUNCA corrige. Corrigir (`/reversa-debugger-fix`) segue dois gates de
   aprovação com diff (testes que falham; change set que faz os testes passarem).
2. A spec original NUNCA é editada. Mudança de spec vira adendo versionado e imutável em
   `<output_folder>/addenda/bug-<ID>-vNNN.md`, com decisão humana registrada.
3. Diff do código e diff/adendo da spec ficam registrados JUNTOS na Resolution do bug.
4. Bugs com `visibility: restricted` ficam fora das views e nada explorável vai a harness externo.
5. Relação e causa raiz têm estado epistemológico: hipótese não é fato.

## Convenções

- ID canônico: `BUG-<YYYYMMDD>-<sufixo>` (merge-safe). `display_number` é apelido humano.
- Referências sempre por ID; as views resolvem o caminho.
- Evidências em `evidence/`, nunca logs gigantes dentro do Markdown.
- Schema completo: ver `bug-schema` na documentação do Reversa (agents/reversa-debugger/references/).
