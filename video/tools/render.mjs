// Xuất video MP4 từ kịch bản. Có giọng đọc (public/voice/<id>/manifest.json) thì dùng, chưa có thì xuất bản không tiếng.
// Cách dùng: node tools/render.mjs <slug> [số video...]          ví dụ: node tools/render.mjs aio-la-gi
//            node tools/render.mjs <slug> [số...] --stills        chỉ chụp 1 khung mỗi cảnh để duyệt nhanh
//            node tools/render.mjs <slug> [số...] --fps 60        xuất 60 hình/giây (mượt hơn, render lâu gấp đôi)
//            node tools/render.mjs <slug> [số...] --format 1:1    khổ vuông 1080x1080 (hoặc 16:9: 1920x1080), file out/<id>-1x1.mp4
//            node tools/render.mjs <slug> [số...] --carousel      bản ảnh lướt cho TikTok: mỗi cảnh 1 ảnh out/<id>-slide<n>.png
//            node tools/render.mjs <slug> [số...] --mascot        thêm mèo Adtek ở góc trái, miệng mở theo độ to giọng đọc
// Kết quả: out/<id>.mp4 và out/<id>.txt (caption + hashtag để đăng TikTok).
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { timeline } from "../src/timing.ts"; // Node 22.18+ đọc thẳng TypeScript

const ROOT = path.resolve(import.meta.dirname, "..");
const OUT = path.join(ROOT, "out");
const browserExecutable = process.env.REMOTION_BROWSER || null;

const args = process.argv.slice(2);
const stills = args.includes("--stills");
const opt = (k) => (args.includes(k) ? args[args.indexOf(k) + 1] : undefined);
const fps = Number(opt("--fps") ?? 30);
const format = opt("--format") ?? "9:16";
const carousel = args.includes("--carousel");
const mascot = args.includes("--mascot");
const suffix = (format === "9:16" ? "" : `-${format.replace(":", "x")}`) + (args.includes("--mascot") ? "-meo" : "");
const [slug, ...nums] = args.filter((a, i) => !a.startsWith("--") && !["--fps", "--format"].includes(args[i - 1]));
const dir = path.join(ROOT, "scripts", slug);
const files = nums.length ? nums.map((n) => `${n}.json`) : readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

// Cân giọng về -14 LUFS (mức to chuẩn của TikTok), để khi chèn nhạc TikTok ở mức Sound khoảng 15% nhạc vẫn nằm dưới giọng.
// Đo trước, chỉnh sau (loudnorm 2 lượt), giữ nguyên hình. Dùng ffmpeg đi kèm Remotion nên không cần cài thêm.
// Hai hashtag mặc định luôn đứng đầu, sau đó là hashtag riêng của video (bỏ trùng).
const DEFAULT_TAGS = ["#adtekagency", "#growthmarketing"];
const hashtags = (tags = []) => [...new Set([...DEFAULT_TAGS, ...tags])];

const LOUDNESS = "I=-14:TP=-1.5:LRA=11";
function ffmpeg(args) {
  const r = spawnSync(path.join(ROOT, "node_modules", ".bin", "remotion"), ["ffmpeg", "-hide_banner", "-y", ...args], { encoding: "utf8" });
  if (r.status !== 0) throw new Error(`ffmpeg lỗi: ${r.stderr.slice(-500)}`);
  return r.stderr;
}
function normalize(file) {
  const log = ffmpeg(["-i", file, "-vn", "-af", `loudnorm=${LOUDNESS}:print_format=json`, "-f", "null", "-"]);
  const m = JSON.parse(log.match(/\{[^{}]*"input_i"[^{}]*\}/)[0]);
  const tmp = file.replace(/\.mp4$/, ".tmp.mp4");
  const measured = `measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}`;
  ffmpeg(["-i", file, "-c:v", "copy", "-af", `loudnorm=${LOUDNESS}:${measured}:linear=true`, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp]);
  renameSync(tmp, file);
  return Number(m.input_i);
}

