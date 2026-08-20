# Asterra: As Dezesseis Fraturas

RPG tático executável, orientado a dados, com campanha, IA adversária, mapas,
história e códice completo.

## Jogar no Windows

1. Execute `JOGAR.bat`.
2. Abra `http://127.0.0.1:8765` se o navegador não abrir automaticamente.

O iniciador procura `py`, `python` e, dentro do Codex desktop, o runtime Python
integrado. Em outro computador sem Python, instale Python 3.11 ou superior.

Alternativa no terminal:

```powershell
python -m tactical_rpg.web
```

O jogo possui quatro áreas: Batalha, Campanha, Códice e Mundo. No Códice é
possível escolher qualquer classe de personagem e duas classes de tropa; a
formação escolhida pode ser usada em qualquer cenário.

## Usar em outro computador

1. Baixe `releases/Asterra_As_Dezesseis_Fraturas_v_2_2_1.zip` neste repositório.
2. Extraia todo o ZIP para uma pasta comum, sem executar o jogo dentro do arquivo compactado.
3. Execute `JOGAR.bat`. O jogo abrirá em `http://127.0.0.1:8765`.
4. Se Python não estiver instalado, instale Python 3.11 ou superior.

O Documento Mestre consolidado está em `docs/Documento_Mestre_RPG_Tatico_v_4.docx`.

## Conteúdo entregue

- 240 classes de personagens/comandantes: 16 famílias × 15 nós, em cinco tiers;
- 144 classes de tropas (o alvo solicitado de aproximadamente 140): 16 famílias
  × 9 tropas, em três tiers;
- 16 regiões, 32 personagens centrais e direção visual por cultura;
- 160 cenários/mapas: 16 regiões × 10 estágios, organizados em quatro atos;
- todas as 240 classes e 144 tropas selecionáveis e convertidas em definições
  jogáveis pelo motor;
- ativação alternada por unidade com movimento + ação, reação, CAP, CMD, modos
  ATAQUE/DEFESA/LIVRE, terreno ponderado e cinco condições de vitória;
- Investida, Preparar Lança, Escaramuça e resposta anti-cavalaria;
- IA tática para inimigos e NPCs, com geração de ações legais, avaliação de
  dano, eliminação, posição, proteção, objetivos, terreno, comandos e habilidades;
- direção visual v_2 com arte autoral de comandantes e quatro atos, tabuleiro
  texturizado, fichas de unidade legíveis e interface responsiva;
- mapas v_3 com paredes, estruturas, picos, escarpas, abismos, lava e água
  profunda explicitamente intransponíveis; encostas `M` continuam transitáveis;
- destinos legais destacados a partir do mesmo cálculo de caminho usado pelo
  motor e pela IA, sem regras duplicadas na interface;
- matriz de level design com bioma, inimigos das 16 famílias, objetivo, soft
  counter e respostas sugeridas para cada um dos 160 estágios;
- campanha narrativa v_3 com contexto histórico, continuidade, diálogos antes e
  depois da batalha, dilemas, revelações e Marcas Políticas em todos os estágios;
- seis Marcas Políticas persistentes no contrato de dados e três desfechos
  documentados, sem alterar as regras táticas validadas.

## Testes

```powershell
python -m unittest discover -s tests -v
```

Os testes cobrem regras, exploits, árvores, contagens, referências, geometria,
objetivos, terreno, conversão das 384 opções em conteúdo jogável, integração da
IA, conectividade dos 160 mapas, bloqueio defensivo de terreno e simulação
terminal dos 160 cenários.

## Estrutura

- `tactical_rpg/`: motor, modelos, resolvedor e servidor local;
- `web/`: interface responsiva;
- `data/`: classes, tropas, campanha, personagens, mapas e regiões;
- `docs/`: GDD implementado, história, arte, arquitetura e rastreabilidade;
- `tools/build_content.py`: geração determinística dos catálogos;
- `tests/`: suíte automatizada.

As versões anteriores do vertical slice, campanha, mundo e mapas foram
preservados para rastreabilidade. A definição executável é
`data/vertical_slice_v_3.json`, a campanha ativa é v_3, o mundo narrativo é v_2,
os mapas ativos são `data/mapas_v_3.json` e a edição do jogo é `2.2.1`.

