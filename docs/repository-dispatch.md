# Repository dispatch

## O que é

`repository_dispatch` é um evento customizado do GitHub que permite disparar workflows a partir de sistemas externos ou de outros repositórios.

Neste laboratório, ele aparece como uma forma controlada de simular um gatilho externo para o pipeline de dados sem depender de uma plataforma paga ou de uma integração mais pesada.

## Quando usar

Esse recurso faz bastante sentido quando o fluxo depende de integração entre componentes diferentes. Alguns exemplos:

- um repositório de infraestrutura aciona um pipeline de dados
- um processo externo informa que um arquivo novo foi publicado
- uma automação central coordena execuções em vários projetos

No contexto deste projeto, o workflow `repository-dispatch.yml` escuta o evento `external-data-refresh`, lê o `client_payload`, executa o pipeline Python e publica os diretórios `data/processed/` e `reports/` como artifacts.

## Exemplo de cenário em Engenharia de Dados

Um cenário comum seria este:

- um processo externo detecta que uma nova versão de um arquivo foi publicada em um data lake
- esse processo chama a API do GitHub com `repository_dispatch`
- o workflow do repositório recebe o evento `external-data-refresh`
- o pipeline roda, gera a saída tratada e publica os artifacts para inspeção

Esse padrão é útil porque desacopla o produtor do evento do repositório que executa o pipeline. O sistema externo não precisa conhecer a lógica interna do workflow; ele só precisa enviar um evento bem definido.

## Exemplo de chamada com `curl`

```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "external-data-refresh",
    "client_payload": {
      "source": "data-lake-ingestion-job",
      "requested_by": "orchestrator-service",
      "reason": "new customer export available"
    }
  }'
```

Nesse exemplo:

- `event_type` precisa ser `external-data-refresh`
- `client_payload` carrega o contexto que o workflow usa no resumo da execução
- `OWNER` e `REPO` devem ser substituídos pelos dados reais do repositório

## Cuidados de segurança

Ao usar `repository_dispatch`, eu sigo duas regras básicas:

- o token usado na chamada precisa ter permissão adequada para disparar workflows no repositório
- esse token nunca deve aparecer em commits, scripts versionados com valor embutido ou prints de terminal

Na prática, o token deve ser mantido em secret e injetado no ambiente de execução que faz a chamada.

## Por que isso importa em DataOps

Times de dados raramente trabalham isolados. Muitas vezes o pipeline depende de catálogo, storage, orquestração, observabilidade ou serviços de plataforma. `repository_dispatch` ajuda a conectar essas peças sem acoplamento excessivo dentro do mesmo repositório.

O ganho principal aqui é transformar um workflow do GitHub Actions em uma interface de automação bem definida, segura e fácil de integrar com processos externos.
