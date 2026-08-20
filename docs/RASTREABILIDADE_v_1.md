# Rastreabilidade v_1

| Requisito | Implementação | Verificação |
|---|---|---|
| 240 classes | `classes_personagens_v_1.json` | contagem, unicidade e árvores |
| Aproximadamente 140 tropas | 144 em `classes_tropas_v_1.json` | 9 por família |
| Jogo funcional | `tactical_rpg.web` + `web/` | HTTP, ações, IA e testes |
| Definition/State | `model.py` | catálogo imutável |
| ActionResolver | `resolver.py` | preview, aplicação e atomicidade |
| Ativação e reações | `resolver.py` | testes de turno, rodada e limite |
| CAP/CMD e modos | motor + interface | testes de separação e gasto |
| Personagens | `personagens_v_1.json` | 32 registros referenciados |
| Mapas | `mapas_v_1.json` | geometria, spawns e bloqueios |
| História e regiões | JSON + documentos | referências cruzadas |
| IA sólida de NPCs/inimigos | `ai.py` | decisões, determinismo e 12 simulações |

## Alteração de escopo

A estimativa de 160 tropas em documentação anterior foi substituída pela
indicação final de aproximadamente 140. A implementação consolidada usa 144.
Documentos v_1/v_2 anteriores permanecem como histórico.
