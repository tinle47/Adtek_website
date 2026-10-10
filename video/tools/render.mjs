// Xuất video MP4 từ kịch bản. Có giọng đọc (public/voice/<id>/manifest.json) thì dùng, chưa có thì xuất bản không tiếng.
// Cách dùng: node tools/render.mjs <slug> [số video...]          ví dụ: node tools/render.mjs aio-la-gi
//            node tools/render.mjs <slug> [số...] --stills        chỉ chụp 1 khung mỗi cảnh để duyệt nhanh
//            node tools/render.mjs <slug> [số...] --fps 60        xuất 60 hình/giây (mượt hơn, render lâu gấp đôi)
//            node tools/render.mjs <slug> [số...] --format 1:1    khổ vuông 1080x1080 (hoặc 16:9: 1920x1080), file out/<id>-1x1.mp4
//            node tools/render.mjs <slug> [số...] --carousel      bản ảnh lướt cho TikTok: mỗi cảnh 1 ảnh out/<id>-slide<n>.png
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
const suffix = format === "9:16" ? "" : `-${format.replace(":", "x")}`;
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

mkdirSync(OUT, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(ROOT, "src/index.ts") });

for (const file of files) {
  const script = JSON.parse(readFileSync(path.join(dir, file), "utf8"));
  const manifest = path.join(ROOT, "public", "voice", script.id, "manifest.json");
  const voice = existsSync(manifest) ? JSON.parse(readFileSync(manifest, "utf8")) : null;
  if (voice && voice.scenes.length !== script.scenes.length) {
    throw new Error(`${script.id}: giọng đọc cũ không khớp số cảnh, chạy lại tools/voice.mjs`);
  }
  const inputProps = { script, voice, fps, format, carousel };
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
