# Arquitetura Final v_1

## Camadas

- Dados: JSON versionado para combate, classes, tropas e mundo.
- Domínio: `Definition` imutável e `State` mutável.
- Regras: `ActionResolver`, transacional e determinístico.
- Aplicação: `GameSession`, seleção, conversão do catálogo e IA.
- Interface: HTML/CSS/JS sem dependências externas.

## Catálogo jogável

As 240 classes e 144 tropas são convertidas em `CommanderDefinition` ou
`UnitDefinition` usando tier, crescimento, papel e stats. Isso evita centenas
de subclasses rígidas e mantém o catálogo extensível.

## Segurança de regras

Falha restaura o RNG. Movimento usa busca em largura. São rejeitados alvo
aliado, turno incorreto, repetição, CMD insuficiente, CAP inválido, alcance de
comando, alvos duplicados e casas bloqueadas. Preview e execução compartilham
código.

O servidor usa somente a biblioteca padrão, escuta em `127.0.0.1:8000` e não
requer internet, banco de dados ou pacotes externos.

## IA

`TacticalAI` gera ataques, movimentos, modos, comandos e habilidades para todas
as unidades disponíveis. Cada opção passa pelo mesmo preview do jogador e recebe
pontuação por dano, eliminações, vitória, segurança, papel, modo, distância do
inimigo e proteção do comandante. O desempate é determinístico.

