#!/usr/bin/env node
// Builds voice/voice.wav + voice.json in the exact format of the animate skill's tools/voice.mjs, from the
// already-approved ElevenLabs takes and their per-word times in public/voice/thue-kol-khach-co-tin/manifest.json.
// (faster-whisper small.en cannot hear Vietnamese, and no TTS service is called here.)
// Each take keeps its own start (no leading trim, so the manifest's word times stay valid); trailing silence is trimmed.
// The pause after a line is chosen so the scene cut (line end + ~0.15s, rounded up to the 8th grid of 112.5 BPM at
// 30fps = 8 frames) lands 0.15s before the next line starts.
//   usage: node tools/make-voice.mjs   (run from anywhere)
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.resolve(ROOT, '../../public/voice/thue-kol-khach-co-tin');
const SR = 48000, FPS = 30, E8 = 8 / FPS;
const LEAD = 0.3, GAP = 0.15, TAIL = 1.6;
const M = JSON.parse(fs.readFileSync(path.join(SRC, 'manifest.json'), 'utf8'));
const IDS = ['myth', 'versus', 'weight', 'trust', 'todo', 'follow'];

function decode(file) {
  const r = spawnSync('ffmpeg', ['-v', 'error', '-i', file, '-ac', '1', '-ar', String(SR), '-f', 's16le', '-'], { maxBuffer: 1 << 30 });
  if (r.status !== 0) { console.error('could not decode', file); process.exit(1); }
  // trailing silence: cut after the last 10ms block louder than -45 dBFS (+60ms of release)
  const n = r.stdout.length / 2, blk = SR / 100, thr = 10 ** (-45 / 20);
  let last = n;
  for (let b = Math.floor(n / blk) - 1; b >= 0; b--) {
    let pk = 0; for (let i = b * blk; i < (b + 1) * blk; i++) pk = Math.max(pk, Math.abs(r.stdout.readInt16LE(i * 2) / 32768));
    if (pk > thr) { last = Math.min(n, (b + 1) * blk + Math.round(0.06 * SR)); break; }
  }
  return r.stdout.subarray(0, last * 2);
}

const parts = [], lines = [];
let t = LEAD;
M.scenes.forEach((S, i) => {
  const file = path.join(SRC, `${i}.mp3`), pcm = decode(file), dur = pcm.length / 2 / SR;
  const words = S.words.map((w) => ({ w: w.text, t0: +(t + Math.min(w.start, dur)).toFixed(3), t1: +(t + Math.min(w.end, dur)).toFixed(3) }));
  lines.push({ id: IDS[i], text: S.text, t0: +t.toFixed(3), t1: +(t + dur).toFixed(3), take: path.relative(ROOT, file).replace(/\\/g, '/'), words });
  parts.push([Math.round(t * SR), pcm]);
  const cut = Math.ceil((t + dur + GAP) / E8 - 1e-9) * E8;   // the next scene's cut, on the grid
  t = cut + GAP;
});
const last = lines[lines.length - 1];
const total = Math.ceil((last.t1 + TAIL) * FPS) / FPS;
const out = Buffer.alloc(Math.ceil(total * SR) * 2);
for (const [s0, pcm] of parts) pcm.copy(out, s0 * 2);
const hdr = Buffer.alloc(44);
hdr.write('RIFF', 0); hdr.writeUInt32LE(36 + out.length, 4); hdr.write('WAVE', 8); hdr.write('fmt ', 12);
hdr.writeUInt32LE(16, 16); hdr.writeUInt16LE(1, 20); hdr.writeUInt16LE(1, 22); hdr.writeUInt32LE(SR, 24); hdr.writeUInt32LE(SR * 2, 28);
hdr.writeUInt16LE(2, 32); hdr.writeUInt16LE(16, 34); hdr.write('data', 36); hdr.writeUInt32LE(out.length, 40);
fs.writeFileSync(path.join(ROOT, 'voice', 'voice.wav'), Buffer.concat([hdr, out]));
const voice = { duration: +total.toFixed(3), lead: LEAD, tail: TAIL, lines };
fs.writeFileSync(path.join(ROOT, 'voice.json'), JSON.stringify(voice, null, 1));
console.log(`voice: ${lines.length} lines, ${lines.reduce((n, L) => n + L.words.length, 0)} words, ${total.toFixed(3)}s = ${Math.round(total * FPS)} frames; word times from manifest.json`);
for (const L of lines) console.log(`  ${L.id.padEnd(7)} ${L.t0.toFixed(3)}-${L.t1.toFixed(3)}s  ${(L.words.length / (L.t1 - L.t0)).toFixed(2)} w/s  "${L.text.slice(0, 60)}"`);
