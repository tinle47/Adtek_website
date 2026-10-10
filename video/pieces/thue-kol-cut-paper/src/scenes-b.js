
// =====================================================================
//  SCENES (2/2): what makes a review trustworthy (bars), under 3.6 stars (the bin), 50 reviews (the stack),
//  what to do now (the packing table)
// =====================================================================
// ---- three paper bars, true to scale from zero (10px per point): real photo/video 69, detail 60, stars 51
function camIcon(x, y, k) { cut(rect(x - 40, y - 26, 80, 56, 10), '#2b2733', { key: k + 'b', sb: 4 }); cut(rect(x - 18, y - 36, 30, 14, 4), '#2b2733', { key: k + 't', shadow: false }); cut(ellipsePts(x, y + 2, 18, 18, 0, 16), '#9fd3f0', { key: k + 'l', shadow: false }); dot(x + 26, y - 14, 4, '#ff5f5f'); }
function docIcon(x, y, k) { cut(rect(x - 30, y - 38, 60, 76, 4), PAL.paper, { key: k + 'd', sb: 4 }); for (let i = 0; i < 4; i++) ink([[x - 18, y - 22 + i * 15], [x + (i === 3 ? 4 : 18), y - 22 + i * 15]], { w: 4, color: 'rgba(0,36,95,0.55)', key: k + 'l' + i }); }
function sBars() {
  const cu = TIMELINE.cues;
  wall(PAL.mint, pat.stripes('rgba(255,255,255,0.22)', 20, 64, 0.0), 'mintW');
  floor(1250, '#e9dcc0', pat.lines('rgba(120,90,50,0.18)', 34), 'barF');
  const rows = [
    ['Có ảnh hoặc video thật', 69, cu.photo, cu.p69, BR.orange, camIcon],
    ['Nội dung chi tiết', 60, cu.detail, cu.p60, BR.navy, docIcon],
    ['Số sao', 51, cu.star, cu.p51, BR.navy, (x, y, k) => star(x, y, 38, PAL.yellow, k, { crayon: PAL.mustard })],
  ];
  rows.forEach(([label, v, tl, tv, c, icon], i) => {
    const y = 540 + i * 230, len = v * 10 * springMove(tv - 0.12, 0, 1, SPRING.heavy);
    if (TT >= tl - 0.1) { cut(ellipsePts(140, y + 50, 62, 62, 0, 30), '#ffffff', { key: 'ib' + i, sb: 8 }); icon(140, y + 50, 'ic' + i); }
    txt(label, 220, y - 14, 46, { weight: 800, key: 'bl' + i, frac: ev(tl - 0.1, 0.5) });
    if (len > 4) cut(rect(220, y + 6, len, 92, 8), c, { key: 'bar' + i, crayon: c === BR.orange ? BR.orangeD : null, crAl: 0.25, pat: c === BR.navy ? pat.stripes('rgba(255,255,255,0.06)', 6, 22, 0.6) : null });
    if (len > v * 10 * 0.9) txt(`${v}%`, 220 + len - 24, y + 76, 62, { align: 'right', weight: 900, font: DISPLAY, color: c === BR.orange ? BR.navy : '#ffffff', key: 'bv' + i });
  });
  // the buyer studies a real review through a magnifier; the review card has a real photo
  ctx.save(); ctx.translate(330, 1330); ctx.rotate(-0.04);
  cut(rect(-250, -130, 500, 260, 10), PAL.paper, { key: 'rcard' });
  cut(rect(-226, -106, 170, 150, 4), PAL.sky, { key: 'rphoto', shadow: false, pat: (bb) => { ctx.fillStyle = PAL.green; ctx.beginPath(); ctx.moveTo(bb.x0, bb.y1); ctx.lineTo(bb.x0 + 60, bb.y0 + 70); ctx.lineTo(bb.x0 + 110, bb.y1 - 30); ctx.lineTo(bb.x1, bb.y0 + 60); ctx.lineTo(bb.x1, bb.y1); ctx.fill(); dot(bb.x1 - 40, bb.y0 + 34, 16, PAL.yellow); } });
  for (let i = 0; i < 5; i++) star(-20 + i * 46, -80, 18, BR.orange, 'rcs' + i);
  for (let i = 0; i < 3; i++) ink([[-30, -30 + i * 34], [200 - i * 40, -30 + i * 34]], { w: 7, color: 'rgba(0,36,95,0.35)', key: 'rcl' + i });
  ctx.restore();
  const Bh = buyer(830, 1660, 0.95, { mood: TT >= cu.p51 ? 'smile' : 'focus', armL: Math.PI - 0.45, armR: Math.PI / 2 - 0.1 });
  const [mx, my] = [Bh.hands.L[0] - 80 + Math.sin(TT * 2.4) * 12, Bh.hands.L[1] - 40];
  cut(capsulePts(Bh.hands.L[0], Bh.hands.L[1], mx + 30, my + 30, 18), '#5a3a28', { key: 'mgH', sb: 4 });
  ctx.save(); ctx.strokeStyle = '#2b2733'; ctx.lineWidth = 12; ctx.beginPath(); ctx.arc(mx, my, 62, 0, TAU); ctx.stroke(); ctx.fillStyle = 'rgba(200,235,255,0.35)'; ctx.fill(); ctx.restore();
  plant(60, 1250, 0.9, PAL.pink, 'plB');
  overlay(() => ptag([{ t: 'Review nào đáng tin?', size: 62, weight: 800 }], 470, 330, { key: 'qT', tape: true, rot: -0.02, s: popS(E0) }));
  srcLine('Nguồn: Q&Me, 200 người 20 đến 49 tuổi, 09/2026');
}
// ---- under 3.6 stars: the buyer flicks the product into the bin
function prodBox(x, y, s, rot0, key) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot0); ctx.scale(s, s);
  cut(rect(-90, -110, 180, 220, 8), '#f4d9e6', { key: key + 'b', pat: pat.stripes('rgba(140,122,216,0.3)', 12, 36) });
  cut(rect(-70, -40, 140, 70, 6), PAL.paper, { key: key + 'l', shadow: false });
  for (let i = 0; i < 5; i++) { const sx = -56 + i * 28; if (i < 2) star(sx, -4, 13, PAL.yellow, key + 's' + i); else { ctx.strokeStyle = 'rgba(0,36,95,0.45)'; ctx.lineWidth = 2.5; trace(starPts5(sx, -4, 13), true); ctx.stroke(); } }
  ctx.restore();
}
function sDrop() {
  const cu = TIMELINE.cues;
  wall('#c9b9da', pat.stripes('rgba(255,255,255,0.18)', 34, 90, 0.0), 'lavW');
  clock(830, 360, 80, 3, 40, 'ckD');
  // the star meter: five big stars, a red cut line at 3.6 (true to scale); everything left of it is filled
  const CUTX = 150 + 3.6 * 130, mk = ev(cu.p36 - 0.1, 0.5);
  cut(rect(110, 640, 730, 170, 12), PAL.paper, { key: 'meter', tear: 1.0 });
  for (let i = 0; i < 5; i++) { const x = 215 + i * 130; ctx.save(); trace(starPts5(x, 725, 56), true); ctx.fillStyle = '#d9d3e2'; ctx.fill(); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, lerp(150, CUTX, mk), H); ctx.clip(); star(x, 725, 56, PAL.yellow, 'ms' + i, { crayon: PAL.mustard }); ctx.restore(); }
  if (mk > 0.95) { ctx.setLineDash([16, 12]); ink([[CUTX, 600], [CUTX, 850]], { w: 8, color: BR.red, key: 'cutL' }); ctx.setLineDash([]); }
  floor(1350, '#a98d72', pat.grainWood('rgba(80,50,20,0.18)'), 'dFloor');
  // the bin
  const wob = TT >= cu.loai + 0.4 ? Math.sin((TT - cu.loai - 0.4) * 30) * 0.06 * Math.exp(-(TT - cu.loai - 0.4) * 5) : 0;
  ctx.save(); ctx.translate(760, 1390); ctx.rotate(wob);
  cut([[-120, -260], [120, -260], [100, 0], [-100, 0]], '#8a8590', { key: 'bin', pat: pat.stripes('rgba(255,255,255,0.18)', 8, 30, Math.PI / 2) });
  cut(rect(-136, -284, 272, 34, 8), '#6e6a76', { key: 'binL' });
  ctx.restore();
  // a fly circles the bin
  const fa = TT * 5; cut(ellipsePts(760 + Math.cos(fa) * 120, 1020 + Math.sin(fa) * 40, 9, 7, 0, 10), '#2b2733', { key: 'fly', sb: 2 }); dot(752 + Math.cos(fa) * 120, 1012 + Math.sin(fa) * 40, 7, 'rgba(255,255,255,0.7)');
  // the product: in her hand, then flicked in an arc into the bin
  const u = clamp((TT - cu.loai) / 0.4);
  const Bh = buyer(300, 1460, 1.0, { mood: TT < cu.loai ? 'focus' : 'smile', armR: TT < cu.loai ? -0.5 : -0.2 + u * 0.4, armL: Math.PI / 2 + 0.2 });
  if (u < 1) { const [hx, hy] = Bh.hands.R, x = lerp(hx + 70, 760, u), y = lerp(hy - 60, 1120, u) - Math.sin(u * Math.PI) * 240; prodBox(x, y, 1 - u * 0.45, u * 4, 'prod'); }
  if (u >= 1 && TT - cu.loai < 0.9) { const R = RNG('puff'); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + R.n(1.2), d = 30 + (TT - cu.loai - 0.4) * 300; dot(760 + Math.cos(a) * d, 1110 + Math.sin(a) * d * 0.6, 6, 'rgba(255,255,255,0.75)'); } }
  overlay(() => ptag([{ t: 'Dưới 3.6 sao', size: 84, weight: 900 }, { t: 'bị loại', size: 64, weight: 800, color: BR.red }], 470, 420, { key: 'p36', s: popS(cu.p36 - 0.1), tape: true }));
  srcLine('Nguồn: Q&Me, 09/2026');
}
// ---- 74% need 50 reviews: the stack of real reviews grows on 2s
function reviewCard(x, y, k, i) {
  cut(rect(x - 150, y - 20, 300, 40, 5), i % 3 ? PAL.paper : '#fff7ea', { key: k, sb: 4, sy: 3, grain: 0.3, shade: false });
  dot(x - 124, y, 11, [PAL.skin1, PAL.skin2, PAL.skin3][i % 3]);
  for (let s = 0; s < 4; s++) star(x - 92 + s * 24, y, 9, BR.orange, k + 's' + s);
  ink([[x + 10, y], [x + 120 - (i % 4) * 14, y]], { w: 5, color: 'rgba(0,36,95,0.3)', key: k + 'l' });
}
function sFifty() {
  const cu = TIMELINE.cues;
  wall('#f3d6be', pat.dots('rgba(255,255,255,0.35)', 5, 46), 'peachW');
  floor(1420, '#c08048', pat.grainWood('rgba(120,60,20,0.18)'), 'fFloor');
  plant(70, 1420, 1.0, PAL.teal, 'plF');
  // the stack: one card every 2 frames from the cut until "50"
  const n = Math.min(24, Math.max(4, Math.floor((TT - E0) * 15) + 4)), R = RNG('stack');
  for (let i = 0; i < n; i++) reviewCard(730 + R.n(16), 1400 - i * 22, 'rc' + i, i);
  const topY = 1400 - (n - 1) * 22;
  if (n < 24) { const fy = topY - 90; reviewCard(730, fy, 'rcF', n); }
  const Bh = buyer(300, 1460, 1.0, { mood: TT >= cu.n50 ? 'happy' : 'wow', armL: Math.PI / 2 + 0.2, armR: TT >= cu.n50 ? -0.9 : -0.3 });
  if (TT >= cu.n50) { const [hx, hy] = Bh.hands.R; cut(ellipsePts(hx, hy - 30, 14, 24, 0, 12), PAL.skin1, { key: 'thumb', sb: 3 }); }
  confetti('f50', cu.n50, 70, 260, 1400, [BR.orangeL, PAL.paper, PAL.mint, PAL.yellow]);
  overlay(() => {
    ptag([{ t: '74%', size: 150, weight: 900, font: DISPLAY, color: BR.orangeD }, { t: 'cần từ 50 đánh giá', size: 54, weight: 800 }, { t: 'mới tin', size: 54, weight: 800 }], 470, 520, { key: 'p74', s: popS(cu.p74), tape: true, padY: 14, gap: 0 });
    ptag([{ t: '50 đánh giá', size: 44, weight: 800 }], 730, topY - 90, { key: 'n50', s: popS(cu.n50), rot: 0.03, fill: '#fff3df' });
  });
  srcLine('Nguồn: Q&Me, 200 người 20 đến 49 tuổi, 09/2026');
}
// ---- what to do now: a checklist pinned to a cork board; the seller (navy apron) acts each step out on the table
function sTodo() {
  const cu = TIMELINE.cues;
  wall('#c9a46a', (bb) => { pat.dots('rgba(120,80,30,0.25)', 2.5, 14)(bb); pat.dots('rgba(255,240,210,0.25)', 2, 19)(bb); }, 'cork');
  // the notepad
  ctx.save(); ctx.translate(500, 590); ctx.rotate(-0.012);
  cut(rect(-440, -330, 880, 660, 6), PAL.paper, { key: 'note', pat: pat.lines('rgba(76,111,181,0.22)', 60, 50) });
  ink([[-370, -330], [-370, 330]], { w: 3, color: 'rgba(216,51,74,0.45)', key: 'margin' });
  dot(-380, -300, 13, '#d8334a'); dot(380, -300, 13, '#2f7a5c');
  ctx.restore();
  txt('Làm gì ngay?', 140, 352, 66, { weight: 900, key: 'todoT', frac: ev(cu.todo - 0.2, 0.5) });
  const items = [
    ['Mã QR, link trên gói hàng', 'nhắm tới 50 đánh giá đầu tiên', cu.i1, cu.i1b],
    ['Xin khách kèm ảnh, video', null, cu.i2, 0],
    ['Không tặng quà đổi đánh giá', 'Google cấm, xem là đánh giá giả', cu.i3, cu.i3 + 0.9],
    ['Trả lời mọi đánh giá', 'kể cả lời chê', cu.i4, cu.i4 + 0.7],
  ];
  items.forEach(([t, sub, at, sat], i) => {
    const y = 470 + i * 118;
    cut(rect(122, y - 42, 46, 46, 5), '#ffffff', { key: 'tb' + i, sb: 3, line: BR.navy, lw: 3 });
    if (TT >= at) ink([[130, y - 20], [142, y - 4], [176, y - 50]], { w: 8, color: BR.navy, key: 'tk' + i, frac: ev(at, 0.2) });
    const size = fitSize(t, 720, 48, 800);
    txt(t, 190, y, size, { weight: 800, key: 'it' + i, frac: ev(at - 0.05, 0.6), color: i === 2 ? BR.red : BR.navy });
    if (sub) txt(sub, 190, y + 44, 34, { weight: 600, key: 'is' + i, frac: ev(sat, 0.5), color: 'rgba(0,36,95,0.85)' });
  });
  // the table
  floor(1170, '#b9824a', pat.grainWood('rgba(90,45,10,0.18)'), 'table');
  // the seller behind the table (navy apron: the shop, the viewer)
  person(930, 1110, 0.62, { key: 'seller', skin: PAL.skin2, hair: '#1f1a24', shirt: BR.navy, shirtPat: pat.stripes('rgba(255,255,255,0.08)', 6, 26), mood: TT >= cu.i3 && TT < cu.i4 ? 'focus' : 'happy' });
  cut(rect(-30, 1170, W + 60, 40, 0), '#9c6a3a', { key: 'tedge', tear: 0.3, sy: 4 });
  // 1: a parcel; the QR sticker slaps on
  cut(rect(110, 1240, 230, 170, 6), '#c9925a', { key: 'parcel', pat: pat.stripes('rgba(90,45,10,0.12)', 4, 18) });
  cut(rect(205, 1240, 40, 170, 2), 'rgba(235,215,170,0.85)', { key: 'ptape', shadow: false, grain: 0.3, shade: false });
  const q = popS(cu.i1 + 0.3);
  if (q > 0.01) { ctx.save(); ctx.translate(160, 1300); ctx.scale(q, q); ctx.rotate(-0.08); cut(rect(-40, -40, 80, 80, 3), '#ffffff', { key: 'qr', sb: 4 }); const R = RNG('qr'); ctx.fillStyle = '#1d1a22'; for (let a = 0; a < 7; a++) for (let b = 0; b < 7; b++) if (R.f() > 0.5 || (a < 2 && b < 2) || (a > 4 && b < 2) || (a < 2 && b > 4)) ctx.fillRect(-32 + a * 9.2, -32 + b * 9.2, 8.6, 8.6); ctx.restore(); }
  // 2: the phone takes a photo: a flash and a polaroid pops out
  phone(470, 1320, 110, 190, TT >= cu.i2 ? '#ffffff' : '#c9c4d4', 'tph', { rot: -0.08 });
  if (TT >= cu.i2 && TT < cu.i2 + 0.2) { ctx.save(); ctx.fillStyle = 'rgba(255,255,240,0.75)'; ctx.beginPath(); ctx.arc(470, 1240, 120, 0, TAU); ctx.fill(); ctx.restore(); }
  const pp = popS(cu.i2 + 0.25);
  if (pp > 0.01) { ctx.save(); ctx.translate(560, 1230); ctx.rotate(0.12); ctx.scale(pp, pp); cut(rect(-60, -70, 120, 140, 3), '#fbf8f0', { key: 'tpol' }); cut(rect(-48, -58, 96, 92, 2), PAL.sky, { key: 'tpolI', shadow: false }); star(0, -12, 26, BR.orange, 'tpolS'); ctx.restore(); }
  // 3: the gift box; a red cross slams over it
  cut(rect(650, 1280, 150, 130, 6), PAL.pink, { key: 'gift', pat: pat.dots('rgba(255,255,255,0.4)', 4, 20) });
  cut(rect(714, 1280, 22, 130, 2), PAL.purple, { key: 'ribV', shadow: false }); cut(rect(650, 1330, 150, 22, 2), PAL.purple, { key: 'ribH', shadow: false });
  cut(ellipsePts(704, 1270, 30, 18, -0.4, 14), PAL.purple, { key: 'bowL', sb: 3 }); cut(ellipsePts(746, 1270, 30, 18, 0.4, 14), PAL.purple, { key: 'bowR', sb: 3 });
  const x3 = popS(cu.i3 + 0.3);
  if (x3 > 0.01) { ctx.save(); ctx.translate(725, 1340); ctx.scale(x3, x3); cut(rot(capsulePts(-100, 0, 100, 0, 30), 0, 0, 0.78), BR.red, { key: 'xA', sb: 6 }); cut(rot(capsulePts(-100, 0, 100, 0, 30), 0, 0, -0.78), BR.red, { key: 'xB', sb: 6 }); ctx.restore(); }
  // 4: a grey complaint bubble, answered by a reply bubble with a heart
  if (TT >= cu.i4 - 0.1) { const s4 = popS(cu.i4 - 0.1); ctx.save(); ctx.translate(880, 1240); ctx.scale(s4, s4); bubble(-90, -60, 170, 100, -40, 70, '#d9d5df', 'cplB'); face(-5, -14, 0.55, 'sad'); ctx.restore(); }
  if (TT >= cu.che) { const s5 = popS(cu.che); ctx.save(); ctx.translate(880, 1400); ctx.scale(s5, s5); bubble(-90, -50, 170, 96, 60, 70, '#ffffff', 'rplB'); heart(-5, -4, 26, BR.orange, 'rplH'); ctx.restore(); }
  srcLine('Nguồn: Google Business Profile Help; Q&Me, 09/2026');
}
