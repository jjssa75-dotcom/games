# Decisões Técnicas v_3

## Correções críticas

### Movimento não é ativação inteira

A v_1 executável marcava `activated = true` depois de qualquer ação. Isso destruía o loop “posicionar → decidir”. A v_3 de arquitetura introduz `movement_spent`, `action_spent` e `current_actor_id`: mover bloqueia a unidade corrente; uma ação principal ou encerramento explícito entrega a iniciativa.

### Objetivos são regras, não texto

Sobrevivência, controle, escolta e interceptação passaram para `BattleState` e `ActionResolver`. Limites de rodada, progresso e unidades-alvo ficam serializáveis e verificáveis. Matar o comandante permanece saída terminal universal.

### Terreno é data

O mapa injeta um dicionário de terreno no estado. Movimento usa custo ponderado; cobertura, elevação, Investida e afinidades consultam símbolos/tags. Nenhuma regra depende do nome de uma região.

### Campanha gerada e auditável

`tools/build_content.py` produz deterministicamente os JSON v_2 e a matriz humana de 160 estágios. Os v_1 foram preservados. IDs incluem região e ordem local, evitando dependência de índice global na interface.

## Limites deliberados

- Moral possui estado e comandos, mas sua consequência sistêmica continua protótipo; não foi inventada uma árvore paralela.
- Não foram criadas 240 habilidades exclusivas. O catálogo completo é jogável por conversão de stats/papéis, enquanto o conjunto mecânico permanece pequeno e testável.
- Não há metaprogressão persistente nem economia de campanha nesta etapa; recompensas são dados preparados para a próxima camada.
- Terreno usa três efeitos legíveis. Linha de visão, névoa e destruição de cenário permanecem fora para evitar sistemas sem prova de diversão.

## Versionamento

- Conteúdo legado: `*_v_1.json`.
- Campanha executável: `campanha_v_2.json`, `cenarios_v_2.json`, `mapas_v_2.json`.
- Catálogo-base: `vertical_slice_v_3.json`.
- Edição integrada: `2.0.0`.
