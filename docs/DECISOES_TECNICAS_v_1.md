# Decisões Técnicas v_1

## Arquitetura

- `Definition` é imutável e carregada de JSON; `State` é uma instância mutável.
- `ActionResolver` é a única autoridade de regras. `preview` e `apply` percorrem
  a mesma lógica, eliminando divergência entre interface, IA e combate.
- O resolvedor devolve cópia do estado. Uma ação inválida não deixa mutação parcial.
- CAP valida composição antes da batalha; CMD é gasto regenerável em batalha.
- A alternância é por unidade. A unidade ativada não pode agir novamente na rodada.
- Reação é um orçamento independente, restaurado uma vez por rodada.
- RNG tem semente e o preview restaura seu estado; a v_1 é quase determinística,
  mas o contrato já permite aleatoriedade auditável no futuro.

## Versionamento

Dados e documentos carregam `_v_1`. O `schema_version` possibilita migração futura
de saves. Versões novas devem coexistir quando quebrarem schema ou decisão de design.

## Riscos em aberto

Os comandos hoje registram efeitos temporários, mas nem todos os modificadores são
consumidos pelo cálculo; moral, terreno, investida e objetivos precisam de testes de
game feel antes de implementação. A alternância inicial ainda usa lado fixo por
rodada; iniciativa e desempate permanecem decisão posterior do GDD.

