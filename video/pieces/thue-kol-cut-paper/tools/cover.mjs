#!/usr/bin/env node
// TikTok cover: the hook frame (before the stamp, so the answer "SAI" is never shown) with the hook set larger.
//   usage: node tools/cover.mjs <out.png>      (index.html must be built; ?cover=1 enlarges the banner)
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = process.argv[2] || path.join(ROOT, 'check', 'cover.png');
const b = await chromium.launch(), p = await b.newPage();
p.on('pageerror', (e) => { console.error('PAGE ERROR:', e.message); process.exitCode = 1; });
await p.goto(pathToFileURL(path.join(ROOT, 'index.html')).href + '?export=1&cover=1');
await p.waitForFunction(() => window.TIMELINE && window.renderFrame);
await p.evaluate(() => document.fonts.ready);
const url = await p.evaluate(() => { const c = document.createElement('canvas'); c.width = 1080; c.height = 1920; window.renderFrame(48 / 30, c); return c.toDataURL('image/png'); });
fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64'));
console.log('cover', out);
await b.close();
