# Campanha e Level Design v_2 — 16 Regiões / 160 Estágios

Este documento é a leitura humana da matriz executável em `data/cenarios_v_2.json`. Cada linha abaixo possui mapa próprio, composição inimiga, condição de vitória e soft counter; o JSON acrescenta premissa, limite de rodadas, recompensas, direção visual e referências completas.

## Gramática de progressão

Cada região ensina e depois combina dez problemas: patrulha, controle curto, escolta, sobrevivência, interceptação, controle prolongado, desgaste, escolta sob foco, perseguição e chefe. Soft counters nunca proíbem uma formação: eles alteram custo, rota e risco, preservando vitória por execução superior.

Terreno difícil (`F`, `M`, `~`) custa movimento adicional salvo afinidade cultural; floresta concede cobertura contra disparos, elevação melhora pressão ofensiva e floresta/água reduzem o impacto de Investida. `O` marca controle e `E`, saída de escolta/interceptação.

## Região 1 — Reinos da Coroa Partida

Bioma: planícies, fortalezas e estradas. Identidade: disciplina, adaptabilidade e comando. Conflito: a Fratura distorce formações coordenadas.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | A Estrada Sem Bandeira | Humanos + Elfos Silvestres | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Pedágio de Sangue | Humanos + Anões | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | O Estandarte Perdido | Humanos + Umbrais | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Sete Sinos de Alarme | Humanos + Nascidos da Chama | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Correio da Convergência | Humanos + Dracônicos | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Praça dos Juramentos | Humanos + Humanos | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | A Noite das Muralhas | Humanos + Goblins | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | A Última Caravana | Humanos + Luminares | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Regente em Fuga | Humanos + Povos das Marés | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Coroa Partida | Humanos + Avarianos | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 2 — Bosque de Lythara

Bioma: florestas antigas e passarelas vivas. Identidade: precisão, floresta e mobilidade. Conflito: a Fratura distorce vantagem em cobertura natural.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Pegadas sob Lythara | Elfos Silvestres + Orcs | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Clareira Disputada | Elfos Silvestres + Arcanos | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Sementes em Marcha | Elfos Silvestres + Necromantes | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | A Caçada da Lua Nova | Elfos Silvestres + Nascidos da Geada | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Flecha entre as Copas | Elfos Silvestres + Povos do Deserto | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | O Círculo Ferido | Elfos Silvestres + Elfos Silvestres | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Chuva de Folhas Negras | Elfos Silvestres + Anões | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | Ponte de Raízes | Elfos Silvestres + Umbrais | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Veado de Vidro | Elfos Silvestres + Nascidos da Chama | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Coração do Bosque | Elfos Silvestres + Dracônicos | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 3 — Terras Rubras

Bioma: estepes, cânions e arenas. Identidade: ímpeto, moral ofensiva e força. Conflito: a Fratura distorce ímpeto após avançar.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Poeira de Khar-Dumak | Orcs + Goblins | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Arena dos Três Clãs | Orcs + Luminares | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | A Marcha do Ferreiro | Orcs + Povos das Marés | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Tambores no Cânion | Orcs + Avarianos | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | O Porta-Voz Capturado | Orcs + Clãs Bestiais | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Desfiladeiro das Presas | Orcs + Orcs | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Cerco da Lua Rubra | Orcs + Arcanos | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | A Coluna Sem-Clã | Orcs + Necromantes | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Caçada ao Estandarte | Orcs + Nascidos da Geada | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Juramento da Horda | Orcs + Povos do Deserto | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 4 — Liga das Engrenagens

Bioma: pântanos, sucata e túneis. Identidade: número, engenho e oportunismo. Conflito: a Fratura distorce baixo CAP e reposicionamento.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Parafusos na Lama | Goblins + Anões | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Pátio das Caldeiras | Goblins + Umbrais | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Comboio de Sucata | Goblins + Nascidos da Chama | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Fumaça no Túnel | Goblins + Dracônicos | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | O Mapa Roubado | Goblins + Humanos | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Trinco-Fundo | Goblins + Goblins | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Pântano Eletrizado | Goblins + Luminares | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | A Bomba Ambulante | Goblins + Povos das Marés | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Lobo Mensageiro | Goblins + Avarianos | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Rei das Engrenagens | Goblins + Clãs Bestiais | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 5 — Montanhas de Karad

