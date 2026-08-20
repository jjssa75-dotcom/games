from .model import Catalog, CommanderState, Side, UnitState


def build_detachment(catalog: Catalog, commander_definition_id: str, troop_definition_ids: list[str], side: Side, prefix: str, origin=(0, 0)):
    if not prefix or any(character.isspace() for character in prefix):
        raise ValueError("Prefixo de destacamento inválido")
    if commander_definition_id not in catalog.commanders:
        raise ValueError("Comandante desconhecido")
    unknown = [item for item in troop_definition_ids if item not in catalog.units]
    if unknown:
        raise ValueError(f"Tropas desconhecidas: {unknown}")
    commander_def = catalog.commanders[commander_definition_id]
    cost = sum(catalog.units[x].cap_cost for x in troop_definition_ids)
    if cost > commander_def.cap_limit:
        raise ValueError(f"CAP excedido: {cost}/{commander_def.cap_limit}")
    commander_id = f"{prefix}-cmd"
    units = {
        commander_id: CommanderState(commander_id, commander_def.id, side, commander_def.hp, origin, cmd=commander_def.cmd_max)
    }
    for index, definition_id in enumerate(troop_definition_ids, 1):
        definition = catalog.units[definition_id]
        instance_id = f"{prefix}-t{index}"
        units[instance_id] = UnitState(instance_id, definition_id, side, definition.hp, (origin[0], origin[1] + index), commander_id)
    return units
