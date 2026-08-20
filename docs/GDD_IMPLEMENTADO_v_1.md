# GDD Implementado v_1 — Asterra

## Visão

Asterra é um RPG tático sobre uma coalizão de dezesseis povos. A campanha
combina escolha de formação, combate em grade, especialização cultural e uma
história em que nenhuma doutrina isolada consegue estabilizar o mundo.

## Core loop

1. Consultar a campanha e o conflito regional.
2. Escolher uma das 240 classes de comandante e duas das 144 tropas.
3. Entrar em um mapa com obstáculos, cobertura temática e objetivo.
4. Alternar ativações com a IA, usando movimento, ataque, modo ou comando.
5. Derrotar o comandante inimigo e avançar ao cenário seguinte.
6. Revisar o Códice e experimentar outra formação.

## Combate

- Grade ortogonal e movimento calculado por caminho, sem atravessar bloqueios.
- Uma ativação por unidade a cada rodada; o iniciador da rodada alterna.
- Uma reação por unidade por rodada.
- ATAQUE aumenta pressão; DEFESA aumenta mitigação; LIVRE mantém neutralidade.
- CAP mede composição; CMD é recurso regenerável para ordens.
- `ActionResolver` é a única autoridade de validação, preview e aplicação.
- RNG tem semente e é restaurado quando uma ação falha.
- A batalha termina ao derrotar o comandante adversário.

## Conteúdo sistêmico

Cada classe possui família, tier, pai, papel, identidade, assinatura, crescimento
e direção visual. Cada tropa possui stats, CAP, custos, função, fraqueza, modo
preferido e assinatura cultural. A interface converte qualquer registro em uma
definição jogável, preservando diferenças de tier e papel.

## Escopo integral

- Personagens: 240 classes, exatamente 15 por família.
- Tropas: 144 classes, atendendo ao alvo aproximado de 140.
- Mundo: 16 regiões e 32 personagens centrais.
- Campanha: 3 atos, 12 cenários e 12 mapas.

