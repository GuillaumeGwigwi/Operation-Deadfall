/* Atlas de Thay — interactions (script classique, aucune requête réseau). */
(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const feedback = $('feedback');
  const say = (msg) => {
    feedback.textContent = msg;
    feedback.classList.toggle('visually-hidden', !/indisponibles|n’a pas pu|Ce lien/.test(msg));
  };

  const DATA = window.THAY_ATLAS;
  if (!DATA || !Array.isArray(DATA.landmarks)) {
    say('Les données de l’atlas sont indisponibles.');
    return;
  }

  const KINDS = {
    province: 'Province',
    ville: 'Ville',
    nature: 'Site naturel',
    route: 'Route',
    patrimoine: 'Patrimoine',
    guide: 'Guide de voyage',
  };
  const W = DATA.mapWidth;
  const H = DATA.mapHeight;
  const MAX_ZOOM = 8;


  const stage = $('map-stage');
  const world = $('map-world');
  const mapImage = $('map-image');
  const markerLayer = $('map-markers');
  const sidebar = $('sidebar');
  const sidebarPanel = $('sidebar-panel');
  const toggle = $('list-toggle');
  const search = $('search');
  const category = $('category');
  const clearBtn = $('clear-search');
  const resultCount = $('result-count');
  const list = $('landmark-list');
  const emptyState = $('empty-state');
  const panel = $('detail-panel');
  const detailTitle = $('detail-title');
  const detailKind = $('detail-kind');
  const detailMedia = $('detail-media');
  const detailBody = $('detail-body');
  const expandButton = $('detail-expand');

  const wide = window.matchMedia('(min-width: 900px)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const byId = new Map([...DATA.landmarks, DATA.guide].filter(Boolean).map((l) => [l.id, l]));
  const markers = new Map();
  const listButtons = new Map();
  const haystack = new Map();

  const norm = (s) => String(s)
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/œ/g, 'oe').replace(/æ/g, 'ae')
    .replace(/[’‘`]/g, "'")
    .toLowerCase();

  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  };
  const glyph = (kind) => {
    const g = el('span', 'glyph');
    g.dataset.kind = kind;
    g.setAttribute('aria-hidden', 'true');
    return g;
  };
  const kindLabel = (l) => KINDS[l.kind] || 'Lieu';
  const metaLabel = (l) => (l.kind === 'province' ? 'Province de Thay' : `${kindLabel(l)}, région ${l.region}`);

  /* ---------- Contenu statique issu des données ---------- */


  world.style.width = `${W}px`;
  world.style.height = `${H}px`;


  /* ---------- Repères et liste ---------- */

  for (const l of DATA.landmarks) {
    const m = el('button', 'map-marker');
    m.type = 'button';
    m.dataset.id = l.id;
    m.dataset.kind = l.kind;
    m.style.left = `${l.x}%`;
    m.style.top = `${l.y}%`;
    m.setAttribute('aria-label', `${l.name}, ${kindLabel(l).toLowerCase()}`);
    const label = el('span', 'marker-label', l.name);
    label.setAttribute('aria-hidden', 'true');
    m.append(glyph(l.kind), label);
    markerLayer.append(m);
    markers.set(l.id, m);

    const li = el('li');
    const b = el('button', 'landmark');
    b.type = 'button';
    b.dataset.id = l.id;
    const text = el('span', 'landmark-text');
    text.append(el('span', 'landmark-name', l.name), el('span', 'landmark-meta', metaLabel(l)));
    b.append(glyph(l.kind), text);
    li.append(b);
    list.append(li);
    listButtons.set(l.id, b);

    haystack.set(l.id, norm([l.name, l.region, kindLabel(l), l.summary, l.bodyHTML.replace(/<[^>]*>/g, ' ')].join(' ')));
  }

  /* ---------- Vue de la carte : fit, pan, zoom ancré ---------- */

  let s = 1;
  let tx = 0;
  let ty = 0;
  let fit = 1;
  let center = null; // point de la carte au centre de la zone visible

  // Zone de carte non recouverte par la barre latérale ou la fiche (desktop).
  function viewBox() {
    const r = stage.getBoundingClientRect();
    let left = 0;
    let right = r.width;
    if (wide.matches) {
      left = sidebar.getBoundingClientRect().right - r.left;
      if (!panel.hidden) right = panel.getBoundingClientRect().left - r.left;
      if (right - left < 200) { left = 0; right = r.width; }
    }
    return { left, top: 0, width: right - left, height: r.height };
  }

  const fitScale = (v) => Math.max(0.01, Math.min((v.width - 32) / W, (v.height - 32) / H));

  function apply(animate) {
    const v = viewBox();
    const cx = v.left + v.width / 2;
    const cy = v.top + v.height / 2;
    s = Math.min(Math.max(s, fit), fit * MAX_ZOOM);
    // Le centre visible reste toujours sur la carte.
    tx = Math.min(cx, Math.max(cx - W * s, tx));
    ty = Math.min(cy, Math.max(cy - H * s, ty));
    world.classList.toggle('is-animating', Boolean(animate) && !reducedMotion.matches);
    world.style.transform = `translate(${tx}px, ${ty}px) scale(${s})`;
    world.style.setProperty('--inv', String(1 / s));
    const z = s / fit;
    stage.dataset.zoom = z.toFixed(2);

    center = { x: (cx - tx) / s, y: (cy - ty) / s };
  }

  function resetView(animate) {
    const v = viewBox();
    fit = fitScale(v);
    s = fit;
    tx = v.left + (v.width - W * s) / 2;
    ty = v.top + (v.height - H * s) / 2;
    apply(animate);
  }

  function zoomAt(px, py, factor, animate) {
    const next = Math.min(Math.max(s * factor, fit), fit * MAX_ZOOM);
    const k = next / s;
    tx = px - (px - tx) * k;
    ty = py - (py - ty) * k;
    s = next;
    apply(animate);
  }

  function zoomCentered(factor) {
    const v = viewBox();
    zoomAt(v.left + v.width / 2, v.top + v.height / 2, factor, true);
    say(`Zoom : ${Math.round((s / fit) * 100)} %`);
  }

  function centerOn(l, minZoom) {
    const v = viewBox();
    if (minZoom && s < fit * minZoom) s = fit * minZoom;
    tx = v.left + v.width / 2 - (l.x / 100) * W * s;
    ty = v.top + v.height / 2 - (l.y / 100) * H * s;
    apply(true);
  }

  window.addEventListener('resize', () => {
    const z = s / fit;
    const c = center;
    const v = viewBox();
    fit = fitScale(v);
    s = fit * z;
    if (c) {
      tx = v.left + v.width / 2 - c.x * s;
      ty = v.top + v.height / 2 - c.y * s;
    }
    apply(false);
  });

  $('zoom-in').addEventListener('click', () => zoomCentered(1.5));
  $('zoom-out').addEventListener('click', () => zoomCentered(1 / 1.5));
  $('reset-view').addEventListener('click', () => {
    resetView(true);
    say('Vue d’ensemble de la carte.');
  });

  stage.addEventListener('wheel', (e) => {
    e.preventDefault();
    const r = stage.getBoundingClientRect();
    const unit = e.deltaMode === 1 ? 0.05 : e.deltaMode === 2 ? 1 : 0.0015;
    zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * unit), false);
  }, { passive: false });

  // Pointer events : souris, stylet et tactile ; pincement à deux doigts.
  const pointers = new Map();
  let moved = false;
  let pinch = null;

  const pinchState = () => {
    const [a, b] = [...pointers.values()];
    return { d: Math.hypot(a.x - b.x, a.y - b.y) || 1, x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
  };

  stage.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    const r = stage.getBoundingClientRect();
    pointers.set(e.pointerId, { x: e.clientX - r.left, y: e.clientY - r.top, x0: e.clientX, y0: e.clientY });
    if (pointers.size === 1) moved = false;
    if (pointers.size === 2) {
      pinch = pinchState();
      moved = true;
      for (const id of pointers.keys()) {
        try { stage.setPointerCapture(id); } catch (_) { /* pointeur déjà relâché */ }
      }
    }
  });

  stage.addEventListener('pointermove', (e) => {
    const p = pointers.get(e.pointerId);
    if (!p) return;
    const r = stage.getBoundingClientRect();
    const x = e.clientX - r.left;
    const y = e.clientY - r.top;

    if (pointers.size === 1) {
      if (!moved && Math.hypot(e.clientX - p.x0, e.clientY - p.y0) > 5) {
        moved = true;
        stage.classList.add('is-panning');
        try { stage.setPointerCapture(e.pointerId); } catch (_) { /* ignoré */ }
      }
      if (moved) {
        tx += x - p.x;
        ty += y - p.y;
        apply(false);
      }
      p.x = x; p.y = y;
      return;
    }

    p.x = x; p.y = y;
    if (pointers.size === 2 && pinch) {
      const now = pinchState();
      tx += now.x - pinch.x;
      ty += now.y - pinch.y;
      zoomAt(now.x, now.y, now.d / pinch.d, false);
      pinch = now;
    }
  });

  const endPointer = (e) => {
    if (!pointers.delete(e.pointerId)) return;
    if (pointers.size < 2) pinch = null;
    if (pointers.size === 0) stage.classList.remove('is-panning');
  };
  stage.addEventListener('pointerup', endPointer);
  stage.addEventListener('pointercancel', endPointer);
  stage.addEventListener('lostpointercapture', endPointer);

  // Un glisser ne doit pas ouvrir la fiche du repère sous le pointeur.
  stage.addEventListener('click', (e) => {
    if (moved) {
      e.stopPropagation();
      e.preventDefault();
      moved = false;
    }
  }, true);

  stage.addEventListener('keydown', (e) => {
    if (e.target !== stage) return;
    const step = 90;
    const actions = {
      ArrowLeft: () => { tx += step; apply(false); },
      ArrowRight: () => { tx -= step; apply(false); },
      ArrowUp: () => { ty += step; apply(false); },
      ArrowDown: () => { ty -= step; apply(false); },
      '+': () => zoomCentered(1.5),
      '=': () => zoomCentered(1.5),
      '-': () => zoomCentered(1 / 1.5),
      0: () => { resetView(true); say('Vue d’ensemble de la carte.'); },
    };
    const act = actions[e.key];
    if (act) {
      e.preventDefault();
      act();
    }
  });

  mapImage.addEventListener('error', () => say('L’image de la carte n’a pas pu être chargée.'));

  /* ---------- Recherche et filtre ---------- */

  let rankedQuery = '';
  function applyFilter(announce) {
    const q = norm(search.value.trim());
    const cat = category.value;
    if (q !== rankedQuery) {
      const rank = (l) => {
        const name = norm(l.name);
        if (!q || name === q) return 0;
        if (name.startsWith(q)) return 1;
        if (name.includes(q)) return 2;
        if (norm(l.region).includes(q)) return 3;
        return 4;
      };
      const ordered = [...DATA.landmarks].sort((a, b) => rank(a) - rank(b));
      list.append(...ordered.map(l => listButtons.get(l.id).parentElement));
      rankedQuery = q;
    }
    let n = 0;
    for (const l of DATA.landmarks) {
      const ok = (cat === 'tous' || l.kind === cat) && (!q || haystack.get(l.id).includes(q));
      markers.get(l.id).hidden = !ok;
      listButtons.get(l.id).parentElement.hidden = !ok;
      if (ok) n += 1;
    }
    const total = DATA.landmarks.length;
    const text = n === total
      ? `${total} lieux affichés`
      : n === 0
        ? `Aucun lieu sur ${total}`
        : `${n} lieu${n > 1 ? 'x' : ''} sur ${total}`;
    resultCount.textContent = text;
    emptyState.hidden = n !== 0;
    clearBtn.hidden = !q && cat === 'tous';
    if (announce) say(n === 0 ? 'Aucun lieu ne correspond à cette recherche.' : text);
  }

  let filterTimer = 0;
  search.addEventListener('input', () => {
    if (search.value.trim()) setSidebar(true);
    applyFilter(false);
    clearTimeout(filterTimer);
    filterTimer = setTimeout(() => applyFilter(true), 400);
  });
  category.addEventListener('change', () => applyFilter(true));
  clearBtn.addEventListener('click', () => {
    search.value = '';
    category.value = 'tous';
    applyFilter(false);
    say(`Recherche effacée : ${DATA.landmarks.length} lieux affichés.`);
    search.focus();
  });

  /* ---------- Barre latérale repliable ---------- */

  function setSidebar(open) {
    toggle.setAttribute('aria-expanded', String(open));
    sidebarPanel.hidden = !open;
    sidebar.classList.toggle('is-collapsed', !open);
  }
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    setSidebar(open);
    say(open ? 'Liste des lieux affichée.' : 'Liste des lieux masquée.');
  });

  /* ---------- Fiche ---------- */

  let current = null;
  let lastTrigger = null;
  let readerOpen = false;

  function setReader(open) {
    if (open && panel.hidden) return;
    const scroll = panel.scrollTop;
    readerOpen = open;
    panel.classList.toggle('is-expanded', open);
    expandButton.setAttribute('aria-expanded', String(open));
    expandButton.textContent = open ? 'Réduire' : 'Agrandir';
    for (const node of [sidebar, stage, document.querySelector('.map-tools')]) node.inert = open;
    if (open) {
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true');
    } else {
      panel.removeAttribute('role');
      panel.removeAttribute('aria-modal');
    }
    panel.scrollTop = scroll;
    expandButton.focus({ preventScroll: true });
    say(open ? 'Mode lecture agrandi.' : 'Retour à la carte.');
  }
  expandButton.addEventListener('click', () => setReader(!readerOpen));

  function renderMedia(l) {
    detailMedia.replaceChildren();
    if (l.kind === 'guide') {
      const image = el('img', 'photo'); image.src = DATA.map; image.alt = 'Carte géographique de Thay';
      detailMedia.append(image); return;
    }
    if (l.image) {
      const img = el('img', 'photo');
      img.src = l.image;
      img.alt = l.imageCaption || l.name;
      img.decoding = 'async';
      detailMedia.append(img);
    } else {
      const inset = el('div', 'inset');
      const img = document.createElement('img');
      img.src = mapImage.getAttribute('src');
      img.alt = `Extrait de la carte de Thay centré sur ${l.name}.`;
      img.decoding = 'async';
      const insetRatio = 10 / 16;
      img.style.left = `${50 - l.x * 4}%`;
      img.style.top = `${50 - (l.y / 100) * 400 * (H / W) / insetRatio}%`;
      const mark = el('span', 'inset-mark');
      mark.setAttribute('aria-hidden', 'true');
      inset.append(img, mark);
      detailMedia.append(inset);
    }
  }

  function markSelection(id) {
    for (const [key, m] of markers) m.classList.toggle('is-selected', key === id);
    for (const [key, b] of listButtons) {
      if (key === id) b.setAttribute('aria-current', 'true');
      else b.removeAttribute('aria-current');
    }
  }

  function setHash(id) {
    const base = location.pathname + location.search;
    try {
      history.replaceState(null, '', id ? `${base}#lieu=${encodeURIComponent(id)}` : base);
    } catch (_) {
      // Certains navigateurs refusent replaceState en file:// : repli sur le hash.
      if (id) location.hash = `lieu=${id}`;
    }
  }

  function select(id, opts = {}) {
    const l = byId.get(id);
    if (!l) return false;
    current = id;
    lastTrigger = opts.trigger || listButtons.get(id);
    markSelection(id);

    detailKind.textContent = metaLabel(l);
    detailTitle.textContent = l.name;
    renderMedia(l);
    // bodyHTML : rendu Homebrewery V3 validé, inséré tel quel.
    detailBody.innerHTML = l.bodyHTML;
    $('detail-locate').hidden = l.kind === 'guide';
    const sections = [...detailBody.querySelectorAll('h3, h4')];
    const sectionSelect = $('detail-section');
    sectionSelect.replaceChildren(el('option', null, 'Sommaire'));
    sectionSelect.firstChild.value = '';
    sections.forEach((heading, index) => {
      heading.id = `fiche-${id}-section-${index}`;
      const option = el('option', null, heading.textContent); option.value = heading.id;
      sectionSelect.append(option);
    });
    $('detail-navigation').hidden = sections.length < 2;
    panel.hidden = false;
    panel.dataset.selected = id;
    panel.scrollTop = 0;

    setHash(id);
    if (opts.center) centerOn(l, 2);
    else apply(false); // la zone visible change quand la fiche s'ouvre
    say(`Fiche ouverte : ${l.name}.`);
    if (opts.focus !== false) detailTitle.focus({ preventScroll: true });
    return true;
  }

  const isShown = (node) => Boolean(node && node.isConnected && node.offsetParent !== null);

  function closeDetail() {
    if (panel.hidden) return;
    if (readerOpen) setReader(false);
    const id = current;
    panel.hidden = true;
    panel.dataset.selected = '';
    detailBody.replaceChildren();
    detailMedia.replaceChildren();
    current = null;
    markSelection(null);
    setHash(null);
    apply(false);
    say('Fiche fermée.');
    const back = [lastTrigger, listButtons.get(id), markers.get(id), toggle].find(isShown);
    if (back) back.focus();
  }

  markerLayer.addEventListener('click', (e) => {
    const m = e.target.closest('.map-marker[data-id]');
    if (m) select(m.dataset.id, { trigger: m });
  });
  list.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-id]');
    if (b) select(b.dataset.id, { trigger: b, center: true });
  });
  $('detail-close').addEventListener('click', closeDetail);
  $('country-guide').addEventListener('click', () => {
    if (select('guide-thay', { trigger: $('country-guide') })) setReader(true);
  });
  $('detail-section').addEventListener('change', (event) => {
    const heading = document.getElementById(event.target.value);
    if (!heading || !detailBody.contains(heading)) return;
    const top = panel.scrollTop + heading.getBoundingClientRect().top - panel.getBoundingClientRect().top - panel.querySelector('.detail-head').offsetHeight - 16;
    panel.scrollTo({ top, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  });
  $('detail-locate').addEventListener('click', () => {
    const l = byId.get(current);
    if (!l) return;
    if (readerOpen) setReader(false);
    centerOn(l, 3);
    say(`Carte centrée sur ${l.name}.`);
  });

  document.addEventListener('keydown', (e) => {
    if (readerOpen && e.key === 'Tab') {
      const focusable = [...panel.querySelectorAll('button, a[href], select, input, [tabindex]:not([tabindex="-1"])')].filter(node => node.offsetParent !== null);
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      return;
    }
    if (e.key !== 'Escape' || e.defaultPrevented) return;
    if (readerOpen) { e.preventDefault(); setReader(false); return; }
    if (!panel.hidden) {
      e.preventDefault();
      closeDetail();
    } else if (!wide.matches && toggle.getAttribute('aria-expanded') === 'true') {
      e.preventDefault();
      setSidebar(false);
      toggle.focus();
    }
  });

  /* ---------- Liens profonds #lieu=id ---------- */

  function readHash() {
    const raw = location.hash.replace(/^#/, '');
    if (!raw) {
      if (current) closeDetail();
      return;
    }
    const match = /^lieu=([a-z0-9-]{1,64})$/.exec(raw);
    const id = match && match[1];
    if (id && byId.has(id)) {
      if (id !== current) select(id, { center: true });
      return;
    }
    if (current) closeDetail();
    else setHash(null);
    say('Ce lien ne correspond à aucun lieu de l’atlas.');
  }
  window.addEventListener('hashchange', readHash);

  /* ---------- Démarrage ---------- */

  setSidebar(wide.matches);
  wide.addEventListener('change', (e) => setSidebar(e.matches));
  applyFilter(false);
  resetView(false);
  readHash();
})();