// Độ to giọng đọc 30 lần mỗi giây (cho mèo nói theo): giải mã mp3 thành PCM, tính RMS từng đoạn 1/30 giây, đổi ra dB
// rồi quy về 0..1 theo cả video (95% độ to lớn nhất là 1, thấp hơn 28 dB là 0).
function envelope(files) {
  const SR = 9000, N = 300; // 9000 mẫu mỗi giây chia chẵn thành 30 đoạn 300 mẫu
  const dbs = files.map((file) => {
    if (!file) return [];
    // ffmpeg của Remotion không có định dạng PCM thô, nên xuất WAV rồi bỏ phần đầu tới khối "data".
    const r = spawnSync(path.join(ROOT, "node_modules", ".bin", "remotion"), ["ffmpeg", "-v", "error", "-i", path.join(ROOT, "public", file), "-ac", "1", "-ar", String(SR), "-c:a", "pcm_s16le", "-bitexact", "-f", "wav", "-"], { maxBuffer: 1 << 28 });
    if (r.status !== 0) throw new Error(`không đọc được ${file}: ${String(r.stderr).slice(-300)}`);
    const start = r.stdout.indexOf("data") + 8;
    const body = Buffer.from(r.stdout.subarray(start, start + Math.floor((r.stdout.length - start) / 2) * 2));
    const pcm = new Int16Array(body.buffer, body.byteOffset, body.length / 2);
    const out = [];
    for (let i = 0; i + N <= pcm.length; i += N) {
      let s = 0;
      for (let j = i; j < i + N; j++) s += pcm[j] * pcm[j];
      out.push(10 * Math.log10(s / N / 32768 / 32768 + 1e-12));
    }
    return out;
  });
  const all = dbs.flat().sort((a, b) => a - b);
  const peak = all[Math.floor(all.length * 0.95)] ?? -20;
  const floor = peak - 22;
  const clamp01 = (x) => Math.min(1, Math.max(0, x));
  // Nhịp âm tiết: so với độ to thấp nhất, cao nhất trong khoảng 0.25 giây xung quanh, để miệng khép giữa các tiếng.
  return dbs.map((d) => {
    const g = d.map((v) => clamp01((v - floor) / (peak - floor)));
    return g.map((v, i) => {
      const win = g.slice(Math.max(0, i - 4), i + 5);
      const lo = Math.min(...win), hi = Math.max(...win);
      const local = hi - lo > 0.05 ? (v - lo) / (hi - lo) : 0.5;
      return Math.round(v * (0.35 + 0.65 * local) * 100) / 100;
    });
  });
}

mkdirSync(OUT, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(ROOT, "src/index.ts") });

for (const file of files) {
  const script = JSON.parse(readFileSync(path.join(dir, file), "utf8"));
  const manifest = path.join(ROOT, "public", "voice", script.id, "manifest.json");
  const voice = existsSync(manifest) ? JSON.parse(readFileSync(manifest, "utf8")) : null;
  if (voice && voice.scenes.length !== script.scenes.length) {
    throw new Error(`${script.id}: giọng đọc cũ không khớp số cảnh, chạy lại tools/voice.mjs`);
  }
  const inputProps = { script, voice, fps, format, carousel, mascot: mascot && voice ? envelope(voice.scenes.map((v) => v.file)) : undefined };
  const composition = await selectComposition({ serveUrl, id: "Infographic", inputProps, browserExecutable });

  if (stills) {
    // Chụp khung ở khoảng 80% mỗi cảnh, lúc mọi phần tử đã hiện đủ.
    for (const [i, s] of timeline(inputProps).entries()) {
      const output = path.join(OUT, `${script.id}-scene${i + 1}.png`);
      await renderStill({ serveUrl, composition, inputProps, frame: s.from + Math.floor(s.frames * 0.8), output, browserExecutable });
    }
    console.log(`${script.id}: đã chụp ${script.scenes.length} cảnh`);
    continue;
  }

  if (carousel) {
    // Mỗi cảnh 1 ảnh, chụp ngay trước khi cảnh mờ dần (mọi phần tử đã hiện đủ).
    for (const [i, s] of timeline(inputProps).entries()) {
      const output = path.join(OUT, `${script.id}${suffix}-slide${i + 1}.png`);
      await renderStill({ serveUrl, composition, inputProps, frame: s.from + s.frames - Math.round((9 * fps) / 30), output, browserExecutable });
    }
    console.log(`${script.id}: ${script.scenes.length} ảnh lướt -> out/${script.id}${suffix}-slide*.png`);
    continue;
  }

  // Ảnh bìa: 3 đến 5 chữ thật to (trường "cover" trong kịch bản, mặc định lấy tiêu đề cảnh đầu).
  if (format === "9:16") {
  const cover = await selectComposition({ serveUrl, id: "Cover", inputProps, browserExecutable });
  await renderStill({ serveUrl, composition: cover, inputProps, frame: 0, output: path.join(OUT, `${script.id}-cover.png`), browserExecutable });
  }

  const output = path.join(OUT, `${script.id}${suffix}.mp4`);
  await renderMedia({
    serveUrl,
    composition,
    inputProps,
    codec: "h264",
    crf: 18,
    outputLocation: output,
    browserExecutable,
    muted: !voice,
  });
  const before = voice ? normalize(output) : null;
  writeFileSync(
    path.join(OUT, `${script.id}${suffix}.txt`),
    `${script.caption}\n\n${hashtags(script.hashtags).join(" ")}\n`,
  );
  const secs = (composition.durationInFrames / composition.fps).toFixed(1);
  console.log(`${script.id}: ${secs}s ${voice ? `có giọng, âm lượng ${before} -> -14 LUFS` : "chưa có giọng"} -> ${path.relative(ROOT, output)}`);
}
