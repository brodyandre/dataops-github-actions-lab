# CI/CD

## Visão geral

Neste laboratório, CI/CD não aparece como slogan. Aparece como fluxo operacional. A separação entre CI e CD existe para deixar claro que validar mudança e publicar resultado são partes diferentes do trabalho, mesmo quando acontecem no mesmo repositório.

## CI: Continuous Integration

Na prática, CI significa validar alterações com frequência. O objetivo é reduzir o risco de descobrir problemas só no fim do trabalho e impedir que uma mudança aparentemente pequena quebre o pipeline.

Neste projeto, CI aparece em:

- lint com `ruff`
- testes automatizados com `pytest`
- execução do pipeline com o dataset de exemplo
- validação automática em `push`, `pull_request` e execução manual

O papel do CI aqui é responder rápido se o projeto continua saudável do ponto de vista de código, teste e execução.

## CD: Continuous Delivery ou Continuous Deployment

CD pode significar duas coisas:

- Continuous Delivery: o pacote fica pronto para entrega, mas alguém ainda decide o momento do deploy
- Continuous Deployment: a liberação acontece automaticamente após as validações

A diferença prática aqui é simples:

- CI verifica se a mudança pode entrar com segurança
- CD cuida do que acontece depois que essa mudança já foi validada

## Como CI/CD se aplica a Engenharia de Dados

Em Engenharia de Dados, o "produto" nem sempre é uma aplicação web ou uma API. Muitas vezes o que precisa ser entregue com confiança é:

- um dataset processado
- um relatório de execução
- um artefato que será consumido por outra etapa do ecossistema
- uma automação pronta para rodar em ambiente controlado

É por isso que CI/CD em dados precisa olhar não só para teste de código, mas também para integridade de saída, rastreabilidade e repetibilidade do pipeline.

## O que este repositório implementa hoje

Hoje o repositório implementa:

- um workflow de CI para validar qualidade, testes e execução do pipeline
- um workflow de CD simulado para publicar os artefatos gerados após a validação na branch `main`

O CD deste laboratório não faz deploy em cloud. Em vez disso, ele publica como artifacts:

- `data/processed/customers_processed.csv`
- `reports/pipeline_summary.md`

Essa escolha é intencional. O objetivo aqui é mostrar o raciocínio correto de entrega contínua sem depender de uma conta paga, credenciais externas ou infraestrutura paralela só para fins de demonstração.

## Por que este projeto usa CD simulado

Como projeto de portfólio, eu quis manter o escopo realista e reproduzível. Um CD simulado funciona bem porque:

- demonstra a separação entre validar e publicar
- deixa claro que o pipeline gera saídas úteis, não apenas logs de execução
- cria evidência concreta de entrega por meio de artifacts do GitHub Actions
- evita acoplamento prematuro com um provedor específico

Em outras palavras, o projeto mostra a disciplina de CD mesmo sem transformar a demonstração em um exercício de configuração de cloud.

## O que pode evoluir no futuro

Se este laboratório crescer, o próximo passo natural é trocar a publicação local de artifacts por destinos mais próximos de um ambiente real, como:

- envio do CSV processado para Amazon S3
- publicação em Google Cloud Storage
- armazenamento em Azure Blob Storage
- escrita em um ambiente de trabalho do Databricks
- disparo de um fluxo posterior em Airflow
- execução ou publicação dentro de um ambiente orquestrado com Kubernetes

Essas evoluções fariam sentido quando a meta deixasse de ser apenas demonstrar fundamentos e passasse a incluir integração com plataforma, governança e operação em escala.

## Por que isso importa em DataOps

Em dados, um pipeline sem validação automatizada vira um ponto frágil muito rápido. CI/CD ajuda a tratar pipeline como software de verdade: com revisão, rastreabilidade, repetibilidade e confiança para mudar.

Neste repositório, isso aparece de forma simples e objetiva:

- o CI protege a qualidade da mudança
- o CD publica o resultado validado
- os artifacts criam um histórico verificável do que o pipeline produziu
