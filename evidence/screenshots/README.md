# Evidências visuais

Esta pasta foi reservada para screenshots que ajudem a mostrar o projeto em execução.

O ideal é manter uma convenção simples de nomes, para que o README principal e o histórico do repositório continuem fáceis de entender.

## Prints recomendados

### `01-local-make-validate.png`

Captura da execução local de:

```bash
make validate
```

O print deve mostrar, de preferência:

- lint executado com sucesso
- testes passando
- pipeline gerando o CSV processado e o relatório

### `02-actions-ci-success.png`

Captura da aba `Actions` com o workflow de CI concluído com sucesso.

### `03-artifact-generated.png`

Captura da run mostrando o artifact publicado pelo workflow.

### `04-workflow-dispatch-manual-run.png`

Captura de uma execução manual com `workflow_dispatch`, incluindo os inputs usados quando isso aparecer na interface.

### `05-matrix-python-versions.png`

Captura do workflow com matrix mostrando execuções em múltiplas versões de Python.

### `06-reusable-workflow-run.png`

Captura da execução do workflow consumidor que chama o workflow reutilizável.

### `07-repository-dispatch-run.png`

Captura da execução do workflow acionado por `repository_dispatch`, quando esse cenário for configurado e executado no repositório.

## Boas práticas

- prefira prints limpos, com foco no resultado da execução
- evite capturar tokens, secrets, e-mails privados ou qualquer informação sensível
- se houver dados sensíveis na tela, masque antes de salvar o arquivo
- mantenha os nomes dos arquivos estáveis para não quebrar links futuros no README
