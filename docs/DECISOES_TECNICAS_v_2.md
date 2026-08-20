# Decisões Técnicas v_2

## Mudanças desde a v_1

- Efeitos de comandos agora vêm do JSON como modificadores tipados.
- Movimento, defesa, precisão e moral podem ser afetados sem lógica específica
  por comandante.
- Precisão usa RNG com semente; `preview` preserva o estado do gerador.
- O lado que inicia a rodada alterna explicitamente, inclusive quando os
  destacamentos têm quantidades diferentes de unidades.
- O schema de dados v_2 registra os catálogos futuros sem carregá-los na memória.

## Invariantes

CAP continua sendo validação de composição; CMD continua sendo recurso de batalha.
Uma unidade ativa uma vez por rodada e possui no máximo uma reação. Ações inválidas
são atômicas. Comandos só alcançam tropas vivas ligadas ao emissor.

## Dívida deliberada

Moral já possui estado e comandos, mas suas consequências de baixa Moral ainda
dependem de teste de game feel. `Preparar Lança`, investida, cobertura, terreno e
objetivos continuam como próximos incrementos possíveis, não como sistemas
implicitamente completos.

