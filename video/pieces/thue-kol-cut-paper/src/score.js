  // =====================================================================
  //  SCORE — quiet under the voice (piece.json voice.music = -15 dB); the owner adds TikTok music at ~15%.
  //  D, 112.5 BPM (an 8th = 8 frames at 30fps). The KOL's show is glossy; it stops dead before "Sai."
  //  The stamp is the loudest hit (a D minor stab + sub), then everything after is warmer and quieter.
  //  The buyer's motif: a rising fifth (D4 -> A4). Each world voices itself: ticks, a bin thud, cards, a shutter.
  // =====================================================================
  const T = TIMELINE, cu = T.cues, R = RNG('score');
  const st = (k) => T.shots.find((s) => s.key === k).t0;
  const each = (t0, t1, step, fn) => { for (let k = 0; t0 + k * step < t1 - 1e-6; k++) fn(t0 + k * step, k); };
  const motif = (t, vel, notes = [['D4', 0], ['A4', E8]]) => notes.forEach(([n, dt], i) => pluck(t + dt, nz(n), vel, 0.1 - i * 0.15, 0.6, 2600, 0.3));
  const FIG = ['D4', 'A4', 'Fs4', 'A4', 'B4', 'A4', 'Fs4', 'E4'];

  to = 'm';
  // 1 the KOL's show: a glossy pad and glitter on 8ths, all dry, cut hard at the hush
  pad(0, cu.hush, ['D3', 'A3', 'Fs4', 'A4'], 0.026, { cut: 1500, att: 0.04, rel: 0.1, send: 0 });
  each(0, cu.hush - 0.05, E8, (t, k) => pluck(t, nz(['A4', 'D5', 'Fs5', 'A5'][k % 4]), 0.03, Math.sin(k) * 0.4, 0.18, 5200, 0));
  each(0, cu.hush - 0.05, BEAT, (t) => bass(t, nz('D2'), 0.1));
  // 2 the hush (score silent), 3 the stamp: a D minor stab + sub, then a flat low chord
  ['D3', 'A3', 'D4', 'F4', 'A4'].forEach((n, i) => pluck(cu.sai + i * 0.006, nz(n), 0.4, (i - 2) * 0.18, 0.55, 3200, 0.25));
  pad(cu.sai, cu.sai + 0.4, ['D3', 'A3', 'D4', 'F4'], 0.5, { cut: 3200, att: 0.006, rel: 0.3, send: 0.2 });
  pad(cu.sai + 0.35, st('survey') + 0.1, ['D3', 'A3', 'F4'], 0.03, { cut: 800, att: 0.2, rel: 0.25, send: 0.2 });
  // 4 the survey: light plucks on quarters
  pad(st('survey'), st('versus') + 0.05, ['D3', 'A3', 'E4'], 0.022, { cut: 900, att: 0.3, rel: 0.2, send: 0.3 });
  each(st('survey'), st('versus'), BEAT, (t, k) => pluck(t, nz(FIG[(k * 2) % 8]), 0.04, Math.sin(k) * 0.3, 0.35, 2400, 0.2));
  // 5 the proof: the buyer's motif as her column rises; the KOL's two falling notes; then 8 plucks for 8 phones
  pad(st('versus'), st('bars') + 0.05, ['D3', 'A3', 'D4', 'Fs4'], 0.024, { cut: 1000, att: 0.3, rel: 0.2, send: 0.3 });
  each(st('versus'), st('bars'), BEAT, (t, k) => bass(t, nz(Math.floor(k / 4) % 2 ? 'A2' : 'D2'), 0.1));
  motif(cu.p54 + 0.35, 0.16);
  [['A3', 0], ['F3', 0.27]].forEach(([n, dt]) => pluck(cu.p13 + 0.3 + dt, nz(n), 0.1, 0.3, 0.7, 1400, 0.3));
  ['D5', 'E5', 'Fs5', 'A5', 'B5', 'D6', 'E6', 'Fs6'].forEach((n, i) => pluck(cu.p78 + i * 0.07, nz(n), 0.07, -0.5 + i * 0.13, 0.4, 4200, 0.3));
  each(st('shoppers'), st('bars'), E8, (t, k) => { if (k % 2 === 0 || k % 8 === 5) pluck(t, nz(FIG[k % 8]), 0.035, Math.sin(k) * 0.3, 0.3, 2800, 0.2); });
  chime(cu.p87, [nz('A5'), nz('D6'), nz('Fs6')], 0.08, 0.1);
  // 6 trust: an 8th groove for the bars, a pluck on each bar
  pad(st('bars'), st('drop') + 0.05, ['D3', 'A3', 'E4', 'A4'], 0.024, { cut: 1100, att: 0.3, rel: 0.1, send: 0.25 });
  each(st('bars'), st('drop'), E8, (t, k) => { pluck(t, nz(FIG[k % 8]), 0.04 * (k % 2 ? 0.75 : 1), Math.sin(k * 0.9) * 0.35, 0.28, 3200, 0.15); if (k % 2 === 0) bass(t, nz(Math.floor(k / 8) % 2 ? 'A2' : 'D2'), 0.12); });
  [[cu.p69, 'A4'], [cu.p60, 'Fs4'], [cu.p51, 'D4']].forEach(([t, n]) => pluck(t - 0.12, nz(n), 0.12, 0, 0.5, 3600, 0.3));
  // the busiest stretch: the bin and the stack, 16ths
  pad(st('drop'), st('todo') + 0.05, ['D3', 'A3', 'E4', 'B4'], 0.026, { cut: 1300, att: 0.1, rel: 0.1, send: 0.2 });
  each(st('drop'), st('todo'), E16, (t, k) => { const f = FIG[Math.floor(k / 2) % 8]; pluck(t, nz(f) * (k % 2 ? 2 : 1), 0.03 * (k % 4 === 0 ? 1.3 : 0.85), Math.sin(k * 0.9) * 0.4, 0.2, 4200, 0.1); if (k % 4 === 0) bass(t, nz(Math.floor(k / 16) % 2 ? 'A2' : 'D2'), 0.12); });
  chime(cu.n50, [nz('D5'), nz('A5'), nz('D6')], 0.09, 0);
  // 7 what to do now: warm, quarter notes, a chime per step
  pad(st('todo'), st('finale') + 0.05, ['D3', 'A3', 'D4', 'Fs4'], 0.024, { cut: 1000, att: 0.3, rel: 0.2, send: 0.35 });
  each(st('todo'), st('finale'), BEAT, (t, k) => { pluck(t, nz(FIG[(k * 3) % 8]), 0.035, Math.sin(k) * 0.3, 0.35, 2400, 0.25); if (k % 2 === 0) bass(t, nz(k % 8 < 4 ? 'D2' : 'A2'), 0.1); });
  [cu.i1, cu.i2, cu.i3, cu.i4].forEach((t, i) => chime(t, [nz(['D5', 'E5', 'Fs5', 'A5'][i]), nz(['A5', 'B5', 'D6', 'E6'][i])], 0.06, 0.2));
  // 8 the ask: back on the stage, warm; the buyer's motif, a chord on "Follow" held to the end
  pad(st('finale'), DURATION, ['D3', 'A3', 'Fs4'], 0.026, { cut: 1100, att: 0.4, rel: 0.8, send: 0.4 });
  motif(cu.ask + 0.1, 0.13);
  motif(cu.follow, 0.15, [['D4', 0], ['A4', E8], ['D5', BEAT]]);
  pad(cu.follow + BEAT, DURATION, ['D3', 'A3', 'D4', 'Fs4', 'A4'], 0.03, { cut: 1300, att: 0.3, rel: 1.0, send: 0.45 });

  to = 's';
  // the stamp's thunk
  sub(cu.sai, 0.6); noiseHit(cu.sai, 0.14, 'lowpass', 900, 0.7, 0.45, 0, 0.1);
  // paper swishes into every cut (never into the hush)
  T.cuts.forEach((c, i) => sweep(c - 0.22, c + 0.01, 0.012, 500, 2600, i % 2 ? 0.2 : -0.2));
  // pencil ticks on the clipboard, the photo falling
  [cu.ppl, cu.ppl + 0.35, cu.hn, cu.thay].forEach((t) => { for (let j = 0; j < 3; j++) noiseHit(t + j * 0.05, 0.06, 'bandpass', 3000 + R.n(400), 1.4, 0.05, 0.2); });
  blip(cu.nguoc + 0.2, 900, 300, 0.4, 0.03, 0.3);
  // the columns rise
  sweep(cu.p54 - 0.05, cu.p54 + 0.45, 0.02, 300, 2400, -0.2); sweep(cu.p13 - 0.05, cu.p13 + 0.2, 0.012, 300, 900, 0.2);
  // phones buzz, then light
  for (let j = 0; j < 6; j++) blip(cu.heavy + j * 0.08, 180, 170, 0.05, 0.02, 0);
  // the bars slap down
  [cu.p69, cu.p60, cu.p51].forEach((t) => noiseHit(t - 0.1, 0.06, 'lowpass', 1800, 0.8, 0.12, 0));
  // the flick and the bin
  sweep(cu.loai - 0.02, cu.loai + 0.38, 0.016, 2000, 600, 0.3);
  sub(cu.loai + 0.4, 0.22); noiseHit(cu.loai + 0.4, 0.12, 'bandpass', 500, 1.2, 0.18, 0.3);
  // cards landing on the stack (every 2 frames until 50)
  each(st('fifty') + 0.05, cu.n50, 2 / FPS, (t, k) => noiseHit(t, 0.03, 'highpass', 5000 + R.n(800), 0.7, 0.025, 0.25));
  // the to-do: a sticker slap, a shutter, a buzzer, a pop
  noiseHit(cu.i1 + 0.3, 0.05, 'lowpass', 2200, 0.8, 0.12, -0.3);
  noiseHit(cu.i2, 0.025, 'highpass', 4000, 0.8, 0.1, 0); noiseHit(cu.i2 + 0.07, 0.04, 'highpass', 3000, 0.8, 0.08, 0);
  blip(cu.i3 + 0.3, 140, 120, 0.25, 0.06, 0.2);
  blip(cu.che, 600, 1400, 0.08, 0.05, 0.3);
  // the comment tag and the follow button pop
  blip(cu.comment, 500, 1200, 0.08, 0.05, -0.2); blip(cu.follow, 400, 1300, 0.1, 0.06, 0);
