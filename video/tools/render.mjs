// Xuất video MP4 từ kịch bản. Có giọng đọc (public/voice/<id>/manifest.json) thì dùng, chưa có thì xuất bản không tiếng.
// Cách dùng: node tools/render.mjs <slug> [số video...]          ví dụ: node tools/render.mjs aio-la-gi
//            node tools/render.mjs <slug> [số...] --stills        chỉ chụp 1 khung mỗi cảnh để duyệt nhanh
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
const [slug, ...nums] = args.filter((a) => !a.startsWith("--"));
const dir = path.join(ROOT, "scripts", slug);
const files = nums.length ? nums.map((n) => `${n}.json`) : readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

// Cân giọng về -14 LUFS (mức to chuẩn của TikTok), để khi chèn nhạc TikTok ở mức Sound khoảng 15% nhạc vẫn nằm dưới giọng.
// Đo trước, chỉnh sau (loudnorm 2 lượt), giữ nguyên hình. Dùng ffmpeg đi kèm Remotion nên không cần cài thêm.
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
  const inputProps = { script, voice };
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

  const output = path.join(OUT, `${script.id}.mp4`);
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
    path.join(OUT, `${script.id}.txt`),
    `${script.caption}\n\n${script.hashtags.join(" ")}\n\nBài gốc: ${script.post_url}\n`,
  );
  const secs = (composition.durationInFrames / composition.fps).toFixed(1);
  console.log(`${script.id}: ${secs}s ${voice ? `có giọng, âm lượng ${before} -> -14 LUFS` : "chưa có giọng"} -> ${path.relative(ROOT, output)}`);
}
