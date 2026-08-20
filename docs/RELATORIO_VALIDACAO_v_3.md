# Relatório de Validação v_3 — Visual e Navegação

Data: 20 de agosto de 2026  
Versão avaliada: 2.1.0

## Resultado executivo

A edição 2.1.0 foi aprovada. A suíte completa concluiu 51 testes sem falhas em
259,591 segundos. O teste de campanha jogou os 160 cenários até um estado
terminal depois da inclusão das novas barreiras, sem softlocks conhecidos.

## Navegação

| Verificação | Resultado |
|---|---:|
| Mapas v_3 analisados | 160/160 |
| Mapas com espaço transitável conectado | 160/160 |
| Spawns, objetivos e saídas transitáveis | 160/160 |
| Símbolos intransponíveis verificados | `#`, `B`, `^`, `X` |
| Destinos legais incluindo bloqueio | 0 |
| Movimento cardinal sem corte diagonal | aprovado |
| IA e jogador usando o mesmo cálculo | aprovado |
| Defesa contra mapa malformado | aprovado |

Paredes, estruturas, picos/escarpas e perigos naturais são bloqueados pelo
carregador e pelo resolvedor. Unidades voadoras não ignoram bloqueios sólidos ou
abismos. Elevação `M` permanece transitável e preserva as regras anteriores.

## Interface

A aplicação foi aberta e exercitada no navegador local em desktop e em viewport
móvel de 390 × 844.

- 16 regiões e 160 botões de cenário presentes.
- Cinco imagens de arte carregadas localmente.
- Tabuleiro com 96 casas, rótulos acessíveis e legenda visual.
- Seleção de unidade exibiu 15 destinos legais no cenário inicial.
- Nenhum destino legal coincidiu com casa intransponível.
- Clique numa estrutura retornou “estrutura intransponível” sem mover a unidade.
- Zero erro ou aviso no console.
- Zero rolagem horizontal na página em desktop e celular; no celular, o mapa
  possui rolagem interna intencional.

## Conteúdo preservado

- 240 classes de personagem/comandante.
- 144 classes de tropa, atendendo ao alvo aproximado de 140.
- 16 regiões, 160 cenários, 5 condições de vitória e IA determinística.
- Ativação alternada, movimento + ação, reação, CAP, CMD e modos
  ATAQUE/DEFESA/LIVRE sem alteração de regra.

## Critério final

Aprovado para playtest humano estruturado como edição visual/navegação 2.1. A
validação não afirma balanceamento comercial final; afirma coerência das regras,
geometria conectada, colisão defensiva, interface responsiva e execução terminal
de toda a campanha entregue.
