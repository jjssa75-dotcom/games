# GDD Implementado v_2 — Asterra

## Visão e promessa

Asterra é um RPG tático de formação sobre dezesseis culturas que precisam cooperar sem perder identidade. A campanha foi desenhada para invalidar a “formação universal”: cada estágio pressiona uma fraqueza, mas oferece mais de uma resposta e nunca exige uma classe específica.

## Core loop validado

1. Preparar: ler objetivo, terreno, famílias inimigas e soft counter; escolher comandante e duas tropas dentro do CAP.
2. Posicionar: mover uma vez dentro da ativação, pagando custos de terreno.
3. Decidir: atacar, comandar, usar habilidade, mudar modo ou encerrar a ativação.
4. Consequência: resolver acerto, dano, reação e objetivo por uma única autoridade.
5. Resposta: alternar para uma unidade adversária; quando todas agem, inverter o iniciador da rodada.
6. Adaptar: trocar a formação para o próximo problema regional.

Mover não encerra sozinho a ativação. A unidade fica bloqueada como ator corrente e não pode mover duas vezes nem ceder a ação a outra unidade. Ataque, comando, habilidade ou mudança de modo concluem a ativação; “Encerrar ativação” permite desistir da ação principal. Isso preserva “posicionar → decidir” sem abrir alpha strike.

## Economia e invariantes

- CAP/Pontos de Tropa valida a composição antes da batalha; não é consumível.
- CMD é recurso de comando, pago antes do efeito, regenerado com teto e incapaz de ficar negativo.
- Uma unidade possui no máximo um movimento, uma ação principal e uma reação por rodada.
- Uma reação não cria outra reação; unidade derrotada não age.
- Ações inválidas são atômicas e não avançam RNG, turno ou objetivo.
- `preview`, jogador e IA usam o mesmo `ActionResolver`.
- O lado inicial alterna por rodada; unidades excedentes não ganham uma segunda ativação.

O protótipo não possui uma reserva genérica de MP. Quando MP for introduzido, deverá obedecer “gasto antes do efeito”, teto rígido e proibição de uma ação repor mais MP do que consumiu no mesmo ciclo.

## Combate e terreno

- Grade ortogonal, caminho ponderado, bloqueios, ocupação e limites validados.
- `F`, `M` e `~` custam movimento adicional, salvo afinidades culturais declaradas em tags.
- Floresta concede cobertura contra ataques à distância; elevação melhora pressão ofensiva.
- Floresta e água reduzem a força de Investida. Distância mínima de Investida continua obrigatória.
- ATAQUE aumenta pressão, DEFESA aumenta mitigação e LIVRE preserva neutralidade.
- Preparar Lança gasta ação e uma única reação pode interceptar cavalaria.

## Condições de vitória

- `defeat_commander`: eliminar o comandante rival.
- `control_area`: ocupar `O` sem contestação por rodadas consecutivas; contestação zera progresso.
- `escort`: levar a tropa designada a `E` antes do limite; perder a escolta causa derrota.
- `survive`: manter o comandante vivo até completar o limite.
- `intercept`: eliminar a tropa designada antes que alcance `E`.

A queda de um comandante continua terminal em qualquer missão, evitando estados sem cadeia de comando e simplificando leitura.

## Campanha

- 4 atos, 16 regiões e exatamente 10 estágios por região.
- 160 cenários e 160 registros de mapa.
- 32 ocorrências de cada uma das cinco condições de vitória.
- Cada estágio declara bioma, inimigos, objetivo, limite, plano, formação punida, respostas sugeridas, twist, recompensa e direção de arte.
- A matriz humana completa está em `CAMPANHA_E_LEVEL_DESIGN_v_2.md`; a fonte executável é `data/cenarios_v_2.json`.

## Conteúdo e escopo

O códice mantém 240 classes de personagens (16 × 15) e 144 classes de tropas (16 × 9, atendendo “aproximadamente 140”). Todos os registros são selecionáveis e convertidos em definições jogáveis. O vertical slice continua sendo a régua de mecânicas: seis arquétipos de comandante, oito tropas de referência e sete habilidades implementadas. O catálogo amplo não autoriza criar centenas de mecânicas não validadas.

## Critérios de diversão

- Soft counter altera eficiência, não concede imunidade nem trava a formação.
- Objetivos curtos terminam antes que defesa estática vire espera.
- Estágios 1–5 apresentam problemas; 6–9 combinam-nos; 10 testa formação combinada.
- O jogador sempre enxerga objetivo, progresso, CAP, unidade corrente e estado de reação.
- Resultados probabilísticos são limitados a 5–95% e reproduzíveis por semente.
