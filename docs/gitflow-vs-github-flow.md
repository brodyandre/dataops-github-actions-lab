# GitFlow vs GitHub Flow

## Objetivo deste material

Este documento registra a escolha de fluxo de branches usada no laboratório. A comparação entre GitFlow e GitHub Flow existe aqui para justificar uma decisão prática de operação, não para apresentar teoria isolada.

## GitFlow

O GitFlow costuma usar branches fixas para `main`, `develop`, `feature`, `release` e `hotfix`. Ele funciona bem quando o time precisa controlar ciclos mais formais de entrega, múltiplas versões em paralelo ou janelas de release bem definidas.

Pontos fortes:

- boa organização para times grandes
- separação clara entre desenvolvimento e release
- processo previsível para manutenção de versões

Pontos de atenção:

- adiciona mais cerimônia
- cria mais overhead para projetos pequenos
- pode deixar o fluxo mais lento se o time não precisar dessa estrutura toda

## GitHub Flow

O GitHub Flow trabalha de forma mais direta: `main` está sempre pronta, novas mudanças saem de branches curtas e tudo passa por pull request antes do merge.

Pontos fortes:

- fluxo simples de explicar e manter
- combina bem com CI automatizada
- incentiva mudanças menores e revisão contínua

Pontos de atenção:

- exige disciplina para manter `main` saudável
- depende de testes e revisão funcionando bem

## Decisão para este repositório

Aqui eu optei por algo próximo de GitHub Flow. O projeto é pequeno, o objetivo é manter revisão simples e a prioridade é deixar o histórico do repositório fácil de acompanhar.

Na prática, isso significa:

- branch principal protegida por revisão e testes
- mudanças pequenas via pull request
- automação validando o essencial antes do merge

## Quando eu escolheria GitFlow

Eu consideraria GitFlow se este laboratório evoluísse para:

- múltiplas versões em produção
- calendário de releases formal
- manutenção paralela de linhas diferentes do produto

Para o escopo atual, GitHub Flow entrega o que eu preciso com menos atrito.
