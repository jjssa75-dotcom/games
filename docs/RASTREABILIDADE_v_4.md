# Rastreabilidade v_4 — Edição 2.2.0

| Solicitação | Implementação | Evidência |
|---|---|---|
| Auditar roteiro e lore | Diagnóstico de ritmo, clichês, causalidade e limites | `docs/AUDITORIA_NARRATIVA_v_1.md` |
| 16 regiões × 10 estágios | 160 arcos contínuos, ligados por quatro atos | `data/cenarios_v_3.json` |
| História justificar batalha | Contexto, terreno, inimigo, objetivo e soft counter por estágio | `docs/HISTORIA_E_CAMPANHA_v_2.md` |
| Diálogos antes/depois | Dois beats pré-batalha e dois pós-batalha por estágio | `data/cenarios_v_3.json` |
| Marcas Políticas | Seis eixos, deltas canônicos, escolhas e três finais | `data/campanha_v_3.json` |
| Facções críveis | Interesses políticos, econômicos e territoriais para 16 famílias | `data/regioes_v_2.json` |
| Personagens e rivais | 32 agentes com posição, interesse, contradição e limite moral | `data/personagens_v_2.json` |
| Preservar regras táticas | Contratos dos 160 cenários comparados com v_2 | `tests/test_narrative_content.py` |
| Preservar catálogo | 240 classes e 144 tropas continuam jogáveis | `data/release_manifest_v_4.json` |
| IA sólida | IA usa o mesmo resolvedor e geometria do jogador | `tactical_rpg/ai.py`, `tests/test_ai.py` |
| Impedir travessia inválida | Muros, edifícios, picos e riscos permanecem bloqueados | `tests/test_tactical_engine.py` |
| Documento consolidado | Documento Mestre v_4, 93 páginas revisadas | `Documento_Mestre_RPG_Tatico_v_4.docx` |

## Contrato de versões

- `cenarios_v_2.json` permanece como baseline tático; `cenarios_v_3.json` adiciona narrativa sem mudar seus contratos.
- `campanha_v_3.json`, `regioes_v_2.json` e `personagens_v_2.json` são as fontes narrativas ativas.
- `mapas_v_3.json` e `vertical_slice_v_3.json` permanecem as fontes táticas ativas.
- `release_manifest_v_4.json` registra a edição 2.2.0.

## Limite deliberado

As escolhas e os três finais possuem contrato de dados e documentação, mas o protótipo executa a rota canônica. Persistência completa de ramificações fica condicionada a playtests e não foi improvisada fora do GDD.
