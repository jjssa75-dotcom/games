# Decisões Técnicas v_4

## Escopo preservado

A edição 2.1 não altera ativação alternada, economia de ações, reações, CAP,
CMD, modos, condições de vitória, árvores, progressão ou balanceamento-base. O
catálogo continua com 240 classes de personagem e 144 classes de tropa. O
trabalho é uma evolução visual e uma correção defensiva de navegação.

## Navegação data-driven

`IMPASSABLE_TERRAIN` centraliza `#`, `B`, `^` e `X`. O carregador cria
`BattleState.blocked`, mas o resolvedor também consulta o terreno bruto. O mapa
de alcance é calculado uma única vez e reutilizado por interface e IA.

Os mapas v_1 e v_2 permanecem preservados. `mapas_v_3.json` acrescenta
metadados de adjacência, símbolos difíceis/intransponíveis, regra de voo e a
garantia de conectividade.

## Interface visual

A interface recebeu uma hierarquia cinematográfica sem sacrificar leitura:
arte de comandantes na missão, quatro paisagens para os atos, brasões vetoriais
via CSS, miniaturas de unidade em forma de escudo, barra de vida, legenda de
terreno, custos de movimento e estados de foco. Paredes, estruturas, picos e
perigos naturais possuem silhuetas diferentes, não apenas cores.

O tabuleiro mantém a grade e os estados de jogo no DOM, é utilizável por teclado
e expõe rótulos acessíveis por casa. Em celular, a página não ganha rolagem
horizontal; apenas o quadro do mapa permite deslocamento controlado.

## Limites deliberados

Não foram adicionadas linha de visão, destruição de cenário, salto, escalada,
teleporte, terreno dinâmico ou física. Essas mecânicas mudariam as regras do GDD
e exigiriam uma nova etapa de prototipação e balanceamento.

## Versionamento

- Catálogo executável: `vertical_slice_v_3.json`.
- Campanha e cenários: `campanha_v_2.json` e `cenarios_v_2.json`.
- Mapas ativos: `mapas_v_3.json`.
- Direção visual: `DIRECAO_VISUAL_v_2.md`.
- Edição integrada: `2.1.0`.
