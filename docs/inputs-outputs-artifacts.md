# Inputs, outputs e artifacts

## Inputs

Inputs são parâmetros recebidos por um workflow manual. Eles permitem mudar o comportamento da execução sem editar o YAML e sem abrir um pull request só para testar um cenário diferente.

No workflow `manual-data-pipeline.yml`, os inputs servem para duas decisões práticas:

- escolher o ambiente da execução manual entre `dev`, `staging` e `prod`
- decidir se o pipeline completo deve rodar junto com a validação de qualidade

Isso ajuda a mostrar uma visão importante de automação: o mesmo workflow pode atender cenários diferentes com controle explícito de execução.

## Outputs

Outputs são valores que um step ou job expõe para etapas seguintes. Eles ajudam quando uma decisão tomada no começo do workflow precisa ser reaproveitada depois, sem duplicar lógica.

No `manual-data-pipeline.yml`, o job `prepare` transforma os inputs em dois outputs:

- `selected_environment`
- `quality_gate_enabled`

Esses outputs são lidos no job `validate` e também no job `publish-artifacts`. Na prática, isso evita que cada job precise reinterpretar os inputs por conta própria.

## Como outputs ajudam a passar informações entre jobs

Jobs diferentes no GitHub Actions não compartilham estado automaticamente. Cada job começa em um ambiente isolado. Por isso, quando eu preciso passar uma decisão de um job para outro, outputs são uma forma clara e segura de fazer isso.

Neste projeto, esse padrão aparece assim:

- `prepare` recebe os inputs do `workflow_dispatch`
- `validate` usa os outputs para decidir se executa apenas lint e testes ou também o pipeline
- `publish-artifacts` usa esses mesmos outputs para montar o resumo final da execução

Esse tipo de separação ajuda bastante em projetos maiores, porque deixa o fluxo mais modular e mais fácil de manter.

## Artifacts

Artifacts são arquivos gerados pelo workflow e preservados pelo GitHub Actions ao final da execução. Eles são úteis quando eu quero:

- inspecionar uma saída sem rodar o pipeline localmente
- guardar evidências da execução
- compartilhar resultados entre etapas diferentes do processo
- manter rastros úteis para revisão técnica e auditoria

No `manual-data-pipeline.yml`, os artifacts entram em dois papéis:

- primeiro, os arquivos gerados no job `validate` são empacotados para que o job `publish-artifacts` consiga acessá-los
- depois, o resultado final é publicado como artifact de saída da execução manual

## O que isso representa em um pipeline de dados

Em um pipeline de dados, artifact não é só "arquivo anexado". Ele pode representar:

- dataset processado
- relatório de execução
- evidência de qualidade
- insumo para outra etapa operacional

Por isso, artifacts ajudam muito em auditoria e rastreabilidade. Eles permitem responder perguntas como:

- qual arquivo esse workflow gerou?
- em qual execução isso aconteceu?
- qual ambiente foi escolhido?
- o pipeline rodou ou apenas validou código?

## Exemplo prático neste projeto

No fluxo manual deste laboratório, o GitHub Actions pode publicar:

- arquivos processados em `data/processed/`
- relatórios em `reports/`

Isso deixa um histórico verificável do que foi produzido em cada execução. No contexto do laboratório, artifacts não servem só para anexar arquivos: eles servem para sustentar auditoria, revisão técnica e confiança operacional.
