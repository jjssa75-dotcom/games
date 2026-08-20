# Rastreabilidade v_3 — Edição 2.1.0

| Solicitação | Implementação | Evidência |
|---|---|---|
| Preservar regras | Nenhum sistema de turno/economia/objetivo alterado | `tests/test_invariants.py` |
| Melhorar personagens | Arte de seis comandantes, brasões e fichas responsivas | `web/assets/art/asterra-commanders-v1.png`, `web/styles.css` |
| Melhorar cenários e regiões | Quatro paisagens de atos e 16 capas regionais | `web/assets/art/campaign-act-*-v1.png`, `web/app.js` |
| Impedir atravessar muros | `#` e `B` em autoridade central de bloqueios | `tactical_rpg/model.py`, `tactical_rpg/resolver.py` |
| Impedir atravessar picos | Novo `^` intransponível; `M` permanece encosta | `data/mapas_v_3.json` |
| Impedir atravessar riscos | Novo `X` para abismo/lava/água profunda | `data/mapas_v_3.json` |
| Evitar mapa insolúvel | Inserção condicional e prova de conectividade | `tools/build_content.py`, `tests/test_content_catalogs.py` |
| Orientar jogador | Destaque de destinos e custo vindo do servidor | `GameSession.snapshot`, `web/app.js` |
| IA sólida sob nova geometria | IA reutiliza `reachable_positions` | `tactical_rpg/ai.py`, `tests/test_ai.py` |
| Manter catálogo integral | 240 classes e 144 tropas preservadas | `data/release_manifest_v_3.json` |
| Validar campanha | 160 cenários simulados até terminal | `docs/RELATORIO_VALIDACAO_v_3.md` |

## Arquivos versionados

- `mapas_v_1.json` e `mapas_v_2.json`: preservados.
- `mapas_v_3.json`: versão ativa com navegação explícita.
- `DIRECAO_VISUAL_v_1.md`: preservada.
- `DIRECAO_VISUAL_v_2.md`: arte e linguagem visual integradas.
- `release_manifest_v_1.json` e `release_manifest_v_2.json`: preservados.
- `release_manifest_v_3.json`: manifesto da edição 2.1.0.
