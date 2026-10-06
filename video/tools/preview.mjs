// Xuất 3 hướng thiết kế (Preview-glow, Preview-editorial, Preview-data) thành MP4 và ảnh chụp từng cảnh.
// Cách dùng: node tools/preview.mjs [--stills]
import { mkdirSync } from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";

const ROOT = path.resolve(import.meta.dirname, "..");
const OUT = path.join(ROOT, "out", "preview");
const browserExecutable = process.env.REMOTION_BROWSER || null;
const stills = process.argv.includes("--stills");

mkdirSync(OUT, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(ROOT, "src/index.ts") });
for (const theme of ["glow", "editorial", "data"]) {
  const composition = await selectComposition({ serveUrl, id: `Preview-${theme}`, browserExecutable });
  if (stills) {
    // Chụp ở cuối mỗi cảnh, lúc mọi phần tử đã hiện đủ.
    for (const [i, frame] of process.env.FRAMES.split(",").map(Number).entries()) {
      await renderStill({ serveUrl, composition, frame, output: path.join(OUT, `${theme}-${i + 1}.png`), browserExecutable });
    }
  } else {
    await renderMedia({ serveUrl, composition, codec: "h264", crf: 18, outputLocation: path.join(OUT, `${theme}.mp4`), browserExecutable, muted: true });
  }
  console.log(`${theme}: xong`);
}
