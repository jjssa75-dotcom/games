# Relatório de Validação v_1

## Resultado

- 37 testes automatizados aprovados.
- 240/240 classes convertidas em comandantes jogáveis.
- 144/144 tropas convertidas em unidades jogáveis.
- 12/12 cenários simulados até vitória ou derrota, sem softlock.
- 11 arquivos JSON analisados estruturalmente.
- JavaScript validado sintaticamente.
- Módulos Python compilados.
- Interface e API local responderam com HTTP 200.
- Seleção de classe/tropa confirmada dentro da batalha.
- Virada de rodada com iniciativa inimiga confirmada.

## QA de exploits

Foram cobertos: ativação dupla, ação fora do turno, fogo amigo, movimento fora do
mapa, atravessar bloqueios, casa ocupada, CMD negativo, CAP excedido, comando em
inimigo, comando fora do alcance, alvos duplicados, reação repetida, Investida
sem distância, RNG alterado por ação inválida e ações após o fim da batalha.

## IA

Foram validados golpe letal prioritário no comandante, comandos sobre formação,
preparação de lança contra cavalaria, legalidade, determinismo e encerramento
dos 12 cenários com o planejador tático ativo.
