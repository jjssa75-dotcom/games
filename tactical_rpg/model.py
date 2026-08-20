from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping


# Fonte única para terrenos que nenhuma unidade pode atravessar. Afinidades e
# voo alteram o custo de terreno transitável, nunca paredes, picos ou abismos.
IMPASSABLE_TERRAIN = frozenset({"#", "B", "^", "X"})


class Mode(str, Enum):
    ATTACK = "ATAQUE"
    DEFENSE = "DEFESA"
    FREE = "LIVRE"


class Side(str, Enum):
    BLUE = "AZUL"
    RED = "VERMELHO"


@dataclass(frozen=True)
class AbilityDefinition:
    id: str
    name: str
    kind: str
    cmd_cost: int = 0
    power: int = 0
    range: int = 0
    tags: tuple[str, ...] = ()
    duration_rounds: int = 0
    modifiers: tuple[tuple[str, int], ...] = ()
    mechanic: str = ""
    damage_bonus: int = 0
    armor_piercing: int = 0
    min_move: int = 0
    max_reposition: int = 0
    max_targets: int = 1


@dataclass(frozen=True)
class UnitDefinition:
    id: str
    name: str
    role: str
    hp: int
    attack: int
    defense: int
    movement: int
    attack_range: int
    cap_cost: int
    accuracy: int = 80
    evasion: int = 10
    armor_piercing: int = 0
    tags: tuple[str, ...] = ()
    abilities: tuple[str, ...] = ()
    allowed_modes: tuple[Mode, ...] = (Mode.ATTACK, Mode.DEFENSE, Mode.FREE)


@dataclass(frozen=True)
class CommanderDefinition(UnitDefinition):
    cap_limit: int = 0
    cmd_max: int = 0
    cmd_regen: int = 0
    command_range: int = 4


@dataclass
class UnitState:
    instance_id: str
    definition_id: str
    side: Side
    hp: int
    position: tuple[int, int]
    commander_id: str | None = None
    mode: Mode = Mode.FREE
    activated: bool = False
    movement_spent: bool = False
    action_spent: bool = False
    reaction_available: bool = True
    morale: int = 100
    status: dict[str, int] = field(default_factory=dict)

    @property
    def alive(self) -> bool:
        return self.hp > 0


@dataclass
class CommanderState(UnitState):
    cmd: int = 0


@dataclass
class BattleState:
    units: dict[str, UnitState]
    active_side: Side
    round_number: int = 1
    winner: Side | None = None
    events: list[str] = field(default_factory=list)
    round_starter: Side | None = None
    board_width: int = 8
    board_height: int = 8
    blocked: set[tuple[int, int]] = field(default_factory=set)
    terrain: dict[tuple[int, int], str] = field(default_factory=dict)
    victory_condition: str = "defeat_commander"
    current_actor_id: str | None = None
    round_limit: int | None = None
    objective_tiles: set[tuple[int, int]] = field(default_factory=set)
    control_required: int = 0
    control_progress: int = 0
    escort_unit_id: str | None = None
    escort_exit: tuple[int, int] | None = None
    intercept_unit_id: str | None = None
    intercept_exit: tuple[int, int] | None = None

    def __post_init__(self):
        if self.round_starter is None:
            self.round_starter = self.active_side


@dataclass(frozen=True)
class Catalog:
    units: Mapping[str, UnitDefinition]
    commanders: Mapping[str, CommanderDefinition]
    abilities: Mapping[str, AbilityDefinition]
    schema_version: int = 1
    scope: Mapping[str, object] = field(default_factory=dict)

    @staticmethod
    def frozen(units, commanders, abilities, schema_version=1, scope=None) -> "Catalog":
        return Catalog(
            MappingProxyType(units),
            MappingProxyType(commanders),
            MappingProxyType(abilities),
            schema_version,
            MappingProxyType(scope or {}),
        )
