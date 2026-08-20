from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def write_json(name: str, payload):
    (DATA / name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


PROFILES = {
    "humano": {
        "polity": "Conselho de Regência de Valedouro",
        "governance": "monarquia sem herdeiro reconhecido, administrada por cidades juramentadas e um regente de guerra",
        "economy": "celeiros, estradas, pedágios e crédito militar",
        "resources": ["grão", "cavalos", "pontes", "selos de dívida"],
        "territory": "o corredor central que liga oito rotas continentais",
        "grievance": "as províncias alimentam a guerra, mas a capital decide quem recebe pão e proteção",
        "fracture_stake": "a Fratura corta estradas e descoordena os marcos de comando que mantêm o reino abastecido",
        "coalition_demand": "auditoria pública dos celeiros e voto provincial sobre requisições",
        "convergence_offer": "um único comando capaz de racionar grão e mover exércitos sem veto local",
        "hero_goal": "provar que ordem não exige uma coroa absoluta nem fome administrada",
        "hero_conflict": "Alda precisa usar a máquina logística que condena enquanto tenta democratizá-la",
        "hero_creed": "Nenhuma estrada vale mais que as pessoas que a pavimentaram.",
        "rival_goal": "centralizar o abastecimento antes que a disputa sucessória transforme escassez em guerra civil",
        "rival_conflict": "Cael sabe que sua solução salva cidades no curto prazo e enterra qualquer limite ao poder",
        "rival_creed": "Direitos não alimentam uma cidade quando todos os celeiros queimam.",
        "public_voice": "Mira, intendente dos celeiros livres",
        "blocs": ["províncias juramentadas", "guildas de estrada", "guarda da regência"],
        "betrayal": "O marechal Edran entrega rotas da Coalizão a Cael para impedir que Valedouro seja a próxima cidade sacrificada.",
        "resolution": "Cael aceita depor a coroa de emergência em troca de um conselho logístico vinculante.",
        "beats": [
            ("Patrulhas sem brasão confiscam grão de aldeias já tributadas.", "Romper o bloqueio sem legitimar saques da própria Coalizão.", "Os mandados levam a assinatura do marechal Edran, não de Cael."),
            ("O pedágio central decide qual bairro receberá a última remessa de trigo.", "Controlar o marco e publicar a lista de prioridades, expondo aliados.", "Os anões cobram uma dívida antiga por pontes que nunca foram pagas."),
            ("Um estandarte provincial carrega livros-caixa capazes de provar a fraude sucessória.", "Escoltar a prova ou usar a rota curta e abandonar refugiados.", "O selo real foi duplicado anos antes da primeira Fratura."),
            ("Sete torres tocam alarmes diferentes enquanto tropas de Pyr cercam os armazéns.", "Salvar o celeiro ou a muralha que protege a população.", "Cael contratou Pyr para conter incêndios; Edran redirecionou os contratos."),
            ("Um correio dracônico leva a Edran a ordem que criaria uma coroa de emergência.", "Interceptar o mensageiro vivo ou destruir a prova com ele.", "Cael promete eleições após a crise, mas sem prazo nem fiscalização."),
            ("A Praça dos Juramentos vira tribunal armado entre províncias e regência.", "Reconhecer a autoridade de Cael por uma noite para evitar linchamentos.", "Alda é herdeira legal distante e ocultou o fato para não virar bandeira."),
            ("Mercenários goblins atacam muralhas que a própria Liga construiu.", "Usar explosivos nos bairros externos ou sustentar duas frentes.", "Edran vendeu acesso às muralhas em troca de grão para hospitais."),
            ("A última caravana leva famílias e também oficiais responsáveis pelas requisições.", "Escoltar culpados junto com inocentes ou separar o comboio e perder tempo.", "A Igreja oferece asilo desde que os livros-caixa permaneçam selados."),
            ("Cael foge com um tratado marítimo que pode alimentar Valedouro por uma estação.", "Capturá-lo ou permitir a fuga para que o tratado seja assinado.", "O tratado entrega portos de Nymar como garantia sem consentimento insular."),
            ("A coroação de emergência ocorre sobre a Fratura aberta.", "Derrotar Cael sem destruir o único centro capaz de distribuir grão.", "Cael não abriu a Fratura; ele tentou assumir uma rede já sabotada por Edran."),
        ],
    },
    "elfo": {
        "polity": "Círculo das Copas de Lythara",
        "governance": "assembleia de casas-árvore, guardiões de nascente e comunidades de borda",
        "economy": "madeira viva licenciada, remédios, sementes e controle das bacias d'água",
        "resources": ["madeira viva", "ervas", "sementes", "nascentes"],
        "territory": "a floresta que regula as chuvas das planícies humanas e das estepes orcs",
        "grievance": "tratados de emergência sempre viram estradas permanentes e assentamentos armados",
        "fracture_stake": "raízes perdem memória, nascentes mudam de curso e antigas passarelas atacam invasores e habitantes",
        "coalition_demand": "corredores temporários com retirada verificável e reparação ecológica",
        "convergence_offer": "fechar as bordas, militarizar as copas e decidir sozinho quem recebe água",
        "hero_goal": "salvar a floresta sem tratar famintos e migrantes como uma praga",
        "hero_conflict": "Sylwen protege uma cultura que também apagou comunidades de borda dos mapas",
        "hero_creed": "Uma floresta que só protege os antigos já começou a morrer.",
        "rival_goal": "selar Lythara contra qualquer povo externo até que as nascentes estabilizem",
        "rival_conflict": "Thalan tem razão sobre o dano acumulado e está disposto a condenar milhões a jusante",
        "rival_creed": "Toda concessão temporária deixou uma cicatriz permanente.",
        "public_voice": "Iri, agricultora da borda sem assento no Círculo",
        "blocs": ["casas das copas", "comunidades de borda", "guardiões de nascente"],
        "betrayal": "Sylwen autoriza secretamente uma ponte de raízes para refugiados, quebrando o voto do próprio Círculo.",
        "resolution": "Lythara aceita corredores sazonais governados também pelas comunidades de borda.",
        "beats": [
            ("Pegadas de refugiados são confundidas com a vanguarda de uma invasão orc.", "Desarmar a patrulha antes que o medo se torne massacre.", "Os orcs seguiam a antiga rota de migração reconhecida pelo primeiro tratado."),
            ("A clareira que mede a chuva é ocupada por magos enviados para recalibrá-la.", "Tomar o observatório ou permitir um experimento sem supervisão élfica.", "Os dados arcanos preveem seca humana se Lythara fechar as nascentes."),
            ("Sementes-memória carregam nomes de mortos que necromantes podem testemunhar.", "Escoltar as sementes e admitir que o bosque apagou aldeias de borda.", "As raízes guardam contratos que o Círculo declarou inexistentes."),
            ("A Lua Nova desorienta caçadores enquanto a geada mata brotos.", "Proteger as copas antigas ou os viveiros que alimentam a borda.", "Thalan estocou sementes para sustentar apenas as casas centrais."),
            ("Uma flecha com mapa de aquíferos segue para o Mar de Safira.", "Interceptar o mapa ou honrar o acordo de água com os nômades.", "A seca do deserto foi agravada por desvios élficos centenários."),
            ("O Círculo Ferido divide guardiões e agricultores em torno da nascente.", "Dar voto à borda durante a crise, mudando a constituição sob armas.", "Sylwen descobre que sua casa lucrou com licenças de madeira humana."),
            ("Cinzas negras caem de máquinas anãs colocadas para conter fungos.", "Destruir a maquinaria tóxica ou aceitar a perda de um vale inteiro.", "O fungo é uma defesa do bosque contra o Aether, não simples doença."),
            ("A ponte de raízes precisa levar refugiados umbrais por território sagrado.", "Quebrar o voto do Círculo e tornar o corredor irreversível.", "Os umbrais carregam provas de que Edran vendeu as rotas da Coalizão."),
            ("O Veado de Vidro leva a Pyr um broto capaz de resfriar fundições.", "Capturar o mensageiro ou deixar que milhares de operários sejam salvos.", "Thalan armou a perseguição para transformar cooperação em traição."),
            ("O Coração do Bosque escolhe entre fechar as águas e compartilhar a dor da Fratura.", "Vencer Thalan sem matar a raiz consciente que sustenta sua defesa.", "A Fratura reage melhor a pactos distribuídos que a um único selamento."),
        ],
    },
    "orc": {
        "polity": "Confederação dos Três Clãs Rubros",
        "governance": "assembleias de clã, juramentos públicos e liderança temporária por campanha",
        "economy": "rebanhos, ferro de superfície, cavalos e proteção das rotas de migração",
        "resources": ["cavalos", "ferro rubro", "sal", "corredores de pasto"],
        "territory": "estepes e cânions entre os celeiros humanos e as minas goblins",
        "grievance": "fronteiras desenhadas por sedentários criminalizam migrações mais antigas que seus reinos",
        "fracture_stake": "a Fratura desloca poços e concentra rebanhos, tornando inevitável a disputa entre clãs",
        "coalition_demand": "reconhecimento de corredores e representação por clã, não por fronteira estrangeira",
        "convergence_offer": "um único khan com mapas fixos, poços armados e acesso garantido ao comércio",
        "hero_goal": "unir os clãs sem transformar união em império",
        "hero_conflict": "Gorak ascendeu por um código de força que mantém os sem-clã fora de qualquer proteção",
        "hero_creed": "Juramento sem lugar para o fraco é apenas ameaça bem pronunciada.",
        "rival_goal": "criar um khanato central que ninguém possa expulsar de suas próprias rotas",
        "rival_conflict": "Maug nasceu sem-clã e usa autoritarismo para corrigir uma exclusão real",
        "rival_creed": "Vocês chamam de liberdade o direito dos clãs fortes de nos abandonar.",
        "public_voice": "Asha Sem-Fogo, porta-voz dos sem-clã",
        "blocs": ["clãs de pastoreio", "ferreiros de cânion", "sem-clã"],
        "betrayal": "Gorak entrega um poço ancestral aos sem-clã, violando o juramento que lhe deu comando.",
        "resolution": "o juramento final cria cidadania de corredor e assentos permanentes para os sem-clã.",
        "beats": [
            ("Poeira cobre marcas de fronteira recém-erguidas por contratados goblins.", "Romper a patrulha sem tratar trabalhadores como invasores.", "Os marcos foram pagos por comerciantes humanos que querem cobrar a migração."),
            ("A arena dos três clãs decide posse do último poço com bênção luminar.", "Controlar o círculo e recusar um duelo até a morte.", "A Igreja reconhece apenas clãs com terra fixa, apagando os sem-clã."),
            ("Um ferreiro leva peças de bomba d'água trazidas por marinheiros de Nymar.", "Escoltar tecnologia estrangeira que ameaça o poder dos chefes de poço.", "Maug financiou a máquina antes de aderir à Convergência."),
            ("Tambores no cânion encobrem um ataque aéreo a rebanhos encurralados.", "Defender a coluna civil ou perseguir os avarianos que levam os mapas.", "Avarianos foram pagos por um clã rival, não pela Convergência."),
            ("O porta-voz dos sem-clã é levado por rastreadores bestiais.", "Interceptar o comboio e admitir publicamente a exclusão dos sem-clã.", "A captura foi solicitada pelo próprio conselho de Gorak."),
            ("O desfiladeiro das presas vira fronteira entre velhos clãs e novos cidadãos.", "Entregar um poço ancestral para evitar uma guerra interna.", "A água segue um veio conectado à Fratura de Lythara."),
            ("Magos de Aether sustentam um cerco sob a Lua Rubra.", "Quebrar as torres ou preservar o sistema que mantém os poços abertos.", "Ilyra autorizou as torres antes de conhecer o plano de Maug."),
            ("A coluna sem-clã marcha com ancestrais necromantes como testemunhas.", "Proteger os mortos convocados ou exigir que sejam devolvidos ao repouso.", "Os ancestrais confirmam que o primeiro juramento incluía os sem-clã."),
            ("Um estandarte levado por batedores de geada provaria a legitimidade de Maug.", "Capturar a prova ou reconhecer a parte verdadeira da reivindicação rival.", "Maug descende do quarto clã apagado após uma fome."),
            ("O juramento da Horda ocorre diante de emissários do deserto.", "Derrotar Maug e incorporar sua causa sem premiar seus crimes.", "Maug aceita depor armas se os sem-clã receberem voz constitucional."),
        ],
    },
    "goblin": {
        "polity": "Liga Cooperativa das Engrenagens",
        "governance": "guildas de oficina com votos proporcionais a patentes, produção e risco assumido",
        "economy": "reciclagem, bombas, canais, munição e contratos de manutenção",
        "resources": ["sucata", "turfa", "bombas d'água", "patentes"],
        "territory": "pântanos industriais e túneis que drenam o centro do continente",
        "grievance": "quem cria a máquina raramente possui a patente; dívida técnica virou trabalho hereditário",
        "fracture_stake": "a energia instável torna oficinas vitais e explosivas ao mesmo tempo",
        "coalition_demand": "licenças abertas para tecnologia de sobrevivência e fim da dívida hereditária",
        "convergence_offer": "compras militares garantidas, proteção de patentes e uma diretoria única",
        "hero_goal": "libertar o engenho goblin sem transformar cada descoberta em arma da Coalizão",
        "hero_conflict": "Nix roubou patentes para os trabalhadores e também vendeu projetos perigosos",
        "hero_creed": "Se todos dependem da máquina, todos devem entender quem paga quando ela falha.",
        "rival_goal": "industrializar a Liga rápido o bastante para que ninguém volte a tratá-la como depósito",
        "rival_conflict": "Grizna oferece emprego e dignidade por meio de uma economia de guerra que nunca poderá parar",
        "rival_creed": "Moral é luxo de quem nunca teve a oficina penhorada.",
        "public_voice": "Prego, delegado dos devedores de Trinco-Fundo",
        "blocs": ["donos de patente", "cooperativas de sucata", "devedores de oficina"],
        "betrayal": "Nix vendeu o protótipo da Bomba Ambulante anos antes e tenta ocultar sua assinatura.",
        "resolution": "a Liga converte patentes vitais em bens comuns e limita contratos militares.",
        "beats": [
            ("Parafusos marcados como anões aparecem em bombas usadas para expulsar catadores.", "Desarmar a linha sem destruir provas de trabalho forçado.", "Karad forneceu peças sob um contrato de dívida impagável."),
            ("O pátio das caldeiras é ocupado por devedores e infiltradores umbrais.", "Controlar a energia sem entregar os líderes da greve.", "Dama Vanta comprou informações, mas os devedores agiram por conta própria."),
            ("Um comboio de sucata leva válvulas a Pyr em troca de alimentos.", "Escoltar o comércio apesar de ele alimentar a indústria de guerra.", "Sem as válvulas, os fornos explodem com bairros operários dentro."),
            ("Fumaça aprisiona trabalhadores enquanto mercenários dracônicos guardam saídas.", "Salvar operários ou preservar o protótipo que estabiliza a Fratura.", "Grizna segurou as portas para impedir roubo e causou o cerco."),
            ("O mapa roubado revela todos os túneis de drenagem do continente.", "Capturar o ladrão ou divulgar o mapa para auditoria pública.", "Nix desenhou uma rota secreta usada por Edran."),
            ("Trinco-Fundo elege sua diretoria sob canos pressurizados.", "Dar um voto a cada pessoa ou manter peso técnico para evitar decisões letais.", "A cooperativa de Nix também excluiu trabalhadores sem certificação."),
            ("O pântano eletrizado cerca hospitais luminares ligados às oficinas.", "Desligar a rede e perder bombas d'água ou sustentar o cerco.", "A Igreja aceitou devedores como pacientes, depois reteve suas patentes."),
            ("A Bomba Ambulante é, na verdade, um reator com crianças aprendizes dentro.", "Escoltar o reator para desarme ou evacuá-lo e deixá-lo instável.", "A assinatura original do projeto é de Nix."),
            ("Um lobo avariano leva contratos de compra para a Convergência.", "Interceptar os contratos e arriscar o desemprego de milhares.", "Grizna prometeu guerra permanente para quitar todas as dívidas."),
            ("O Rei das Engrenagens opera uma fábrica que mantém o pântano habitável.", "Derrubar Grizna sem parar as bombas e afogar Trinco-Fundo.", "Grizna aceita abrir as patentes, mas exige imunidade para os diretores."),
        ],
    },
    "anao": {
        "polity": "Trono Contratual de Karad",
        "governance": "casas de ofício vinculadas por dívida, segurança de mina e juramentos de pedra",
        "economy": "mineração, trilhos, fortificação e fabricação dos âncoras rúnicos",
        "resources": ["granito rúnico", "ferro", "trilhos", "âncoras de Fratura"],
        "territory": "cadeia montanhosa que sustenta os túneis de comércio e os principais selos",
        "grievance": "o continente depende de Karad, mas empurra para mineiros o custo humano de cada selo",
        "fracture_stake": "os âncoras racham salões e consomem gerações de trabalho subterrâneo",
        "coalition_demand": "segurança de mina independente e partilha continental do custo dos âncoras",
        "convergence_offer": "dívida cancelada para casas que entregarem controle total das forjas",
        "hero_goal": "impedir o colapso de Karad sem manter trabalhadores presos a contratos ancestrais",
        "hero_conflict": "Dhorin herdou o trono e as dívidas que sustentam seu poder",
        "hero_creed": "Pedra firme não desculpa contrato podre.",
        "rival_goal": "honrar todos os contratos para preservar crédito, emprego e a rede de selos",
        "rival_conflict": "Vorik teme com razão que quebrar um juramento derrube toda a confiança comercial",
        "rival_creed": "Quando um contrato cai, a montanha inteira sente o desabamento.",
        "public_voice": "Bera do Poço Nove, inspetora sem casa",
        "blocs": ["casas de ofício", "mineiros vinculados", "engenheiros de âncora"],
        "betrayal": "Vorik revela que os anões construíram os Dezesseis Pesos e que a dívida original foi paga com vidas omitidas.",
        "resolution": "Karad transforma dívidas hereditárias em responsabilidade continental auditada.",
        "beats": [
            ("Os portões fecham para magos que trazem leituras do âncora rachado.", "Forçar entrada ou aceitar inspeção anã sem testemunhas.", "O Círculo de Aether encomendou o projeto original."),
            ("Trilhos da mina atravessam um ossuário de trabalhadores sem nome.", "Controlar o entroncamento e suspender extração em plena crise.", "Necromantes identificam gerações apagadas dos livros de dívida."),
            ("O engenheiro ferido conhece uma rota segura sob a geleira.", "Escoltá-lo ou salvar a equipe que ele abandonou para proteger o projeto.", "Ele sabotou um pilar para forçar uma auditoria."),
            ("Um salão desaba enquanto guias do deserto procuram runas contrabandeadas.", "Sustentar o teto ou capturar quem roubou a única peça de reposição.", "As runas foram trocadas por água durante uma greve ocultada."),
            ("Runas seguem para Lythara dentro de raízes vivas.", "Interceptar o contrabando ou permitir que o bosque estabilize suas nascentes.", "O Trono recusou vender as peças para manter o preço."),
            ("A Forja-Mãe torna-se tribunal entre casas e mineiros.", "Suspender contratos durante a emergência, quebrando crédito continental.", "Dhorin herdou ações secretas em três casas devedoras."),
            ("A ponte dos martelos é atacada por agentes umbrais com documentos autênticos.", "Defender a ponte ou deixar que provas cheguem à praça.", "Nyx expõe que o custo dos selos sempre foi socializado como morte."),
            ("O Poço Nove evacua operários enquanto Pyr exige produção contínua.", "Escoltar trabalhadores e abandonar um âncora ainda reparável.", "A parada acelera a Fratura de Pyr, mas evita outra geração vinculada."),
            ("Um trem de cerco leva o molde do Peso Central aos dracônicos.", "Interceptar o molde ou deixá-lo criar uma reserva contra a Convergência.", "Vorik pretende distribuir poder, não entregá-lo a um único regime."),
            ("O Trono de Granito está construído sobre o primeiro livro de sacrifícios.", "Derrotar Vorik e publicar o registro, arriscando colapso de crédito.", "Os Dezesseis Pesos sempre exigiram consentimento regional que nunca foi obtido."),
        ],
    },
    "arcano": {
        "polity": "Círculo Septuário de Aether",
        "governance": "sete cátedras técnicas com autoridade sobre pesquisa, previsão e licenças mágicas",
        "economy": "navegação, previsão climática, portais limitados e educação monopolizada",
        "resources": ["Aether", "mapas de probabilidade", "prismas", "licenças"],
        "territory": "ilhas flutuantes acima das correntes que conectam todas as Fraturas",
        "grievance": "todos exigem previsões perfeitas, mas nenhum governo aceita o custo de errar sob incerteza",
        "fracture_stake": "os cálculos mostram colapso sistêmico, mas também revelam que o experimento arcano acelerou a crise",
        "coalition_demand": "dados abertos, revisão externa e limite civil ao uso do Aether",
        "convergence_offer": "estado de exceção tecnocrático até que a probabilidade de extinção caia",
        "hero_goal": "abrir o conhecimento arcano e admitir a responsabilidade do próprio Círculo",
        "hero_conflict": "Ilyra participou do experimento que sincronizou as Fraturas e ocultou sua assinatura",
        "hero_creed": "Incerteza não nos absolve de explicar quem corre o risco.",
        "rival_goal": "centralizar decisões em especialistas antes que plebiscitos lentos matem continentes",
        "rival_conflict": "Oryn manipula dados, mas seu diagnóstico de urgência é real",
        "rival_creed": "A realidade não negocia com quem prefere uma mentira confortável.",
        "public_voice": "Tess, aprendiz sem cátedra",
        "blocs": ["sete cátedras", "aprendizes licenciados", "comunidades abaixo das ilhas"],
        "betrayal": "Ilyra entrega temporariamente a Chave de Septúria a Oryn para impedir uma queda imediata e parece desertar.",
        "resolution": "o Círculo perde soberania sobre dados e passa a responder a um conselho multirregional.",
        "beats": [
            ("A escada para o Aether fecha enquanto luminários exigem acesso aos cálculos.", "Romper a guarda ou negociar com uma Igreja que já censurou ciência.", "Oryn ofereceu dados à Igreja em troca de legitimidade."),
            ("O observatório quebrado aponta a próxima Fratura para Nymar.", "Controlar as lentes e divulgar uma previsão que causará pânico portuário.", "A margem de erro foi removida dos relatórios oficiais."),
            ("Um aprendiz instável carrega a única memória do experimento.", "Escoltá-lo como testemunha, não como propriedade do Círculo.", "Tess viu a assinatura de Ilyra no protocolo."),
            ("Minutos roubados repetem um cerco enquanto bestiais sentem a saída correta.", "Confiar em instinto não verificável ou permanecer no ciclo calculável.", "Os sentidos bestiais detectam algo que o modelo excluiu."),
            ("A Chave de Septúria segue com guardas orcs contratados por Oryn.", "Interceptar a chave e arriscar a queda das ilhas.", "Ilyra entregou a chave para estabilizar o campo por seis horas."),
            ("Sete Círculos julgam Ilyra enquanto cada cátedra protege seus dados.", "Confessar sob cerco e perder comando no meio da crise.", "O experimento buscava distribuir energia, mas sincronizou as falhas."),
            ("A ilha perde chão e necromantes oferecem memória de técnicos mortos.", "Usar testemunhas mortas sem consentimento registrado.", "Os mortos provam que Oryn falsificou probabilidades, não a causa."),
            ("Um prisma errante contém rotas que a geada poderia usar para salvar refugiados.", "Escoltar o prisma e abrir uma tecnologia estratégica.", "A Coroa Invernal pagou por esses dados há anos e nunca os recebeu."),
            ("Oryn foge pelo impossível com um modelo capaz de prever a Primeira Fratura.", "Capturá-lo ou permitir que complete o cálculo durante a fuga.", "O modelo exige dados guardados no arquivo da Igreja."),
            ("A Torre que se Repete força Ilyra a reviver a decisão original.", "Vencer Oryn sem apagar o registro de culpa compartilhada.", "Nenhum selo único funciona: a estabilidade exige comando distribuído."),
        ],
    },
    "luz": {
        "polity": "Sínodo dos Sete Sóis",
        "governance": "rede de basílicas, hospitais, tribunais de juramento e arquivos canônicos",
        "economy": "dízimos, cura, acolhimento de refugiados e certificação de tratados",
        "resources": ["legitimidade", "hospitais", "arquivos", "relíquias-selo"],
        "territory": "vales centrais que recebem peregrinos e reconhecem governos",
        "grievance": "todos criticam a Igreja até precisarem de abrigo, cura ou um tratado que alguém cumpra",
        "fracture_stake": "milagres falham de modo desigual e o arquivo secreto liga a doutrina aos sacrifícios antigos",
        "coalition_demand": "abrir os arquivos e separar socorro humanitário de obediência religiosa",
        "convergence_offer": "um dogma unificado que legitima o comando central e preserva a rede hospitalar",
        "hero_goal": "manter a rede de cuidado ao mesmo tempo que desmonta a autoridade que a financia",
        "hero_conflict": "Seren deve denunciar a instituição que alimentou, curou e educou milhões",
        "hero_creed": "Fé que cobra silêncio de quem sofre serve ao altar, não à luz.",
        "rival_goal": "preservar a Igreja intacta porque sua queda deixaria refugiados sem nenhum sistema comum",
        "rival_conflict": "Solmar encobre crimes para proteger serviços cuja ausência também mataria",
        "rival_creed": "Uma verdade lançada sem abrigo pode matar mais que a mentira.",
        "public_voice": "Ione, arquivista dos nomes riscados",
        "blocs": ["ordens hospitalares", "inquisidores", "paróquias de fronteira"],
        "betrayal": "Seren entrega o relicário a umbrais para copiar o arquivo, violando seu voto e expondo pacientes.",
        "resolution": "o Sínodo é substituído por um pacto de cuidados civis e religiosos com arquivos abertos.",
        "beats": [
            ("Peregrinos umbrais são acusados de apagar milagres.", "Romper a escolta inquisitorial sem profanar o santuário.", "A falha vem do selo sob a estrada, não dos peregrinos."),
            ("O adro distribui água apenas a juramentados enquanto Pyr envia feridos.", "Controlar a praça e suspender o critério de fé.", "Os dízimos de Pyr financiam metade dos hospitais."),
            ("Uma procissão leva crianças e uma relíquia cobiçada por dracônicos.", "Escoltar vidas sem usar civis como escudo para o objeto.", "A relíquia é parte de um Peso, não prova divina."),
            ("Sete sóis artificiais cercam Seren com tropas humanas.", "Defender o arquivo ou o hospital fora das muralhas.", "Edran pediu à Igreja que ocultasse as requisições da Coroa."),
            ("Um falso prelado leva selos autênticos em veículo goblin.", "Interceptá-lo vivo e admitir que a falsificação veio do Sínodo.", "Solmar criou identidades falsas para retirar testemunhas de zonas sacrificadas."),
            ("A nave da Basílica vira assembleia armada sobre o arquivo.", "Abrir registros sem expor refugiados perseguidos.", "A lista de sacrifícios inclui fundadores canonizados."),
            ("A noite sem milagres deixa marinheiros sustentando hospitais inundados.", "Manter a vigília ou evacuar e admitir a falência pública da fé.", "Nymar mantém a rede viva sem exigir conversão."),
            ("O relicário em marcha carrega cópias para os Picos de Avar.", "Escoltar a prova, tornando impossível o sigilo.", "Seren entregou o relicário a Nyx antes da autorização."),
            ("O inquisidor fugitivo leva nomes de agentes bestiais marcados como feras.", "Capturá-lo para julgamento ou deixá-lo salvar os perseguidos que denunciou.", "O inquisidor rompeu com Solmar ao descobrir a Primeira Fratura."),
            ("O julgamento de Helianto decide se cuidado pode sobreviver à perda de dogma.", "Derrotar Solmar e garantir hospitais antes de dissolver o Sínodo.", "Solmar entrega o arquivo completo se a Coalizão assumir a rede de socorro."),
        ],
    },
    "sombrio": {
        "polity": "Conclave das Máscaras de Nox",
        "governance": "casas de informação equilibradas por anonimato, chantagem recíproca e proteção de testemunhas",
        "economy": "inteligência, contrabando, rotas noturnas e identidade segura",
        "resources": ["segredos", "rotas ocultas", "máscaras", "antídotos"],
        "territory": "charnecas e ruínas entre os centros de poder, fora de mapas oficiais",
        "grievance": "reinos usam espiões umbrais em paz e os culpam publicamente quando a guerra chega",
        "fracture_stake": "a névoa expõe memórias e destrói o anonimato que mantém o equilíbrio político",
        "coalition_demand": "proteção jurídica a testemunhas e limites ao uso militar de dossiês",
        "convergence_offer": "um serviço secreto único com imunidade e acesso a todos os arquivos",
        "hero_goal": "usar segredos para impedir tirania sem governar por chantagem",
        "hero_conflict": "Nyx protegeu inocentes apagando provas que também incriminavam aliados",
        "hero_creed": "Segredo pode ser abrigo; quando vira trono, todos respiram medo.",
        "rival_goal": "unificar a inteligência para eliminar guerras antes que comecem",
        "rival_conflict": "Vanta evita massacres por meios que tornam qualquer oposição impossível",
        "rival_creed": "A verdade pública chega sempre depois dos funerais.",
        "public_voice": "Sem-Nome Quatro, testemunha que recusou nova máscara",
        "blocs": ["casas de informação", "contrabandistas", "testemunhas protegidas"],
        "betrayal": "Nyx apaga a identidade de Edran para protegê-lo de execução e perde a confiança da Coalizão.",
        "resolution": "Nox mantém sua rede, mas transfere custódia de provas políticas a um arquivo multilateral.",
        "beats": [
            ("Névoa revela necromantes transportando memórias roubadas.", "Romper a coleta sem destruir lembranças de vítimas.", "Vanta comprou memórias para mapear os sacrifícios antigos."),
            ("O pátio sem sombras expõe todas as identidades sob luz de geada.", "Controlar o foco e decidir quem continuará anônimo.", "Algumas máscaras protegem criminosos; outras protegem testemunhas."),
            ("Uma testemunha velada conhece o acordo de água do deserto.", "Escoltá-la sem revelar seu rosto nem sua culpa passada.", "Ela falsificou mapas para salvar sua aldeia e condenou outra rota."),
            ("Elfos cercam Nyx até o amanhecer por causa da ponte de raízes.", "Resistir sem divulgar os nomes dos refugiados.", "Sylwen pediu a operação e depois negou participação."),
            ("Uma máscara em fuga leva contratos anões e chaves de cofres.", "Interceptar o portador ou permitir que publique tudo sem contexto.", "As provas incriminam Dhorin e libertam mineiros."),
            ("Umbracorte decide se segredos podem ser propriedade.", "Entregar o arquivo ao público ou criar custódia compartilhada.", "Nyx apagou a identidade de Edran após a traição."),
            ("Pyr incendeia a charneca para retirar agentes escondidos.", "Salvar arquivos ou moradias sem uma muralha estática.", "Vanta ofereceu os esconderijos em troca de cessar ataques maiores."),
            ("A Lanterna dos Condenados guia dracônicos acusados sem julgamento.", "Escoltar possíveis criminosos para um tribunal legítimo.", "Um deles conhece a localização do Primeiro Peso."),
            ("O assassino sem rosto leva a confissão de Edran à Coroa.", "Capturá-lo ou deixar que a confissão cause guerra civil imediata.", "O assassino é uma identidade coletiva usada por três facções."),
            ("Rasgar o Véu expõe Vanta e Nyx à mesma luz.", "Vencer a rede central sem destruir a proteção de milhares.", "Vanta aceita supervisão se testemunhas não forem entregues a governos vingativos."),
        ],
    },
    "necromante": {
        "polity": "Conselho Mortuário de Morvath",
        "governance": "coveiros vivos, curadores de memória e representantes temporários dos mortos consentidos",
        "economy": "sal, funerais, testemunho ancestral e trabalho cadavérico regulamentado",
        "resources": ["sal", "memórias", "ossos rúnicos", "testemunhos"],
        "territory": "salinas e criptas onde convergem mortos de todas as guerras",
        "grievance": "outros povos exigem testemunho dos mortos, mas negam a Morvath qualquer voz política",
        "fracture_stake": "mortos despertam sem consentimento e antigos crimes retornam como prova material",
        "coalition_demand": "protocolo de consentimento e reconhecimento jurídico limitado do testemunho ancestral",
        "convergence_offer": "acesso irrestrito a cadáveres de guerra em troca de estabilização e cidadania",
        "hero_goal": "dar voz aos mortos sem transformar corpos em recurso estatal",
        "hero_conflict": "Mara usou o corpo da própria mãe sem consentimento para impedir uma epidemia",
        "hero_creed": "Memória não é munição, mesmo quando os vivos temem o que ela dirá.",
        "rival_goal": "usar todos os mortos disponíveis para impedir que mais vivos se juntem a eles",
        "rival_conflict": "Veyr viola consentimento por um cálculo utilitário que frequentemente salva cidades",
        "rival_creed": "Os mortos já pagaram. Recusar sua força é cobrar dos vivos outra vez.",
        "public_voice": "Tomas, coveiro vivo e defensor do repouso",
        "blocs": ["coveiros vivos", "curadores de memória", "utilitaristas do osso"],
        "betrayal": "Mara admite ter despertado sua mãe e permite que o testemunho a condene.",
        "resolution": "Morvath cria mandatos funerários renováveis e proíbe alistamento automático de mortos de guerra.",
        "beats": [
            ("Sinos despertam marinheiros mortos num naufrágio não investigado.", "Derrotar a guarda sem usar os próprios mortos contra parentes.", "Nymar afundou o navio para conter uma peste."),
            ("Avarianos ocupam o salão das lápides buscando nomes de desaparecidos.", "Controlar o arquivo e permitir acesso estrangeiro.", "Os nomes foram vendidos como mão de obra póstuma."),
            ("Um coveiro vivo leva registros de consentimento por selvas bestiais.", "Escoltá-lo em vez do filactério mais valioso.", "Veyr destruiu contratos expirados para manter o exército."),
            ("Clãs orcs cercam Mara durante a lua que desperta ancestrais.", "Sobreviver sem convocar líderes cuja voz mudaria a política orc.", "Um ancestral confirma a existência do quarto clã."),
            ("Um filactério roubado segue para Septúria.", "Interceptar a memória e admitir que ela contém dados científicos vitais.", "Ilyra pediu a cópia antes da guerra."),
            ("A Necrópole Cinzenta julga vivos e mortos no mesmo plenário.", "Reconhecer testemunho ancestral sem dar poder eterno aos antepassados.", "A mãe de Mara pede que a filha seja condenada."),
            ("Geada congela uma maré de ossos e preserva identidades.", "Sustentar a linha ou descongelar provas que também reanimam soldados.", "Veyr tenta salvar nomes, não apenas tropas."),
            ("A última pira leva corpos sem consentimento para cremação no deserto.", "Escoltar o direito ao repouso contra necromantes da própria cidade.", "Alguns mortos pediram para permanecer como testemunhas."),
            ("Um arauto sem pulso leva a Lythara o primeiro contrato dos Pesos.", "Interceptá-lo ou deixar que a floresta conheça o crime anão-arcano.", "O documento prova consentimento regional falsificado."),
            ("Os portões de Morvath abrem para a dívida de todas as guerras.", "Derrotar Veyr sem apagar o serviço real que os mortos prestaram.", "Veyr aceita limites se os vivos assumirem o custo de reconstrução."),
        ],
    },
    "mares": {
        "polity": "Assembleia das Ilhas de Nymar",
        "governance": "conselhos insulares, capitães eleitos e pactos de maré revistos a cada estação",
        "economy": "sal, pesca, cura marinha, faróis e cobrança de rotas oceânicas",
        "resources": ["peixe", "sal", "coral curativo", "rotas marítimas"],
        "territory": "arquipélago que liga continentes e controla correntes de tempestade",
        "grievance": "potências continentais tratam ilhas como portos, nunca como comunidades soberanas",
        "fracture_stake": "marés imprevisíveis afogam ilhas baixas enquanto rotas de socorro viram bloqueios",
        "coalition_demand": "soberania portuária, fim de garantias territoriais e fundo comum para ilhas submersas",
        "convergence_offer": "uma marinha central que mantém rotas abertas e relocaliza ilhas por decreto",
        "hero_goal": "preservar as ilhas sem usar naufrágio e fome como arma diplomática",
        "hero_conflict": "Neris participou de um bloqueio que conteve peste e matou civis",
        "hero_creed": "Rota segura para o império não vale uma ilha sem escolha.",
        "rival_goal": "unificar a marinha para impedir que cada ilha venda a segurança das outras",
        "rival_conflict": "Nereth pratica pirataria, mas protege ilhas que a Assembleia abandonou",
        "rival_creed": "Soberania sem navio é uma palavra escrita antes da inundação.",
        "public_voice": "Lume, parteira da Ilha Baixa",
        "blocs": ["ilhas altas", "comunidades submersíveis", "corsários"],
        "betrayal": "Neris admite ter ordenado o naufrágio que abriu o arco de Morvath.",
        "resolution": "Nymar cria uma frota confederada sob veto das ilhas baixas e anula garantias territoriais.",
        "beats": [
            ("Tropas de Pyr ocupam um cais alegando escolta de combustível.", "Romper o desembarque sem incendiar armazéns civis.", "O combustível mantém bombas de uma ilha baixa."),
            ("Dracônicos reivindicam um recife partido como herança mineral.", "Controlar o recife sem destruir ninhos e corais.", "O tratado humano entregou o local como garantia."),
            ("Uma barca de curadores leva remédios e oficiais do bloqueio.", "Escoltar quem salvou doentes e condenou tripulações.", "Neris assinou a ordem de afundamento."),
            ("Goblins tentam reparar o farol no olho da tormenta.", "Defender técnicos impopulares ou a frota que quer partir.", "A sabotagem veio de uma ilha alta para manter taxas."),
            ("O Corsário do Coral leva um édito da Igreja reconhecendo Nereth.", "Interceptar o édito ou permitir uma legitimidade comprada.", "Solmar reconheceu a corsária em troca de rotas de refugiados."),
            ("Canais de Nymar dividem ilhas altas e baixas.", "Dar veto às ilhas ameaçadas mesmo contra a maioria populacional.", "Neris ocultou projeções de submersão para evitar pânico."),
            ("Avarianos cercam o porto na maré baixa.", "Sustentar duas entradas ou abrir passagem aérea paga.", "Avar oferece evacuação, não conquista, mas exige monopólio de correio."),
            ("Um farol flutuante leva famílias bestiais e registros de biodiversidade.", "Escoltar refugiados ou salvar o mapa de correntes.", "A Fronteira Primeva conhece a origem biológica da Fratura."),
            ("Um leviatã orc transporta o tratado que venderia três portos.", "Interceptar o tratado e arriscar fome em Valedouro.", "Cael não tinha autoridade para oferecer Nymar."),
            ("O Trono Abissal controla a maré por cálculos arcanos.", "Derrotar Nereth sem desligar a única defesa das ilhas baixas.", "Nereth aceita uma frota confederada se as ilhas baixas tiverem veto."),
        ],
    },
    "chama": {
        "polity": "Consórcio Cívico da Caldeira de Pyr",
        "governance": "bairros-forja, sindicatos de risco e um cônsul eleito por produção e segurança",
        "economy": "fundição, armas, cerâmica, calor e processamento de minérios",
        "resources": ["calor", "aço", "obsidiana", "armas"],
        "territory": "caldeira industrial que equipa exércitos e aquece cidades de geada",
        "grievance": "o continente condena as forjas enquanto exige armas, ferramentas e aquecimento barato",
        "fracture_stake": "pressão térmica ameaça bairros operários e torna paralisação tão mortal quanto produção",
        "coalition_demand": "controle operário de segurança e conversão progressiva da economia de guerra",
        "convergence_offer": "encomendas permanentes, água garantida e evacuação seletiva dos técnicos",
        "hero_goal": "manter Pyr viva sem alimentar uma guerra necessária para pagar sua água",
        "hero_conflict": "Kael organizou greves e depois autorizou fornos militares para evitar fome",
        "hero_creed": "A forja existe para servir à cidade; a cidade não é combustível da forja.",
        "rival_goal": "garantir trabalho, água e defesa por meio de produção militar contínua",
        "rival_conflict": "Brasa sustenta bairros inteiros com contratos que prolongam o conflito",
        "rival_creed": "Paz sem salário e sem água é só guerra vencida por quem já tinha tudo.",
        "public_voice": "Vela, inspetora dos bairros-forja",
        "blocs": ["sindicatos de risco", "donos de forno", "bairros dependentes"],
        "betrayal": "Kael esconde que o Coração Refrigerado foi comprado com portos de Nymar oferecidos por Cael.",
        "resolution": "Pyr converte fornos militares em âncoras e infraestrutura sob controle dos bairros.",
        "beats": [
            ("Geada fecha a estrada de cinzas e exige armas em troca de gelo.", "Romper a escolta sem perder o refrigerante vital.", "Yrsa não autorizou a cobrança; mercadores de Skeld a impuseram."),
            ("O pátio da fundição disputa a última cisterna com caravanas do deserto.", "Controlar a água e reconhecer direitos de quem a transportou.", "Pyr paga abaixo do custo há três gerações."),
            ("Uma caravana de água escoltada por elfos atravessa cinza tóxica.", "Proteger a água ou sementes capazes de recuperar o solo.", "Lythara exige redução de produção em plena crise."),
            ("Anões sustentam o salão até a lava subir.", "Salvar os pilares ou os operários presos em outra ala.", "Vorik priorizou o âncora; Bera alterou a rota de evacuação."),
            ("O Portador da Brasa leva projetos a Vanta.", "Interceptar o projeto ou permitir que umbrais exponham falhas de segurança.", "Kael assinou uma dispensa de inspeção."),
            ("Cinerária vota com fornos apontados para a praça.", "Suspender contratos e aceitar desemprego imediato.", "Brasa falsificou riscos, mas os salários são reais."),
            ("Dracônicos cercam Pyr sob chuva incandescente.", "Defender a caldeira ou permitir acesso ao núcleo ancestral.", "O calor dracônico pode estabilizar a Fratura sem armas."),
            ("O Coração Refrigerado chega com escolta humana.", "Escoltar a máquina e divulgar a garantia ilegal sobre Nymar.", "Kael conhecia a origem do pagamento."),
            ("Uma salamandra goblin leva contratos de conversão industrial.", "Capturar o mensageiro ou deixar a alternativa chegar à Liga.", "Grizna oferece paz industrial em troca de monopólio técnico."),
            ("A Boca da Caldeira alimenta a guerra e também todas as bombas de água.", "Derrubar Brasa sem desligar a cidade.", "O cônsul aceita conversão se a Coalizão financiar cinco anos de transição."),
        ],
    },
    "geada": {
        "polity": "Althing da Coroa Invernal",
        "governance": "assembleia de fiordes, jarls temporários e juramentos de provisão no inverno",
        "economy": "gelo, água doce, conservação de alimento e rotas sazonais",
        "resources": ["água doce", "gelo", "peixe preservado", "passagens"],
        "territory": "geleiras que alimentam rios e abrem rotas apenas parte do ano",
        "grievance": "o sul exige água e passagem enquanto trata refugiados do degelo como problema local",
        "fracture_stake": "a Fratura alterna congelamento e degelo, deslocando aldeias e tornando mapas políticos obsoletos",
        "coalition_demand": "cotas de água negociadas e reassentamento continental de refugiados climáticos",
        "convergence_offer": "racionamento central e fronteiras móveis impostas por um comando técnico",
        "hero_goal": "salvar comunidades do degelo sem transformar água em arma",
        "hero_conflict": "Yrsa fechou um fiorde para preservar reservas e condenou uma frota estrangeira",
        "hero_creed": "Água guardada para um povo só apodrece em guerra.",
        "rival_goal": "preservar Skeld fechando rotas até que o ciclo climático estabilize",
        "rival_conflict": "Hroth protege famílias reais, mas exporta o custo para refugiados e vizinhos",
        "rival_creed": "Quem abre o portão no inverno precisa dizer qual criança ficará sem comida.",
        "public_voice": "Eyd, capitã de um fiorde submerso",
        "blocs": ["fiordes antigos", "refugiados do degelo", "mercadores de gelo"],
        "betrayal": "Yrsa admite ter fechado o fiorde do naufrágio e aceita reparação a Nymar.",
        "resolution": "Skeld vincula cotas de água a reassentamento e representação dos deslocados.",
        "beats": [
            ("Avarianos cobram passagem aérea quando o primeiro gelo fecha estradas.", "Romper o bloqueio ou reconhecer o custo real do resgate.", "A tarifa financia ninhos destruídos pela mesma tempestade."),
            ("Clãs bestiais ocupam um fiorde de pesca ancestral.", "Controlar o cais e admitir que a fronteira de gelo se moveu.", "O fiorde era selva antes do último ciclo."),
            ("Um trenó leva feridos orcs e alimento de Skeld.", "Escoltar vidas ou preservar a ração de uma aldeia isolada.", "Maug prometeu cavalos em troca e não pôde cumprir."),
            ("Arcanos sustentam uma longa noite artificial para reduzir degelo.", "Sobreviver ao cerco sem destruir a barreira climática.", "O modelo de Oryn desloca a tempestade para Nymar."),
            ("Um batedor necromante leva nomes do naufrágio.", "Interceptar a prova ou permitir que Morvath a torne pública.", "Yrsa ordenou o fechamento do fiorde."),
            ("Muralhas de Skeld separam cidadãos de refugiados.", "Dar acesso igual às reservas e romper juramentos antigos.", "Hroth falsificou contagens para favorecer fiordes aliados."),
            ("O lago se parte enquanto guias do deserto buscam água.", "Defender a ponte ou abrir a reserva ao sul.", "A água enviada ao deserto reduz pressão sob a geleira."),
            ("Uma chama de Pyr aquece o corredor de evacuação.", "Escoltar o reator apesar da dívida ilegal.", "Kael prometeu reparação usando tecnologia convertida."),
            ("Hroth recua com o livro de cotas e engenheiros anões.", "Capturá-lo ou deixar que repare a barragem durante a fuga.", "O jarl aceita reassentamento se o continente assumir quotas."),
            ("A Coroa Invernal é uma máquina de racionamento, não um trono.", "Derrotar Hroth sem romper o controle das águas.", "A solução depende de pactos de reassentamento, não de vitória militar."),
        ],
    },
    "avariano": {
        "polity": "Conselho dos Ninhos do Zênite",
        "governance": "ninhos por altitude, correios juramentados e voto ligado à manutenção das pontes aéreas",
        "economy": "mensageria, meteorologia, resgate e controle de passagens elevadas",
        "resources": ["rotas aéreas", "previsão", "penas-selo", "resgate"],
        "territory": "picos que dominam comunicações e atalhos entre todas as regiões",
        "grievance": "os vales exigem correio neutro, mas recusam pagar pelos riscos e pelas aldeias atingidas por tempestades",
        "fracture_stake": "correntes aéreas fecham rotas e tornam o monopólio de comunicação uma arma política",
        "coalition_demand": "neutralidade verificável do correio e fundo comum de resgate",
        "convergence_offer": "monopólio oficial, rotas militares protegidas e prioridade de evacuação aos ninhos altos",
        "hero_goal": "manter o céu aberto sem vender informação e resgate ao maior pagador",
        "hero_conflict": "Aren protege a neutralidade de uma rede que sempre privilegiou ninhos altos",
        "hero_creed": "Mensagem neutra não existe quando alguns esperam no abismo.",
        "rival_goal": "financiar a sobrevivência avariana cobrando prioridade e alinhando o correio à Convergência",
        "rival_conflict": "Silex explora a crise, mas paga resgates que o Conselho ignorou",
        "rival_creed": "Quem quer o céu aberto precisa sustentar as asas que caem.",
        "public_voice": "Pia, resgatadora de ninho baixo",
        "blocs": ["ninhos altos", "resgatadores", "correios neutros"],
        "betrayal": "Aren desviou correios para salvar aliados e destruiu a neutralidade que defendia.",
        "resolution": "as rotas tornam-se bem comum com prioridade definida por risco humano, não riqueza.",
        "beats": [
            ("Dracônicos ocupam uma plataforma alegando direito ancestral ao céu.", "Romper a guarda sem destruir ovos transportados.", "O tratado antigo reconhece passagem, não soberania."),
            ("Humanos compram prioridade na Plataforma dos Ventos.", "Controlar a torre e suspender contratos em plena evacuação.", "Alda usou a prioridade para salvar a prova contra Edran."),
            ("Goblins presos no abismo carregam peças de farol.", "Escoltar trabalhadores antes da carga estratégica.", "Silex planejou o acidente para justificar tarifas."),
            ("Luminários cercam Aren no olho do furacão.", "Sobreviver sem usar peregrinos como escudo aéreo.", "A Igreja deseja controlar mensagens sobre o arquivo."),
            ("Um mensageiro de Nymar leva prova das garantias portuárias.", "Interceptá-lo por violar rota fechada ou deixá-lo expor Cael.", "Aren desviou mensagens anteriores a pedido de Alda."),
            ("Pontes do Ninho dividem altitude e cidadania.", "Dar voto aos ninhos baixos e alterar prioridades de resgate.", "O Conselho subnotificou mortes nas rotas baratas."),
            ("Bestiais bloqueiam o céu guiados por aves migratórias.", "Defender os ninhos ou reconhecer um corredor ecológico.", "A Fratura interrompeu a migração que prevê tempestades."),
            ("Um Ovo Solar contém cartografia viva das correntes.", "Escoltar o ovo sem tratá-lo como instrumento.", "Orcs o protegeram durante gerações no cânion."),
            ("Silex foge com o código arcano que abre todas as rotas.", "Capturá-lo ou permitir que resgate um ninho isolado.", "Ele vendeu prioridade para financiar resgates negados pelo Conselho."),
            ("A Batalha do Firmamento decide quem pode fechar o céu.", "Derrotar Silex e substituir monopólio por obrigação comum.", "Silex aceita julgamento se o fundo de resgate for garantido."),
        ],
    },
    "draconico": {
        "polity": "Conclave das Escamas Ancestrais",
        "governance": "linhagens com custódia de ovos, templos de memória e pactos de não proliferação",
        "economy": "núcleos térmicos, proteção de mesetas e aluguel de força estratégica",
        "resources": ["núcleos", "ovos", "metais raros", "memória ancestral"],
        "territory": "mesetas fortificadas acima de reservas energéticas e templos do Primeiro",
        "grievance": "outros povos temem o poder dracônico, mas compram sua dissuasão quando conveniente",
        "fracture_stake": "núcleos despertam e transformam herança biológica em arma de escala continental",
        "coalition_demand": "custódia compartilhada dos núcleos e reconhecimento dos crimes antigos contra linhagens",
        "convergence_offer": "soberania dracônica em troca de um arsenal central de dissuasão",
        "hero_goal": "proteger ovos e memória sem reconstruir o império dos Primeiros",
        "hero_conflict": "Varkesh descende da linhagem que ajudou a impor os Pesos",
        "hero_creed": "Herança explica nosso poder; não nos concede o direito de repeti-lo.",
        "rival_goal": "criar uma dissuasão dracônica que impeça qualquer região de dominar as demais",
        "rival_conflict": "Sarthax responde a perseguições reais com ameaça de destruição coletiva",
        "rival_creed": "Só chamam nossa força de monstruosa quando não está a serviço deles.",
        "public_voice": "Azra, guardiã de ovos sem linhagem",
        "blocs": ["linhagens de templo", "guardiões sem sangue", "militaristas de núcleo"],
        "betrayal": "Varkesh entrega um núcleo aos guardiões sem linhagem e rompe o privilégio ancestral.",
        "resolution": "os núcleos passam a custódia multirregional e ovos deixam de definir cidadania.",
        "beats": [
            ("Guias do deserto chegam à meseta seguindo um tratado apagado.", "Romper a patrulha ou reconhecer passagem ancestral.", "A linhagem de Varkesh falsificou o fim do tratado."),
            ("Elfos ocupam o Templo das Garras para conter calor nas raízes.", "Controlar o templo sem profanar memórias.", "O núcleo dracônico alimenta uma nascente de Lythara."),
            ("Um herdeiro ferido viaja com engenheiros anões.", "Escoltar a pessoa sem priorizar seu sangue sobre guardiões.", "O herdeiro quer renunciar ao privilégio."),
            ("Umbrais cercam o vale com provas de massacres antigos.", "Sobreviver e preservar arquivos que incriminam o próprio Conclave.", "Vanta não falsificou as provas."),
            ("Um arauto leva uma brasa-núcleo a Pyr.", "Interceptar a arma ou permitir uso civil supervisionado.", "Kael planeja convertê-la em âncora."),
            ("Drak-Azur decide se linhagem ainda define cidadania.", "Dar voto aos guardiões sem sangue sob ameaça de Sarthax.", "Varkesh ocultou sua participação num conselho militar."),
            ("Humanos atacam sob chuva de brasas por medo de mobilização.", "Defender a cidade sem despertar o arsenal completo.", "Cael pediu apenas inspeção; Edran fabricou a ordem de ataque."),
            ("O Ovo Primordial segue em veículo goblin para um santuário neutro.", "Escoltar vida e abrir custódia a não dracônicos.", "O ovo contém memória do Pacto dos Pesos."),
            ("Sarthax foge com reconhecimento luminar de soberania.", "Capturá-lo ou permitir que leia o documento ao público.", "A Igreja prometeu soberania em troca do arsenal."),
            ("O Primeiro desperta como memória coletiva, não deus.", "Derrotar Sarthax sem silenciar as vítimas ancestrais.", "Os dracônicos foram agentes e reféns do sistema original."),
        ],
    },
    "deserto": {
        "polity": "Pacto dos Poços de Qasr-Sahir",
        "governance": "cidades-oásis e caravanas nômades com direitos sazonais sobre água e passagem",
        "economy": "água, vidro de safira, cartografia e comércio de longa distância",
        "resources": ["água", "vidro-safira", "mapas", "especiarias"],
        "territory": "dunas e cânions entre as rotas do sul e a Fronteira Primeva",
        "grievance": "cidades registram poços; nômades os mantêm e desaparecem dos tratados",
        "fracture_stake": "miragens alteram mapas e a Fratura drena o aquífero compartilhado com Lythara",
        "coalition_demand": "direitos móveis de água e representação nômade nos tratados",
        "convergence_offer": "canais fortificados e racionamento urbano em troca do fim das rotas livres",
        "hero_goal": "preservar o Pacto dos Poços sem congelar nômades em fronteiras urbanas",
        "hero_conflict": "Samira é filha da corte e enriqueceu com taxas que quer abolir",
        "hero_creed": "Mapa que ignora quem move a água é só uma arma com bordas bonitas.",
        "rival_goal": "centralizar os poços antes que cidades e caravanas morram disputando miragens",
        "rival_conflict": "Namar constrói canais eficientes que também tornam nômades dependentes",
        "rival_creed": "Liberdade de rota não enche um odre quando o poço desaparece.",
        "public_voice": "Dara, mestra de uma caravana sem cidade",
        "blocs": ["cidades-oásis", "caravanas nômades", "cartógrafos de safira"],
        "betrayal": "Samira usa um mapa falso para atrair Namar e condena uma caravana aliada à tempestade.",
        "resolution": "o Pacto reconhece cidadania móvel e gestão conjunta do aquífero com Lythara.",
        "beats": [
            ("Rastreadores bestiais seguem pegadas até um poço declarado urbano.", "Romper a guarda e reconhecer uso ancestral.", "A Fronteira Primeva protege a nascente subterrânea."),
            ("Orcs ocupam um oásis em rota migratória.", "Controlar a água sem expulsar rebanhos.", "O Pacto antigo concede passagem, mas a cidade apagou a cláusula."),
            ("Uma caravana arcana transporta mapas que mudam com a Fratura.", "Escoltar tecnologia sem ceder monopólio cartográfico.", "Oryn removeu rotas nômades do modelo."),
            ("Necromantes cercam Samira ao sol do meio-dia por causa de corpos sem nome.", "Sobreviver e admitir mortes ocultadas nas caravanas fiscais.", "A corte deixou de registrar trabalhadores nômades."),
            ("Namar cruza as dunas com batedores de geada e um plano de canal.", "Interceptar o plano ou permitir obra que salvará cidades primeiro.", "O canal secaria rotas móveis em cinco anos."),
            ("Qasr-Sahir vota enquanto caravanas ficam fora das muralhas.", "Conceder cidadania móvel e perder controle fiscal.", "Samira lucrou com as taxas da própria família."),
            ("Uma tempestade de vidro fecha a rota para Lythara.", "Sustentar duas frentes ou abrir o aquífero à floresta.", "A drenagem é compartilhada; nenhuma região pode selar sozinha."),
            ("A Fonte Nômade viaja com perfuradores anões.", "Escoltar a fonte e impedir que a tecnologia seja patenteada.", "Dhorin oferece reparação pelas primeiras perfurações."),
            ("Um falcão umbral leva o mapa falso usado por Samira.", "Capturá-lo ou aceitar que a Coalizão conheça a traição.", "Samira atraiu Namar e abandonou uma caravana."),
            ("O Horizonte Velado cobre o canal central de Pyr.", "Derrotar Namar e preservar trechos que realmente salvam vidas.", "Namar aceita gestão conjunta se cidades mantiverem reserva mínima."),
        ],
    },
    "bestial": {
        "polity": "Círculo de Totens da Fronteira Primeva",
        "governance": "clãs por habitat, guardiões de migração e assembleias convocadas por sinais naturais",
        "economy": "medicinas, resinas, caça regulada e manejo de biodiversidade",
        "resources": ["medicinas", "sementes primevas", "resinas", "conhecimento ecológico"],
        "territory": "selva, savana e cavernas sobre a Primeira Fratura",
        "grievance": "exploradores chamam conhecimento bestial de instinto para usá-lo sem reconhecer soberania",
        "fracture_stake": "a Primeira Fratura é também um órgão vivo; selá-la como máquina destruiria ecossistemas inteiros",
        "coalition_demand": "soberania ecológica e veto local sobre extração ou selamento",
        "convergence_offer": "proteção militar e reservas fechadas em troca de acesso ao núcleo vivo",
        "hero_goal": "defender a Fronteira sem idealizar tradições que excluem clãs transformados",
        "hero_conflict": "Rauk pertence ao clã dominante e aceitou caçadas contra metamorfos instáveis",
        "hero_creed": "Natureza não é inocente; poder também não é inevitável.",
        "rival_goal": "fechar a Fronteira e expulsar todos os povos antes que o núcleo seja explorado",
        "rival_conflict": "Urrak sobreviveu a experimentos arcanos e transforma trauma legítimo em pureza territorial",
        "rival_creed": "Toda promessa externa chegou com uma jaula escondida.",
        "public_voice": "Suma, metamorfa marcada e guardiã do Primeiro Totem",
        "blocs": ["clãs de habitat", "metamorfos marcados", "guardiões do núcleo"],
        "betrayal": "Rauk admite as caçadas e entrega o Totem de comando a Suma antes da batalha final.",
        "resolution": "a Primeira Fratura torna-se um pacto vivo distribuído; nenhum povo possui o núcleo.",
        "beats": [
            ("Tropas humanas marcam trilhas para extração medicinal.", "Romper a expedição sem destruir remédios destinados a hospitais.", "Alda autorizou coleta limitada; Edran ampliou as cotas."),
            ("Goblins ocupam o círculo dos totens com sensores.", "Controlar o sítio e decidir se dados ecológicos podem ser copiados.", "Os sensores detectam que a Fratura está viva."),
            ("Uma alcateia ferida viaja com curadores luminares.", "Escoltar metamorfos que a própria tradição caçou.", "Rauk assinou ordens antigas contra os marcados."),
            ("Marinheiros cercam o acampamento durante a noite dos predadores.", "Sobreviver sem incendiar a mata e sem abandonar refugiados.", "Nymar busca uma rota de evacuação, não território."),
            ("Um caçador marcado leva aos Picos o mapa do núcleo.", "Interceptá-lo ou permitir que Aren convoque testemunhas externas.", "O caçador foge de Urrak e também de Rauk."),
            ("Pedra-Uivo decide quem fala pelo território.", "Entregar o Totem de comando a uma metamorfa sem clã.", "Suma guardou a memória do primeiro pacto."),
            ("Orcs atravessam a selva sem pássaros seguindo migração interrompida.", "Defender aldeias e manter aberto um corredor ancestral.", "As aves apontam o pulso do núcleo."),
            ("O Totem Errante segue com arcanos que querem medir, não possuir.", "Escoltar o totem e impor limites ao conhecimento de Ilyra.", "O núcleo responde a múltiplas vozes coordenadas."),
            ("Um alfa foge com necromantes e nomes das vítimas de caçadas.", "Capturá-lo ou permitir que os mortos testemunhem.", "Rauk é responsável político pelas caçadas, embora não as tenha iniciado."),
            ("O Rugido da Fratura convoca as dezesseis regiões.", "Derrotar Urrak e escolher entre Escudo Central, Ruptura Livre ou Pacto Distribuído.", "A Primeira Fratura é a memória viva do acordo; estabilidade exige consentimento renovado."),
        ],
    },
}


MARKS = [
    {
        "id": "legitimidade_coalizao",
        "name": "Legitimidade da Coalizão",
        "meaning": "confiança de que a campanha responde a pactos públicos, não só à vitória militar",
        "low_state": "a Coalizão é vista como novo império",
        "high_state": "as regiões aceitam decisões difíceis porque custos e limites são verificáveis",
    },
    {
        "id": "autonomia_regional",
        "name": "Autonomia Regional",
        "meaning": "capacidade real de cada povo decidir recursos, fronteiras e participação nos Pesos",
        "low_state": "ordens centrais substituem instituições locais",
        "high_state": "o poder é distribuído, embora a resposta a crises seja mais lenta",
    },
    {
        "id": "amparo_popular",
        "name": "Amparo Popular",
        "meaning": "proteção de civis, refugiados, trabalhadores e grupos sem representação",
        "low_state": "vitórias táticas acumulam fome, deslocamento e radicalização",
        "high_state": "a campanha mantém apoio social, com maior custo logístico",
    },
    {
        "id": "poder_convergencia",
        "name": "Poder da Convergência",
        "meaning": "capacidade do comando central de controlar rotas, dados, exércitos e âncoras",
        "low_state": "a Convergência perde coerência e depende de negociação",
        "high_state": "o Escudo Central torna-se a opção mais fácil e autoritária",
    },
    {
        "id": "estabilidade_fraturas",
        "name": "Estabilidade das Fraturas",
        "meaning": "margem técnica antes de falhas em cascata",
        "low_state": "o mundo ganha liberdade imediata com risco ecológico e mágico",
        "high_state": "o sistema resiste, mas pode ocultar zonas que pagam a estabilidade",
    },
    {
        "id": "divida_de_guerra",
        "name": "Dívida de Guerra",
        "meaning": "carga futura de requisições, contratos, danos e reparações",
        "low_state": "a reconstrução é financiável e as alianças não dependem de coerção econômica",
        "high_state": "a paz nasce hipotecada e favorece credores e potências logísticas",
    },
]


CANONICAL_DELTAS = [
    {"legitimidade_coalizao": 1, "poder_convergencia": -1},
    {"autonomia_regional": 1, "divida_de_guerra": 1},
    {"amparo_popular": 2, "divida_de_guerra": 1},
    {"estabilidade_fraturas": 1, "amparo_popular": -1},
    {"legitimidade_coalizao": 1, "poder_convergencia": -1},
    {"autonomia_regional": 2, "legitimidade_coalizao": -1},
    {"estabilidade_fraturas": 1, "amparo_popular": -1},
    {"amparo_popular": 2, "divida_de_guerra": 1},
    {"legitimidade_coalizao": 1, "poder_convergencia": -1},
    {"estabilidade_fraturas": 2, "autonomia_regional": 1, "divida_de_guerra": 1},
]


COERCIVE_DELTAS = [
    {"legitimidade_coalizao": -1, "poder_convergencia": 1},
    {"autonomia_regional": -1, "estabilidade_fraturas": 1},
    {"amparo_popular": -1, "divida_de_guerra": -1},
    {"estabilidade_fraturas": 2, "amparo_popular": -2},
    {"legitimidade_coalizao": -1, "poder_convergencia": 1},
    {"autonomia_regional": -2, "estabilidade_fraturas": 1},
    {"estabilidade_fraturas": 2, "amparo_popular": -2},
    {"amparo_popular": -1, "divida_de_guerra": -1},
    {"legitimidade_coalizao": -1, "poder_convergencia": 1},
    {"estabilidade_fraturas": 3, "autonomia_regional": -2, "poder_convergencia": 1},
]


PHASES = [
    ("entrada", "Abram uma rota; não colecionem troféus de quem ainda pode depor armas."),
    ("recurso", "Tomem o marco e tornem público quem dependia dele antes de nós."),
    ("testemunho", "A escolta é a missão. Prova, pessoa e carga não são a mesma coisa."),
    ("retaliação", "Guardem CMD para a segunda ameaça; o cerco quer nos fazer reagir cedo."),
    ("interceptação", "O mensageiro vale pelo que sabe. Evitem transformar prova em cadáver."),
    ("cisão", "Esta praça não é território inimigo; é uma instituição em disputa."),
    ("cerco", "Duas frentes, uma reserva móvel e nenhum bairro usado como muralha."),
    ("êxodo", "Quem estamos escoltando define a vitória mais do que a saída no mapa."),
    ("acerto de contas", "Fechem a rota, mas deixem espaço para rendição e testemunho."),
    ("pacto regional", "Derrubem o comando rival; preservem o que ainda mantém a região viva."),
]


SECONDARY_SUPPORT = {
    "humano": "logística, cavalaria e mandados de emergência",
    "elfo": "batedores, controle de cobertura e tratados de nascente",
    "orc": "pressão de corredor, rebanhos e mercenários de clã",
    "goblin": "engenhos, sabotagem e contratos de manutenção",
    "anao": "armadura, pontes e tecnologia de âncora",
    "arcano": "previsão, prismas e controle de Aether",
    "luz": "legitimidade, hospitais e juramentos canônicos",
    "sombrio": "informação, rotas clandestinas e proteção de identidades",
    "necromante": "testemunho dos mortos, desgaste e memória material",
    "mares": "transporte, bloqueio e controle de canais",
    "chama": "cerco térmico, fundição e economia de guerra",
    "geada": "racionamento, preservação e controle de movimento",
    "avariano": "mensageria, resgate e superioridade de rota",
    "draconico": "dissuasão, núcleos e reivindicação ancestral",
    "deserto": "guias, água e cartografia móvel",
    "bestial": "rastreamento, corredores ecológicos e conhecimento do núcleo vivo",
}


FAMILY_NAMES = {
    "humano": "Humanos",
    "elfo": "Elfos Silvestres",
    "orc": "Orcs",
    "goblin": "Goblins",
    "anao": "Anões",
    "arcano": "Arcanos",
    "luz": "Luminares",
    "sombrio": "Umbrais",
    "necromante": "Necromantes",
    "mares": "Povos das Marés",
    "chama": "Nascidos da Chama",
    "geada": "Nascidos da Geada",
    "avariano": "Avarianos",
    "draconico": "Dracônicos",
    "deserto": "Povos do Deserto",
    "bestial": "Clãs Bestiais",
}


def alternative_deltas(canonical):
    return deepcopy(COERCIVE_DELTAS)


def build():
    old_regions = load("regioes_v_1.json")["regions"]
    old_characters = load("personagens_v_1.json")["characters"]
    old_scenarios = load("cenarios_v_2.json")["scenarios"]
    old_campaign = load("campanha_v_2.json")

    characters_by_family = {}
    for character in old_characters:
        characters_by_family.setdefault(character["family_id"], {})[
            "hero" if character["id"].startswith("heroi_") else "rival"
        ] = character

    regions_v2 = []
    for region in old_regions:
        family = region["family_id"]
        profile = PROFILES[family]
        item = deepcopy(region)
        item.update(
            {
                "schema_version": 2,
                "polity": profile["polity"],
                "governance": profile["governance"],
                "political_economy": profile["economy"],
                "strategic_resources": profile["resources"],
                "territorial_role": profile["territory"],
                "historical_grievance": profile["grievance"],
                "fracture_stake": profile["fracture_stake"],
                "coalition_demand": profile["coalition_demand"],
                "convergence_offer": profile["convergence_offer"],
                "internal_blocs": profile["blocs"],
                "credible_betrayal": profile["betrayal"],
                "regional_resolution": profile["resolution"],
            }
        )
        regions_v2.append(item)

    characters_v2 = []
    for character in old_characters:
        profile = PROFILES[character["family_id"]]
        hero = character["id"].startswith("heroi_")
        item = deepcopy(character)
        item["schema_version"] = 2
        item["goal"] = profile["hero_goal"] if hero else profile["rival_goal"]
        item["internal_conflict"] = (
            profile["hero_conflict"] if hero else profile["rival_conflict"]
        )
        item["political_position"] = (
            profile["coalition_demand"] if hero else profile["convergence_offer"]
        )
        item["creed"] = profile["hero_creed"] if hero else profile["rival_creed"]
        item["moral_gray_function"] = (
            "aliado responsável por escolhas contestáveis"
            if hero
            else "rival com diagnóstico legítimo e método coercivo"
        )
        item["regional_betrayal_or_reversal"] = profile["betrayal"]
        characters_v2.append(item)

    previous_id = None
    scenarios_v3 = []
    for scenario in old_scenarios:
        item = deepcopy(scenario)
        family = scenario["region_id"].replace("regiao_", "")
        profile = PROFILES[family]
        stage = scenario["stage_in_region"]
        phase_id, hero_order = PHASES[stage - 1]
        event, dilemma, reveal = profile["beats"][stage - 1]
        hero = characters_by_family[family]["hero"]["name"]
        rival = characters_by_family[family]["rival"]["name"]
        second_family = scenario["enemy_family_ids"][1]
        interlocutor = (
            profile["public_voice"] if stage in {3, 6, 8} else rival
        )
        prior = previous_id
        next_id = (
            old_scenarios[scenario["order"]]["id"]
            if scenario["order"] < len(old_scenarios)
            else None
        )
        canonical = CANONICAL_DELTAS[stage - 1]
        coercive = COERCIVE_DELTAS[stage - 1]
        narrative = {
            "regional_phase": phase_id,
            "historical_context": (
                f"{event} A disputa nasce de {profile['grievance'].lower()} "
                f"e coloca em risco {profile['fracture_stake'].lower()}."
            ),
            "continuity": {
                "from_scenario_id": prior,
                "to_scenario_id": next_id,
                "regional_payoff": profile["resolution"] if stage == 10 else None,
            },
            "pre_battle_dialogue": [
                {"speaker": hero, "line": hero_order},
                {
                    "speaker": interlocutor,
                    "line": (
                        f"{profile['rival_creed']} Hoje, {dilemma[0].lower() + dilemma[1:]}"
                        if interlocutor == rival
                        else f"Se vencerem, respondam por isto: {dilemma[0].lower() + dilemma[1:]}"
                    ),
                },
            ],
            "post_battle_dialogue": [
                {
                    "speaker": hero,
                    "line": (
                        f"Cumprimos o objetivo, mas a marca política permanece: "
                        f"{dilemma[0].lower() + dilemma[1:]}"
                    ),
                },
                {"speaker": interlocutor, "line": reveal},
            ],
            "moral_dilemma": dilemma,
            "revelation": reveal,
            "betrayal_or_reversal": (
                profile["betrayal"] if stage in {6, 9} else None
            ),
            "political_marks": {
                "canonical_route": canonical,
                "choice": {
                    "prompt": dilemma,
                    "canonical_option_id": "limites_publicos",
                    "options": [
                        {
                            "id": "limites_publicos",
                            "label": "Cumprir o objetivo com limites públicos",
                            "effects": canonical,
                        },
                        {
                            "id": "coercao_eficiente",
                            "label": "Maximizar a vitória por coerção",
                            "effects": coercive,
                        },
                    ],
                },
            },
            "enemy_justification": (
                f"{FAMILY_NAMES[family]} representam a cisão interna de "
                f"{profile['polity']}; {FAMILY_NAMES[second_family]} fornecem "
                f"{SECONDARY_SUPPORT[second_family]} porque seus próprios interesses "
                f"estão ligados a esta disputa."
            ),
            "level_design_justification": (
                f"A condição {scenario['victory_condition']} traduz a crise: "
                f"{scenario['objective']}. {scenario['formation_twist'][0].upper() + scenario['formation_twist'][1:]}."
            ),
            "soft_counter_narrative": (
                f"A oposição pune {scenario['soft_counter']['punishes']} porque "
                f"opera com {scenario['soft_counter']['enemy_plan']}; a resposta "
                f"continua flexível por {', '.join(scenario['soft_counter']['recommended_roles'])}."
            ),
        }
        item["schema_version"] = 3
        item["premise"] = event
        item["story_beat"] = f"{stage}/10 — {phase_id}"
        item["narrative"] = narrative
        scenarios_v3.append(item)
        previous_id = item["id"]

    acts = [
        {
            "number": 1,
            "title": "Pão, Terra e Engrenagens",
            "regions": [1, 2, 3, 4],
            "dramatic_question": "Uma coalizão pode nascer sem repetir as coerções que combate?",
            "arc": "A disputa começa por grão, água, migração e dívida industrial; a Convergência aparece como resposta eficiente a instituições incapazes de cooperar.",
            "turn": "O mapa roubado revela que o marechal Edran, chefe logístico da Coalizão, vendeu rotas para salvar Valedouro.",
        },
        {
            "number": 2,
            "title": "O Preço da Verdade",
            "regions": [5, 6, 7, 8],
            "dramatic_question": "Quem tem autoridade para administrar um risco que nenhum povo entende sozinho?",
            "arc": "Karad, Septúria, Helianto e Nox expõem a origem dos Pesos, o experimento que sincronizou as falhas e os arquivos de sacrifícios.",
            "turn": "Ilyra parece trair a Coalizão ao entregar a Chave de Septúria, e Seren rompe a Igreja para tornar o arquivo copiável.",
        },
        {
            "number": 3,
            "title": "A Guerra que Alimenta a Paz",
            "regions": [9, 10, 11, 12],
            "dramatic_question": "É possível vencer sem transformar mortos, portos, trabalho e água em combustível?",
            "arc": "A campanha confronta consentimento dos mortos, soberania insular, economia de guerra e refugiados climáticos.",
            "turn": "Neris e Yrsa assumem decisões do naufrágio; Kael expõe que a própria Coalizão financiou armas com território alheio.",
        },
        {
            "number": 4,
            "title": "Quem Possui o Futuro",
            "regions": [13, 14, 15, 16],
            "dramatic_question": "O mundo precisa de um escudo central, de liberdade arriscada ou de um pacto lento e distribuído?",
            "arc": "Céu, dissuasão dracônica, água nômade e soberania ecológica convergem sobre o núcleo vivo da Primeira Fratura.",
            "turn": "O Pacto dos Dezesseis Pesos nunca foi consentido; ele precisa ser renovado, centralizado ou rompido.",
        },
    ]

    campaign_v3 = {
        "schema_version": 3,
        "title": "Asterra: Os Dezesseis Pesos",
        "logline": (
            "Quando a infraestrutura mágica que sustenta clima, rotas e colheitas falha, "
            "uma coalizão atravessa dezesseis regiões para decidir não apenas como salvar "
            "o mundo, mas quem terá o direito de governar o preço da salvação."
        ),
        "historical_truth": (
            "As Fraturas são órgãos e âncoras do Pacto dos Dezesseis Pesos, criado por "
            "anões, arcanos, dracônicos e luminários para redistribuir excedente mágico. "
            "O sistema evitou catástrofes, mas deslocou o dano para periferias sem "
            "consentimento e teve sua história convertida em mito."
        ),
        "political_thesis": (
            "Eficiência sem legitimidade produz estabilidade autoritária; autonomia sem "
            "responsabilidade comum exporta sofrimento. A rota canônica busca um pacto "
            "distribuído, verificável e sempre revogável."
        ),
        "region_count": 16,
        "stages_per_region": 10,
        "scenario_count": 160,
        "political_marks": MARKS,
        "initial_marks": {mark["id"]: 0 for mark in MARKS},
        "acts": acts,
        "supporting_cast": [
            {
                "id": "npc_edran",
                "name": "Marechal Edran",
                "role": "chefe logístico da Coalizão e traidor por lealdade provincial",
                "motivation": "salvar Valedouro da fome mesmo que precise vender rotas e destruir a confiança da Coalizão",
                "payoff": "sua confissão prova que traição crível nasce de deveres incompatíveis, não de loucura súbita",
            },
            {
                "id": "npc_ione",
                "name": "Ione dos Nomes Riscados",
                "role": "arquivista luminar e guardiã da lista de zonas sacrificadas",
                "motivation": "abrir os arquivos sem entregar refugiados e testemunhas à vingança",
                "payoff": "transforma exposição da verdade em problema de custódia e proteção, não em catarse simples",
            },
            {
                "id": "npc_suma",
                "name": "Suma Primeva",
                "role": "metamorfa perseguida e guardiã da memória da Primeira Fratura",
                "motivation": "renovar o pacto sob consentimento dos povos e do núcleo vivo",
                "payoff": "recebe de Rauk o Totem de comando e formula a terceira via do final",
            },
        ],
        "ending_routes": [
            {
                "id": "pacto_distribuido",
                "name": "Pacto Distribuído",
                "requirements": {
                    "legitimidade_coalizao": "alta",
                    "autonomia_regional": "alta",
                    "estabilidade_fraturas": "positiva",
                },
                "outcome": "dezesseis conselhos compartilham comando, auditoria e zonas de risco; a resposta é mais lenta, mas nenhum território pode ser sacrificado em segredo",
                "canonical": True,
            },
            {
                "id": "escudo_central",
                "name": "Escudo Central",
                "requirements": {
                    "poder_convergencia": "alto",
                    "estabilidade_fraturas": "muito alta",
                },
                "outcome": "o mundo estabiliza rapidamente sob um diretório permanente; oposição e deslocamentos tornam-se custos administrados",
                "canonical": False,
            },
            {
                "id": "ruptura_livre",
                "name": "Ruptura Livre",
                "requirements": {
                    "autonomia_regional": "muito alta",
                    "estabilidade_fraturas": "baixa",
                },
                "outcome": "os Pesos são rompidos; magia e ecossistemas recuperam autonomia, mas clima e rotas entram em uma era de incerteza",
                "canonical": False,
            },
        ],
        "region_arcs": [
            {
                "region_id": region["id"],
                "title": region["name"],
                "political_conflict": PROFILES[region["family_id"]]["grievance"],
                "betrayal_or_reversal": PROFILES[region["family_id"]]["betrayal"],
                "resolution": PROFILES[region["family_id"]]["resolution"],
                "stages": [
                    scenario["id"]
                    for scenario in scenarios_v3
                    if scenario["region_id"] == region["id"]
                ],
            }
            for region in regions_v2
        ],
        "scenario_ids": [scenario["id"] for scenario in scenarios_v3],
        "catalog_scope": {
            "character_classes": 240,
            "troop_classes": 144,
            "policy": "catálogo completo preservado; narrativa não inventa novas árvores de classe nem exige uma mecânica exclusiva por entrada",
        },
        "source_version": old_campaign["schema_version"],
    }

    write_json(
        "regioes_v_2.json",
        {"schema_version": 2, "count": len(regions_v2), "regions": regions_v2},
    )
    write_json(
        "personagens_v_2.json",
        {
            "schema_version": 2,
            "count": len(characters_v2),
            "characters": characters_v2,
        },
    )
    write_json("campanha_v_3.json", campaign_v3)
    write_json(
        "cenarios_v_3.json",
        {
            "schema_version": 3,
            "count": len(scenarios_v3),
            "regions": 16,
            "stages_per_region": 10,
            "scenarios": scenarios_v3,
        },
    )

    lines = [
        "# Asterra — História e Campanha v2",
        "",
        "## Premissa revisada",
        "",
        campaign_v3["logline"],
        "",
        "## Verdade histórica",
        "",
        campaign_v3["historical_truth"],
        "",
        "## Marcas Políticas",
        "",
    ]
    for mark in MARKS:
        lines.append(f"- **{mark['name']}** — {mark['meaning']}.")
    for region in regions_v2:
        family = region["family_id"]
        profile = PROFILES[family]
        hero = characters_by_family[family]["hero"]["name"]
        rival = characters_by_family[family]["rival"]["name"]
        lines.extend(
            [
                "",
                f"## Região {old_regions.index(next(r for r in old_regions if r['id'] == region['id'])) + 1} — {region['name']}",
                "",
                f"**Política e economia.** {profile['governance'].capitalize()}. {profile['economy'].capitalize()}.",
                "",
                f"**Conflito territorial.** {profile['territory'].capitalize()}. {profile['grievance']}",
                "",
                f"**{hero} × {rival}.** {profile['hero_goal']} Em oposição, {profile['rival_goal'][0].lower() + profile['rival_goal'][1:]}.",
                "",
                f"**Reversão.** {profile['betrayal']}",
                "",
            ]
        )
        for scenario in (s for s in scenarios_v3 if s["region_id"] == region["id"]):
            narrative = scenario["narrative"]
            marks = ", ".join(
                f"{key} {value:+d}"
                for key, value in narrative["political_marks"]["canonical_route"].items()
            )
            pre = " / ".join(
                f"{line['speaker']}: “{line['line']}”"
                for line in narrative["pre_battle_dialogue"]
            )
            post = " / ".join(
                f"{line['speaker']}: “{line['line']}”"
                for line in narrative["post_battle_dialogue"]
            )
            lines.extend(
                [
                    f"### {scenario['stage_in_region']}. {scenario['name']}",
                    "",
                    f"**Contexto histórico:** {narrative['historical_context']}",
                    "",
                    f"**Antes:** {pre}",
                    "",
                    f"**Depois:** {post}",
                    "",
                    f"**Marcas:** {marks}.",
                    "",
                    f"**Dilema:** {narrative['moral_dilemma']}",
                    "",
                    f"**Justificativa tática:** {narrative['level_design_justification']} {narrative['enemy_justification']}",
                    "",
                ]
            )
    (DOCS / "HISTORIA_E_CAMPANHA_v_2.md").write_text(
        "\n".join(lines).strip() + "\n", encoding="utf-8"
    )

    audit = """# Auditoria Narrativa v1

## Alertas vermelhos encontrados na v1

- A Convergência era um inimigo funcional, porém abstrato: faltavam benefícios concretos que explicassem adesões.
- Heróis e rivais repetiam a mesma motivação em dezesseis skins, anulando conflito de personagem.
- Cada região reiniciava o arco em vez de pagar consequências do ato anterior.
- A Fratura era apenas ameaça e não instituição histórica; por isso política, economia e mapa não se cruzavam.
- “Selar a Fratura” resolvia conflitos locais complexos com uma ação final genérica.
- Traições não tinham custo material nem dever conflitante que as tornasse críveis.

## Correções aplicadas

- As Fraturas agora são os Dezesseis Pesos: infraestrutura necessária, injusta e historicamente falsificada.
- Toda facção possui governo, economia, território, ressentimento, demanda à Coalizão e oferta concreta da Convergência.
- Cada herói participa do problema que tenta resolver; cada rival diagnostica uma ameaça real e escolhe coerção.
- Os quatro atos têm pergunta dramática, revelação e consequência que atravessam regiões.
- Cada um dos 160 estágios contém contexto, diálogo antes/depois, dilema, revelação, Marcas Políticas e justificativa tática.
- O final possui três rotas ideológicas; a rota canônica é o Pacto Distribuído, não uma vitória sem custo.

## Ritmo

- Estágios 1–2: entrada e disputa do recurso.
- Estágio 3: testemunho ou pessoa que humaniza o conflito.
- Estágios 4–5: retaliação e primeira revelação.
- Estágio 6: cisão institucional e escolha irreversível.
- Estágios 7–8: cerco e custo civil.
- Estágio 9: perseguição com acerto de contas.
- Estágio 10: pacto regional que altera a leitura do conflito global.

## Limite de escopo

O trabalho amplia roteiro, dados e apresentação. Não cria novas árvores de classe, famílias, economias paralelas ou uma mecânica exclusiva por estágio. As 240 classes e 144 tropas permanecem catálogo de design e conteúdo jogável compartilhado.
"""
    (DOCS / "AUDITORIA_NARRATIVA_v_1.md").write_text(audit, encoding="utf-8")

    sources = """# Referências Históricas de Design Narrativo v1

Princípios estudados; nenhum personagem, diálogo, cenário ou nomenclatura foi copiado.

- **Tactics Ogre: Reborn** — facções em guerra civil, decisões que alteram alianças e personagens capazes de romper com o jogador por ideologia. Fonte oficial: https://tactics-ogre.square-enix-games.com/en-us/ e https://amp.square-enix-games.com/en_US/news/tactics-ogre-reborn-preview
- **Final Fantasy Tactics: The Ivalice Chronicles** — sucessão pós-guerra, regência, rivalidade entre elites e conflito de classe encarnado em trajetórias pessoais. Fonte oficial: https://final-fantasy-tactics-the-ivalice-chronicles.square-enix-games.com/en-us
- **Fire Emblem: Three Houses** — territórios concorrentes, instituição religiosa central, escolha de caminho e relações de personagem ligadas ao combate. Fonte oficial: https://www.nintendo.com/us/store/products/fire-emblem-three-houses-switch/ e https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/Fire-Emblem-Three-Houses-1175482.html
- **Fire Emblem Engage — Ask the Developer** — contraste declarado entre drama histórico de rotas e uma estrutura tática mais acessível. Fonte oficial: https://www.nintendo.com/en-gb/News/2023/January/Ask-the-Developer-Vol-8-Fire-Emblem-Engage-Chapter-1-2328361.html
- **Langrisser** — tradição de linhas narrativas ramificadas em que o jogador pode aderir a forças ideologicamente distintas. Fonte oficial: https://langrisser.zlongame.com/hd/202207/pc/

Aplicação em Asterra: política material, rivais defensáveis, traições por dever incompatível, consequências registradas por Marcas Políticas e escolhas finais sem solução moral perfeita.
"""
    (DOCS / "FONTES_NARRATIVAS_v_1.md").write_text(sources, encoding="utf-8")


if __name__ == "__main__":
    build()
