# Triggers, matrix e concurrency

## Triggers

Trigger é o evento que inicia um workflow. No arquivo `matrix-and-concurrency.yml`, eu uso quatro triggers porque cada um cobre uma necessidade diferente do ciclo de trabalho deste laboratório.

### `push`

Uso `push` para validar alterações assim que elas entram em qualquer branch. Isso é útil porque, mesmo em um projeto de portfólio, eu quero ver rápido se uma mudança simples quebrou lint ou testes.

### `pull_request`

Uso `pull_request` para reforçar o momento de revisão. Para este laboratório, esse gatilho faz sentido porque o repositório foi estruturado como se passasse por fluxo de colaboração real, com revisão antes do merge.

### `workflow_dispatch`

Uso `workflow_dispatch` para permitir execução manual quando eu quiser demonstrar o comportamento do workflow sem depender de um novo commit. Em entrevista, isso ajuda bastante porque permite abrir o Actions e disparar a execução ao vivo.

### `schedule`

Uso `schedule` com execução semanal para simular uma verificação recorrente de compatibilidade. Em projetos de dados, isso é útil para detectar quebras provocadas por dependências, runner image ou mudanças indiretas, mesmo quando ninguém alterou o código naquela semana.

Neste laboratório, a execução agendada ajuda a mostrar que pipeline profissional não depende só de evento humano; ele também pode se autocontrolar ao longo do tempo.

## Matrix strategy

Matrix strategy permite rodar o mesmo job em múltiplas combinações. No `matrix-and-concurrency.yml`, eu executo o mesmo fluxo com Python 3.10, 3.11 e 3.12.

Isso ajuda a:

- reduzir dependência de um único ambiente
- antecipar incompatibilidades
- demonstrar cuidado com portabilidade

Para este projeto, isso é especialmente útil porque o pipeline é simples e deveria continuar saudável em mais de uma versão do Python. Mostrar essa compatibilidade passa uma mensagem importante de maturidade técnica.

## Condicionais

Condicionais ajudam a executar uma etapa apenas quando ela faz sentido. No workflow novo, a etapa de smoke validation do pipeline só roda quando a execução está associada à branch `main`.

Eu gosto desse padrão porque ele mostra discernimento operacional. Nem tudo precisa rodar em todo contexto da mesma forma. Às vezes faz mais sentido manter a validação base em qualquer branch e reservar uma checagem adicional para a branch principal.

## Concurrency

Concurrency evita desperdício quando vários commits são enviados em sequência para a mesma branch. Em vez de manter várias execuções antigas ocupando fila e tempo, o GitHub cancela as que perderam relevância.

Isso traz dois ganhos:

- feedback mais limpo
- menor custo operacional

No `matrix-and-concurrency.yml`, a chave de concorrência considera o nome do workflow e a branch. Na prática, isso significa que um novo push na mesma branch substitui a execução anterior ainda em andamento.

Esse detalhe é importante em pipelines profissionais porque reduz ruído, evita fila desnecessária e faz o time olhar sempre para o resultado mais recente.

## Por que isso é útil em pipelines profissionais

Neste laboratório, o workflow mostra um conjunto de decisões que aparecem com frequência em times reais:

- disparar automação em momentos diferentes do ciclo de mudança
- validar compatibilidade em múltiplas versões de runtime
- aplicar regras condicionais de acordo com a branch
- evitar execuções redundantes com concurrency

Para Engenharia de Dados, isso faz bastante diferença. Um pipeline pode parecer estável em uma versão de Python e falhar em outra. Um PR pode passar, mas uma execução semanal pode revelar um problema que só aparece com o tempo. E sem controle de concorrência, o histórico de automação fica mais barulhento do que útil.

O valor desse workflow está justamente aí: não é um YAML feito para impressionar por volume, e sim um exemplo enxuto de decisões que melhoram confiabilidade e operação.
