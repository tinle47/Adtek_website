// Tạo nhạc nền nhẹ bằng code (không lấy nhạc của ai nên không lo bản quyền TikTok).
// Cách dùng: node tools/music.mjs            -> public/music/nhe-nhang.mp3 (cần ffmpeg)
// Nhạc: Fmaj7 - Dm9 - Bbmaj7 - Csus, 84 BPM, piano điện + pad + arpeggio + bass, hi-hat rất nhỏ.
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const OUT = path.join(ROOT, "public", "music", "nhe-nhang.mp3");
const SR = 44100;
const BPM = 84;
const BEAT = 60 / BPM;
const BAR = BEAT * 4;
const BARS = 18; // khoảng 51 giây, dài hơn mọi video 30 đến 45 giây
const LEN = Math.ceil((BARS * BAR + 4) * SR);

const L = new Float32Array(LEN);
const R = new Float32Array(LEN);
const hz = (midi) => 440 * 2 ** ((midi - 69) / 12);

// Mỗi hợp âm giữ 2 ô nhịp. root: nốt bass, notes: các nốt bè.
const CHORDS = [
  { root: 41, notes: [57, 60, 64, 65] }, // Fmaj7
  { root: 38, notes: [57, 60, 62, 64] }, // Dm9
  { root: 46, notes: [58, 62, 65, 69] }, // Bbmaj7
  { root: 48, notes: [55, 60, 65, 67] }, // Csus
];
const chordAt = (bar) => CHORDS[Math.floor(bar / 2) % CHORDS.length];

// Cộng một nốt vào bản nhạc. env(t) trả âm lượng theo thời gian, wave(phase) trả dạng sóng.
function addNote({ start, dur, freq, gain, pan = 0, env, wave }) {
  const i0 = Math.floor(start * SR);
  const n = Math.floor(dur * SR);
  const gl = gain * Math.cos(((pan + 1) * Math.PI) / 4);
  const gr = gain * Math.sin(((pan + 1) * Math.PI) / 4);
  for (let k = 0; k < n && i0 + k < LEN; k++) {
    const t = k / SR;
    const v = wave(2 * Math.PI * freq * t, t) * env(t, dur);
    L[i0 + k] += v * gl;
    R[i0 + k] += v * gr;
  }
}

// Piano điện: âm gốc + bồi âm tắt nhanh, rung nhẹ.
const epiano = (p, t) =>
  Math.sin(p) + 0.25 * Math.sin(2 * p) * Math.exp(-t * 3) + 0.08 * Math.sin(3 * p) * Math.exp(-t * 6);
const epEnv = (t, d) => Math.min(1, t / 0.008) * Math.exp(-t / 1.6) * Math.min(1, (d - t) / 0.3) * (1 + 0.04 * Math.sin(2 * Math.PI * 4.5 * t));
// Pad: ba sóng lệch nhau một chút, vào ra chậm.
const pad = (p) => (Math.sin(p) + Math.sin(p * 1.003) + Math.sin(p * 0.997)) / 3 + 0.12 * Math.sin(2 * p);
const padEnv = (t, d) => Math.min(1, t / 1.2) * Math.min(1, Math.max(0, (d - t) / 1.2));
// Arpeggio: tiếng gảy ngắn.
const pluck = (p, t) => Math.sin(p) + 0.3 * Math.sin(2 * p) * Math.exp(-t * 10);
const pluckEnv = (t) => Math.min(1, t / 0.004) * Math.exp(-t / 0.22);
const bassEnv = (t, d) => Math.min(1, t / 0.02) * Math.exp(-t / 1.2) * Math.min(1, (d - t) / 0.1);

let seed = 7;
const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) * 2 - 1;

