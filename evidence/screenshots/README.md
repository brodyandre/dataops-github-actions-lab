# Evidências visuais

Esta pasta reúne os prints usados para sustentar a execução prática do laboratório. A ideia aqui não é colecionar imagens, e sim registrar evidências objetivas de que os fluxos documentados no repositório realmente foram executados.

Os arquivos atuais estão organizados com prefixo numérico para facilitar leitura sequencial no README principal, em apresentações e em revisões técnicas.

## O que cada print comprova

| Arquivo | O que comprova |
| --- | --- |
| `01-local-make-validate-success.png` | Validação local completa com `ruff`, `pytest` e execução do pipeline, incluindo geração do CSV processado e do relatório final. |
| `02-github-actions-workflows-list.png` | Visão geral da aba `Actions`, mostrando que o repositório possui múltiplos workflows configurados e com execuções registradas. |
| `03-ci-workflow-success.png` | Execução bem-sucedida do workflow `CI`, com job `Validate project` concluído e artifact gerado na run. |
| `04-ci-artifact-generated.png` | Publicação do artifact `pipeline-summary` na execução do `CI`, evidenciando rastreabilidade da saída do pipeline. |
| `05-manual-data-pipeline-run.png` | Execução concluída do workflow `Manual Data Pipeline`, com os jobs `prepare`, `validate` e `publish-artifacts` finalizados com sucesso e artifacts publicados. |
| `05b-manual-data-pipeline-inputs.png` | Registro complementar da execução manual, reforçando que a run foi disparada por `workflow_dispatch` e percorreu o fluxo definido para esse cenário. |
| `06-context-vars-secrets-summary.png` | Execução do workflow `Contexts, Vars and Secrets`, confirmando a checagem de contexto de execução e a validação controlada da presença de secret. |
| `07-matrix-build-success.png` | Sucesso do workflow com matrix, incluindo execuções em Python 3.10, 3.11 e 3.12 e resumo de execução no GitHub Actions. |
| `08-reusable-workflow-success.png` | Execução bem-sucedida do workflow consumidor que chama o workflow reutilizável com `workflow_call`. |
| `09-repository-dispatch-success.png` | Execução disparada por `repository_dispatch`, incluindo leitura do payload e publicação dos artifacts gerados pelo pipeline. |

## Critério de organização

- Os nomes seguem uma sequência lógica de leitura, do fluxo local para os workflows do GitHub Actions.
- O prefixo `05b` foi mantido como complemento direto da evidência de execução manual.
- Não há arquivos extras com nomes ambíguos além do `.gitkeep`, usado apenas para versionar a pasta.

## Boas práticas

- Mantenha apenas prints que comprovem execução real do projeto.
- Evite capturar tokens, secrets, e-mails privados ou qualquer dado sensível.
- Quando uma imagem for substituída por versão mais atual, preserve o mesmo nome para não quebrar referências no README principal.
