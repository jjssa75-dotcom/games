# Relatório de Validação v_2 — Asterra: As Dezesseis Fraturas

Data: 20 de agosto de 2026  
Versão avaliada: 2.0.0

## Resultado executivo

A edição 2.0.0 foi aprovada como protótipo tático local e campanha executável. A validação automatizada final concluiu 46 testes sem falhas em 153,022 segundos. A matriz completa de 160 cenários também foi simulada até estado terminal, cobrindo vitória e derrota sem softlocks conhecidos.

## Correções críticas de design

- Movimento deixou de encerrar a ativação. A unidade pode mover uma vez e depois atacar, usar habilidade, emitir comando, mudar modo ou encerrar voluntariamente.
- `current_actor_id` impede trocar de unidade depois de mover e elimina ativação dupla disfarçada.
- A ação principal encerra a ativação e alterna o lado, removendo alpha strike de formação.
- CAP limita composição; CMD paga ordens e nunca se converte em tropa ou pontos de formação.
- Reação é limitada a uma por rodada e não dispara outra reação.
- Controle, escolta, sobrevivência, interceptação e derrota de comandante são condições resolvidas pelo núcleo, não apenas texto de missão.
- Terreno passou a alterar custo de caminho, cobertura, elevação e impacto de Investida.

## Evidência automatizada

| Área | Resultado |
|---|---:|
| Testes automatizados | 46/46 aprovados |
| Cenários simulados até estado terminal | 160/160 |
| Regiões e estágios | 16 × 10 |
| Condições de vitória | 5, com 32 cenários cada |
| Famílias inimigas usadas | 16/16 |
| Classes de personagem validadas | 240 |
| Classes de tropa validadas | 144 |
| Arquivos JSON analisados | 15/15 |

Os testes cobrem ativação alternada, movimento seguido de ação, bloqueio de segundo movimento e troca de ator, CAP, CMD, alcance, vínculo de comando, alvos duplicados, fogo amigo, RNG sem mutação no preview, reações, Investida, terreno, ocupação, morte de comandante e todos os objetivos da campanha.

## IA de NPCs e inimigos

A IA usa o mesmo `ActionResolver` do jogador e não possui regras paralelas. Ela gera ações legais, usa preview sem mutar estado, pontua vitória, baixa, dano, reação, função tática, terreno e objetivo, e decide com desempate determinístico.

- Interceptação: o mensageiro busca a saída e perseguidores fecham rota.
- Controle: unidades priorizam disputar ou consolidar o ponto.
- Escolta: a IA identifica e pressiona a unidade de missão.
- Combate: golpe letal e vitória superam preferências de postura.
- Performance: destinos alcançáveis são podados para até 16 opções estratégicas por ator sem ignorar custo de caminho.

## Interface e execução

- Interface HTTP local aberta e exercitada no navegador.
- Fluxo verificado: selecionar unidade, mover, encerrar ativação e receber resposta da IA.
- Campanha exibiu 16 regiões e 160 cartões de missão.
- Códice exibiu 240 classes e 144 tropas.
- Missão de escolta carregou mapa, unidades, saída e objetivo corretos.
- JavaScript carregou sem erros ou avisos de console.
- Layout desktop (1280 px) e móvel (390 × 844) sem rolagem horizontal.

## Documento e rastreabilidade

O Documento Mestre v_3 foi renderizado em 39 páginas e revisado visualmente página por página. Não foram encontrados cortes, sobreposições ou tabelas partidas de modo impróprio. Dados executáveis permanecem versionados em JSON; decisões e alterações estão registradas nos documentos de arquitetura, IA, campanha e rastreabilidade.

## Limites conscientes

As 240 classes e 144 tropas são um catálogo jogável e extensível, mas o balanceamento fino continua ancorado no vertical slice de seis comandantes e oito tropas. Persistência de metaprogressão, economia de campanha, linha de visão, névoa e destruição de cenário não foram inventadas além do GDD. Esses sistemas só devem avançar depois de telemetria real de duração de rodada, variedade de formação e taxa de intervenção manual.

## Critério final

Protótipo e campanha aprovados para playtest humano estruturado. A entrega não afirma balanceamento comercial final; afirma regras coerentes, campanha completa em dados, interface funcional, IA determinística e ausência de falhas conhecidas na matriz de invariantes entregue.
