# Reusable workflows

## O que são

Reusable workflows permitem centralizar automações que se repetem em vários repositórios ou em várias partes de uma organização.

Em vez de copiar e colar o mesmo YAML, eu defino um workflow reutilizável e o chamo quando precisar. Neste laboratório, isso aparece no arquivo `reusable-python-quality.yml`, que concentra um fluxo de qualidade para projetos Python com lint, testes, execução opcional do pipeline e checagem de secret.

## Diferença entre workflow normal e workflow chamado por `workflow_call`

Um workflow normal é disparado diretamente por eventos como `push`, `pull_request` ou `workflow_dispatch`. Ele é pensado para rodar por conta própria.

Já um workflow reutilizável é desenhado para ser chamado por outro workflow por meio de `workflow_call`.

Na prática, a diferença é esta:

- o workflow consumidor decide quando a execução deve acontecer
- o workflow reutilizável define o comportamento padronizado que será reaproveitado

Neste projeto, `use-reusable-workflow.yml` é o workflow consumidor. Ele dispara manualmente e delega a validação para `reusable-python-quality.yml`.

## Como inputs e secrets funcionam nesse cenário

No padrão de `workflow_call`, o workflow reutilizável declara explicitamente quais `inputs` e `secrets` aceita.

No caso deste laboratório:

- `python-version` define a versão do Python usada no setup
- `run-pipeline` controla se o pipeline deve rodar depois de lint e testes
- `FAKE_API_TOKEN` pode ser repassado como secret opcional

Isso é importante porque deixa o contrato do workflow bem claro. Quem chama o workflow sabe exatamente o que precisa informar e o que pode customizar.

Também gosto desse formato porque ele reduz ambiguidade. Em vez de depender de comportamento implícito, o repositório passa a ter uma interface explícita de automação.

## Como isso aparece neste projeto

O workflow reutilizável deste laboratório executa o seguinte fluxo:

- checkout do código
- setup do Python com a versão recebida via input
- instalação de dependências
- lint com `ruff`
- testes com `pytest`
- execução opcional do pipeline
- validação da presença de `FAKE_API_TOKEN`, sem expor o valor

O workflow consumidor mostra a chamada prática:

- passa `python-version: 3.11`
- passa `run-pipeline: true`
- repassa `FAKE_API_TOKEN`

Esse desenho parece simples, mas ele representa uma prática muito comum em times maduros: manter um padrão de qualidade compartilhado entre vários pipelines.

## Por que isso é útil em múltiplos repositórios

Se eu tiver vários repositórios de dados, bibliotecas internas ou serviços auxiliares, reusable workflows ajudam a:

- reduzir duplicação
- padronizar validações
- facilitar manutenção do CI ao longo do tempo
- diminuir divergência entre equipes ou projetos

Em vez de atualizar cinco ou dez arquivos YAML diferentes sempre que o processo mudar, eu atualizo um fluxo reutilizável e mantenho o padrão mais estável.

## Leitura prática de portfólio

Reusable workflow não é recurso para "enfeitar" repositório. Ele vale a pena quando resolve repetição real sem esconder demais o comportamento da automação.

Neste laboratório, eu usei esse recurso como aprendizado prático: sair do YAML isolado e tratar automação como componente reutilizável. Esse é o tipo de detalhe que costuma fazer diferença quando o trabalho envolve vários pipelines, múltiplos repositórios e necessidade de manter padrão com baixo atrito.
