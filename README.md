# dataops-github-actions-lab

![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![Lint](https://img.shields.io/badge/lint-ruff-111827?logo=ruff&logoColor=white)
![Automation](https://img.shields.io/badge/automation-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Focus](https://img.shields.io/badge/focus-DataOps-0B7285)

Laboratório de DataOps com Python e GitHub Actions voltado para um fluxo completo de entrega: validação de dados, automação de qualidade, execução controlada do pipeline, publicação de artifacts e documentação operacional.

Este repositório não tenta simular uma plataforma inteira de dados. Ele foca em um recorte menor e mais verificável: como estruturar um pipeline simples de forma organizada, rastreável e fácil de revisar, tanto localmente quanto dentro do GitHub Actions.

<a id="indice"></a>
## Índice

- [Visão geral](#visao-geral)
- [Arquitetura](#arquitetura)
- [Estrutura do repositório](#estrutura-do-repositorio)
- [Workflows do GitHub Actions](#workflows-do-github-actions)
- [Execução local](#execucao-local)
- [Exemplos de execução](#exemplos-de-execucao)
- [Evidências de execução](#evidencias-de-execucao)
- [Competências demonstradas](#competencias-demonstradas)
- [Checklist técnico do laboratório](#checklist-tecnico-do-laboratorio)
- [Como este projeto se conecta com Engenharia de Dados](#como-este-projeto-se-conecta-com-engenharia-de-dados)
- [Revisão e colaboração](#revisao-e-colaboracao)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Documentação complementar](#documentacao-complementar)
- [GitHub](#github)

<a id="visao-geral"></a>
## Visão geral

O núcleo do laboratório é um pipeline Python que lê um CSV de clientes, valida colunas obrigatórias, limpa campos de texto, segmenta clientes por faixa de gasto e gera dois produtos:

- `data/processed/customers_processed.csv`
- `reports/pipeline_summary.md`

Em volta desse pipeline, o repositório concentra workflows do GitHub Actions para:

- CI
- CD simulado com publicação de artifacts
- execução manual com inputs e outputs entre jobs
- demonstração de `env`, `vars`, `secrets` e `contexts`
- uso de `matrix`, `concurrency` e condicionais
- workflow reutilizável com `workflow_call`
- gatilho externo com `repository_dispatch`

O objetivo prático é mostrar como um pipeline de dados simples pode ser tratado com a mesma disciplina de engenharia aplicada a software: revisão, teste, automação, rastreabilidade e documentação.

[Voltar ao índice](#indice)

<a id="arquitetura"></a>
## Arquitetura

O fluxo principal do pipeline é este:

```text
data/raw/customers.csv
        |
        v
src/dataops_pipeline/pipeline.py
  - valida colunas obrigatórias
  - limpa espaços em branco
  - calcula customer_segment
        |
        +--> data/processed/customers_processed.csv
        |
        +--> reports/pipeline_summary.md
```

Acima dessa camada de transformação, o GitHub Actions atua como orquestrador de qualidade e operação:

- valida código com `ruff`
- valida comportamento com `pytest`
- executa o pipeline em cenários controlados
- publica artifacts para inspeção
- registra contexto de execução e decisões operacionais

Esse desenho é intencionalmente simples. A ideia aqui não é resolver escala, e sim deixar claras as responsabilidades de cada parte do fluxo.

[Voltar ao índice](#indice)

<a id="estrutura-do-repositorio"></a>
## Estrutura do repositório

```text
.
|-- .github/
|   |-- pull_request_template.md
|   `-- workflows/
|       |-- cd.yml
|       |-- ci.yml
|       |-- context-vars-secrets.yml
|       |-- manual-data-pipeline.yml
|       |-- matrix-and-concurrency.yml
|       |-- pipeline-manual.yml
|       |-- repository-dispatch.yml
|       |-- reusable-python-quality.yml
|       `-- use-reusable-workflow.yml
|-- data/
|   |-- processed/
|   `-- raw/
|-- docs/
|-- evidence/
|   `-- screenshots/
|       `-- README.md
|-- reports/
|-- src/dataops_pipeline/
|-- tests/
|-- Makefile
|-- README.md
|-- requirements-dev.txt
`-- requirements.txt
```

Diretórios principais:

- `src/dataops_pipeline/`: implementação do pipeline
- `tests/`: suíte automatizada com `pytest`
- `.github/workflows/`: workflows usados como laboratório de GitHub Actions
- `docs/`: explicações curtas e objetivas sobre os conceitos usados no projeto
- `evidence/screenshots/`: espaço reservado para prints de runs, checks e artifacts

[Voltar ao índice](#indice)

<a id="workflows-do-github-actions"></a>
## Workflows do GitHub Actions

| Workflow | Trigger principal | Papel no laboratório |
| --- | --- | --- |
| `ci.yml` | `push`, `pull_request`, `workflow_dispatch` | Valida lint, testes, pipeline e gera o relatório como artifact. |
| `cd.yml` | `push` em `main` | Simula uma etapa de entrega contínua publicando saídas validadas do pipeline. |
| `pipeline-manual.yml` | `workflow_dispatch` | Executa o pipeline manualmente a partir de um arquivo informado no input. |
| `manual-data-pipeline.yml` | `workflow_dispatch` | Demonstra `inputs`, `outputs` entre jobs e publicação condicional de artifacts. |
| `context-vars-secrets.yml` | `workflow_dispatch` | Mostra uso prático de `env`, `vars`, `secrets` e `contexts`. |
| `matrix-and-concurrency.yml` | `push`, `pull_request`, `workflow_dispatch`, `schedule` | Demonstra matriz de versões de Python, condicionais e controle de concorrência. |
| `reusable-python-quality.yml` | `workflow_call` | Encapsula um fluxo reutilizável de lint, testes e execução opcional do pipeline. |
| `use-reusable-workflow.yml` | `workflow_dispatch` | Chama o workflow reutilizável com `inputs` e repasse de `secrets`. |
| `repository-dispatch.yml` | `repository_dispatch` | Simula um gatilho externo disparando o pipeline via GitHub API. |

Os arquivos em `docs/` explicam cada um desses temas com mais profundidade, sempre usando este repositório como referência e não um exemplo abstrato.

[Voltar ao índice](#indice)

<a id="execucao-local"></a>
## Execução local

O runtime do pipeline usa apenas a biblioteca padrão do Python. As dependências de desenvolvimento existem para lint e testes.

### Preparação do ambiente

```bash
make install
```

### Comandos disponíveis

| Comando | Uso |
| --- | --- |
| `make install` | Instala `requirements.txt` e `requirements-dev.txt`. |
| `make lint` | Executa `ruff`. |
| `make test` | Executa `pytest`. |
| `make run` | Roda o pipeline e gera CSV processado + relatório. |
| `make clean` | Remove arquivos gerados em `data/processed/` e `reports/`. |
| `make validate` | Roda `lint`, testes e pipeline em sequência. |

### Execução manual do pipeline

```bash
PYTHONPATH=src python3 -m dataops_pipeline.pipeline \
  --input data/raw/customers.csv \
  --output data/processed/customers_processed.csv \
  --report reports/pipeline_summary.md
```

[Voltar ao índice](#indice)

<a id="exemplos-de-execucao"></a>
## Exemplos de execução

### Fluxo local completo

```bash
make install
make validate
```

Saída esperada:

```text
All checks passed!
7 passed
Processed 6 customers
Output file: data/processed/customers_processed.csv
Report file: reports/pipeline_summary.md
```

### Exemplo de relatório gerado

```md
# Pipeline Summary

- Input file: `data/raw/customers.csv`
- Output file: `data/processed/customers_processed.csv`
- Processed records: 6
```

### Exemplo de execução manual no GitHub Actions

Um cenário útil para demonstração é disparar `manual-data-pipeline.yml` com:

- `environment = staging`
- `run_quality_gate = true`

Nesse caso, o workflow valida o projeto, executa o pipeline e publica `data/processed/` e `reports/` como artifacts da run.

[Voltar ao índice](#indice)

<a id="evidencias-de-execucao"></a>
## Evidências de execução

O diretório `evidence/screenshots/` foi preparado para receber prints do projeto em execução. As instruções detalhadas de captura estão em [evidence/screenshots/README.md](/home/luizandre/dataops-github-actions-lab/evidence/screenshots/README.md:1).

Os caminhos abaixo funcionam como placeholders planejados. A ideia é salvar os arquivos com esses nomes quando as capturas forem feitas.

| Evidência | Caminho sugerido | O que registrar |
| --- | --- | --- |
| Execução local do `make validate` | `evidence/screenshots/01-local-make-validate.png` | Terminal com lint, testes e pipeline executados com sucesso. |
| Aba Actions com CI concluído | `evidence/screenshots/02-actions-ci-success.png` | Run bem-sucedida do workflow `ci.yml`. |
| Artifact gerado pelo workflow | `evidence/screenshots/03-artifact-generated.png` | Artifact publicado após a execução do pipeline. |
| Execução manual com `workflow_dispatch` | `evidence/screenshots/04-workflow-dispatch-manual-run.png` | Tela do workflow manual com inputs e resultado da execução. |
| Matrix build com múltiplas versões de Python | `evidence/screenshots/05-matrix-python-versions.png` | Execução do workflow com Python 3.10, 3.11 e 3.12. |
| Workflow reutilizável executado | `evidence/screenshots/06-reusable-workflow-run.png` | Run do workflow consumidor chamando `workflow_call`. |
| `repository_dispatch` executado, se aplicável | `evidence/screenshots/07-repository-dispatch-run.png` | Run disparada por evento externo com `client_payload`. |

Quando esses arquivos existirem, eles podem ser referenciados diretamente no README ou em uma apresentação do projeto sem necessidade de reorganizar a estrutura.

[Voltar ao índice](#indice)

<a id="competencias-demonstradas"></a>
## Competências demonstradas

- Estruturação de pipeline Python com funções pequenas, legíveis e testáveis.
- Validação de dados e enriquecimento de saída com regra de negócio simples.
- Padronização de qualidade com `ruff` e `pytest`.
- Construção de workflows de CI e CD sem depender de infraestrutura paga.
- Uso de `workflow_dispatch`, `workflow_call`, `repository_dispatch`, `matrix`, `concurrency`, `artifacts`, `env`, `vars`, `secrets` e `contexts`.
- Organização de revisão com Pull Request Template.
- Documentação técnica pensada para leitura rápida por pessoas técnicas e recrutadores.

[Voltar ao índice](#indice)

<a id="checklist-tecnico-do-laboratorio"></a>
## Checklist técnico do laboratório

- [x] Pipeline Python com leitura de CSV, validação de colunas, limpeza de strings e segmentação de clientes.
- [x] Geração de saída processada em `data/processed/` e relatório em `reports/`.
- [x] Testes automatizados com `pytest` cobrindo regra de segmentação, validação de colunas e geração de artefatos.
- [x] Padronização de qualidade local com `ruff`, `pytest` e `Makefile`.
- [x] Workflow de CI para validar lint, testes, pipeline e publicar relatório como artifact.
- [x] Workflow de CD simulado para publicar saídas validadas do pipeline após `push` em `main`.
- [x] Workflow manual com `workflow_dispatch`, `inputs`, `outputs` entre jobs e publicação condicional de artifacts.
- [x] Workflow dedicado para demonstrar `env`, `vars`, `secrets` e `contexts` com resumo operacional.
- [x] Workflow com `matrix`, `schedule`, condicionais e `concurrency`.
- [x] Workflow reutilizável com `workflow_call` e workflow consumidor com repasse de `secrets`.
- [x] Workflow acionado por `repository_dispatch` com leitura de `client_payload`.
- [x] Pull Request Template para revisão, rastreabilidade e colaboração.
- [x] Estrutura preparada para evidências visuais em `evidence/screenshots/`.

[Voltar ao índice](#indice)

<a id="como-este-projeto-se-conecta-com-engenharia-de-dados"></a>
## Como este projeto se conecta com Engenharia de Dados

Este laboratório conversa com Engenharia de Dados em pontos bem concretos:

- o pipeline valida contrato mínimo de entrada antes de gerar saída
- o processamento é reproduzível e gera um relatório simples para auditoria
- os workflows tratam dados processados e relatórios como artifacts verificáveis
- o repositório mostra padrões de integração com gatilhos externos e múltiplos cenários de execução
- o fluxo de revisão considera impacto em automação, rastreabilidade e documentação

Em um ambiente maior, a mesma lógica poderia ser conectada a storage, orquestração, catálogos ou jobs distribuídos. Aqui, o foco está em deixar a base limpa e compreensível.

[Voltar ao índice](#indice)

<a id="revisao-e-colaboracao"></a>
## Revisão e colaboração

O projeto usa `.github/pull_request_template.md` para manter um padrão mínimo de revisão. Cada PR deve trazer:

- resumo da alteração
- evidências de teste
- impacto em CI/CD
- riscos e observações

Isso torna o histórico do repositório mais útil para quem revisa, para quem retoma contexto depois e para quem quer avaliar a maturidade do fluxo de entrega.

[Voltar ao índice](#indice)

<a id="troubleshooting"></a>
## Troubleshooting

| Sintoma | O que verificar |
| --- | --- |
| `pytest` ou `ruff` não encontrado | Rode `make install`. |
| `ModuleNotFoundError: dataops_pipeline` em execução manual | Use `make run` ou defina `PYTHONPATH=src`. |
| `reports/pipeline_summary.md` não existe | Rode `make run` ou `make validate` após `make clean`. |
| Workflow manual não publicou artifacts | Verifique se `run_quality_gate` foi executado como `true`. |
| `PROJECT_ENV` ou `FAKE_API_TOKEN` não aparecem nos workflows de demonstração | Configure o valor em `Settings > Secrets and variables > Actions`. |

[Voltar ao índice](#indice)

<a id="roadmap"></a>
## Roadmap

- adicionar regras de qualidade de dados além da validação de colunas
- gerar relatórios mais analíticos em `reports/`
- publicar artifacts em um destino externo, como S3, GCS ou Azure Blob
- conectar o pipeline a um orquestrador, como Airflow
- expandir o uso de reusable workflows para um cenário com múltiplos repositórios
- adicionar um exemplo de execução agendada com persistência de evidências

[Voltar ao índice](#indice)

<a id="documentacao-complementar"></a>
## Documentação complementar

Os arquivos em `docs/` aprofundam os pontos que aparecem nos workflows:

- `docs/github-actions-concepts.md`
- `docs/ci-cd.md`
- `docs/runners-vars-secrets.md`
- `docs/inputs-outputs-artifacts.md`
- `docs/triggers-matrix-concurrency.md`
- `docs/reusable-workflows.md`
- `docs/repository-dispatch.md`
- `docs/gitflow-vs-github-flow.md`

[Voltar ao índice](#indice)

<a id="github"></a>
## GitHub

Perfil: https://github.com/brodyandre

[Voltar ao índice](#indice)
