// Xuất video MP4 từ kịch bản. Có giọng đọc (public/voice/<id>/manifest.json) thì dùng, chưa có thì xuất bản không tiếng.
// Cách dùng: node tools/render.mjs <slug> [số video...]          ví dụ: node tools/render.mjs aio-la-gi
//            node tools/render.mjs <slug> [số...] --stills        chỉ chụp 1 khung mỗi cảnh để duyệt nhanh
// Kết quả: out/<id>.mp4 và out/<id>.txt (caption + hashtag để đăng TikTok).
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
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
    muted: !voice && script.music === false,
  });
  writeFileSync(
    path.join(OUT, `${script.id}.txt`),
    `${script.caption}\n\n${script.hashtags.join(" ")}\n\nBài gốc: ${script.post_url}\n`,
  );
  const secs = (composition.durationInFrames / composition.fps).toFixed(1);
  console.log(`${script.id}: ${secs}s ${voice ? "có giọng" : "chưa có giọng"} -> ${path.relative(ROOT, output)}`);
}
