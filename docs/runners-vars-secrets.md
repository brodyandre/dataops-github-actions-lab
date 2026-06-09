# Runners, vars e secrets

## Visão geral

Este projeto tem um workflow específico, `context-vars-secrets.yml`, criado para demonstrar como eu organizo configuração e dados sensíveis no GitHub Actions sem transformar a automação em uma caixa-preta.

O objetivo não é simular um cenário complexo de produção. O objetivo é mostrar, de forma clara, que eu entendo a diferença entre configuração operacional, contexto de execução e informação sensível.

## O que é um runner

Runner é a máquina que executa um job do GitHub Actions.

Neste laboratório eu uso `ubuntu-latest`, que é um runner hospedado pelo GitHub. Para este tipo de projeto, isso faz sentido porque:

- reduz setup inicial
- deixa o comportamento do workflow previsível
- facilita a reprodução por qualquer pessoa que estiver avaliando o repositório

Se o projeto precisasse acessar rede interna, binários específicos do ambiente ou infraestrutura própria, aí faria sentido discutir self-hosted runners. Aqui, a escolha por runner hospedado mantém o foco no que interessa: automação limpa e fácil de explicar.

## Diferença entre `env`, `vars` e `secrets`

### `env`

`env` serve para valores usados durante a execução do workflow ou do job.

No workflow `context-vars-secrets.yml`, eu uso `env` em dois níveis:

- no nível do workflow, para valores compartilhados, como `WORKFLOW_LABEL`
- no nível do job, para valores locais daquele fluxo, como `JOB_LABEL`

Também uso `env` para resolver o ambiente do projeto com base em `vars.PROJECT_ENV`.

### `vars`

`vars` representa variáveis configuradas no repositório, na organização ou no ambiente do GitHub. Elas são úteis para valores que não são sensíveis, mas que eu não quero hardcoded no YAML.

Neste projeto, `PROJECT_ENV` é um bom exemplo. Ele pode receber valores como:

- `development`
- `staging`
- `portfolio`

O workflow lê `vars.PROJECT_ENV` e escreve esse valor no resumo da execução.

### `secrets`

`secrets` guarda valores sensíveis, como tokens, credenciais e chaves.

Neste laboratório eu uso o secret `FAKE_API_TOKEN` apenas para fins educacionais. Ele não representa uma integração real e não deve conter nenhum dado de acesso importante. O foco aqui é mostrar o padrão correto de uso: verificar se o secret existe sem imprimir o valor.

## O que são contexts

Contexts são objetos que o GitHub Actions disponibiliza em tempo de execução para que o workflow saiba onde está rodando, quem disparou a execução e quais dados estão disponíveis naquele momento.

No workflow deste projeto, os contexts mais importantes são:

- `github`, para informações como branch e actor
- `runner`, para informações como sistema operacional
- `env`, para acessar valores definidos no próprio workflow

Exemplos usados no repositório:

- `github.ref_name`
- `github.actor`
- `runner.os`
- `env.PROJECT_ENVIRONMENT`

Eu gosto de pensar em contexts como a camada que conecta o YAML ao momento real da execução.

## Boas práticas para não expor dados sensíveis

Algumas regras que eu sigo sempre que trabalho com `secrets`:

- nunca versionar tokens no repositório
- nunca escrever o valor do secret em log, artifact ou summary
- validar presença do secret sem revelar conteúdo
- usar nomes claros para facilitar auditoria
- preferir credenciais com menor privilégio possível

Neste projeto, o workflow não imprime `FAKE_API_TOKEN`. Ele apenas informa se o secret foi encontrado ou não.

## Como criar `PROJECT_ENV`

Para criar a variável de repositório:

1. Acesse o repositório no GitHub.
2. Vá em `Settings`.
3. Abra `Secrets and variables`.
4. Clique em `Actions`.
5. Entre na aba `Variables`.
6. Crie uma variável chamada `PROJECT_ENV`.
7. Defina um valor compatível com o cenário que você quer demonstrar, como `portfolio`.

## Como criar `FAKE_API_TOKEN`

Para criar o secret de demonstração:

1. Acesse o repositório no GitHub.
2. Vá em `Settings`.
3. Abra `Secrets and variables`.
4. Clique em `Actions`.
5. Entre na aba `Secrets`.
6. Crie um secret chamado `FAKE_API_TOKEN`.
7. Use um valor fictício, apenas para validar o fluxo do workflow.

Esse token é propositalmente fictício e existe só para fins educacionais. A ideia não é integrar com uma API real, e sim mostrar a forma certa de lidar com secrets no GitHub Actions.

## Como isso aparece neste projeto

Quando o workflow `context-vars-secrets.yml` é executado manualmente:

- ele lê a branch e o actor a partir do context `github`
- identifica o sistema operacional pelo context `runner`
- resolve o ambiente do projeto por meio de `vars.PROJECT_ENV`
- valida a presença de `FAKE_API_TOKEN` sem expor o valor
- escreve um resumo no `GITHUB_STEP_SUMMARY`

Esse workflow é pequeno, mas útil como registro de maturidade operacional. Ele mostra que eu não penso apenas em rodar código: eu também penso em configuração, segurança e clareza de execução.
