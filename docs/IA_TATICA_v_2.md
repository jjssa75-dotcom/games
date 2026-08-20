# IA Tática de NPCs e Inimigos v_2

## Contrato de honestidade

A IA recebe o mesmo estado visível, usa as mesmas ações e passa pelo mesmo `ActionResolver` do jogador. Não teleporta, não ignora terreno, não recebe CAP/CMD/reações extras e não manipula RNG. O planejador serve para inimigos e pode ser reutilizado por NPCs aliados ao trocar o lado controlado.

## Ciclo decisório

1. Se uma unidade já moveu, considerar somente esse ator até concluir a ativação.
2. Gerar ataques, comandos, habilidades, modos, encerramento e até 16 destinos alcançáveis relevantes por ator.
3. Simular cada opção com `preview`, sem mutação nem consumo de RNG.
4. Pontuar vitória, morte, dano líquido após reação, função, proteção e objetivo.
5. Aplicar a melhor ação com desempate determinístico.

O recorte de destinos usa caminho ponderado e afinidades de terreno. Ele elimina centenas de previews inúteis, mas preserva rotas de aproximação, alcance ideal, controle, perseguição da escolta e fuga do alvo de interceptação.

## Prioridades

- vitória/derrota e comandante valem ordens de grandeza acima de dano comum;
- golpe útil recebe bônus para evitar ciclos de postura em contato;
- dano recebido por reação reduz valor de uma troca;
- o alvo de interceptação busca `E`, enquanto perseguidores tentam fechá-lo;
- forças de controle aproximam-se de `O` e forças de escolta pressionam a unidade protegida;
- papéis ofensivos reduzem distância; defensores preservam cadeia de comando;
- lanceiros preparam reação quando cavalaria ameaça;
- comandos consideram custo, alcance e quantidade de tropas afetadas;
- mudar de modo tem valor moderado e nunca supera indefinidamente um ataque produtivo.

## Robustez

A IA é determinística sob a mesma semente. Testes cobrem ação legal, golpe letal, comando, anti-cavalaria, bloqueio do ator após movimento e terminação da campanha. As 160 missões são executadas por um agente de teste até vitória ou derrota para detectar softlocks de iniciativa, caminho e objetivo.
