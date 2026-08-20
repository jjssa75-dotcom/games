# Navegação e Colisão v_1

## Decisão de design

A edição 2.1 preserva as regras de combate validadas e separa duas leituras de
montanha. `M` representa encosta ou elevação transitável, custa movimento
adicional e mantém o bônus de altura. `^` representa pico ou escarpa e nunca é
transitável. Isso evita transformar toda região montanhosa num muro e mantém a
escolha tática entre rota rápida e posição elevada.

## Gramática executável

| Símbolo | Leitura | Navegação |
|---|---|---|
| `.` | solo | transitável, custo 1 |
| `F` | floresta/cobertura | transitável, custo 2 sem afinidade |
| `M` | encosta/elevação | transitável, custo 2 sem afinidade |
| `~` | terreno difícil ou água rasa | transitável, custo 2 sem afinidade |
| `#` | parede ou muralha | intransponível |
| `B` | estrutura sólida | intransponível |
| `^` | pico ou escarpa | intransponível |
| `X` | abismo, lava, água profunda ou obstáculo natural | intransponível |
| `O` | área de controle | transitável |
| `E` | saída de missão | transitável |

Voo e afinidades reduzem custos de terrenos difíceis, mas não ignoram
`#`, `B`, `^` ou `X`. Essa escolha impede que unidades atravessem o teto lógico
de uma fortaleza, um pico maciço ou um abismo apenas por possuírem mobilidade
especial.

## Autoridade única

`ActionResolver.reachable_positions` calcula os destinos e custos por busca de
custo mínimo com vizinhança cardinal. O jogador, a IA, o preview e a aplicação
da ação consultam a mesma autoridade. A interface recebe somente as casas
legais calculadas pelo servidor e as destaca; clicar fora delas não envia um
movimento.

O resolvedor ainda verifica o símbolo do terreno diretamente. Portanto, um
mapa malformado não se torna atravessável se a camada de carregamento esquecer
de copiar uma casa para `BattleState.blocked`.

## Garantias dos mapas v_3

- 160 mapas retangulares de 12 × 8.
- Todos os pontos de surgimento, objetivos e saídas são transitáveis.
- Todo o espaço transitável de cada mapa pertence a um único componente
  conectado por passos cardinais.
- Barreiras temáticas são inseridas apenas quando não criam ilha inacessível.
- A geração determinística aborta se um mapa perder conectividade.
- A IA não possui atalho de movimento e não atravessa barreiras.

## Matriz de QA

- Destino sobre qualquer símbolo intransponível deve falhar.
- Barreira deve bloquear caminho mesmo se não estiver em `state.blocked`.
- Destinos destacados nunca podem incluir unidade, parede, estrutura, pico ou
  perigo natural.
- Seleção e tentativa inválida devem preservar ator, posição e quantidade de
  destinos legais.
- Os 160 cenários devem atingir um estado terminal sem softlock depois da nova
  geometria.
