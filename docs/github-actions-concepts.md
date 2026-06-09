# GitHub Actions: conceitos principais

## O que é GitHub Actions

GitHub Actions é a camada de automação do GitHub. Neste laboratório, ele é tratado como parte da arquitetura de entrega do projeto, não como um anexo do repositório.

## Como isso aparece neste projeto

Neste repositório, GitHub Actions foi colocado para validar o que realmente importa no fluxo local:

- lint com `ruff`
- testes com `pytest`
- execução do pipeline de clientes
- publicação do relatório `reports/pipeline_summary.md` como artifact

Na prática, isso significa que cada alteração enviada para `main`, cada pull request aberto contra `main` e cada execução manual pode seguir o mesmo ritual básico de validação.

## Conceitos que eu considero essenciais aqui

### Workflow

Workflow é o arquivo YAML que define uma automação. Neste projeto, o exemplo mais importante é `.github/workflows/ci.yml`.

Esse workflow foi desenhado para responder a uma pergunta simples: "se eu fizer uma mudança agora, o projeto continua íntegro?" Em vez de deixar essa checagem só na máquina local, o workflow repete o processo dentro do GitHub e padroniza a validação para qualquer contribuição.

### Job

Job é um bloco de execução dentro do workflow. No `ci.yml`, o job `validate-project` concentra toda a validação do projeto em um único fluxo:

- baixar o código
- preparar o ambiente Python
- instalar dependências
- rodar lint
- rodar testes
- executar o pipeline
- publicar o relatório gerado

Neste caso eu preferi um único job porque a leitura fica mais direta para quem está avaliando o repositório. Como o projeto ainda é pequeno, separar em vários jobs deixaria o YAML mais longo sem trazer ganho real.

### Step

Step é cada etapa individual dentro do job. É no nível de step que a automação fica realmente legível.

No `ci.yml`, cada step representa uma decisão concreta do fluxo:

- `Check out repository` traz o código para o ambiente de execução
- `Set up Python 3.11` garante a mesma base de runtime
- `Install project dependencies` prepara o ambiente
- `Run lint with Ruff` protege a qualidade do código
- `Run test suite with Pytest` valida comportamento
- `Execute customer pipeline` confirma que o pipeline roda do início ao fim
- `Upload pipeline summary report` guarda uma evidência útil da execução

Esse encadeamento ajuda bastante em entrevista porque mostra que o pipeline de dados não está isolado do resto da engenharia. Ele faz parte da rotina de validação.

### Runner

Runner é a máquina onde o job roda. Neste projeto eu uso `ubuntu-latest`, que é um runner hospedado pelo GitHub.

Essa escolha faz sentido aqui por alguns motivos:

- o pipeline usa Python e arquivos CSV simples, então não precisa de infraestrutura especial
- o ambiente fica fácil de reproduzir
- o custo de manutenção é baixo
- o workflow fica legível para quem quiser entender o projeto rapidamente

Se o projeto evoluísse para integrações com rede interna, credenciais específicas ou ferramentas fora do ambiente padrão, aí faria sentido discutir self-hosted runners. Para este laboratório, `ubuntu-latest` cobre bem a necessidade.

## Por que CI é importante em projetos de dados

Em projetos de dados, o erro nem sempre aparece como uma falha óbvia de aplicação. Muitas vezes o problema está em uma coluna faltando, em uma regra de transformação quebrada ou em uma saída gerada com formato inconsistente.

Neste repositório, o CI ajuda a evitar exatamente esse tipo de regressão:

- o `ruff` reduz ruído e melhora consistência do código
- o `pytest` protege regras importantes, como validação de colunas e segmentação de clientes
- a execução do pipeline garante que o fluxo completo ainda funciona com o dataset de exemplo
- o artifact com `pipeline_summary.md` deixa um rastro verificável da execução

Esse é o ponto principal de CI em dados: tratar pipeline como software de verdade, com repetibilidade, feedback rápido e evidência concreta de que a mudança não quebrou o processo.