Bioma: montanhas, salões e minas. Identidade: armadura, engenharia e resistência. Conflito: a Fratura distorce bloqueio e ruptura.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Portões de Karad | Anões + Arcanos | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Trilhos da Mina | Anões + Necromantes | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | O Engenheiro Ferido | Anões + Nascidos da Geada | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Colapso no Salão | Anões + Povos do Deserto | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Runas Contrabandeadas | Anões + Elfos Silvestres | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Forja-Mãe | Anões + Anões | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | A Ponte dos Martelos | Anões + Umbrais | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | Êxodo do Poço Nove | Anões + Nascidos da Chama | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Trem de Cerco | Anões + Dracônicos | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Trono de Granito | Anões + Humanos | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 6 — Círculo de Aether

Bioma: ilhas flutuantes e observatórios. Identidade: mana, manipulação e conhecimento. Conflito: a Fratura distorce flexibilidade mágica.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Escada para o Aether | Arcanos + Luminares | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Observatório Quebrado | Arcanos + Povos das Marés | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | O Aprendiz Instável | Arcanos + Avarianos | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Minutos Roubados | Arcanos + Clãs Bestiais | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | A Chave de Septúria | Arcanos + Orcs | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Sete Círculos | Arcanos + Arcanos | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Queda sem Chão | Arcanos + Necromantes | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | O Prisma Errante | Arcanos + Nascidos da Geada | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Fuga pelo Impossível | Arcanos + Povos do Deserto | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | A Torre que se Repete | Arcanos + Elfos Silvestres | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 7 — Domínios da Aurora

Bioma: vales solares e basílicas. Identidade: proteção, cura e convicção. Conflito: a Fratura distorce proteção e recuperação.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Peregrinos da Aurora | Luminares + Umbrais | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Adro em Disputa | Luminares + Nascidos da Chama | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Procissão sob Flechas | Luminares + Dracônicos | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Vigília dos Sete Sóis | Luminares + Humanos | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | O Falso Prelado | Luminares + Goblins | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Nave da Basílica | Luminares + Luminares | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Noite sem Milagres | Luminares + Povos das Marés | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | Relicário em Marcha | Luminares + Avarianos | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Inquisidor Fugitivo | Luminares + Clãs Bestiais | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Julgamento de Helianto | Luminares + Orcs | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 8 — Véu de Nox

Bioma: charnecas, ruínas e névoa. Identidade: furtividade, medo e maldições. Conflito: a Fratura distorce debilitação e emboscada.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Névoa sobre Nox | Umbrais + Necromantes | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Pátio sem Sombras | Umbrais + Nascidos da Geada | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | A Testemunha Velada | Umbrais + Povos do Deserto | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Sussurros até o Amanhecer | Umbrais + Elfos Silvestres | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Máscara em Fuga | Umbrais + Anões | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Umbracorte | Umbrais + Umbrais | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Medo na Charneca | Umbrais + Nascidos da Chama | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | Lanterna dos Condenados | Umbrais + Dracônicos | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Assassino sem Rosto | Umbrais + Humanos | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Rasgar o Véu | Umbrais + Goblins | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 9 — Ossuário de Morvath

Bioma: cemitérios, salinas e criptas. Identidade: controle de mortos e desgaste. Conflito: a Fratura distorce invocações temporárias.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Sinos do Ossuário | Necromantes + Povos das Marés | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Salão das Lápides | Necromantes + Avarianos | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | O Coveiro Vivo | Necromantes + Clãs Bestiais | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Seis Turnos até a Lua | Necromantes + Orcs | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Filactério Roubado | Necromantes + Arcanos | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Necrópole Cinzenta | Necromantes + Necromantes | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Maré de Ossos | Necromantes + Nascidos da Geada | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | A Última Pira | Necromantes + Povos do Deserto | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Arauto sem Pulso | Necromantes + Elfos Silvestres | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Portões de Morvath | Necromantes + Anões | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 10 — Arquipélago de Nymar

