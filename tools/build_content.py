"""Gera os catálogos integrais e auditáveis do jogo a partir de matrizes autorais."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def slug(text: str) -> str:
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", plain).strip("_")


FAMILIES = [
    {"id":"humano","name":"Humanos","identity":"disciplina, adaptabilidade e comando","region":"Reinos da Coroa Partida","capital":"Valedouro","terrain":"planícies, fortalezas e estradas","palette":["azul aço","marfim","ouro"],"trait":"formações coordenadas","cost":1.0},
    {"id":"elfo","name":"Elfos Silvestres","identity":"precisão, floresta e mobilidade","region":"Bosque de Lythara","capital":"Copa de Elarin","terrain":"florestas antigas e passarelas vivas","palette":["verde musgo","âmbar","prata"],"trait":"vantagem em cobertura natural","cost":1.2},
    {"id":"orc","name":"Orcs","identity":"ímpeto, moral ofensiva e força","region":"Terras Rubras","capital":"Khar-Dumak","terrain":"estepes, cânions e arenas","palette":["vermelho óxido","carvão","osso"],"trait":"ímpeto após avançar","cost":0.9},
    {"id":"goblin","name":"Goblins","identity":"número, engenho e oportunismo","region":"Liga das Engrenagens","capital":"Trinco-Fundo","terrain":"pântanos, sucata e túneis","palette":["verde ácido","cobre","preto"],"trait":"baixo CAP e reposicionamento","cost":0.7},
    {"id":"anao","name":"Anões","identity":"armadura, engenharia e resistência","region":"Montanhas de Karad","capital":"Forja-Mãe","terrain":"montanhas, salões e minas","palette":["bronze","granito","azul rúnico"],"trait":"bloqueio e ruptura","cost":1.3},
    {"id":"arcano","name":"Arcanos","identity":"mana, manipulação e conhecimento","region":"Círculo de Aether","capital":"Septúria","terrain":"ilhas flutuantes e observatórios","palette":["violeta","ciano","branco"],"trait":"flexibilidade mágica","cost":1.35},
    {"id":"luz","name":"Luminares","identity":"proteção, cura e convicção","region":"Domínios da Aurora","capital":"Helianto","terrain":"vales solares e basílicas","palette":["branco","ouro","azul celeste"],"trait":"proteção e recuperação","cost":1.15},
    {"id":"sombrio","name":"Umbrais","identity":"furtividade, medo e maldições","region":"Véu de Nox","capital":"Umbracorte","terrain":"charnecas, ruínas e névoa","palette":["índigo","preto","magenta"],"trait":"debilitação e emboscada","cost":1.05},
    {"id":"necromante","name":"Necromantes","identity":"controle de mortos e desgaste","region":"Ossuário de Morvath","capital":"Necrópole Cinzenta","terrain":"cemitérios, salinas e criptas","palette":["cinza osso","verde espectral","vinho"],"trait":"invocações temporárias","cost":1.0},
    {"id":"mares","name":"Povos das Marés","identity":"fluxo, cura e terreno molhado","region":"Arquipélago de Nymar","capital":"Porto-Coral","terrain":"ilhas, recifes e canais","palette":["turquesa","coral","azul profundo"],"trait":"adaptação anfíbia","cost":1.0},
    {"id":"chama","name":"Nascidos da Chama","identity":"pressão, queimadura e risco","region":"Caldeira de Pyr","capital":"Cinerária","terrain":"vulcões, cinza e fundições","palette":["laranja","escarlate","obsidiana"],"trait":"dano crescente por queimadura","cost":1.15},
    {"id":"geada","name":"Nascidos da Geada","identity":"controle, defesa e lentidão","region":"Coroa Invernal","capital":"Skeld","terrain":"geleiras, fiordes e cavernas","palette":["azul gelo","prata","branco"],"trait":"controle de movimento","cost":1.15},
    {"id":"avariano","name":"Avarianos","identity":"voo, ângulo e resgate","region":"Picos de Avar","capital":"Ninho do Zênite","terrain":"picos, pontes e correntes aéreas","palette":["azul céu","ocre","branco"],"trait":"mobilidade aérea limitada pelo mapa","cost":1.3},
    {"id":"draconico","name":"Dracônicos","identity":"poder, presença e herança elemental","region":"Escamas Ancestrais","capital":"Drak-Azur","terrain":"mesetas, vulcões e templos","palette":["bronze","esmeralda","carmesim"],"trait":"alto poder e alto CAP","cost":1.55},
    {"id":"deserto","name":"Povos do Deserto","identity":"mobilidade, atrito e sobrevivência","region":"Mar de Safira","capital":"Qasr-Sahir","terrain":"dunas, oásis e cânions","palette":["areia","azul safira","cobre"],"trait":"ignora parte do atrito do terreno","cost":0.95},
    {"id":"bestial","name":"Clãs Bestiais","identity":"instinto, sentidos e transformação","region":"Fronteira Primeva","capital":"Pedra-Uivo","terrain":"selvas, savanas e cavernas","palette":["ocre","verde escuro","marrom"],"trait":"sentidos e ataques naturais","cost":1.0}
]


CLASS_TREES = {
"humano":["Aspirante Humano","Guerreiro","Oficial","Cavaleiro","Mestre da Espada","Capitão","Estrategista","Paladino","Espadachim","General","Comandante Tático","Campeão Real","Lâmina Suprema","Grande Marechal","Senhor da Estratégia"],
"elfo":["Iniciado do Bosque","Batedor Silvestre","Místico Verde","Olho da Floresta","Dançarino de Lâminas","Guardião dos Círculos","Tecelão de Raízes","Arqueiro Lunar","Lâmina das Folhas","Druida Ancião","Vidente dos Caminhos","Flecha do Horizonte","Dança-Eterna","Coração da Floresta","Oráculo de Lythara"],
"orc":["Jovem do Clã","Brutamontes","Porta-Voz","Berserker","Quebra-Escudos","Chefe de Guerra","Xamã de Sangue","Devastador","Muralha de Presas","Grande Khan","Leitor de Cicatrizes","Fúria Ancestral","Punho da Horda","Senhor dos Clãs","Profeta da Guerra"],
"goblin":["Catador Goblin","Saqueador","Funileiro","Cavaleiro de Lobo","Apunhalador","Mestre de Bando","Alquimista de Sucata","Raptor da Lama","Sombra Miúda","Rei de Bando","Engenhoqueiro","Lança-Rápida","Faca Invisível","Grão-Chefe","Arquiteto do Caos"],
"anao":["Aprendiz da Forja","Guerreiro do Salão","Artífice Rúnico","Guarda de Ferro","Rompedor","Capitão da Mina","Gravador de Runas","Rei da Fortaleza","Martelo Profundo","Mestre Engenheiro","Tecelão de Pedra","Bastião Eterno","Quebra-Montanhas","Senhor das Forjas","Arquimante Rúnico"],
"arcano":["Adepto do Aether","Evocador","Manipulador","Mago de Batalha","Canalizador","Cronista Arcano","Ilusionista","Arconte Elemental","Condutor Supremo","Mestre do Tempo","Dobrador do Espaço","Avatar do Aether","Fonte Viva","Guardião das Eras","Soberano do Impossível"],
"luz":["Acólito da Aurora","Templário","Clérigo","Guardião Solar","Inquisidor","Curador Radiante","Arauto","Paladino do Alvorecer","Juiz Solar","Santo de Campanha","Porta-Luz","Campeão da Aurora","Veredito Vivo","Milagre Encarnado","Farol Eterno"],
"sombrio":["Tocado pelo Véu","Lâmina Umbral","Ocultista","Assassino da Névoa","Ceifador do Medo","Bruxo das Correntes","Tecelão de Pesadelos","Sombra Perfeita","Carrasco Noturno","Senhor das Maldições","Arquiteto do Pavor","Ausência Silenciosa","Lua Sangrenta","Rei do Véu","Sonho Devorador"],
"necromante":["Discípulo do Ossuário","Guardião Fúnebre","Invocador","Cavaleiro Ósseo","Ceifador","Pastor de Mortos","Espiritualista","General Imortal","Lâmina Cadavérica","Mestre do Ossuário","Senhor de Espectros","Rei Sem Pulso","Último Ceifador","Legião Encarnada","Portal dos Ancestrais"],
"mares":["Filho das Marés","Guerreiro de Coral","Místico das Águas","Navegante de Lança","Guardião do Recife","Curador de Maré","Tecelão de Correntes","Almirante Abissal","Bastião Coralino","Oráculo das Águas","Senhor das Tormentas","Leviatã de Guerra","Muralha do Oceano","Fonte Primordial","Voz da Tempestade"],
"chama":["Nascido da Chama","Guerreiro Ígneo","Piromante","Cavaleiro da Brasa","Carrasco Incandescente","Conjurador de Fogo","Tecelão de Cinzas","Senhor da Labareda","Coração Vulcânico","Mestre da Chama","Arquiteto da Caldeira","Avatar do Incêndio","Montanha Viva","Sol Devastador","Soberano das Cinzas"],
"geada":["Nascido da Geada","Guardião Glacial","Criomante","Cavaleiro Glacial","Bastião de Gelo","Conjurador de Geada","Tecelão do Inverno","Senhor da Lança Glacial","Muralha Viva","Mestre da Geada","Arquiteto do Inverno","Coração do Inverno","Fortaleza Glacial","Inverno Eterno","Soberano da Geada"],
"avariano":["Nascido dos Céus","Caçador dos Céus","Guardião Alado","Arqueiro Celeste","Raptor","Sentinela Alada","Porta-Escudo Celeste","Olho do Zênite","Garra da Tempestade","Vigia das Correntes","Resgatador Solar","Horizonte Vivo","Predador Supremo","Muralha do Firmamento","Asa da Salvação"],
"draconico":["Sangue de Dragão","Dracomante","Guerreiro de Escamas","Sopro Elemental","Guardião Rúnico","Lanceiro Dracônico","Arauto Ancestral","Coração de Fogo","Tempestade Alada","Escudo de Escamas","Voz dos Antigos","Avatar Dracônico","Garra Celestial","Bastião Ancestral","Herdeiro do Primeiro"],
"deserto":["Andarilho das Dunas","Nômade da Lâmina","Místico da Miragem","Cavaleiro do Vento","Duelista de Safira","Guardião do Oásis","Tecelão de Areia","Khan das Dunas","Lâmina do Poente","Sábio do Oásis","Senhor das Miragens","Tempestade Nômade","Horizonte Cortante","Fonte do Deserto","Sol Velado"],
"bestial":["Desperto Primevo","Caçador Feral","Totemista","Predador","Guardião da Alcateia","Xamã das Presas","Metamorfo","Alfa Implacável","Pele de Pedra","Voz dos Totens","Forma Quimérica","Rei da Caçada","Bastião Primevo","Espírito Ancestral","Fera Perfeita"]
}


TROOPS = {
"humano":["Recrutas da Coroa","Espadachins da Linha","Lanceiros de Fronteira","Arqueiros de Campanha","Besteiros de Cerco","Cavalaria Leve","Guarda Real","Cavaleiros Pesados","Veteranos do Estandarte"],
"elfo":["Batedores do Bosque","Arqueiros Verdes","Lanceiros das Folhas","Dançarinos Silvestres","Guardiões de Raiz","Montadores de Cervo","Olhos Lunares","Círculo Druídico","Sentinelas Anciãs"],
"orc":["Guerreiros Jovens","Lanceiros do Clã","Caçadores Orcs","Berserkers","Quebra-Escudos","Montadores de Javali","Guardas do Khan","Tambores de Guerra","Campeões da Horda"],
"goblin":["Lanceiros Goblins","Atiradores de Funda","Catadores","Cavaleiros de Lobo","Bombardeiros de Sucata","Esfaqueadores","Guardas do Grão-Chefe","Artilheiros de Engrenagem","Matilha Escarlate"],
"anao":["Guardas da Mina","Besteiros Anões","Escudeiros de Ferro","Fuzileiros Rúnicos","Martelos de Cerco","Sapadores","Guardas de Ferro","Canhões de Salão","Bastiões Rúnicos"],
"arcano":["Ajudantes Arcanos","Sentinelas de Mana","Atiradores de Aether","Golens Menores","Evocadores de Campo","Ilusionistas","Golens de Guerra","Baterias Arcanas","Círculo de Arquimagos"],
"luz":["Novatos da Aurora","Escudeiros Solares","Acólitos Curadores","Templários","Arqueiros Radiantes","Porta-Estandartes","Guardas do Alvorecer","Coro de Batalha","Juízes Solares"],
"sombrio":["Batedores do Véu","Lâminas Sombrias","Atiradores da Névoa","Assassinos Umbrais","Bruxos de Campo","Caçadores do Medo","Carrascos Noturnos","Círculo de Maldições","Sombras Vivas"],
"necromante":["Cultistas do Ossuário","Esqueletos Temporários","Arqueiros Ósseos","Guardas Cadavéricos","Cavaleiros Esqueléticos","Aparições","Guerreiros Revenantes","Coro Espectral","Colosso de Ossos"],
"mares":["Marinheiros de Coral","Lanceiros Anfíbios","Atiradores de Concha","Guardiões do Recife","Curadores de Maré","Cavaleiros de Hipocampo","Bastiões Coralinos","Conjuradores de Tormenta","Leviatãs Jovens"],
"chama":["Guardas da Brasa","Lanceiros Ígneos","Atiradores de Cinza","Guerreiros Incandescentes","Piromantes de Campo","Cavalaria de Salamandra","Bastiões Vulcânicos","Bombardeiros de Magma","Avatares Menores"],
"geada":["Guardas da Geada","Lanceiros Glaciais","Arqueiros da Geada","Escudeiros de Gelo","Criomantes de Campo","Cavaleiros Glaciais","Guardas Cristalinos","Tecelões de Nevasca","Bastiões de Permafrost"],
"avariano":["Batedores Alados","Arqueiros Avarianos","Lanceiros Alados","Sentinelas do Ninho","Raptors","Resgatadores","Guardas Celestes","Atiradores do Zênite","Falange do Firmamento"],
"draconico":["Draconatos Jovens","Lanceiros de Escama","Atiradores de Sopro","Guardas Dragão","Garras de Assalto","Arautos","Bastiões Dracônicos","Tempestários","Herdeiros Alados"],
"deserto":["Batedores das Dunas","Lanceiros Nômades","Arqueiros do Oásis","Cavaleiros do Vento","Duelistas de Safira","Tecelões de Areia","Guardas do Khan","Atiradores de Miragem","Tempestade Montada"],
"bestial":["Caçadores da Alcateia","Lanceiros de Osso","Atiradores Feral","Predadores","Guardiões Totêmicos","Xamãs de Campo","Peles de Pedra","Quimeras","Alfas da Caçada"]
}


ROLES = ["linha","distancia","controle","mobilidade","defesa","suporte","ruptura","comando","especialista"]
TIER_BY_INDEX = [1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]
PARENT_BY_INDEX = [None, 0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10]
BRANCH_ROLE = ["hibrido","marcial","mistico","assalto","defesa","lideranca","controle","assalto","defesa","lideranca","controle","assalto","defesa","lideranca","controle"]
ROLE_STATS = {
    "linha":(14,6,5,4,1),"distancia":(10,6,3,4,4),"controle":(11,5,4,4,3),
    "mobilidade":(11,6,3,6,2),"defesa":(18,5,8,3,1),"suporte":(12,4,5,4,3),
    "ruptura":(15,8,4,4,1),"comando":(13,5,5,4,2),"especialista":(12,7,4,4,3)
}


def infer_troop_role(name: str, index: int) -> str:
    key = slug(name)
    if any(word in key for word in ("arqueir", "atirador", "besteir", "funda", "fuzileir")):
        return "distancia"
    if any(word in key for word in ("lanceir", "piqueir")):
        return "controle"
    if any(word in key for word in ("caval", "montador", "lobo", "javali", "hipocampo", "raptor", "tempestade_montada")):
        return "mobilidade"
    if any(word in key for word in ("guarda", "bastiao", "escudeir", "sentinela", "pele_de_pedra", "muralha")):
        return "defesa"
    if any(word in key for word in ("curador", "acolito", "porta_estandarte", "coro", "resgatador", "ajudante")):
        return "suporte"
    if any(word in key for word in ("canhao", "bombardeir", "martelo", "colosso", "quebra", "artilheiro")):
        return "ruptura"
    if any(word in key for word in ("mante", "mago", "brux", "xama", "tecela", "conjurador", "circulo")):
        return "especialista"
    return "linha" if index < 6 else "comando"


def build_classes():
    records = []
    for family in FAMILIES:
        names = CLASS_TREES[family["id"]]
        assert len(names) == 15
        ids = [f"classe_{family['id']}_{slug(name)}" for name in names]
        for index, name in enumerate(names):
            tier = TIER_BY_INDEX[index]
            role = BRANCH_ROLE[index]
            parent = None if PARENT_BY_INDEX[index] is None else ids[PARENT_BY_INDEX[index]]
            records.append({
                "id": ids[index], "name": name, "family_id": family["id"], "tier": tier,
                "parent_id": parent, "role": role,
                "identity": f"{name} expressa {family['identity']} pelo papel de {role}.",
                "signature": f"{name}: converte {family['trait']} em uma decisão de {role}, sem bônus universais.",
                "gameplay": f"Prioriza {role}; exige posicionamento e preserva a fraqueza contra respostas especializadas.",
                "visual": {"silhouette": f"silhueta {role} de {family['name']}", "palette": family["palette"], "motif": family["trait"]},
                "growth": {"forca": 1 + (role in {"marcial","assalto"}) * 2, "vigor": 1 + (role == "defesa") * 3, "destreza": 1 + (role == "assalto") * 2, "mente": 1 + (role in {"mistico","controle"}) * 3, "presenca": 1 + (role == "lideranca") * 3},
                "implementation_status": "catalogo_completo_v1"
            })
    return records


def build_troops():
    records = []
    for family in FAMILIES:
        names = TROOPS[family["id"]]
        assert len(names) == 9
        for index, name in enumerate(names):
            tier = index // 3 + 1
            role = infer_troop_role(name, index)
            hp, attack, defense, movement, attack_range = ROLE_STATS[role]
            scale = tier - 1
            records.append({
                "id": f"tropa_{family['id']}_{slug(name)}", "name": name, "family_id": family["id"],
                "tier": tier, "role": role,
                "stats": {"hp": hp + scale * 4, "attack": attack + scale * 2, "defense": defense + scale * 2, "movement": movement, "range": attack_range},
                "cap_cost": min(5, tier + (role in {"defesa","ruptura"})),
                "recruit_cost_cu": round((8 + tier * 9 + (role in {"defesa","ruptura"}) * 3) * family["cost"]),
                "mobilization_supply": tier + (family["id"] in {"anao","avariano","draconico"}),
                "signature": f"{family['trait']} aplicado à função de {role}.",
                "tactical_use": f"Cumpre {role} quando a formação explora {family['identity']}.",
                "weakness": {"linha":"ruptura","distancia":"corpo a corpo","controle":"pressão direta","mobilidade":"bloqueio","defesa":"anti-armadura","suporte":"foco inimigo","ruptura":"controle","comando":"isolamento","especialista":"condição desfavorável"}[role],
                "preferred_mode": {"defesa":"DEFESA","suporte":"DEFESA","mobilidade":"LIVRE","controle":"LIVRE"}.get(role,"ATAQUE"),
                "visual": {"palette": family["palette"], "equipment_language": family["trait"]}
            })
    return records


HERO_NAMES = ["Alda Varen","Sylwen Aeril","Gorak Três-Marcas","Nix Parafuso","Dhorin Karad","Ilyra Septa","Seren Helianto","Nyx Vesper","Mara Ossária","Neris Coral","Kael Pyr","Yrsa Skeld","Aren Zênite","Varkesh Azur","Samira Sahir","Rauk Pedra-Uivo"]
RIVAL_NAMES = ["Regente Cael","Thalan Espinho","Maug Sem-Clã","Grizna Estopim","Vorik Cinza","Magíster Oryn","Prelado Solmar","Dama Vanta","Arquimorto Veyr","Corsária Nereth","Cônsul Brasa","Jarl Hroth","Garra Silex","Sarthax Rubro","Vizir Namar","Urrak Lua-Cega"]


def build_world():
    regions, characters = [], []
    for index, family in enumerate(FAMILIES):
        regions.append({
            "id": f"regiao_{family['id']}", "name": family["region"], "family_id": family["id"],
            "capital": family["capital"], "terrain": family["terrain"],
            "identity": family["identity"], "strategic_resource": ["ouro","suprimentos","reputação"][index % 3],
            "conflict": f"A Fratura desestabiliza {family['trait']} e divide as lideranças locais.",
            "art_direction": {"palette": family["palette"], "landmark": f"marco de {family['trait']}"}
        })
        root_class = f"classe_{family['id']}_{slug(CLASS_TREES[family['id']][0])}"
        characters.extend([
            {"id":f"heroi_{family['id']}","name":HERO_NAMES[index],"family_id":family["id"],"alignment":"Coalizão","starting_class_id":root_class,"goal":f"proteger {family['region']} sem sacrificar sua autonomia","internal_conflict":"dever contra identidade","visual":{"palette":family["palette"],"silhouette":"comandante legível a distância","motif":family["trait"]}},
            {"id":f"rival_{family['id']}","name":RIVAL_NAMES[index],"family_id":family["id"],"alignment":"Convergência","starting_class_id":root_class,"goal":f"usar a Fratura para controlar {family['region']}","internal_conflict":"ordem imposta contra sobrevivência","visual":{"palette":list(reversed(family["palette"])),"silhouette":"rival angular e assimétrico","motif":"fragmento da Fratura"}}
        ])
    return regions, characters


MAP_TEMPLATES = [
    ["..........","..F..F....","..F.......",".....#....","..B..#....",".....#....","..........","....O....."],
    ["..M....M..","..M....M..",".....F....",".##..F..#.",".....F....","..M....M..","..M....M..","....O....."],
    ["~~..~~..~~","~~..~~..~~","....B.....","..##..##..",".....B....","~~..~~..~~","~~..~~..~~","....O....."],
    ["....#.....",".F..#..F..","....#.....","..B....B..",".....#....",".F..#..F..","....#.....","....O....."]
]


def build_campaign_v1():
    scenarios = []
    scenario_names = ["A Ponte Partida","Ecos no Bosque","O Juramento Rubro","Engrenagens na Névoa","A Forja Silenciada","A Torre Impossível","Aurora Cercada","Sob o Véu","Ossos que Marcham","Maré de Cinzas","Coração da Caldeira","O Último Inverno"]
    for index, name in enumerate(scenario_names):
        family = FAMILIES[index]
        scenarios.append({
            "id":f"cenario_{index+1:02d}","order":index+1,"act":index//4+1,"name":name,
            "region_id":f"regiao_{family['id']}","map_id":f"mapa_{index+1:02d}",
            "premise":f"A Coalizão entra em {family['region']} para impedir que a Convergência domine a Fratura local.",
            "objective":"derrotar o comandante inimigo","optional_objective":"controlar o marco O ao final de uma rodada",
            "player_commander":"cmd_vanguarda" if index < 4 else "cmd_estrategista",
            "enemy_commander":"cmd_bastiao" if index % 2 == 0 else "cmd_hibrido",
            "reward":{"ouro":30+index*5,"suprimentos":4+index//3,"reputacao_family_id":family["id"]},
            "story_beat":["formação da Coalizão","revelação das Fraturas","cerco à Convergência"][index//4]
        })
    maps = []
    for index, scenario in enumerate(scenarios):
        grid = MAP_TEMPLATES[index % len(MAP_TEMPLATES)]
        maps.append({
            "id":scenario["map_id"],"name":scenario["name"],"width":10,"height":8,"grid":grid,
            "legend":{".":"chão","F":"floresta/cobertura","#":"parede","M":"elevação","~":"água","B":"bloqueio","O":"objetivo"},
            "blue_spawns":[[0,1],[0,3],[0,5]],"red_spawns":[[9,1],[9,3],[9,5]]
        })
    campaign = {
        "title":"Asterra: As Dezesseis Fraturas","logline":"Dezesseis povos precisam formar uma coalizão antes que a Convergência transforme as Fraturas do mundo em uma única ordem militar.",
        "acts":[
            {"number":1,"title":"Sinais da Ruptura","chapters":[1,2,3,4],"arc":"Alda reúne os primeiros aliados e descobre que as crises regionais compartilham uma origem."},
            {"number":2,"title":"A Marcha da Convergência","chapters":[5,6,7,8],"arc":"A guerra revela que cada solução absoluta alimenta a Fratura central."},
            {"number":3,"title":"O Conselho das Dezesseis","chapters":[9,10,11,12],"arc":"A Coalizão aceita diferenças táticas e fecha a Fratura sem apagar as culturas."}
        ],
        "ending":"A vitória preserva as dezesseis regiões e abre a campanha pós-jogo de reconstrução e conflitos locais.",
        "scenario_ids":[item["id"] for item in scenarios]
    }
    return campaign, scenarios, maps


REGION_STAGE_TITLES = {
    "humano":["A Estrada Sem Bandeira","Pedágio de Sangue","O Estandarte Perdido","Sete Sinos de Alarme","Correio da Convergência","Praça dos Juramentos","A Noite das Muralhas","A Última Caravana","O Regente em Fuga","Coroa Partida"],
    "elfo":["Pegadas sob Lythara","Clareira Disputada","Sementes em Marcha","A Caçada da Lua Nova","Flecha entre as Copas","O Círculo Ferido","Chuva de Folhas Negras","Ponte de Raízes","O Veado de Vidro","Coração do Bosque"],
    "orc":["Poeira de Khar-Dumak","Arena dos Três Clãs","A Marcha do Ferreiro","Tambores no Cânion","O Porta-Voz Capturado","Desfiladeiro das Presas","Cerco da Lua Rubra","A Coluna Sem-Clã","Caçada ao Estandarte","Juramento da Horda"],
    "goblin":["Parafusos na Lama","Pátio das Caldeiras","Comboio de Sucata","Fumaça no Túnel","O Mapa Roubado","Trinco-Fundo","Pântano Eletrizado","A Bomba Ambulante","Lobo Mensageiro","Rei das Engrenagens"],
    "anao":["Portões de Karad","Trilhos da Mina","O Engenheiro Ferido","Colapso no Salão","Runas Contrabandeadas","Forja-Mãe","A Ponte dos Martelos","Êxodo do Poço Nove","O Trem de Cerco","Trono de Granito"],
    "arcano":["Escada para o Aether","Observatório Quebrado","O Aprendiz Instável","Minutos Roubados","A Chave de Septúria","Sete Círculos","Queda sem Chão","O Prisma Errante","Fuga pelo Impossível","A Torre que se Repete"],
    "luz":["Peregrinos da Aurora","Adro em Disputa","Procissão sob Flechas","Vigília dos Sete Sóis","O Falso Prelado","Nave da Basílica","Noite sem Milagres","Relicário em Marcha","O Inquisidor Fugitivo","Julgamento de Helianto"],
    "sombrio":["Névoa sobre Nox","Pátio sem Sombras","A Testemunha Velada","Sussurros até o Amanhecer","Máscara em Fuga","Umbracorte","Medo na Charneca","Lanterna dos Condenados","O Assassino sem Rosto","Rasgar o Véu"],
    "necromante":["Sinos do Ossuário","Salão das Lápides","O Coveiro Vivo","Seis Turnos até a Lua","Filactério Roubado","Necrópole Cinzenta","Maré de Ossos","A Última Pira","O Arauto sem Pulso","Portões de Morvath"],
    "mares":["Maré de Chegada","Recife Partido","Barca dos Curadores","Olho da Tormenta","Corsário do Coral","Canais de Nymar","Cerco na Maré Baixa","O Farol Flutuante","Leviatã em Retirada","Trono Abissal"],
    "chama":["Cinzas na Estrada","Pátio da Fundição","Caravana de Água","Até a Lava Subir","O Portador da Brasa","Cinerária","Chuva Incandescente","O Coração Refrigerado","Salamandra em Fuga","Boca da Caldeira"],
    "geada":["Primeiro Gelo","Fiorde Disputado","Trenó dos Feridos","A Longa Noite","Batedor na Nevasca","Muralhas de Skeld","Lago que se Parte","A Chama Escoltada","O Jarl em Retirada","Coroa Invernal"],
    "avariano":["Sombra sobre Avar","Plataforma dos Ventos","Resgate no Abismo","Olho do Furacão","Mensageiro do Zênite","Pontes do Ninho","Céu Fechado","Ovo Solar","Garra em Fuga","Batalha do Firmamento"],
    "draconico":["Escamas na Meseta","Templo das Garras","O Herdeiro Ferido","Sopro sobre o Vale","Arauto Ancestral","Drak-Azur","Chuva de Brasas","O Ovo Primordial","Sarthax em Fuga","Despertar do Primeiro"],
    "deserto":["Pegadas de Safira","Oásis Disputado","Caravana das Miragens","Sol do Meio-Dia","Vizir entre as Dunas","Qasr-Sahir","Tempestade de Vidro","A Fonte Nômade","Falcão em Fuga","Horizonte Velado"],
    "bestial":["Rastros Primevos","Círculo dos Totens","A Alcateia Ferida","Noite dos Predadores","Caçador Marcado","Pedra-Uivo","Selva sem Pássaros","O Totem Errante","Alfa em Fuga","Rugido da Fratura"],
}


STAGE_DESIGNS = [
    {"victory_condition":"defeat_commander","objective":"romper a patrulha e derrotar o comandante inimigo","counter":"linha compacta","punishes":"avanço frontal sem reconhecimento","recommended_roles":["distancia","mobilidade"],"twist":"duas rotas laterais permitem negar a reação da linha"},
    {"victory_condition":"control_area","objective":"controlar o marco central por 2 rodadas consecutivas","round_limit":8,"control_required":2,"counter":"pressão à distância","punishes":"formação imóvel no objetivo","recommended_roles":["defesa","mobilidade"],"twist":"o ponto aberto exige alternar ocupante e cobertura"},
    {"victory_condition":"escort","objective":"escoltar a segunda tropa até a saída E","round_limit":10,"counter":"interdição de corredores","punishes":"escolta isolada ou toda a força agrupada","recommended_roles":["suporte","controle"],"twist":"a rota curta é exposta; a segura consome rodadas"},
    {"victory_condition":"survive","objective":"manter o comandante vivo por 6 rodadas","round_limit":6,"counter":"ondas de assalto","punishes":"gastar reações e CMD cedo demais","recommended_roles":["defesa","suporte"],"twist":"posições seguras perdem valor conforme o cerco fecha"},
    {"victory_condition":"intercept","objective":"interceptar a segunda tropa inimiga antes que alcance E","round_limit":8,"counter":"alta mobilidade","punishes":"tropas pesadas sem cobertura de alcance","recommended_roles":["mobilidade","distancia"],"twist":"bloquear a saída compra tempo, mas expõe o bloqueador"},
    {"victory_condition":"control_area","objective":"controlar o marco avançado por 3 rodadas consecutivas","round_limit":9,"control_required":3,"counter":"anti-armadura","punishes":"depender apenas de defensores pesados","recommended_roles":["controle","ruptura"],"twist":"o inimigo contesta o ponto e zera o progresso"},
    {"victory_condition":"survive","objective":"resistir por 7 rodadas sem perder o comandante","round_limit":7,"counter":"desgaste e flanqueamento","punishes":"uma única muralha estática","recommended_roles":["controle","suporte"],"twist":"dois eixos de ameaça obrigam uma reserva móvel"},
    {"victory_condition":"escort","objective":"levar a segunda tropa ao refúgio E","round_limit":10,"counter":"emboscada e foco","punishes":"deixar a unidade de missão na vanguarda","recommended_roles":["defesa","mobilidade"],"twist":"o refúgio fica além do principal campo de tiro"},
    {"victory_condition":"intercept","objective":"eliminar o mensageiro inimigo antes da saída E","round_limit":8,"counter":"proteção em camadas","punishes":"focar o comandante e ignorar a missão","recommended_roles":["ruptura","mobilidade"],"twist":"o alvo recua enquanto a escolta inimiga trava atalhos"},
    {"victory_condition":"defeat_commander","objective":"derrotar o rival regional e selar a Fratura","counter":"formação combinada","punishes":"solução monofunção e alpha strike","recommended_roles":["defesa","ruptura","suporte"],"twist":"o chefe é resistente, mas seus flancos e CMD continuam vulneráveis"},
]


def _campaign_grid(region_index, stage_index, victory_condition):
    width, height = 12, 8
    grid = [["." for _ in range(width)] for _ in range(height)]
    terrain_symbol = ["F","F","M","B","#","M","M","F","B","~","M","~","M","#","~","F"][region_index]
    # Dez arquétipos de campo; a região muda a linguagem visual, não as regras ocultas.
    patterns = [
        [(3,1),(3,2),(7,5),(8,5)], [(4,0),(4,1),(4,6),(4,7),(8,3)],
        [(3,2),(3,5),(6,1),(6,6),(8,2),(8,5)], [(4,2),(4,4),(7,1),(7,5)],
        [(2,1),(4,5),(6,2),(8,4),(9,6)], [(3,0),(3,1),(6,4),(8,6),(9,6)],
        [(4,1),(4,6),(7,2),(7,5),(9,3)], [(2,2),(5,1),(5,6),(8,5)],
        [(3,3),(5,1),(5,5),(8,2),(8,6)], [(4,1),(4,5),(7,2),(7,6),(9,4)],
    ]
    for x, y in patterns[stage_index]:
        grid[y][x] = terrain_symbol
    # Bloqueios reais são poucos e sempre deixam rotas alternativas.
    for x, y in ((5 + (stage_index % 2), 2), (6 - (stage_index % 2), 5)):
        if grid[y][x] == ".":
            grid[y][x] = "#"
    if victory_condition == "control_area":
        grid[3][6] = "O"
    elif victory_condition == "escort":
        grid[6][11] = "E"
    elif victory_condition == "intercept":
        grid[1][0] = "E"
    return ["".join(row) for row in grid]


def build_campaign_v2():
    scenarios, maps = [], []
    all_troops = {family["id"]: TROOPS[family["id"]] for family in FAMILIES}
    global_order = 0
    for region_index, family in enumerate(FAMILIES):
        for stage_index, title in enumerate(REGION_STAGE_TITLES[family["id"]]):
            global_order += 1
            design = STAGE_DESIGNS[stage_index]
            secondary = FAMILIES[(region_index + stage_index * 3 + 1) % len(FAMILIES)]
            enemy_class_index = [0,1,2,3,4,5,6,7,8,14][stage_index]
            primary_troop_index = min(8, stage_index)
            secondary_troop_index = (stage_index * 2 + region_index) % 9
            scenario_id = f"cenario_{family['id']}_{stage_index+1:02d}"
            map_id = f"mapa_{family['id']}_{stage_index+1:02d}"
            objective_tiles = [[6,3]] if design["victory_condition"] == "control_area" else []
            escort_exit = [11,6] if design["victory_condition"] == "escort" else None
            intercept_exit = [0,1] if design["victory_condition"] == "intercept" else None
            scenario = {
                "id":scenario_id,"order":global_order,"region_order":region_index+1,"stage_in_region":stage_index+1,
                "act":region_index//4+1,"name":title,"region_id":f"regiao_{family['id']}","map_id":map_id,
                "biome":family["terrain"],
                "terrain_notes":f"Campo de {family['region']} com rotas legíveis, cobertura temática e um corredor de resposta.",
                "premise":f"Em {title}, {HERO_NAMES[region_index]} enfrenta uma manobra da Convergência que explora {family['trait']}.",
                "objective":design["objective"],"victory_condition":design["victory_condition"],
                "round_limit":design.get("round_limit"),"control_required":design.get("control_required",0),
                "objective_tiles":objective_tiles,"escort_exit":escort_exit,"intercept_exit":intercept_exit,
                "enemy_family_ids":[family["id"],secondary["id"]],
                "enemy_class_id":f"classe_{family['id']}_{slug(CLASS_TREES[family['id']][enemy_class_index])}",
                "enemy_troop_ids":[
                    f"tropa_{family['id']}_{slug(all_troops[family['id']][primary_troop_index])}",
                    f"tropa_{secondary['id']}_{slug(all_troops[secondary['id']][secondary_troop_index])}",
                ],
                "soft_counter":{"enemy_plan":design["counter"],"punishes":design["punishes"],"recommended_roles":design["recommended_roles"],"hard_lock":False},
                "formation_twist":design["twist"],"difficulty":1 + region_index * 10 + stage_index,
                "boss":stage_index == 9,
                "story_beat":f"{stage_index+1}/10 — {['chegada','disputa','aliança','crise','revelação','contra-ataque','cerco','sacrifício','perseguição','resolução'][stage_index]} regional",
                "reward":{"ouro":30+region_index*12+stage_index*5,"suprimentos":4+stage_index//3,"reputacao_family_id":family["id"]},
            }
            scenarios.append(scenario)
            maps.append({
                "id":map_id,"name":title,"region_id":scenario["region_id"],"biome":scenario["biome"],
                "width":12,"height":8,"grid":_campaign_grid(region_index,stage_index,design["victory_condition"]),
                "legend":{".":"chão","F":"cobertura natural","#":"bloqueio","M":"elevação","~":"terreno difícil visual","B":"estrutura","O":"área de controle","E":"saída de missão"},
                "blue_spawns":[[0,3],[0,5],[1,4]],"red_spawns":[[11,3],[11,5],[10,4]],
                "objective_tiles":objective_tiles,"exit":escort_exit or intercept_exit,
                "art_direction":{"palette":family["palette"],"landmark":f"marco de {family['trait']}","readability":"objetivo e saídas usam silhueta e cor exclusivas"},
            })
    campaign = {
        "schema_version":2,"title":"Asterra: A Campanha das Dezesseis Fraturas",
        "logline":"A Coalizão atravessa dezesseis regiões e vence cada Fratura aprendendo a mudar de formação, não acumulando uma resposta universal.",
        "region_count":16,"stages_per_region":10,"scenario_count":160,
        "acts":[
            {"number":1,"title":"A Coalizão Improvável","regions":[1,2,3,4],"arc":"Coroa, bosque, clãs e engenhos descobrem o inimigo comum."},
            {"number":2,"title":"Pedra, Aether e Fé","regions":[5,6,7,8],"arc":"Anões, arcanos, Igreja da Aurora e Umbrais disputam como selar as Fraturas."},
            {"number":3,"title":"Mortos, Marés e Elementos","regions":[9,10,11,12],"arc":"A guerra vira cerco de desgaste entre ossos, oceano, fogo e gelo."},
            {"number":4,"title":"O Céu e a Primeira Fratura","regions":[13,14,15,16],"arc":"Avarianos, dracônicos, povos do deserto e clãs bestiais marcham contra a origem."},
        ],
        "region_arcs":[{"region_id":f"regiao_{family['id']}","title":family["region"],"stages":[f"cenario_{family['id']}_{n:02d}" for n in range(1,11)]} for family in FAMILIES],
        "ending":"As dezesseis culturas preservam suas diferenças; o catálogo de 240 classes e 144 tropas sustenta reconstrução, desafios e campanhas futuras.",
        "scenario_ids":[item["id"] for item in scenarios],
    }
    return campaign, scenarios, maps


def _walkable_component(grid):
    hard = {"#", "B", "^", "X"}
    walkable = {
        (x, y)
        for y, row in enumerate(grid)
        for x, tile in enumerate(row)
        if tile not in hard
    }
    if not walkable:
        return set()
    visited, stack = set(), [min(walkable)]
    while stack:
        position = stack.pop()
        if position in visited:
            continue
        visited.add(position)
        x, y = position
        stack.extend(
            neighbor
            for neighbor in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if neighbor in walkable and neighbor not in visited
        )
    return visited


def build_maps_v3(maps_v2):
    """Acrescenta barreiras temáticas explícitas sem alterar as regras do combate."""
    hard_by_region = ["B", "X", "^", "X", "^", "X", "B", "X", "B", "X", "X", "^", "X", "^", "X", "X"]
    barrier_patterns = [
        [(5, 1), (5, 2), (6, 5), (6, 6)],
        [(3, 2), (4, 2), (7, 5), (8, 5)],
        [(4, 2), (5, 3), (6, 4), (7, 5)],
        [(4, 1), (5, 1), (7, 6), (8, 6)],
        [(3, 3), (4, 3), (7, 4), (8, 4)],
    ]
    upgraded = []
    for index, source in enumerate(maps_v2):
        region_index, stage_index = divmod(index, 10)
        grid = [list(row) for row in source["grid"]]
        protected = {
            tuple(position)
            for position in source["blue_spawns"] + source["red_spawns"] + source["objective_tiles"]
        }
        if source["exit"]:
            protected.add(tuple(source["exit"]))
        hard_symbol = hard_by_region[region_index]
        for x, y in barrier_patterns[stage_index % len(barrier_patterns)]:
            if (x, y) not in protected:
                previous = grid[y][x]
                grid[y][x] = hard_symbol
                candidate = ["".join(row) for row in grid]
                candidate_walkable = {
                    (cx, cy)
                    for cy, row in enumerate(candidate)
                    for cx, tile in enumerate(row)
                    if tile not in {"#", "B", "^", "X"}
                }
                if _walkable_component(candidate) != candidate_walkable:
                    grid[y][x] = previous
        rows = ["".join(row) for row in grid]
        connected = _walkable_component(rows)
        walkable = {
            (x, y)
            for y, row in enumerate(rows)
            for x, tile in enumerate(row)
            if tile not in {"#", "B", "^", "X"}
        }
        assert connected == walkable, f"Mapa desconectado: {source['id']}"
        assert protected <= walkable, f"Objetivo ou spawn bloqueado: {source['id']}"
        legend = dict(source["legend"])
        legend.update({"^":"pico ou escarpa intransponível", "X":"abismo, lava, água profunda ou obstáculo natural intransponível"})
        upgraded.append({
            **source,
            "grid":rows,
            "legend":legend,
            "navigation":{
                "version":3,
                "adjacency":"cardinal",
                "impassable_symbols":["#", "B", "^", "X"],
                "difficult_symbols":["F", "M", "~"],
                "all_walkable_tiles_connected":True,
                "flying_ignores_impassable":False,
            },
        })
    return upgraded


def write_json(name, payload):
    (DATA / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_campaign_document(campaign, scenarios):
    labels = {"defeat_commander":"Derrotar comandante","control_area":"Controlar área","escort":"Escoltar","survive":"Sobreviver","intercept":"Interceptar"}
    family_names = {item["id"]:item["name"] for item in FAMILIES}
    lines = [
        "# Campanha e Level Design v_2 — 16 Regiões / 160 Estágios", "",
        "Este documento é a leitura humana da matriz executável em `data/cenarios_v_2.json`. Cada linha abaixo possui mapa próprio, composição inimiga, condição de vitória e soft counter; o JSON acrescenta premissa, limite de rodadas, recompensas, direção visual e referências completas.", "",
        "## Gramática de progressão", "",
        "Cada região ensina e depois combina dez problemas: patrulha, controle curto, escolta, sobrevivência, interceptação, controle prolongado, desgaste, escolta sob foco, perseguição e chefe. Soft counters nunca proíbem uma formação: eles alteram custo, rota e risco, preservando vitória por execução superior.", "",
        "Terreno difícil (`F`, `M`, `~`) custa movimento adicional salvo afinidade cultural; floresta concede cobertura contra disparos, elevação melhora pressão ofensiva e floresta/água reduzem o impacto de Investida. `O` marca controle e `E`, saída de escolta/interceptação.", "",
    ]
    for family in FAMILIES:
        region_scenarios = [item for item in scenarios if item["region_id"] == f"regiao_{family['id']}"]
        lines.extend([
            f"## Região {region_scenarios[0]['region_order']} — {family['region']}", "",
            f"Bioma: {family['terrain']}. Identidade: {family['identity']}. Conflito: a Fratura distorce {family['trait']}.", "",
            "| # | Estágio | Inimigos | Vitória | Soft counter | Respostas sugeridas |", "|---:|---|---|---|---|---|",
        ])
        for item in region_scenarios:
            enemies = " + ".join(family_names[x] for x in item["enemy_family_ids"])
            responses = " + ".join(item["soft_counter"]["recommended_roles"])
            lines.append(f"| {item['stage_in_region']} | {item['name']} | {enemies} | {labels[item['victory_condition']]} — {item['objective']} | {item['soft_counter']['punishes']} | {responses} |")
        lines.extend(["", f"Fecho regional: {region_scenarios[-1]['formation_twist']}", ""])
    lines.extend([
        "## Critérios de aceite", "",
        "- Exatamente 16 regiões e 10 estágios por região.",
        "- As 16 famílias aparecem como inimigas; cada região combina força local e força de incursão.",
        "- As cinco condições de vitória aparecem 32 vezes cada.",
        "- Todo estágio declara plano inimigo, formação punida, ao menos duas respostas e `hard_lock: false`.",
        "- Os 160 cenários são simulados automaticamente até estado terminal para detectar softlocks.", "",
    ])
    (ROOT / "docs" / "CAMPANHA_E_LEVEL_DESIGN_v_2.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    classes = build_classes()
    troops = build_troops()
    regions, characters = build_world()
    campaign, scenarios, maps = build_campaign_v1()
    campaign_v2, scenarios_v2, maps_v2 = build_campaign_v2()
    maps_v3 = build_maps_v3(maps_v2)
    assert len(classes) == 240
    assert len(troops) == 144
    assert len({item["id"] for item in classes}) == 240
    assert len({item["id"] for item in troops}) == 144
    write_json("classes_personagens_v_1.json", {"schema_version":1,"count":len(classes),"families":16,"classes":classes})
    write_json("classes_tropas_v_1.json", {"schema_version":1,"count":len(troops),"target":"aproximadamente 140","troops":troops})
    write_json("regioes_v_1.json", {"schema_version":1,"count":len(regions),"regions":regions})
    write_json("personagens_v_1.json", {"schema_version":1,"count":len(characters),"characters":characters})
    write_json("campanha_v_1.json", campaign)
    write_json("cenarios_v_1.json", {"schema_version":1,"count":len(scenarios),"scenarios":scenarios})
    write_json("mapas_v_1.json", {"schema_version":1,"count":len(maps),"maps":maps})
    write_json("campanha_v_2.json", campaign_v2)
    write_json("cenarios_v_2.json", {"schema_version":2,"count":len(scenarios_v2),"regions":16,"stages_per_region":10,"scenarios":scenarios_v2})
    write_json("mapas_v_2.json", {"schema_version":2,"count":len(maps_v2),"maps":maps_v2})
    write_json("mapas_v_3.json", {"schema_version":3,"count":len(maps_v3),"maps":maps_v3})
    write_campaign_document(campaign_v2, scenarios_v2)
    print(f"Gerados: {len(classes)} classes, {len(troops)} tropas, {len(regions)} regiões, {len(characters)} personagens, {len(scenarios_v2)} cenários v2 e mapas v3.")


if __name__ == "__main__":
    main()
