
// =====================================================================
//  SCENES (1/2): the stage (hook + SAI, and the finale), the survey, the versus columns, the shoppers, age 20
// =====================================================================
// ---- the stage: a KOL livestream. The hook banner is complete on frame 0; SAI is stamped on "Sai."
//      end: the same stage, changed: the buyer holds the mic, the KOL sits in the audience, the banner tells the truth
function sStage(o = {}) {
  const end = !!o.end, cu = TIMELINE.cues, after = !end && TT >= cu.sai;
  wall('#a8406f', (bb) => { pat.stripes('rgba(60,10,40,0.16)', 26, 70)(bb); pat.stripes('rgba(255,255,255,0.07)', 8, 70)(bb); }, 'curtain');
  // curtain swags at the sides
  cut([[-40, 180], [170, 180], [120, 700], [60, 1240], [-40, 1240]], '#8e2f5a', { key: 'swagL', pat: pat.stripes('rgba(0,0,0,0.12)', 14, 44, 0.12) });
  cut([[1120, 180], [910, 180], [960, 700], [1020, 1240], [1120, 1240]], '#8e2f5a', { key: 'swagR', pat: pat.stripes('rgba(0,0,0,0.12)', 14, 44, -0.12) });
  bunting(188, 'buntS');
  // spotlights: on the KOL at the start; off once the myth is stamped; on the buyer at the end
  const spotX = end ? 300 : 600, on = end ? true : !(after && (TT - cu.sai > 0.4 || B % 2));
  if (on) { ctx.save(); const g = ctx.createLinearGradient(0, 0, 0, 1260); g.addColorStop(0, 'rgba(255,240,190,0.05)'); g.addColorStop(1, 'rgba(255,236,170,0.40)'); ctx.fillStyle = g;
    ctx.beginPath(); ctx.moveTo(spotX - 60, 0); ctx.lineTo(spotX + 60, 0); ctx.lineTo(spotX + 250, 1270); ctx.lineTo(spotX - 250, 1270); ctx.closePath(); ctx.fill(); ctx.restore(); }
  // the stage floor
  const FY = end ? 1180 : 1240;
  cut(rect(-30, FY, W + 60, H - FY + 40, 0), PAL.wood, { key: 'stageF' + FY, tear: 0, sy: -8, pat: (bb) => { pat.grainWood('rgba(120,60,20,0.18)')(bb); pat.lines('rgba(80,40,10,0.25)', 70, 30)(bb); } });
  cut(rect(-30, FY - 4, W + 60, 26, 0), '#7a4a26', { key: 'lip' + FY, tear: 0.5 });
  if (on) { ctx.save(); ctx.fillStyle = 'rgba(255,240,180,0.35)'; ctx.beginPath(); ctx.ellipse(spotX, FY + 40, 260, 46, 0, 0, TAU); ctx.fill(); ctx.restore(); }
  // the live phone on a tripod (the KOL's world)
  if (!end) {
    ink([[880, 1240], [880, 1060]], { w: 8, color: '#2b2733', key: 'tri0' }); ink([[880, 1150], [830, 1240]], { w: 6, color: '#2b2733', key: 'tri1' }); ink([[880, 1150], [930, 1240]], { w: 6, color: '#2b2733', key: 'tri2' });
    phone(880, 990, 110, 190, '#f7c9dc', 'livePh', { rot: 0.04 });
    // hearts float up from the live, until the myth is stamped
    const R = RNG('hearts');
    for (let i = 0; i < 9; i++) { const ph = R.f(), tt = (after ? cu.sai : TT) * 0.55 + ph, u = mod(tt, 1), hx = 860 + Math.sin(u * 7 + i) * 40 + R.n(30), hy = 900 - u * 520; if (after && hy < 0) continue; heart(hx, hy, 18 + 10 * R.f(), i % 3 ? '#ff5f8f' : '#ffd1e0', 'ht' + i); }
    ptag([{ t: 'LIVE', size: 34, weight: 800, color: '#ffffff' }], 860, 870, { fill: '#d8334a', key: 'live', rot: 0.05, padX: 18, padY: 8 });
  }
  // the ring light behind the performer
  const rx = end ? 280 : 600, ry = end ? 760 : 800;
  cut(ellipsePts(rx, ry, 190, 190, 0, 48), '#fff5e6', { key: 'ringO' + end, sb: 18 });
  cut(ellipsePts(rx, ry, 150, 150, 0, 48), '#a8406f', { key: 'ringI' + end, shadow: false, pat: pat.stripes('rgba(60,10,40,0.16)', 26, 70), grain: 0.5 });
  if (!end) {
    // the KOL performs: mic in one hand, a product up in the other; sparkles around him
    const pose = TT >= cu.kol && TT < cu.hush ? Math.sin((TT - cu.kol) * 9) * 0.15 : 0;
    const mood = !after ? (TT < cu.hush ? 'happy' : 'smile') : TT - cu.sai < 0.7 ? 'wow' : 'sad';
    const K = kol(600, 1240, 0.92, { mood, armL: -Math.PI / 2 - 0.95 + pose, armR: Math.PI / 2 + 1.05, shadesDrop: after ? Math.min(18, (TT - cu.sai) * 60) : 0 });
    // the product (a serum bottle) held high
    const [px, py] = K.hands.L;
    cut(rect(px - 26, py - 120, 52, 100, 10), '#f6e7f0', { key: 'bottle', pat: pat.stripes('rgba(140,122,216,0.35)', 10, 30) });
    cut(rect(px - 12, py - 146, 24, 30, 4), BR.gold, { key: 'cap', sb: 3 });
    mic(K.hands.R[0], K.hands.R[1], 0.92, 'micK', -0.3);
    if (!after) [[440, 690], [770, 620], [470, 980], [790, 930]].forEach(([x, y], i) => sparkle(x, y, (16 + i * 3) * (0.6 + 0.4 * ((B + i) % 2)), '#fff3c4'));
    if (after && TT - cu.sai > 0.6) sweat(668, 760, 1.1, 'swK');
    // the buyer in front, phone in hand: unconvinced, then delighted
    const bm = !after ? 'focus' : TT - cu.sai < 0.25 ? 'wow' : 'happy';
    const Bh = buyer(220, 1770, 1.3, { mood: bm, armR: -0.95, armL: Math.PI / 2 + 0.25 });
    phone(Bh.hands.R[0] + 10, Bh.hands.R[1] - 40, 84, 150, '#f3ead6', 'bPh', { rot: 0.2, lines: true });
    // her doubt, until the stamp answers it
    if (!after) { const bob = Math.sin(TT * 3) * 6; [[300, 1000, 12], [330, 960, 18]].forEach(([x, y, r], i) => cut(ellipsePts(x, y + bob, r, r, 0, 14), '#ffffff', { key: 'thd' + i, sb: 4 })); cut(ellipsePts(400, 880 + bob, 62, 56, 0, 24), '#ffffff', { key: 'thB', sb: 6 }); txt('?', 400, 906 + bob, 76, { align: 'center', weight: 900, key: 'thQ' }); }
  } else {
    // the end: the buyer has the mic and the spotlight; her phone throws orange stars
    const Bh = buyer(280, 1200, 0.92, { mood: TT >= cu.follow ? 'happy' : 'smile', armL: Math.PI + 0.25, armR: Math.PI / 2 - 0.9 });
    mic(Bh.hands.R[0], Bh.hands.R[1], 0.9, 'micB', 0.2);
    phone(Bh.hands.L[0], Bh.hands.L[1] - 40, 84, 150, BR.orange, 'bPhE', { rot: -0.2, stars: 3 });
    const R = RNG('estars');
    for (let i = 0; i < 7; i++) { const u = mod(TT * 0.5 + R.f(), 1), sx = Bh.hands.L[0] - 20 + Math.sin(u * 6 + i) * 60, sy = Bh.hands.L[1] - 110 - u * 260; star(sx, sy, 16 + R.f() * 10, BR.orange, 'es' + i, { rot: u * 3 }); }
    // the KOL in the audience, clapping along
    const clap = Math.sin(TT * TAU * 2) > 0 ? 0.25 : 0;
    kol(800, 1590, 1.05, { key: 'kolA', mood: 'smile', armL: 0.9 - clap, armR: Math.PI - 0.9 + clap, shadesDrop: 0 });
    // more audience heads along the bottom
    [[100, 1700, PAL.skin3, PAL.teal], [640, 1720, PAL.skin1, PAL.green], [980, 1700, PAL.skin2, PAL.blue]].forEach(([x, y, sk, sh], i) => figure(x, y + 190, 0.8, { key: 'aud' + i, skin: sk, shirt: sh, hairStyle: ['short', 'bun', 'long'][i], hair: ['#2b211d', '#5a3a28', '#1f1a24'][i], mood: 'happy' }));
  }
  // the banner over the stage: the hook (frame 0, complete), and at the end the truth
  const COVER = !end && new URLSearchParams(location.search).has('cover');   // tools/cover.mjs: the hook, larger
  const lines = end ? ['Review thật,', 'bán hàng thật.'] : COVER ? ['Thuê KOL', 'nổi tiếng là', 'khách sẽ tin?'] : ['Thuê KOL nổi tiếng', 'là khách sẽ tin?'];
  const size = end ? 70 : Math.min(...lines.map((l) => fitSize(l, 800, COVER ? 128 : 84, 800)));
  ptag(lines.map((t) => ({ t, size, weight: 800 })), 470, end ? 372 : COVER ? 500 : 392, { key: 'banner' + end, rot: -0.02, padX: 36, padY: 26, gap: 2, tape: true, minW: 760 });
  // SAI: the stamp slams on "Sai." (scale from 2.4 to 1 over 3 frames), with ink dust
  if (after) {
    const u = clamp((TT - cu.sai) / 0.1), k = 1 + 1.4 * (1 - u) ** 2;
    ctx.save(); ctx.translate(600, 650); ctx.rotate(-0.13); ctx.scale(k, k);
    const sw = 400, sh = 180;
    cut(rrectPts(-sw / 2 + 10, -sh / 2 + 10, sw - 20, sh - 20, 12), 'rgba(251,246,234,0.86)', { key: 'stampBg', tear: 0.6, sb: 8, sy: 4, grain: 0.4 });
    ctx.strokeStyle = BR.red; ctx.lineWidth = 12; ctx.lineJoin = 'round'; trace(wobble(rrectPts(-sw / 2, -sh / 2, sw, sh, 16), true, 1.5, 'stampO', 6), true); ctx.stroke();
    ctx.lineWidth = 5; trace(wobble(rrectPts(-sw / 2 + 16, -sh / 2 + 16, sw - 32, sh - 32, 10), true, 1.2, 'stampI', 6), true); ctx.stroke();
    txt('SAI', 0, 56, 160, { align: 'center', weight: 900, font: DISPLAY, color: BR.red, key: 'saiT' });
    // worn ink: paper-coloured specks knocked out of the stamp
    const R = RNG('stampSpecks'); ctx.fillStyle = 'rgba(251,246,234,0.7)';
    for (let i = 0; i < 70; i++) { ctx.beginPath(); ctx.arc(R.r(-sw / 2, sw / 2), R.r(-sh / 2, sh / 2), R.r(1, 3.5), 0, TAU); ctx.fill(); }
    ctx.restore();
    if (TT - cu.sai < 0.5) { const R2 = RNG('dust'); for (let i = 0; i < 14; i++) { const a = R2.r(0, TAU), d = 190 + (TT - cu.sai) * 500 * R2.r(0.6, 1.2); dot(600 + Math.cos(a) * d, 650 + Math.sin(a) * d * 0.6, R2.r(3, 7), 'rgba(255,240,220,0.8)'); } }
  }
  if (end) {
    // the ask, the comment tag and the follow button (Adtek navy)
    overlay(() => {
      bubble(70, 488, 860, 196, 300, 760, '#ffffff', 'askB');
      txt('Bạn tin review của KOL', 500, 568, 60, { align: 'center', weight: 800, key: 'ask1', frac: ev(cu.ask - 0.1, 0.6) });
      txt('hay người mua thật?', 500, 650, 60, { align: 'center', weight: 800, key: 'ask2', frac: ev(cu.ask + 0.9, 0.6) });
      ptag([{ t: 'Comment cho Adtek', size: 54, weight: 800 }], 330, 1300, { key: 'cmt', rot: -0.03, s: popS(cu.comment), tape: true });
      const fs = popS(cu.follow);
      if (fs > 0.01) {
        ctx.save(); ctx.translate(330, 1414); ctx.rotate(0.015); ctx.scale(fs, fs);
        cut(rect(-265, -56, 530, 112, 30), BR.navy, { key: 'fbtn', tear: 1.0, sb: 14, sy: 8, pat: pat.stripes('rgba(255,255,255,0.05)', 6, 20, 0.5) });
        cut(ellipsePts(-205, 0, 32, 32, 0, 24), BR.orange, { key: 'fplus', sb: 4 });
        ink([[-222, 0], [-188, 0]], { w: 9, color: '#ffffff', amt: 0.2, key: 'fp1' }); ink([[-205, -17], [-205, 17]], { w: 9, color: '#ffffff', amt: 0.2, key: 'fp2' });
        txt('Follow Adtek', 50, 22, 62, { align: 'center', weight: 800, color: '#ffffff', key: 'ftxt' });
        ctx.restore();
      }
    });
  } else {
    // the question cards that tell what was asked come with the survey shot; here only the stage
  }
}
// ---- the survey: who Q&Me asked. A clipboard ticks itself off as the voice names them
function sSurvey() {
  const cu = TIMELINE.cues;
  wall(PAL.sky, pat.gingham('rgba(255,255,255,0.22)', 22), 'skyW');
  // a pinned photo of the KOL at the top right: it falls off its pin on "ngược lại"
  const fall = EZ.i2(ev(cu.nguoc, 0.6));
  ctx.save(); ctx.translate(820, 420 + fall * 900); ctx.rotate(0.08 + fall * 1.6);
  cut(rect(-100, -120, 200, 240, 4), '#fbf8f0', { key: 'pola' });
  cut(rect(-84, -104, 168, 170, 2), '#a8406f', { key: 'polaI', shadow: false, pat: pat.stripes('rgba(60,10,40,0.16)', 14, 40) });
  cut(ellipsePts(0, -10, 44, 50, 0, 24), PAL.skin2, { key: 'polaF', sb: 4 });
  cut([[-46, -20], [-40, -60], [0, -80], [44, -66], [46, -20], [30, -40], [-30, -40]], '#1f1a24', { key: 'polaH', sb: 3 });
  [-1, 1].forEach((d) => cut(rrectPts(d * 18 - 16, -16, 32, 22, 8), '#1d1a22', { key: 'polaG' + d, sb: 2, line: '#d04a8c', lw: 4 }));
  ctx.restore();
  if (fall < 0.05) dot(820, 316, 10, '#d8334a');
  clock(150, 330, 70, 9, 10, 'ckS');
  // the desk
  floor(1180, PAL.wood, pat.grainWood('rgba(120,60,20,0.18)'), 'desk');
  mug(560, 1220, 0.9, '#ffffff', 'mugS');
  cat(270, 1300, 0.9, PAL.charcoal, 'catS');
  plant(1000, 1180, 0.9, PAL.purple, 'plS');
  // the clipboard
  ctx.save(); ctx.translate(390, 760); ctx.rotate(-0.025);
  cut(rect(-330, -430, 660, 860, 18), '#b9824a', { key: 'clipB', pat: pat.grainWood('rgba(90,45,10,0.18)') });
  cut(rect(-306, -380, 612, 790, 4), PAL.paper, { key: 'clipP', pat: pat.lines('rgba(76,111,181,0.22)', 60, 40) });
  cut(rect(-90, -460, 180, 70, 14), '#b8b8c4', { key: 'clipM', pat: pat.stripes('rgba(255,255,255,0.3)', 6, 18) });
  txt('Khảo sát Q&Me', 0, -270, 60, { align: 'center', weight: 800, key: 'qTitle' });
  ink([[-210, -244], [210, -246]], { w: 5, color: 'rgba(0,36,95,0.5)', key: 'qUnd' });
  const rows = [['200 người', cu.ppl], ['20 đến 49 tuổi', cu.ppl + 0.35], ['Hà Nội và TP.HCM', cu.hn], ['09/2026', cu.thay]];
  rows.forEach(([t, at], i) => {
    const y = -150 + i * 128;
    cut(rect(-270, y - 46, 54, 54, 6), '#ffffff', { key: 'cb' + i, sb: 4, line: BR.navy, lw: 3 });
    if (TT >= at) ink([[-260, y - 20], [-246, y - 2], [-206, y - 52]], { w: 9, color: BR.navy, key: 'tick' + i, frac: ev(at, 0.2) });
    txt(t, -190, y, 50, { weight: 700, key: 'row' + i });
  });
  ctx.restore();
  // the buyer, pencil in hand, ticks the list; happy on "ngược lại"
  const Bh = buyer(850, 1440, 1.08, { mood: TT >= cu.nguoc ? 'happy' : 'focus', armL: Math.PI - 0.25 + Math.sin(TT * 7) * 0.05, armR: Math.PI / 2 - 0.25 });
  cut(capsulePts(Bh.hands.L[0] + 10, Bh.hands.L[1] + 10, Bh.hands.L[0] - 80, Bh.hands.L[1] - 6, 14), PAL.yellow, { key: 'pencil', sb: 4 });
  srcLine('Nguồn: Q&Me, 09/2026');
}
// ---- 54% vs 13%: two paper columns, true to scale; the buyer rides hers up, the KOL barely leaves the floor
function sVersus() {
  const cu = TIMELINE.cues, FL = 1420, PX = 11.5;
  wall('#e3b55a', pat.stripes('rgba(255,255,255,0.20)', 26, 60), 'musW');
  bunting(250, 'buntV', [PAL.teal, PAL.paper, PAL.blue, PAL.mint]);
  floor(FL, '#b9763f', pat.lines('rgba(90,45,10,0.25)', 40, 10), 'vFloor');
  const h54 = 54 * PX * springMove(cu.p54, 0, 1, SPRING.heavy), h13 = 13 * PX * springMove(cu.p13, 0, 1, SPRING.heavy);
  // the buyer's column (orange) and the KOL's (purple)
  if (h54 > 2) cut(rect(100, FL - h54, 340, h54 + 30, 6), BR.orange, { key: 'col54', crayon: BR.orangeD, crAl: 0.25, sy: 4 });
  if (h13 > 2) cut(rect(580, FL - h13, 340, h13 + 30, 6), '#6a55b8', { key: 'col13', sy: 4, pat: pat.dots('rgba(255,224,120,0.35)', 3, 22) });
  // the characters stand on their columns
  const up = TT >= cu.p54;
  const Bh = buyer(270, FL - h54, 0.82, { mood: up ? 'happy' : 'smile', armL: up ? -Math.PI / 2 - 0.6 : Math.PI / 2 + 0.2, armR: up ? -Math.PI / 2 + 0.6 : Math.PI / 2 - 0.2 });
  const kMood = TT < cu.kolWord ? 'smile' : TT < cu.p13 ? 'wow' : 'sad';
  kol(750, FL - h13, 0.82, { mood: kMood, armL: Math.PI / 2 + 0.3, armR: TT < cu.p13 ? -Math.PI / 2 + 0.7 : Math.PI / 2 - 0.15 });
  if (TT >= cu.p13 + 0.5) sweat(812, FL - h13 - 470, 1, 'swV');
  confetti('v54', cu.p54 + 0.2, 60, 260, FL - 40, [PAL.paper, PAL.yellow, BR.orangeL, PAL.mint]);
  // the crowd at the base: real buyers holding orange hearts up to her
  for (let i = 0; i < 7; i++) { const x = 40 + i * 160, y = 1560 + (i % 2) * 30; cut(ellipsePts(x, y, 62, 70, 0, 24), [PAL.skin1, PAL.skin2, PAL.skin3][i % 3], { key: 'cr' + i }); cut([[x - 64, y - 6], [x - 60, y - 50], [x - 20, y - 76], [x + 30, y - 76], [x + 64, y - 46], [x + 64, y - 6], [x + 40, y - 40], [x - 40, y - 40]], ['#2b211d', '#5a3a28', '#1f1a24'][i % 3], { key: 'crh' + i, sb: 3 }); if (up && i < 5) heart(x + 30, y - 120 - Math.sin(TT * 5 + i) * 10, 26, BR.orange, 'crH' + i); }
  // numbers and names: on the columns, written in once they stand
  if (h54 > 400) { txt('54%', 270, FL - h54 + 150, 124, { align: 'center', weight: 900, font: DISPLAY, key: 'n54' }); txt('Người mua', 270, FL - h54 + 240, 44, { align: 'center', weight: 700, key: 'l54a' }); txt('bình thường', 270, FL - h54 + 296, 44, { align: 'center', weight: 700, key: 'l54b' }); }
  if (h13 > 120) txt('13%', 750, FL - h13 + 110, 96, { align: 'center', weight: 900, font: DISPLAY, color: '#fbf6ea', key: 'n13' });
  overlay(() => {
    ptag([{ t: 'Khách tin', size: 62, weight: 800 }, { t: 'ai hơn?', size: 62, weight: 800 }], 735, 430, { key: 'vsT', rot: 0.02, tape: true });
    ptag([{ t: 'KOL,', size: 42, weight: 800 }, { t: 'người nổi tiếng', size: 42, weight: 700 }], 735, 700, { key: 'vsK', rot: -0.03, s: popS(cu.kolWord - 0.2), fill: '#efe6ff' });
  });
  srcLine('Nguồn: Q&Me, 200 người 20 đến 49 tuổi, 09/2026');
}
// ---- 78%: ten shoppers in a shop; eight phones light up with orange stars (about 8 in 10)
const SHOPPERS = [
  // x, feet y, s, skin, hairStyle, hair, shirt, lit
  [150, 1060, 0.56, PAL.skin2, 'short', '#2b211d', PAL.blue, true], [320, 1060, 0.56, PAL.skin1, 'long', '#5a3a28', PAL.pink, true], [490, 1060, 0.56, PAL.skin3, 'bun', '#1f1a24', PAL.green, false],
  [660, 1060, 0.56, PAL.skin1, 'cap', '#2b211d', PAL.purple, true], [830, 1060, 0.56, PAL.skin2, 'bob', '#3b2a22', PAL.mint, true],
  [150, 1420, 0.62, PAL.skin1, 'bun', '#3b2a22', PAL.yellow, true], [320, 1420, 0.62, PAL.skin3, 'short', '#1f1a24', '#4a4550', true], [490, 1420, 0.62, 'buyer', '', '', '', true],
  [660, 1420, 0.62, PAL.skin2, 'long', '#2b211d', PAL.teal, false], [830, 1420, 0.62, PAL.skin1, 'short', '#5a3a28', PAL.blue, true],
];
function sShoppers() {
  const cu = TIMELINE.cues;
  wall('#6fb7ae', pat.stripes('rgba(255,255,255,0.10)', 40, 120), 'shopW');
  // shelves of products behind
  const R = RNG('shelf'), cols = [PAL.pink, PAL.yellow, PAL.paper, PAL.purple, PAL.blue, PAL.mint, '#e7dcc0'];
  [700, 980].forEach((y, r) => { cut(rect(-20, y, W + 40, 22, 2), PAL.wood, { key: 'sh' + r }); let x = 10; for (let i = 0; i < 16 && x < W; i++) { const w = R.r(44, 80), h = R.r(80, 140); cut(rect(x, y - h, w, h, 4), cols[R.i(0, 6)], { key: 'pr' + r + i, sb: 4, pat: pat.stripes('rgba(255,255,255,0.3)', 8, 1000) }); x += w + R.r(6, 20); } });
  // hanging lamps
  [220, 760].forEach((x, i) => { ink([[x, 0], [x, 150]], { w: 3, color: '#2b2733', key: 'lc' + i }); cut([[x - 60, 200], [x - 30, 140], [x + 30, 140], [x + 60, 200]], PAL.yellow, { key: 'lamp' + i, sb: 6 }); });
  floor(1300, '#e9e2d2', pat.gingham('rgba(63,159,154,0.18)', 30), 'tiles');
  // a shopping basket
  cut([[930, 1430], [1060, 1430], [1040, 1530], [950, 1530]], '#d8334a', { key: 'basket', pat: pat.gingham('rgba(255,255,255,0.25)', 8) });
  const lit = (i) => TT >= cu.p78 + i * 0.07;
  SHOPPERS.forEach(([x, y, s, skin, hs, hair, shirt, on], i) => {
    const L = on && lit(i), buzz = TT >= cu.heavy && TT < cu.p78 ? Math.sin(TT * 40 + i) * 2 : 0;
    const mood = L ? (i % 2 ? 'wow' : 'happy') : on ? 'focus' : 'smile';
    const P = skin === 'buyer' ? buyer(x, y, s, { mood, armL: Math.PI / 2 - 0.9, armR: Math.PI / 2 + 0.9 })
      : figure(x, y, s, { key: 'sp' + i, skin, hairStyle: hs, hair, shirt, mood, armL: Math.PI / 2 - 0.9, armR: Math.PI / 2 + 0.9 });
    const hx = (P.hands.L[0] + P.hands.R[0]) / 2, hy = (P.hands.L[1] + P.hands.R[1]) / 2 - 20 * s;
    phone(hx + buzz, hy, 70 * s, 120 * s, L ? BR.orange : '#c9c4d4', 'php' + i, { stars: L ? 1 : 0 });
    if (L) star(P.head[0] + 70 * s, P.top - 30 * s - Math.sin(TT * 4 + i) * 6, 28 * s + 6, BR.orange, 'sb' + i);
  });
  overlay(() => {
    ptag([{ t: '78%', size: 150, weight: 900, font: DISPLAY, color: BR.orangeD }, { t: 'chọn mua theo review', size: 52, weight: 800 }, { t: 'khoảng 8/10 người', size: 38, weight: 600 }], 470, 470, { key: 'p78', s: popS(cu.p78), tape: true, padY: 14, gap: 0 });
  });
  srcLine('Nguồn: Q&Me, 200 người 20 đến 49 tuổi, 09/2026');
}
// ---- age 20: an extreme close-up; the phone throws orange stars; 87%
function sAge20() {
  const cu = TIMELINE.cues;
  wall('#4c6fb5', pat.dots('rgba(255,255,255,0.12)', 5, 56), 'roomW');
  // fairy lights, a poster, sticky notes
  ink([[-20, 250], [300, 300], [700, 290], [1100, 240]], { w: 3, color: '#2b2733', amt: 0.4, key: 'fl' });
  for (let i = 0; i < 11; i++) { const x = i * 105, y = 262 + Math.sin(i / 10 * Math.PI) * 42; dot(x, y + 14, 11, (B + i) % 3 ? '#fff3b0' : '#ffe066'); }
  cut(rot(rect(720, 760, 220, 280, 4), 830, 900, 0.06), PAL.pink, { key: 'poster', pat: pat.stripes('rgba(255,255,255,0.3)', 12, 40, 0.6) });
  [[110, 820, PAL.yellow], [190, 900, PAL.mint]].forEach(([x, y, c], i) => cut(rot(rect(x - 55, y - 55, 110, 110, 2), x, y, (i - 0.5) * 0.2), c, { key: 'sticky' + i, sb: 5 }));
  // the young buyer, close: headphones round the neck, a cap, phone up
  const s = 1.9, X = 420, Y = 1290;
  person(X, Y, s, { key: 'y20', skin: PAL.skin1, hair: '#2b211d', shirt: BR.orange, shirtPat: pat.stripes('rgba(255,255,255,0.12)', 10, 40), mood: TT >= cu.p87 ? 'happy' : 'wow' });
  cut([[X - 82 * s, Y - 150 * s], [X - 76 * s, Y - 196 * s], [X - 30 * s, Y - 222 * s], [X + 40 * s, Y - 222 * s], [X + 80 * s, Y - 190 * s], [X + 84 * s, Y - 150 * s]], PAL.green, { key: 'y20cap', sb: 5, pat: pat.stripes('rgba(255,255,255,0.18)', 8, 30, 0.3) });
  cut(capsulePts(X - 60 * s, Y - 160 * s, X - 150 * s, Y - 150 * s, 22 * s), PAL.green, { key: 'y20bill', sb: 4 });
  ink(arcPts(X, Y - 10 * s, 70 * s, 0.1, Math.PI - 0.1, 18), { w: 14, color: '#2b2733', key: 'hp' });
  cut(ellipsePts(X - 68 * s, Y + 4 * s, 18 * s, 24 * s, 0, 16), '#2b2733', { key: 'hpL' }); cut(ellipsePts(X + 68 * s, Y + 4 * s, 18 * s, 24 * s, 0, 16), '#2b2733', { key: 'hpR' });
  hand(880, 1250, 1.25, -Math.PI / 2 - 0.35, PAL.skin1, BR.orange, { key: 'y20h' });
  phone(800, 1060, 150, 270, BR.orange, 'y20ph', { rot: -0.3, stars: 3 });
  if (TT >= cu.p87) { const R = RNG('y20s'); for (let i = 0; i < 8; i++) { const a = -Math.PI / 2 + R.n(1.1), d = 160 + (TT - cu.p87) * 520 * R.r(0.7, 1.2); if (d > 650) continue; star(790 + Math.cos(a) * d, 1020 + Math.sin(a) * d, 22 + R.f() * 12, BR.orange, 'y20s' + i, { rot: TT * 3 + i }); } }
  overlay(() => {
    ptag([{ t: 'Ở tuổi 20', size: 64, weight: 800 }], 330, 330, { key: 'age', s: popS(E0 + 0.05), tape: true, rot: -0.03 });
    ptag([{ t: '87%', size: 170, weight: 900, font: DISPLAY, color: BR.orangeD }], 330, 540, { key: 'p87', s: popS(cu.p87), rot: 0.02, padY: 6 });
  });
  srcLine('Nguồn: Q&Me, 09/2026');
}