Bioma: ilhas, recifes e canais. Identidade: fluxo, cura e terreno molhado. Conflito: a Fratura distorce adaptação anfíbia.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Maré de Chegada | Povos das Marés + Nascidos da Chama | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Recife Partido | Povos das Marés + Dracônicos | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Barca dos Curadores | Povos das Marés + Humanos | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Olho da Tormenta | Povos das Marés + Goblins | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Corsário do Coral | Povos das Marés + Luminares | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Canais de Nymar | Povos das Marés + Povos das Marés | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Cerco na Maré Baixa | Povos das Marés + Avarianos | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | O Farol Flutuante | Povos das Marés + Clãs Bestiais | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Leviatã em Retirada | Povos das Marés + Orcs | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Trono Abissal | Povos das Marés + Arcanos | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 11 — Caldeira de Pyr

Bioma: vulcões, cinza e fundições. Identidade: pressão, queimadura e risco. Conflito: a Fratura distorce dano crescente por queimadura.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Cinzas na Estrada | Nascidos da Chama + Nascidos da Geada | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Pátio da Fundição | Nascidos da Chama + Povos do Deserto | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Caravana de Água | Nascidos da Chama + Elfos Silvestres | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Até a Lava Subir | Nascidos da Chama + Anões | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | O Portador da Brasa | Nascidos da Chama + Umbrais | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Cinerária | Nascidos da Chama + Nascidos da Chama | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Chuva Incandescente | Nascidos da Chama + Dracônicos | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | O Coração Refrigerado | Nascidos da Chama + Humanos | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Salamandra em Fuga | Nascidos da Chama + Goblins | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Boca da Caldeira | Nascidos da Chama + Luminares | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 12 — Coroa Invernal

Bioma: geleiras, fiordes e cavernas. Identidade: controle, defesa e lentidão. Conflito: a Fratura distorce controle de movimento.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Primeiro Gelo | Nascidos da Geada + Avarianos | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Fiorde Disputado | Nascidos da Geada + Clãs Bestiais | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Trenó dos Feridos | Nascidos da Geada + Orcs | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | A Longa Noite | Nascidos da Geada + Arcanos | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Batedor na Nevasca | Nascidos da Geada + Necromantes | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Muralhas de Skeld | Nascidos da Geada + Nascidos da Geada | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Lago que se Parte | Nascidos da Geada + Povos do Deserto | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | A Chama Escoltada | Nascidos da Geada + Elfos Silvestres | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | O Jarl em Retirada | Nascidos da Geada + Anões | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Coroa Invernal | Nascidos da Geada + Umbrais | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 13 — Picos de Avar

Bioma: picos, pontes e correntes aéreas. Identidade: voo, ângulo e resgate. Conflito: a Fratura distorce mobilidade aérea limitada pelo mapa.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Sombra sobre Avar | Avarianos + Dracônicos | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Plataforma dos Ventos | Avarianos + Humanos | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Resgate no Abismo | Avarianos + Goblins | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Olho do Furacão | Avarianos + Luminares | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Mensageiro do Zênite | Avarianos + Povos das Marés | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Pontes do Ninho | Avarianos + Avarianos | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Céu Fechado | Avarianos + Clãs Bestiais | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | Ovo Solar | Avarianos + Orcs | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Garra em Fuga | Avarianos + Arcanos | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Batalha do Firmamento | Avarianos + Necromantes | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 14 — Escamas Ancestrais

Bioma: mesetas, vulcões e templos. Identidade: poder, presença e herança elemental. Conflito: a Fratura distorce alto poder e alto CAP.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Escamas na Meseta | Dracônicos + Povos do Deserto | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Templo das Garras | Dracônicos + Elfos Silvestres | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | O Herdeiro Ferido | Dracônicos + Anões | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Sopro sobre o Vale | Dracônicos + Umbrais | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Arauto Ancestral | Dracônicos + Nascidos da Chama | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Drak-Azur | Dracônicos + Dracônicos | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Chuva de Brasas | Dracônicos + Humanos | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | O Ovo Primordial | Dracônicos + Goblins | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Sarthax em Fuga | Dracônicos + Luminares | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Despertar do Primeiro | Dracônicos + Povos das Marés | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 15 — Mar de Safira

