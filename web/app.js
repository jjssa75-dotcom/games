const state = {
  battle: null, selected: null, pendingAbility: null, selectedClass: null,
  selectedTroops: [], classes: [], troops: [], regions: [], characters: [],
  campaign: null, scenarios: [], families: new Map(),
};

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const api = async (path, payload) => {
  const response = await fetch(path, {
    method: payload ? 'POST' : 'GET', headers: {'Content-Type': 'application/json'},
    body: payload ? JSON.stringify(payload) : undefined,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Falha');
  return data;
};

async function boot() {
  const [battle, classes, troops, regions, characters, campaign, scenarios] = await Promise.all([
    api('/api/state'),
    fetch('/data/classes_personagens_v_1.json').then(response => response.json()),
    fetch('/data/classes_tropas_v_1.json').then(response => response.json()),
    fetch('/data/regioes_v_2.json').then(response => response.json()),
    fetch('/data/personagens_v_2.json').then(response => response.json()),
    fetch('/data/campanha_v_3.json').then(response => response.json()),
    fetch('/data/cenarios_v_3.json').then(response => response.json()),
  ]);
  Object.assign(state, {
    battle, selectedClass: battle.player_class_id, selectedTroops: battle.player_troop_ids,
    classes: classes.classes, troops: troops.troops, regions: regions.regions,
    characters: characters.characters, campaign, scenarios: scenarios.scenarios,
  });
  state.regions.forEach(region => state.families.set(region.family_id, region));
  bind();
  renderAll();
}

function bind() {
  $$('.nav').forEach(button => button.onclick = () => showView(button.dataset.view));
  $('#codex-search').oninput = renderCodex;
  $('#codex-type').onchange = renderCodex;
  $('#codex-family').onchange = renderCodex;
}

function showView(id) {
  $$('.nav').forEach(item => item.classList.toggle('active', item.dataset.view === id));
  $$('.view').forEach(item => item.classList.toggle('active', item.id === id));
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function renderAll() {
  renderBattle(); renderCampaign(); renderCodexFilters(); renderCodex(); renderWorld();
}

function legalMoveMap() {
  const entries = state.battle.legal_moves?.[state.selected] || [];
  return new Map(entries.map(([x, y, cost]) => [`${x},${y}`, cost]));
}

function renderBattle() {
  const battle = state.battle;
  $('#scenario-name').textContent = battle.scenario.name;
  $('#scenario-premise').textContent = `${battle.scenario.premise} Objetivo: ${battle.scenario.objective}${battle.control_required ? ` (${battle.control_progress}/${battle.control_required})` : ''}`;
  $('#act-label').textContent = `ATO ${battle.scenario.act} • REGIÃO ${battle.scenario.region_order} • ESTÁGIO ${battle.scenario.stage_in_region}`;
  $('#round').textContent = battle.round;
  $('#turn').textContent = battle.winner ? `VITÓRIA ${battle.winner}` : `TURNO ${battle.active_side}`;

  const unitsAt = new Map(battle.units.filter(unit => unit.alive).map(unit => [unit.position.join(','), unit]));
  const reachable = legalMoveMap();
  const grid = $('#grid');
  grid.innerHTML = '';
  grid.dataset.region = battle.scenario.region_id;
  grid.style.gridTemplateColumns = `repeat(${battle.map.width}, var(--cell))`;
  grid.style.gridTemplateRows = `repeat(${battle.map.height}, var(--cell))`;
  battle.map.grid.forEach((row, y) => [...row].forEach((tile, x) => {
    const key = `${x},${y}`;
    const cell = document.createElement('button');
    const unit = unitsAt.get(key);
    const cost = reachable.get(key);
    cell.className = `cell ${terrainClass(tile)}`;
    cell.dataset.x = x; cell.dataset.y = y; cell.dataset.tile = tile;
    cell.setAttribute('aria-label', `${terrainLabel(tile)}, coluna ${x + 1}, linha ${y + 1}${unit ? `, ${unit.name}` : ''}`);
    cell.title = `${terrainLabel(tile)}${cost ? ` • custo de movimento ${cost}` : ''}`;
    if (isHardTile(tile)) cell.classList.add('blocked');
    if (cost !== undefined && !unit) {
      cell.classList.add('reachable');
      const badge = document.createElement('span');
      badge.className = 'move-cost'; badge.textContent = cost; cell.append(badge);
    }
    if (unit) cell.append(unitToken(unit));
    if (state.selected === unit?.id) cell.classList.add('selected');
    cell.onclick = () => cellClick(x, y, unit, tile);
    grid.append(cell);
  }));

  const blue = battle.units.filter(unit => unit.side === 'AZUL');
  $('#blue-roster').innerHTML = `<div class="formation-cap"><span>CAP DA FORMAÇÃO</span><strong>${battle.formation_cap}<small> / ${battle.formation_cap_limit}</small></strong></div>` + blue.map(unit => `
    <div class="roster-item ${state.selected === unit.id ? 'active' : ''} ${unit.activated ? 'spent' : ''}" data-unit="${unit.id}">
      <span class="roster-glyph">${unit.id.includes('cmd') ? '✦' : unit.range > 1 ? '➶' : '◆'}</span>
      <div><strong>${unit.name}</strong><span>${unit.hp}/${unit.max_hp} PV • ${unit.mode}${unit.movement_spent ? ' • MOVEU' : ''}${unit.activated ? ' • AGIU' : ''}</span></div>
    </div>`).join('');
  $$('[data-unit]').forEach(item => item.onclick = () => selectUnit(item.dataset.unit));
  renderInspector();
  $('#log').innerHTML = [...battle.events].reverse().map(event => `<li>${event}</li>`).join('');
  const victory = $('#victory');
  victory.classList.toggle('hidden', !battle.winner);
  if (battle.winner) {
    victory.innerHTML = `<div><p class="eyebrow">BATALHA ENCERRADA</p><h2>${battle.winner === 'AZUL' ? 'Vitória da Coalizão' : 'A formação foi derrotada'}</h2><p>${battle.scenario.name}</p><button class="action primary" id="replay">Jogar novamente</button></div>`;
    $('#replay').onclick = () => startScenario(battle.scenario.id);
  }
}

function terrainClass(tile) {
  return ({'~':'water', '#':'wall', 'B':'structure', '^':'peak', 'X':'hazard', 'O':'objective', 'E':'exit', 'F':'forest', 'M':'elevation', '.':'ground'})[tile] || 'ground';
}

function terrainLabel(tile) {
  return ({'.':'solo transitável', 'F':'cobertura natural', 'M':'elevação transitável', '~':'terreno difícil', '#':'muralha intransponível', 'B':'estrutura intransponível', '^':'pico ou escarpa intransponível', 'X':'abismo ou risco natural intransponível', 'O':'área de controle', 'E':'saída da missão'})[tile] || 'terreno';
}

function isHardTile(tile) { return ['#', 'B', '^', 'X'].includes(tile); }

function unitToken(unit) {
  const token = document.createElement('div');
  const glyph = unit.id.includes('cmd') ? '✦' : unit.range > 1 ? '➶' : '◆';
  token.className = `unit ${unit.side === 'AZUL' ? 'blue' : 'red'} ${unit.activated ? 'done' : ''}`;
  token.title = unit.name;
  token.innerHTML = `<span class="unit-shadow"></span><span class="unit-face">${glyph}</span><span class="unit-rank">${unit.id.includes('cmd') ? 'CMD' : unit.range > 1 ? 'ALC' : 'LIN'}</span><span class="hpbar"><i style="width:${100 * unit.hp / unit.max_hp}%"></i></span>`;
  return token;
}

function selectUnit(id) {
  const unit = state.battle.units.find(item => item.id === id);
  const locked = state.battle.current_actor_id;
  if (unit?.side === 'AZUL' && !unit.activated && !state.battle.winner && (!locked || locked === id)) {
    state.selected = id; state.pendingAbility = null; renderBattle();
  }
}

async function cellClick(x, y, unit, tile) {
  if (unit?.side === 'AZUL') return selectUnit(unit.id);
  const actor = state.battle.units.find(item => item.id === state.selected);
  if (!actor || actor.activated) return;
  if (!unit && isHardTile(tile)) return flash(terrainLabel(tile));
  if (!unit && !legalMoveMap().has(`${x},${y}`)) return flash('Essa casa não está ao alcance por uma rota legal.');
  try {
    const payload = unit && state.pendingAbility
      ? {type:'ability', actor_id:actor.id, ability_id:state.pendingAbility, target_id:unit.id}
      : unit ? {type:'attack', actor_id:actor.id, target_id:unit.id} : {type:'move', actor_id:actor.id, x, y};
    state.battle = await api('/api/action', payload);
    state.selected = state.battle.current_actor_id;
    state.pendingAbility = null;
    renderBattle();
  } catch (error) { flash(error.message); }
}

function renderInspector() {
  const unit = state.battle.units.find(item => item.id === state.selected);
  const card = $('#unit-card');
  $('#actions').innerHTML = '';
  if (!unit) {
    card.className = 'unit-card empty';
    card.innerHTML = '<span class="empty-sigil">✦</span><p>Selecione uma unidade azul ainda não ativada.</p>';
    return;
  }
  card.className = 'unit-card';
  card.innerHTML = `<div class="unit-card-head"><span class="portrait-medallion">${unit.id.includes('cmd') ? '✦' : unit.range > 1 ? '➶' : '◆'}</span><div><h4>${unit.name}</h4><span class="pill">${unit.mode}</span><span class="pill">${unit.reaction ? 'reação pronta' : 'reação gasta'}</span></div></div><div class="stats"><div class="stat"><b>${unit.hp}/${unit.max_hp}</b><small>PV</small></div><div class="stat"><b>${unit.attack}</b><small>ATQ</small></div><div class="stat"><b>${unit.defense}</b><small>DEF</small></div><div class="stat"><b>${unit.movement}</b><small>MOV</small></div><div class="stat"><b>${unit.range}</b><small>ALC</small></div><div class="stat"><b>${unit.cmd ?? '—'}</b><small>CMD</small></div></div>`;
  ['ATAQUE', 'DEFESA', 'LIVRE'].filter(mode => mode !== unit.mode).forEach(mode => addAction(`Modo ${mode}`, () => perform({type:'mode', actor_id:unit.id, mode})));
  if (unit.cmd !== null) unit.abilities.forEach(ability => addAction(labelAbility(ability), () => {
    const targets = state.battle.units.filter(item => item.commander_id === unit.id && item.alive).slice(0, 4).map(item => item.id);
    perform({type:'command', actor_id:unit.id, ability_id:ability, target_ids:targets});
  }, true));
  if (unit.abilities.includes('preparar_lanca')) addAction('Preparar Lança', () => perform({type:'ability', actor_id:unit.id, ability_id:'preparar_lanca'}), true);
  if (unit.abilities.includes('investida')) addAction(state.pendingAbility === 'investida' ? 'Escolha o alvo' : 'Preparar Investida', () => { state.pendingAbility = 'investida'; renderInspector(); }, true);
  if (unit.abilities.includes('escarmuca')) addAction(state.pendingAbility === 'escarmuca' ? 'Escolha o alvo' : 'Preparar Escaramuça', () => { state.pendingAbility = 'escarmuca'; renderInspector(); }, true);
  if (unit.movement_spent) addAction('Encerrar ativação', () => perform({type:'end', actor_id:unit.id}), true, true);
}

function addAction(label, handler, wide = false, primary = false) {
  const button = document.createElement('button');
  button.className = `action ${wide ? 'wide' : ''} ${primary ? 'primary' : ''}`;
  button.textContent = label; button.onclick = handler; $('#actions').append(button);
}

function labelAbility(id) {
  return ({avancar:'Avançar!', manter_posicao:'Manter Posição!', foco_alvo:'Foco de Alvo', reagrupar:'Reagrupar'})[id] || id;
}

async function perform(payload) {
  try {
    state.battle = await api('/api/action', payload);
    state.selected = state.battle.current_actor_id;
    state.pendingAbility = null; renderBattle();
  } catch (error) { flash(error.message); }
}

function flash(message) {
  const log = $('#log');
  log.insertAdjacentHTML('afterbegin', `<li class="error-event">${message}</li>`);
  log.closest('.inspector')?.classList.add('attention');
  setTimeout(() => log.closest('.inspector')?.classList.remove('attention'), 500);
}

function renderCampaign() {
  $('#campaign-logline').textContent = `${state.campaign.logline} • ${state.campaign.scenario_count} estágios`;
  const markNames = new Map(state.campaign.political_marks.map(mark => [mark.id, mark.name]));
  const renderDialogue = (dialogue = []) => dialogue
    .map(item => `<p><strong>${item.speaker}:</strong> “${item.line}”</p>`).join('');
  const renderMarks = deltas => Object.entries(deltas)
    .map(([id, value]) => `<span class="mark-delta ${value < 0 ? 'negative' : 'positive'}">${markNames.get(id) || id} ${value > 0 ? '+' : ''}${value}</span>`).join('');
  $('#scenario-list').innerHTML = state.regions.map((region, index) => {
    const missions = state.scenarios.filter(scenario => scenario.region_id === region.id);
    const act = Math.floor(index / 4) + 1;
    return `<section class="campaign-region"><header class="campaign-cover act-${act}"><div><span class="tag">ATO ${act} • REGIÃO ${index + 1}/16</span><h2>${region.name}</h2><p>${region.territorial_role}</p><p class="regional-stake">${region.historical_grievance}</p></div></header><div class="region-missions">${missions.map(scenario => {
      const narrative = scenario.narrative || {};
      const marks = narrative.political_marks?.canonical_route || {};
      const preBattle = narrative.pre_battle_dialogue || narrative.dialogue?.pre_battle || [];
      const postBattle = narrative.post_battle_dialogue || narrative.dialogue?.post_battle || [];
      const dilemma = narrative.moral_dilemma || narrative.dilemma || 'A decisão política será registrada após a batalha.';
      return `<article class="story-card narrative-card"><div class="card-number">${String(scenario.stage_in_region).padStart(2, '0')}</div><span class="pill">${narrative.regional_phase || scenario.story_beat}</span><h3>${scenario.name}</h3><p>${scenario.premise}</p><p><strong>Objetivo:</strong> ${scenario.objective}</p><div class="political-marks">${renderMarks(marks)}</div><details><summary>Contexto e diálogos</summary><p>${narrative.historical_context || scenario.premise}</p><h4>Antes da batalha</h4>${renderDialogue(preBattle)}<h4>Depois da batalha</h4>${renderDialogue(postBattle)}<p><strong>Dilema:</strong> ${dilemma}</p></details><div class="tactical-note"><strong>Pressão tática</strong><span>${narrative.soft_counter_narrative || scenario.soft_counter.punishes}</span><small>Respostas: ${scenario.soft_counter.recommended_roles.join(' + ')}</small></div><button data-scenario="${scenario.id}">Iniciar cenário</button></article>`;
    }).join('')}</div></section>`;
  }).join('');
  $$('[data-scenario]').forEach(button => button.onclick = () => startScenario(button.dataset.scenario));
}

async function startScenario(id) {
  state.battle = await api('/api/new', {scenario_id:id, class_id:state.selectedClass, troop_ids:state.selectedTroops});
  state.selected = null; showView('battle'); renderBattle();
}

function renderCodexFilters() {
  const select = $('#codex-family');
  state.regions.forEach(region => select.insertAdjacentHTML('beforeend', `<option value="${region.family_id}">${region.name}</option>`));
}

function renderCodex() {
  const type = $('#codex-type').value;
  const query = $('#codex-search').value.toLowerCase();
  const family = $('#codex-family').value;
  const items = (type === 'classes' ? state.classes : state.troops).filter(item => (!family || item.family_id === family) && (!query || `${item.name} ${item.family_id} ${item.role}`.toLowerCase().includes(query)));
  const className = state.classes.find(item => item.id === state.selectedClass)?.name || '—';
  const troopNames = state.selectedTroops.map(id => state.troops.find(item => item.id === id)?.name).filter(Boolean);
  $('#formation-choice').innerHTML = `<strong>Formação selecionada:</strong> ${className} <span>•</span> ${troopNames.join(' <span>•</span> ')} — inicie qualquer cenário da Campanha para jogar com ela.`;
  $('#codex-count').textContent = `${items.length} registros exibidos`;
  $('#codex-list').innerHTML = items.map(item => {
    const region = state.families.get(item.family_id);
    const chosen = type === 'classes' ? state.selectedClass === item.id : state.selectedTroops.includes(item.id);
    const initial = region?.name?.slice(0, 1) || 'A';
    return `<article class="codex-entry ${chosen ? 'chosen' : ''}"><div class="codex-crest">${initial}</div><div class="codex-body"><span class="pill">${region?.identity || item.family_id}</span><span class="pill">TIER ${item.tier}</span><h3>${item.name}</h3><p><strong>${item.role}</strong> — ${item.identity || item.signature}</p><p>${item.gameplay || item.tactical_use}</p><button class="choose" data-choice="${item.id}" data-kind="${type}">${chosen ? 'SELECIONADO' : 'USAR NA FORMAÇÃO'}</button></div></article>`;
  }).join('');
  $$('[data-choice]').forEach(button => button.onclick = () => chooseCatalog(button.dataset.kind, button.dataset.choice));
}

function chooseCatalog(kind, id) {
  if (kind === 'classes') state.selectedClass = id;
  else {
    state.selectedTroops = state.selectedTroops.filter(item => item !== id);
    state.selectedTroops.push(id); state.selectedTroops = state.selectedTroops.slice(-2);
  }
  renderCodex();
}

function renderWorld() {
  $('#region-list').innerHTML = state.regions.map((region, index) => {
    const characters = state.characters.filter(character => character.family_id === region.family_id);
    const act = Math.floor(index / 4) + 1;
    return `<article class="region-card"><div class="region-art act-${act}"><span>REGIÃO ${String(index + 1).padStart(2, '0')}</span></div><div class="region-card-body"><span class="pill">${region.capital}</span><h3>${region.name}</h3><p><strong>Governo:</strong> ${region.governance}</p><p><strong>Economia:</strong> ${region.political_economy}</p><p><strong>Território:</strong> ${region.territorial_role}</p><p><strong>Ferida histórica:</strong> ${region.historical_grievance}</p><p><strong>Figuras:</strong> ${characters.map(character => character.name).join(' • ')}</p><div class="swatches"><i></i><i></i><i></i></div></div></article>`;
  }).join('');
}

boot().catch(error => document.body.innerHTML = `<main class="fatal"><h1>Falha ao iniciar</h1><p>${error.message}</p><p>Execute <code>python -m tactical_rpg.web</code> na pasta do projeto.</p></main>`);
