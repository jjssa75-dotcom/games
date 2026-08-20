# IA Tática de NPCs e Inimigos v_1

## Princípio

A IA usa as mesmas informações e as mesmas ações legais do jogador. Ela não
teleporta, não ignora bloqueios, não recebe ações extras e não altera resultados
do RNG. O controlador serve tanto para inimigos quanto para NPCs aliados.

## Processo decisório

1. Reúne todas as unidades vivas ainda não ativadas do lado controlado.
2. Gera ataques, movimentos, mudanças de modo, comandos e habilidades possíveis.
3. Elimina opções rejeitadas pelo `ActionResolver`.
4. Simula cada opção com `preview`, sem consumir RNG ou alterar o estado.
5. Pontua o estado resultante e executa a melhor opção.

## Critérios

- vitória e eliminação do comandante têm prioridade máxima;
- dano causado vale mais que aproximação sem propósito;
- dano recebido em reação é penalizado;
- unidades ofensivas reduzem distância e buscam ruptura;
- defensores e suportes preservam proximidade do comandante;
- comandos recebem valor proporcional às tropas afetadas;
- lanceiros preparam reação quando cavalaria se aproxima;
- Investida e Escaramuça entram no conjunto de decisões;
- modos são alinhados ao papel da unidade;
- desempates são estáveis e reproduzíveis.

## Robustez verificada

Testes confirmam prioridade por golpe letal no comandante, uso de comando fora
de contato, preparação anti-cavalaria, determinismo e legalidade. Os 12 cenários
foram simulados até vitória ou derrota sem softlock com o planejador ativo.

