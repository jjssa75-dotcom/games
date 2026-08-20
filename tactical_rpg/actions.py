from dataclasses import dataclass

from .model import Mode


@dataclass(frozen=True)
class MoveAction:
    actor_id: str
    destination: tuple[int, int]


@dataclass(frozen=True)
class AttackAction:
    actor_id: str
    target_id: str


@dataclass(frozen=True)
class SetModeAction:
    actor_id: str
    mode: Mode


@dataclass(frozen=True)
class CommandAction:
    actor_id: str
    ability_id: str
    target_ids: tuple[str, ...]


@dataclass(frozen=True)
class UseAbilityAction:
    actor_id: str
    ability_id: str
    target_id: str | None = None
    destination: tuple[int, int] | None = None


@dataclass(frozen=True)
class EndActivationAction:
    actor_id: str
