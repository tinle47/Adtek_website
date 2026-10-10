
// =====================================================================
//  PEOPLE + PAPER HELPERS for this piece (on top of styles/cut-paper/kit.js)
//  txt / ptag / srcLine: Vietnamese text in Inter on torn paper, navy ink, boiling on 2s.
//  figure(): a full-body paper person (feet at x, y; s = 1 is ~560px tall); buyer() and kol() are the two heroes.
// =====================================================================
const overlay = (f) => { if (DEFER) DEFER.push(f); else f(); };
function fontOf(size, weight = 700, family = HAND) { return `${weight} ${size}px ${family}`; }
function tw(str, size, weight = 700, family = HAND) { ctx.save(); ctx.font = fontOf(size, weight, family); const w = ctx.measureText(str).width; ctx.restore(); return w; }
function fitSize(str, maxW, size, weight = 700, family = HAND) { const w = tw(str, size, weight, family); return w > maxW ? Math.floor(size * maxW / w) : size; }
// text with a little boil; align left | center | right; frac writes it on left to right
function txt(str, x, y, size, o = {}) {
  const family = o.font ?? HAND, weight = o.weight ?? 700;
  ctx.save(); ctx.font = fontOf(size, weight, family);
  const w = ctx.measureText(str).width, x0 = o.align === 'center' ? -w / 2 : o.align === 'right' ? -w : 0;
  const R = RNG('tx', o.key ?? str, B);
  ctx.translate(x + R.n(0.6), y + R.n(0.6)); ctx.rotate((o.rot ?? 0) + R.n(0.003));
  const frac = clamp(o.frac ?? 1);
  if (frac <= 0) { ctx.restore(); return w; }
  if (frac < 1) { ctx.beginPath(); ctx.rect(x0 - 6, -size * 1.4, w * frac + 6, size * 2); ctx.clip(); }
  ctx.fillStyle = o.color ?? BR.navy; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  ctx.fillText(str, x0, 0);
  ctx.restore();
  return w;
}
// a torn paper tag holding lines of text, centred on (x, y).
// lines: [{ t, size, weight, color, font, frac }]; o: fill, rot, s (pop scale), tape, key, padX, padY, gap, minW
function ptag(lines, x, y, o = {}) {
  const s = o.s ?? 1; if (s <= 0.01) return null;
  const padX = o.padX ?? 34, padY = o.padY ?? 20, gap = o.gap ?? 6;
  const L = lines.map((l) => ({ ...l, w: tw(l.t, l.size, l.weight ?? 700, l.font ?? HAND), lh: l.size * 1.22 }));
  const w = Math.max(o.minW ?? 0, ...L.map((l) => l.w)) + padX * 2, h = L.reduce((a, l) => a + l.lh, 0) + gap * (L.length - 1) + padY * 2;
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.rot ?? -0.015); ctx.scale(s, s);
  cut(rect(-w / 2, -h / 2, w, h, 4), o.fill ?? PAL.paper, { key: 'pt' + (o.key ?? L[0].t), tear: 1.4, sb: 10, sy: 6 });
  if (o.tape) cut(rect(-36, -h / 2 - 16, 72, 30, 2), 'rgba(240,230,190,0.78)', { key: 'ptape' + (o.key ?? L[0].t), shadow: false, grain: 0.3, shade: false });
  let yy = -h / 2 + padY;
  for (const l of L) {
    const base = yy + l.size * 0.98;
    const xx = (o.align ?? 'center') === 'center' ? 0 : -w / 2 + padX;
    txt(l.t, xx, base, l.size, { align: o.align ?? 'center', weight: l.weight, color: l.color, font: l.font, frac: l.frac, key: 'ptt' + l.t });
    yy += l.lh + gap;
  }
  ctx.restore();
  return { w: w * s, h: h * s };
}
// the source line every number carries: small, on a cream strip, bottom-left, above the phone UI
function srcLine(str) {
  overlay(() => {
    const size = 28, x = 74, y = H - SAFE.bottom - 24, w = tw(str, size, 500);
    cut(rect(x - 16, y - size - 10, w + 32, size + 24, 3), 'rgba(251,246,234,0.94)', { key: 'src' + str, tear: 0.8, sb: 6, sy: 3, grain: 0.4 });
    txt(str, x, y, size, { weight: 500, color: BR.navy, key: 'srct' + str });
  });
}
function wall(c, p, key = 'wall') { cut(rect(-30, -30, W + 60, H + 60, 0), c, { key: key + c, shadow: false, tear: 0, pat: p, grain: 0.8, shade: false }); }
function floor(y, c, p, key = 'floor') { cut(rect(-30, y, W + 60, H - y + 40, 0), c, { key: key + c, tear: 0, sy: -6, pat: p }); }
function starPts5(x, y, r, rot = -Math.PI / 2, k = 0.45) { const P = []; for (let i = 0; i < 10; i++) { const a = rot + i * Math.PI / 5, rr = i % 2 ? r * k : r; P.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } return P; }
function star(x, y, r, c = BR.orange, key = 'st', o = {}) { cut(starPts5(x, y, r, o.rot), c, { key, tear: 0.4, amt: 0.4, sb: 4, sy: 3, crayon: o.crayon, grain: 0.5 }); }
function heartPts(x, y, r) { const P = []; for (let i = 0; i < 40; i++) { const t = i / 40 * TAU; P.push([x + r / 16 * 16 * Math.sin(t) ** 3, y - r / 16 * (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))]); } return P; }
function heart(x, y, r, c, key) { cut(heartPts(x, y, r), c, { key, tear: 0.5, amt: 0.5, sb: 5, sy: 3, grain: 0.5 }); }
// a phone in a hand or on a table: dark body, a screen of colour scr; o.stars draws review stars on the screen
function phone(x, y, w, h, scr, key, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.rot ?? 0);
  cut(rect(-w / 2, -h / 2, w, h, w * 0.16), '#23202a', { key: key + 'b', sb: 6, sy: 4 });
  cut(rect(-w / 2 + w * 0.09, -h / 2 + h * 0.07, w * 0.82, h * 0.84, w * 0.08), scr, { key: key + 's', shadow: false, grain: 0.4, shade: false });
  if (o.stars) for (let i = 0; i < o.stars; i++) star(-w * 0.27 + i * w * 0.27, -h * 0.05, w * 0.12, PAL.paper, key + 'ps' + i);
  if (o.lines) for (let i = 0; i < 2; i++) ink([[-w * 0.3, h * 0.14 + i * h * 0.12], [w * (0.3 - i * 0.15), h * 0.14 + i * h * 0.12]], { w: Math.max(2, w * 0.05), color: 'rgba(0,36,95,0.45)', key: key + 'pl' + i });
  ctx.restore();
}
// ---- a full-body paper person. Feet at (x, y). o: key, skin, hair, hairStyle (bob | short | quiff | bun | long | cap),
//      shirt, shirtPat, crayon, pants, shoe, mood, armL / armR (angle of the arm, radians, canvas convention: PI/2 = down),
//      dress, glasses ('shades' | 'round'), shadeC, chain, earrings. Returns the head centre and the hands.
function figure(x, y, s, o = {}) {
  const k = o.key ?? 'fg', skin = o.skin ?? PAL.skin1, hair = o.hair ?? '#2b211d', shirt = o.shirt ?? PAL.blue, pants = o.pants ?? '#3a4a6b', shoe = o.shoe ?? '#f4f0e6';
  const ph = k.length * 1.37, breath = Math.sin(TT * TAU * 0.6 + ph) * 3 * s, hop = o.hop ?? 0;
  y -= hop;
  // legs and shoes
  if (!o.dress) {
    cut(capsulePts(x - 28 * s, y - 215 * s, x - 32 * s, y - 28 * s, 50 * s), pants, { key: k + 'lL', sb: 6, pat: o.pantsPat });
    cut(capsulePts(x + 28 * s, y - 215 * s, x + 32 * s, y - 28 * s, 50 * s), pants, { key: k + 'lR', sb: 6, pat: o.pantsPat });
  } else {
    cut(capsulePts(x - 26 * s, y - 150 * s, x - 28 * s, y - 28 * s, 34 * s), skin, { key: k + 'lL', sb: 5 });
    cut(capsulePts(x + 26 * s, y - 150 * s, x + 28 * s, y - 28 * s, 34 * s), skin, { key: k + 'lR', sb: 5 });
  }
  cut(ellipsePts(x - 40 * s, y - 16 * s, 34 * s, 17 * s, 0, 18), shoe, { key: k + 'sL', sb: 4 });
  cut(ellipsePts(x + 40 * s, y - 16 * s, 34 * s, 17 * s, 0, 18), shoe, { key: k + 'sR', sb: 4 });
  const ty = y - 205 * s + breath;   // hip line (the torso breathes)
  // the back of the hair (bob, long) sits behind the body
  const hx = x, hy = ty - 270 * s;      // head centre
  if (o.hairStyle === 'long' || o.hairStyle === 'bob') {
    const lo = o.hairStyle === 'long' ? 110 : 30;
    cut([[hx - 76 * s, hy - 30 * s], [hx - 70 * s, hy - 82 * s], [hx - 30 * s, hy - 104 * s], [hx + 30 * s, hy - 104 * s], [hx + 70 * s, hy - 82 * s], [hx + 76 * s, hy - 30 * s], [hx + 78 * s, hy + (40 + lo) * s], [hx - 78 * s, hy + (40 + lo) * s]], hair, { key: k + 'hb', sb: 6 });
  }
  // torso (a dress flares out below the waist)
  const tP = o.dress
    ? [[x - 74 * s, ty - 178 * s], [x + 74 * s, ty - 178 * s], [x + 66 * s, ty - 60 * s], [x + 104 * s, ty + 60 * s], [x - 104 * s, ty + 60 * s], [x - 66 * s, ty - 60 * s]]
    : rrectPts(x - 76 * s, ty - 182 * s, 152 * s, 196 * s, 34 * s);
  cut(tP, shirt, { key: k + 't', pat: o.shirtPat, crayon: o.crayon, crAl: 0.25, crPer: 40 });
  if (o.apron) cut(rrectPts(x - 56 * s, ty - 150 * s, 112 * s, 170 * s, 14 * s), o.apron, { key: k + 'ap', sb: 4, pat: pat.stripes('rgba(255,255,255,0.10)', 4, 26) });
  if (o.chain) { ink(arcPts(x, ty - 178 * s, 44 * s, 0.25, Math.PI - 0.25, 16), { w: 5 * s, color: BR.gold, key: k + 'ch' }); cut(ellipsePts(x, ty - 132 * s, 12 * s, 14 * s, 0, 14), BR.gold, { key: k + 'chp', sb: 3 }); }
  // neck, ears, head
  cut(rect(x - 20 * s, ty - 210 * s, 40 * s, 40 * s, 8 * s), skin, { key: k + 'n', shadow: false });
  cut(ellipsePts(hx - 60 * s, hy + 6 * s, 12 * s, 17 * s, 0, 12), skin, { key: k + 'eL', sb: 4 });
  cut(ellipsePts(hx + 60 * s, hy + 6 * s, 12 * s, 17 * s, 0, 12), skin, { key: k + 'eR', sb: 4 });
  if (o.earrings) { cut(ellipsePts(hx - 62 * s, hy + 30 * s, 6 * s, 6 * s, 0, 10), BR.gold, { key: k + 'erL', sb: 2 }); cut(ellipsePts(hx + 62 * s, hy + 30 * s, 6 * s, 6 * s, 0, 10), BR.gold, { key: k + 'erR', sb: 2 }); }
  cut(ellipsePts(hx, hy, 60 * s, 68 * s, 0, 30), skin, { key: k + 'h' });
  // hair on top
  const st = o.hairStyle ?? 'short';
  if (st === 'bob' || st === 'long') cut([[hx - 66 * s, hy - 6 * s], [hx - 64 * s, hy - 58 * s], [hx - 30 * s, hy - 82 * s], [hx + 30 * s, hy - 82 * s], [hx + 64 * s, hy - 58 * s], [hx + 66 * s, hy - 6 * s], [hx + 44 * s, hy - 40 * s], [hx - 10 * s, hy - 46 * s], [hx - 40 * s, hy - 26 * s]], hair, { key: k + 'hf', sb: 4 });
  else if (st === 'quiff') {
    cut([[hx - 64 * s, hy - 4 * s], [hx - 66 * s, hy - 60 * s], [hx - 40 * s, hy - 120 * s], [hx + 10 * s, hy - 150 * s], [hx + 70 * s, hy - 136 * s], [hx + 54 * s, hy - 112 * s], [hx + 66 * s, hy - 60 * s], [hx + 64 * s, hy - 4 * s], [hx + 48 * s, hy - 46 * s], [hx - 46 * s, hy - 46 * s]], hair, { key: k + 'hf', sb: 5 });
    if (o.tip) cut([[hx - 6 * s, hy - 142 * s], [hx + 70 * s, hy - 136 * s], [hx + 50 * s, hy - 110 * s], [hx + 10 * s, hy - 116 * s]], o.tip, { key: k + 'tip', sb: 3 });
  } else if (st === 'cap') {
    cut([[hx - 64 * s, hy - 20 * s], [hx - 60 * s, hy - 70 * s], [hx - 20 * s, hy - 92 * s], [hx + 30 * s, hy - 92 * s], [hx + 62 * s, hy - 66 * s], [hx + 66 * s, hy - 20 * s]], o.capC ?? PAL.green, { key: k + 'cap', sb: 4, pat: pat.stripes('rgba(255,255,255,0.18)', 6, 30, 0.3) });
    cut(capsulePts(hx + 30 * s, hy - 26 * s, hx + 110 * s, hy - 18 * s, 18 * s), o.capC ?? PAL.green, { key: k + 'bill', sb: 4 });
  } else {
    cut([[hx - 64 * s, hy - 4 * s], [hx - 64 * s, hy - 58 * s], [hx - 30 * s, hy - 86 * s], [hx + 34 * s, hy - 86 * s], [hx + 66 * s, hy - 56 * s], [hx + 64 * s, hy - 4 * s], [hx + 50 * s, hy - 40 * s], [hx - 50 * s, hy - 44 * s]], hair, { key: k + 'hf', sb: 4 });
    if (st === 'bun') cut(ellipsePts(hx + 8 * s, hy - 100 * s, 30 * s, 26 * s, 0, 18), hair, { key: k + 'bun', sb: 4 });
  }
  face(hx, hy + 8 * s, s * 0.95, o.mood ?? 'smile');
  if (o.glasses === 'shades') {
    const dy = (o.shadesDrop ?? 0) * s, c = o.shadeC ?? '#d04a8c';
    [-1, 1].forEach((d) => cut(rrectPts(hx + d * 24 * s - 21 * s, hy - 6 * s + dy, 42 * s, 28 * s, 10 * s), '#1d1a22', { key: k + 'g' + d, sb: 3, line: c, lw: 5 * s }));
    ink([[hx - 4 * s, hy + 4 * s + dy], [hx + 4 * s, hy + 4 * s + dy]], { w: 5 * s, color: c, key: k + 'gb' });
    dot(hx - 30 * s, hy + 1 * s + dy, 4 * s, 'rgba(255,255,255,0.8)'); dot(hx + 18 * s, hy + 1 * s + dy, 4 * s, 'rgba(255,255,255,0.8)');
  } else if (o.glasses === 'round') {
    ctx.strokeStyle = PAL.ink; ctx.lineWidth = 4 * s; ctx.beginPath(); ctx.arc(hx - 16 * s, hy + 8 * s, 15 * s, 0, TAU); ctx.moveTo(hx + 31 * s, hy + 8 * s); ctx.arc(hx + 16 * s, hy + 8 * s, 15 * s, 0, TAU); ctx.stroke();
  }
  // arms last (in front of the body): shoulder -> hand
  const shY = ty - 166 * s, arm = 170 * s, hands = {};
  [['L', -1, o.armL ?? Math.PI / 2 + 0.2], ['R', 1, o.armR ?? Math.PI / 2 - 0.2]].forEach(([n, d, a]) => {
    const sx = x + d * 66 * s, hxx = sx + Math.cos(a) * arm, hyy = shY + Math.sin(a) * arm;
    cut(capsulePts(sx, shY, hxx, hyy, 40 * s), o.sleeve ?? shirt, { key: k + 'a' + n, sb: 5, pat: o.shirtPat, crayon: o.crayon, crAl: 0.2 });
    cut(ellipsePts(hxx, hyy, 21 * s, 21 * s, 0, 14), skin, { key: k + 'hd' + n, sb: 4 });
    hands[n] = [hxx, hyy];
  });
  return { head: [hx, hy], hands, top: hy - 90 * s };
}
// THE BUYER: an ordinary shopper. Orange (Adtek) shirt = a real buyer; jeans, bob hair, a canvas tote
function buyer(x, y, s, o = {}) {
  const R = figure(x, y, s, { key: 'buyer', skin: PAL.skin1, hair: '#3b2a22', hairStyle: 'bob', shirt: BR.orange, crayon: BR.orangeD, pants: PAL.blue, pantsPat: pat.lines('rgba(255,255,255,0.10)', 9), shoe: '#f7f3ea', earrings: true, ...o });
  return R;
}
// THE KOL: purple sequins, shades, a gold chain, a quiff with a bleached tip. Never orange.
function kol(x, y, s, o = {}) {
  return figure(x, y, s, { key: 'kol', skin: PAL.skin2, hair: '#1f1a24', hairStyle: 'quiff', tip: '#f2d27a', shirt: '#7b5cc9', shirtPat: (bb) => { pat.dots('rgba(255,224,120,0.55)', 4, 22)(bb); pat.dots('rgba(255,255,255,0.35)', 2.5, 34)(bb); }, pants: '#2a2633', shoe: '#e9e2f5', glasses: 'shades', chain: true, ...o });
}
function mic(x, y, s, key = 'mic', a = -0.5) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a);
  cut(capsulePts(0, 0, 0, -70 * s, 16 * s), '#2b2733', { key: key + 'h', sb: 4 });
  cut(ellipsePts(0, -88 * s, 22 * s, 24 * s, 0, 18), '#b9b6c4', { key: key + 'b', sb: 4, pat: pat.gingham('rgba(40,40,50,0.35)', 3) });
  ctx.restore();
}
function sweat(x, y, s, key = 'sw') { cut([[x, y - 22 * s], [x + 12 * s, y], [x + 8 * s, y + 12 * s], [x - 8 * s, y + 12 * s], [x - 12 * s, y]], '#9fd3f0', { key, sb: 3, tear: 0.3 }); }
function confetti(key, t0, n = 90, y0 = 200, y1 = 1500, cols = [PAL.teal, PAL.yellow, PAL.purple, PAL.mint, '#ffffff', PAL.pink]) {
  if (TT < t0) return;
  const R = RNG('cf', key);
  for (let i = 0; i < n; i++) {
    const x = R.r(0, W), sp = R.r(140, 260), y = y0 + mod(R.r(0, y1 - y0) + (TT - t0) * sp, y1 - y0), a = R.r(0, 3) + TT * 3;
    ctx.save(); ctx.translate(x + Math.sin(TT * 2 + i) * 14, y); ctx.rotate(a); ctx.fillStyle = cols[i % cols.length]; ctx.fillRect(-9, -4, 18, 8); ctx.restore();
  }
}
function bunting(y, key = 'bunt', cols = [PAL.purple, PAL.yellow, PAL.teal, PAL.pink]) {
  ink([[-20, y], [300, y + 40], [600, y + 46], [900, y + 30], [1100, y]], { w: 3, color: '#4a4550', amt: 0.4, key: key + 'w' });
  for (let i = 0; i < 12; i++) { const x = 20 + i * 92, yy = y + Math.sin(i / 11 * Math.PI) * 42 + 4; cut([[x - 30, yy], [x + 30, yy], [x, yy + 56 + Math.sin(TT * 3 + i) * 4]], cols[i % cols.length], { key: key + i, sb: 4 }); }
}
// a speech bubble (rounded) with a tail to (tx, ty)
function bubble(x, y, w, h, tx, ty, fill, key) {
  cut([[x + w * 0.22, y + h - 6], [tx, ty], [x + w * 0.38, y + h - 6]], fill, { key: key + 'tl', sb: 6 });
  cut(rect(x, y, w, h, 40), fill, { key: key + 'bb', sb: 10 });
}
