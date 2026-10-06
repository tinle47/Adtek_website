// Xuất các bản thử thiết kế thành MP4, hoặc ảnh chụp tại các frame trong biến FRAMES.
// Cách dùng: node tools/preview.mjs [id...] [--stills]   mặc định: Preview-glow Preview-editorial Preview-data
import { mkdirSync } from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";

const ROOT = path.resolve(import.meta.dirname, "..");
const OUT = path.join(ROOT, "out", "preview");
const browserExecutable = process.env.REMOTION_BROWSER || null;
const stills = process.argv.includes("--stills");
const args = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const ids = args.length ? args : ["Preview-glow", "Preview-editorial", "Preview-data"];

mkdirSync(OUT, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(ROOT, "src/index.ts") });
for (const id of ids) {
  const composition = await selectComposition({ serveUrl, id, browserExecutable });
  if (stills) {
    // Chụp ở cuối mỗi cảnh, lúc mọi phần tử đã hiện đủ.
    for (const [i, frame] of process.env.FRAMES.split(",").map(Number).entries()) {
      await renderStill({ serveUrl, composition, frame, output: path.join(OUT, `${id}-${i + 1}.png`), browserExecutable });
    }
  } else {
    await renderMedia({ serveUrl, composition, codec: "h264", crf: 18, outputLocation: path.join(OUT, `${id}.mp4`), browserExecutable, muted: true });
  }
  console.log(`${id}: xong`);
}
