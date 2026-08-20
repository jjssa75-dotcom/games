# Direção Visual v_2

## Norte artístico

Asterra combina fantasia tática pictórica, materiais críveis e leitura de jogo
moderna. A imagem deve sugerir um mundo antigo sendo reunido por uma fratura de
luz azul e ouro. O tom é épico e determinado, não grotesco. Azul identifica a
Coalizão, vermelho a Convergência, ouro marca missão/seleção e ciano marca rota
legal.

As regras nunca dependem apenas da cor. Unidades usam brasão e glifo; cobertura
usa copa vegetal; elevação usa estratos; paredes usam alvenaria; estruturas usam
bloco/portal; picos usam triângulos rochosos; abismos e riscos naturais usam
vazio concêntrico. Isso preserva leitura para telas pequenas e diferentes
percepções de cor.

## Arte integrada

As cinco imagens foram geradas no modo de criação original do ImageGen
integrado, sem imagem de referência, texto, logotipo, marca-d'água ou personagem
de propriedade alheia.

| Uso | Arquivo |
|---|---|
| Comandantes e cabeçalho da batalha | `web/assets/art/asterra-commanders-v1.png` |
| Ato I — Coroa, bosque, clãs e engenhos | `web/assets/art/campaign-act-1-v1.png` |
| Ato II — pedra, Aether, Igreja e Umbrais | `web/assets/art/campaign-act-2-v1.png` |
| Ato III — mortos, marés, fogo e gelo | `web/assets/art/campaign-act-3-v1.png` |
| Ato IV — céu, dragões, deserto e origem | `web/assets/art/campaign-act-4-v1.png` |

## Conjunto final de prompts

### Comandantes

Arte-chave widescreen 16:9 original para Asterra, RPG tático de fantasia sobre
dezesseis culturas unidas contra fraturas dimensionais. Seis comandantes com
silhuetas inequívocas — marechal humano, patrulheira élfica, estrategista orc,
engenheiro anão, guardiã da Igreja e lâmina umbral — em campo antigo fraturado;
florestas, picos, deserto e catedral ao fundo; pintura conceitual premium,
realismo estilizado, aço/couro/pedra críveis, sombras azul-marinho e recorte
dourado de amanhecer, espaço atmosférico para sobreposição de UI; sem texto,
logos, marcas-d'água, gore, rostos ou membros duplicados.

### Ato I

Paisagem de campanha 16:9 original conectando fortaleza da Coroa, floresta viva,
cânions orcs e pântanos goblins. Estradas, pontes e portões deixam as rotas
seguras legíveis; muralhas, penhascos e vegetação densa deixam bloqueios claros.
Pintura de fantasia tática premium, azul aço, verde musgo, vermelho óxido e
cobre, luz dramática contida; sem personagens em primeiro plano, texto ou UI.

### Ato II

Paisagem de campanha 16:9 original com salões anões, observatórios arcanos
flutuantes, basílica radiante e charneca umbral. Portões, pontes e escadarias
marcam rotas; picos, vãos e paredes marcam áreas impossíveis. Pintura conceitual
sofisticada, granito/bronze, violeta/ciano, marfim/ouro e índigo; sem texto,
logotipos ou UI.

### Ato III

Paisagem de campanha 16:9 original reunindo costa de ossuários, arquipélago de
coral, forja vulcânica e fiordes de gelo. Caminhos, cais e pontes seguros são
claros contra água profunda, lava, muros e escarpas. Fantasia pictórica premium,
atmosfera de cerco, verde espectral, turquesa, laranja de forja e azul glacial;
sem texto, logotipos ou UI.

### Ato IV

Paisagem de campanha 16:9 original com picos celestes, mesas dracônicas, deserto
de safira e fronteira primeva. Passos, trilhas e pontes formam rotas legíveis;
picos, abismos e muralhas naturais são visualmente intransponíveis. Pintura
conceitual épica de fantasia, vento e luz de fim de mundo, azul celeste, bronze,
safira e verde ancestral; sem texto, logotipos ou UI.

## Aplicação na interface

- Cabeçalho de missão usa a arte dos comandantes com gradiente de contraste.
- Cada quatro regiões compartilham a paisagem do ato, preservando unidade sem
  fingir que existem 160 ilustrações únicas.
- Códice e fichas usam brasões gerados por CSS para escalar às 240 classes e 144
  tropas sem custo de memória por retrato individual.
- `prefers-reduced-motion` desliga pulsos e transições.
- A interface não depende de serviços externos e funciona offline.