Bioma: dunas, oásis e cânions. Identidade: mobilidade, atrito e sobrevivência. Conflito: a Fratura distorce ignora parte do atrito do terreno.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Pegadas de Safira | Povos do Deserto + Clãs Bestiais | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Oásis Disputado | Povos do Deserto + Orcs | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | Caravana das Miragens | Povos do Deserto + Arcanos | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Sol do Meio-Dia | Povos do Deserto + Necromantes | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Vizir entre as Dunas | Povos do Deserto + Nascidos da Geada | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Qasr-Sahir | Povos do Deserto + Povos do Deserto | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Tempestade de Vidro | Povos do Deserto + Elfos Silvestres | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | A Fonte Nômade | Povos do Deserto + Anões | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Falcão em Fuga | Povos do Deserto + Umbrais | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Horizonte Velado | Povos do Deserto + Nascidos da Chama | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Região 16 — Fronteira Primeva

Bioma: selvas, savanas e cavernas. Identidade: instinto, sentidos e transformação. Conflito: a Fratura distorce sentidos e ataques naturais.

| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |
|---:|---|---|---|---|---|
| 1 | Rastros Primevos | Clãs Bestiais + Humanos | Derrotar comandante — romper a patrulha e derrotar o comandante inimigo | avanço frontal sem reconhecimento | distancia + mobilidade |
| 2 | Círculo dos Totens | Clãs Bestiais + Goblins | Controlar área — controlar o marco central por 2 rodadas consecutivas | formação imóvel no objetivo | defesa + mobilidade |
| 3 | A Alcateia Ferida | Clãs Bestiais + Luminares | Escoltar — escoltar a segunda tropa até a saída E | escolta isolada ou toda a força agrupada | suporte + controle |
| 4 | Noite dos Predadores | Clãs Bestiais + Povos das Marés | Sobreviver — manter o comandante vivo por 6 rodadas | gastar reações e CMD cedo demais | defesa + suporte |
| 5 | Caçador Marcado | Clãs Bestiais + Avarianos | Interceptar — interceptar a segunda tropa inimiga antes que alcance E | tropas pesadas sem cobertura de alcance | mobilidade + distancia |
| 6 | Pedra-Uivo | Clãs Bestiais + Clãs Bestiais | Controlar área — controlar o marco avançado por 3 rodadas consecutivas | depender apenas de defensores pesados | controle + ruptura |
| 7 | Selva sem Pássaros | Clãs Bestiais + Orcs | Sobreviver — resistir por 7 rodadas sem perder o comandante | uma única muralha estática | controle + suporte |
| 8 | O Totem Errante | Clãs Bestiais + Arcanos | Escoltar — levar a segunda tropa ao refúgio E | deixar a unidade de missão na vanguarda | defesa + mobilidade |
| 9 | Alfa em Fuga | Clãs Bestiais + Necromantes | Interceptar — eliminar o mensageiro inimigo antes da saída E | focar o comandante e ignorar a missão | ruptura + mobilidade |
| 10 | Rugido da Fratura | Clãs Bestiais + Nascidos da Geada | Derrotar comandante — derrotar o rival regional e selar a Fratura | solução monofunção e alpha strike | defesa + ruptura + suporte |

Fecho regional: o chefe é resistente, mas seus flancos e CMD continuam vulneráveis

## Critérios de aceite

- Exatamente 16 regiões e 10 estágios por região.
- As 16 famílias aparecem como inimigas; cada região combina força local e força de incursão.
- As cinco condições de vitória aparecem 32 vezes cada.
- Todo estágio declara plano inimigo, formação punida, ao menos duas respostas e `hard_lock: false`.
- Os 160 cenários são simulados automaticamente até estado terminal para detectar softlocks.
