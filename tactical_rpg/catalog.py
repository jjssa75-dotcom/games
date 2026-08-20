import json
from pathlib import Path

from .model import AbilityDefinition, Catalog, CommanderDefinition, Mode, UnitDefinition


def load_catalog(path: str | Path) -> Catalog:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    schema_version = raw.get("schema_version", 1)
    if schema_version not in {1, 2, 3}:
        raise ValueError(f"Versão de schema não suportada: {schema_version}")
    _reject_duplicate_ids(raw)
    abilities = {
        x["id"]: AbilityDefinition(
            **{
                **x,
                "tags": tuple(x.get("tags", [])),
                "modifiers": tuple(sorted(x.get("modifiers", {}).items())),
            }
        )
        for x in raw["abilities"]
    }

    def common(x):
        return {
            **x,
            "abilities": tuple(x.get("abilities", [])),
            "tags": tuple(x.get("tags", [])),
            "allowed_modes": tuple(Mode(m) for m in x.get("allowed_modes", [m.value for m in Mode])),
        }

    units = {x["id"]: UnitDefinition(**common(x)) for x in raw["troops"]}
    commanders = {x["id"]: CommanderDefinition(**common(x)) for x in raw["commanders"]}
    scope = raw.get("catalog_scope", {})
    _validate_references(units, commanders, abilities, scope)
    return Catalog.frozen(units, commanders, abilities, schema_version, scope)


def _reject_duplicate_ids(raw):
    for section in ("abilities", "commanders", "troops"):
        ids = [item["id"] for item in raw.get(section, [])]
        if len(ids) != len(set(ids)):
            raise ValueError(f"IDs duplicados em {section}")


def _validate_references(units, commanders, abilities, scope):
    all_defs = list(units.values()) + list(commanders.values())
    ids = [d.id for d in all_defs]
    if len(ids) != len(set(ids)):
        raise ValueError("IDs de unidade duplicados")
    for definition in all_defs:
        if definition.hp <= 0 or min(definition.attack, definition.defense, definition.movement, definition.cap_cost) < 0:
            raise ValueError(f"Valor negativo em {definition.id}")
        missing = set(definition.abilities) - abilities.keys()
        if missing:
            raise ValueError(f"Habilidades ausentes em {definition.id}: {sorted(missing)}")
    allowed_modifiers = {"movement", "defense", "accuracy", "morale"}
    for ability in abilities.values():
        unknown = {key for key, _ in ability.modifiers} - allowed_modifiers
        if unknown:
            raise ValueError(f"Modificadores desconhecidos em {ability.id}: {sorted(unknown)}")
        if min(ability.cmd_cost, ability.duration_rounds, ability.max_targets) < 0:
            raise ValueError(f"Valor inválido em {ability.id}")
    if scope:
        if scope.get("vertical_slice_commanders") != len(commanders) or scope.get("vertical_slice_troops") != len(units):
            raise ValueError("Contagens do vertical slice divergem do catálogo")
        if scope.get("future_catalog_is_implementation_scope") is not False:
            raise ValueError("Catálogo futuro não pode ser marcado como escopo atual")
