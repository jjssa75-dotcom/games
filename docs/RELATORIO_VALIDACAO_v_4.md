# Relatório de Validação v_4 — Asterra: As Dezesseis Fraturas

Data: 20 de agosto de 2026  
Versão avaliada: 2.2.0

## Resultado executivo

A edição 2.2.0 foi aprovada como protótipo tático local com campanha narrativa executável. A suíte concluiu 59 testes sem falhas em 221,689 segundos. Os 160 cenários chegaram a estado terminal sem softlocks conhecidos, e a interface JavaScript passou na validação sintática.

## Cobertura

| Área | Resultado |
|---|---:|
| Testes automatizados | 59/59 |
| Cenários simulados | 160/160 |
| Regiões e estágios | 16 × 10 |
| Classes de personagem | 240 |
| Classes de tropa | 144 |
| Estágios com narrativa completa e única | 160/160 |
| Famílias com lógica político-econômica-territorial | 16/16 |
| Protagonistas e rivais | 32 |
| Marcas Políticas | 6 |
| Finais documentados | 3 |

## Invariantes e exploits

Foram revalidados ativação alternada, bloqueio de ativação dupla e troca de ator, movimento seguido de uma única ação, CAP separado de CMD, CMD não negativo, reação no máximo uma vez por rodada, preview sem mutação, atomicidade de ações inválidas, objetivos determinísticos e autoridade única de movimento. Muros, edifícios, picos, abismos, lava e água profunda permanecem intransponíveis para jogador e IA.

## Narrativa e level design

Os testes exigem continuidade sem lacunas entre os 160 estágios, contexto e diálogos não vazios, dilema, revelação, escolha política, justificativa de terreno/inimigos e soft counter. Também comparam os contratos táticos v_2 e v_3 para impedir que a expansão narrativa altere silenciosamente objetivos, limites ou mapas.

## Documento

O Documento Mestre v_4 foi renderizado em 93 páginas e revisado visualmente página por página. Não foram encontrados cortes, sobreposições, páginas vazias ou tabelas impróprias. O arquivo final possui SHA-256 `C13C1ED53C14B84E2A545B705132AE06E801DD9501EC1F7FC3CFF1EB8DA72765`.

## Limite consciente

O protótipo implementa a rota canônica e expõe as consequências políticas. A persistência integral das bifurcações e dos três finais está especificada, mas deve ser promovida ao runtime apenas após playtest da rota principal. A aprovação não representa balanceamento comercial final nem produção de arte final para centenas de entradas do catálogo.
