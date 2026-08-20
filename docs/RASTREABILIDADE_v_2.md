# Rastreabilidade v_2

| Requisito | Evidência de implementação | Evidência de validação |
|---|---|---|
| 16 regiões × 10 estágios | `data/cenarios_v_2.json` | contagem, ordem e agrupamento nos testes de catálogo |
| Biomas, inimigos, vitórias | cenários + `mapas_v_2.json` | referências, geometria, spawns, objetivos e saídas |
| Soft counter | objeto `soft_counter` por estágio | plano, punição, ≥2 respostas, nenhum hard lock |
| 240 classes | `classes_personagens_v_1.json` | unicidade, 15 por família, árvores conectadas |
| Aproximadamente 140 tropas | 144 em `classes_tropas_v_1.json` | unicidade, 9 por família, tiers 1–3 |
| Preparar → posicionar → decidir | `movement_spent`, `action_spent`, `current_actor_id` | mover+agir, bloqueio de ator, movimento duplo e encerramento |
| Sem alpha strike | alternância em `ActionResolver` | ativação dupla, turno inimigo, iniciador alternado |
| CAP separado de CMD | `army.py`, `web.py`, `CommanderState` | composição excedida, gasto/regen/teto de CMD |
| Reações | `reaction_available` | reação única e Preparar Lança |
| Modos | `Mode` + resolução de dano | ações legais e ativação única |
| Objetivos executáveis | estado/resolvedor | controle, sobrevivência, escolta, interceptação e timeout |
| Terreno | custos/tags/cobertura/elevação | caminho difícil, bloqueio, cobertura e Investida |
| IA sólida | `ai.py` | legalidade, determinismo, letal, comando, lança e 160 simulações |
| Interface funcional | `web/` + API local | sintaxe JavaScript, HTTP, ação jogador→IA e inspeção visual |
| Decisões técnicas | GDD e `DECISOES_TECNICAS_v_3.md` | versões preservadas e manifest v_2 |

O documento completo dos 160 estágios é `CAMPANHA_E_LEVEL_DESIGN_v_2.md`. O relatório de execução e os comandos usados estão em `RELATORIO_VALIDACAO_v_2.md`.