for (let bar = 0; bar < BARS; bar++) {
  const c = chordAt(bar);
  const t0 = bar * BAR;
  const enter = (from) => Math.min(1, Math.max(0, (bar - from + 1) / 2)); // các lớp vào dần

  // Piano điện: nhịp 1 và nhịp "và" của phách 3, rải nhẹ từng nốt.
  for (const [hit, g] of [[0, 1], [2.5, 0.6]]) {
    c.notes.forEach((m, j) =>
      addNote({ start: t0 + hit * BEAT + j * 0.012, dur: hit ? 1.5 * BEAT : 2.5 * BEAT, freq: hz(m), gain: 0.07 * g, pan: (j - 1.5) * 0.15, env: epEnv, wave: epiano }),
    );
  }
  // Pad mỗi 2 ô nhịp, cao hơn một quãng tám.
  if (bar % 2 === 0) {
    c.notes.forEach((m, j) =>
      addNote({ start: t0, dur: 2 * BAR + 1.2, freq: hz(m + 12), gain: 0.022, pan: j % 2 ? 0.5 : -0.5, env: padEnv, wave: pad }),
    );
  }
  // Bass nhịp 1 và 3.
  if (bar >= 2) {
    for (const b of [0, 2]) addNote({ start: t0 + b * BEAT, dur: 1.8 * BEAT, freq: hz(c.root), gain: 0.16 * enter(2), env: bassEnv, wave: Math.sin });
  }
  // Arpeggio móc đơn từ ô nhịp thứ 5.
  if (bar >= 4) {
    const seq = [0, 2, 1, 3, 2, 1, 3, 2];
    seq.forEach((j, s) =>
      addNote({ start: t0 + s * (BEAT / 2), dur: 0.9, freq: hz(c.notes[j] + 12), gain: 0.03 * enter(4), pan: s % 2 ? 0.35 : -0.35, env: pluckEnv, wave: pluck }),
    );
  }
  // Hi-hat rất nhỏ ở phách lẻ từ ô nhịp thứ 9.
  if (bar >= 8) {
    for (let s = 1; s < 8; s += 2) {
      const i0 = Math.floor((t0 + s * (BEAT / 2)) * SR);
      let prev = 0;
      for (let k = 0; k < 0.06 * SR && i0 + k < LEN; k++) {
        const x = rand();
        const hp = x - prev; // lọc bỏ âm trầm cho tiếng "tsk" mỏng
        prev = x;
        const v = hp * Math.exp(-k / SR / 0.018) * 0.035 * enter(8);
        L[i0 + k] += v * 0.8;
        R[i0 + k] += v;
      }
    }
  }
}

// Vang (reverb Schroeder) và tiếng vọng nhẹ cho không gian rộng.
function reverb(x, combs, aps) {
  const y = new Float32Array(x.length);
  for (const d of combs) {
    const buf = new Float32Array(d);
    let idx = 0;
    let lp = 0;
    for (let i = 0; i < x.length; i++) {
      const out = buf[idx];
      lp = out * 0.6 + lp * 0.4;
      buf[idx] = x[i] + lp * 0.8;
      idx = (idx + 1) % d;
      y[i] += out / combs.length;
    }
  }
  for (const d of aps) {
    const buf = new Float32Array(d);
    let idx = 0;
    for (let i = 0; i < y.length; i++) {
      const b = buf[idx];
      const v = y[i];
      buf[idx] = v + b * 0.5;
      y[i] = b - v * 0.5;
      idx = (idx + 1) % d;
    }
  }
  return y;
}
const wetL = reverb(L, [1557, 1617, 1491, 1422], [225, 556]);
const wetR = reverb(R, [1580, 1640, 1514, 1445], [248, 579]);
const echo = Math.floor(BEAT * 0.75 * SR); // vọng móc chấm

let peak = 0;
const mix = [new Float32Array(LEN), new Float32Array(LEN)];
const lpState = [0, 0];
for (let i = 0; i < LEN; i++) {
  const t = i / SR;
  const fade = Math.min(1, t / 2) * Math.min(1, Math.max(0, (LEN / SR - t) / 4));
  const src = [
    [L, wetL],
    [R, wetR],
  ];
  src.forEach(([dry, wet], ch) => {
    const other = ch ? L : R;
    let v = dry[i] * 0.75 + wet[i] * 0.45 + (i >= echo ? other[i - echo] * 0.18 : 0);
    lpState[ch] += (v - lpState[ch]) * 0.55; // cắt bớt âm chói
    v = Math.tanh(lpState[ch] * 1.2) * fade;
    mix[ch][i] = v;
    peak = Math.max(peak, Math.abs(v));
  });
}

// Ghi WAV 16-bit rồi nén mp3 bằng ffmpeg.
const norm = 0.7 / peak;
const wav = Buffer.alloc(44 + LEN * 4);
wav.write("RIFF", 0);
wav.writeUInt32LE(36 + LEN * 4, 4);
wav.write("WAVEfmt ", 8);
wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20);
wav.writeUInt16LE(2, 22);
wav.writeUInt32LE(SR, 24);
wav.writeUInt32LE(SR * 4, 28);
wav.writeUInt16LE(4, 32);
wav.writeUInt16LE(16, 34);
wav.write("data", 36);
wav.writeUInt32LE(LEN * 4, 40);
for (let i = 0; i < LEN; i++) {
  wav.writeInt16LE(Math.round(mix[0][i] * norm * 32767), 44 + i * 4);
  wav.writeInt16LE(Math.round(mix[1][i] * norm * 32767), 46 + i * 4);
}
mkdirSync(path.dirname(OUT), { recursive: true });
const tmp = OUT.replace(/\.mp3$/, ".wav");
writeFileSync(tmp, wav);
execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", tmp, "-b:a", "160k", OUT]);
rmSync(tmp);
console.log(`Đã tạo ${path.relative(ROOT, OUT)} (${(LEN / SR).toFixed(1)}s)`);
