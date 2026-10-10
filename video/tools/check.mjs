// Kiểm tra video trước khi xuất (học từ bộ animate): đo bằng máy những lỗi mắt hay bỏ sót trên ảnh nhỏ.
//   CHỮ:      chữ bị cắt (tràn khung hoặc tràn hộp chứa), chữ chồng lên chữ khác, chữ nằm dưới nút bấm của TikTok.
//   ĐỨNG HÌNH: đoạn dài hơn 4 giây mà vùng nội dung gần như không đổi (người xem lướt đi). Phụ đề không tính là "có gì mới".
//   NHỊP ĐỌC: cảnh đọc nhanh hơn 3.5 chữ mỗi giây.
// Cách dùng: node tools/check.mjs <slug> [số video...] [--every 5]
// Kết quả: bảng PASS/WARN/FAIL; có FAIL thì thoát mã 1. Ảnh khung mẫu nằm trong out/check/<id>/.
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync } from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderFrames, selectComposition } from "@remotion/renderer";

const ROOT = path.resolve(import.meta.dirname, "..");
const browserExecutable = process.env.REMOTION_BROWSER || null;
const args = process.argv.slice(2);
const opt = (k, d) => (args.includes(k) ? Number(args[args.indexOf(k) + 1]) : d);
const EVERY = opt("--every", 5); // lấy 1 khung mỗi 5 khung (6 lần mỗi giây ở 30 hình/giây)
const [slug, ...nums] = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--")));
const dir = path.join(ROOT, "scripts", slug);
const files = nums.length ? nums.map((n) => `${n}.json`) : readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

// Vùng an toàn 1080x1920 (khớp L trong design/frame.tsx): trên 260 là thanh tìm kiếm, dưới 1500 là tên kênh, caption, nhạc;
// cột nút bấm (ảnh đại diện, tim, bình luận, lưu, chia sẻ) nằm bên phải (từ x 975), từ khoảng y 900 đến 1500.
const W = 1080, H = 1920;
const SAFE = { top: 260, bottom: 1500, railX: 975, railTop: 900 };
const DEAD_MAX = 4; // giây
const MEO = { x1: 24 + 200, y0: 1224 + 20, y1: 1502 }; // vùng mèo Adtek (design/mascot.tsx), bỏ phần tai trên cùng
const MAX_WPS = 3.5;
const CONTENT = { top: 260, bottom: 1340 }; // vùng tính "có gì mới": bỏ phụ đề và tên miền

const overlap = (a, b) => Math.max(0, Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0)) * Math.max(0, Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0));
const area = (a) => (a.x1 - a.x0) * (a.y1 - a.y0);

const serveUrl = await bundle({ entryPoint: path.join(ROOT, "src/index.ts") });
let failed = false;

for (const file of files) {
  const script = JSON.parse(readFileSync(path.join(dir, file), "utf8"));
  const manifest = path.join(ROOT, "public", "voice", script.id, "manifest.json");
  const voice = existsSync(manifest) ? JSON.parse(readFileSync(manifest, "utf8")) : null;
  // --mascot: kiểm tra bố cục có mèo ở góc trái (phụ đề dời phải, chữ nào lọt vào vùng mèo thì báo).
  const inputProps = { script, voice, audit: true, mascot: args.includes("--mascot") ? script.scenes.map(() => []) : undefined };
  const composition = await selectComposition({ serveUrl, id: "Infographic", inputProps, browserExecutable });
  const fps = composition.fps;
  const outDir = path.join(ROOT, "out", "check", script.id);
  rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });

  // 1 lượt render ảnh nhỏ: vừa lấy vị trí chữ (qua console), vừa lấy ảnh để đo đứng hình.
  const audits = new Map();
  await renderFrames({
    serveUrl, composition, inputProps, browserExecutable,
    outputDir: outDir, imageFormat: "jpeg", jpegQuality: 70, scale: 0.25, everyNthFrame: EVERY,
    onStart: () => {}, onFrameUpdate: () => {}, logLevel: "error",
    onBrowserLog: ({ text }) => {
      if (!text.startsWith("AUDIT ")) return;
      const a = JSON.parse(text.slice(6));
      audits.set(a.frame, a.boxes);
    },
  });

  // ---- CHỮ ----
  const issues = new Map();
  const add = (level, kind, text, frame) => {
    const k = `${kind}|${text}`;
    const t = frame / fps;
    const v = issues.get(k);
    if (v) { v.t1 = t; v.n++; } else issues.set(k, { level, kind, text, t0: t, t1: t, n: 1 });
  };
  for (const [frame, boxes] of audits) {
    for (const b of boxes) {
      if (b.cut || b.x0 < -3 || b.y0 < -3 || b.x1 > W + 3 || b.y1 > H + 3) add("FAIL", "chữ bị cắt", b.s, frame);
      else if (inputProps.mascot && b.x0 < MEO.x1 && b.y1 > MEO.y0 && b.y0 < MEO.y1) add("FAIL", "chữ bị mèo che", b.s, frame);
      else if (b.y1 > SAFE.bottom + 2 || b.y0 < SAFE.top - 2 || (b.x1 > SAFE.railX && b.y1 > SAFE.railTop)) add("WARN", "dưới giao diện TikTok", b.s, frame);
    }
    for (let i = 0; i < boxes.length; i++)
      for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j];
        if (a.el === b.el) continue;
        if (overlap(a, b) > 0.25 * Math.min(area(a), area(b))) add("FAIL", "chữ chồng lên nhau", `"${a.s.slice(0, 24)}" × "${b.s.slice(0, 24)}"`, frame);
      }
  }

  // ---- ĐỨNG HÌNH ----
  const jpgs = readdirSync(outDir).filter((f) => f.endsWith(".jpeg") || f.endsWith(".jpg")).sort();
  const sw = W / 4, sh = H / 4;
  const y0 = Math.round(CONTENT.top / 4), y1 = Math.round(CONTENT.bottom / 4);
  const gray = (f) => spawnSync("ffmpeg", ["-v", "error", "-i", path.join(outDir, f), "-vf", "format=gray", "-f", "rawvideo", "-"], { maxBuffer: 1 << 24 }).stdout;
  const diffs = [];
  let prev = null;
  for (const f of jpgs) {
    const g = gray(f);
    if (prev) {
      // Đếm điểm ảnh đổi rõ (lệch hơn 24 mức xám): một dòng chữ nhỏ hiện ra cũng được tính, nhiễu nén ảnh thì không.
      let n = 0;
      // Mèo nhúc nhích liên tục, không tính là "có gì mới".
      const meoX = inputProps.mascot ? Math.ceil(MEO.x1 / 4) : 0, meoY = Math.floor((MEO.y0 - 20) / 4);
      for (let y = y0; y < y1; y++) for (let x = y >= meoY ? meoX : 0; x < sw; x++) if (Math.abs(g[y * sw + x] - prev[y * sw + x]) > 24) n++;
      diffs.push(n);
    }
    prev = g;
  }
  if (process.env.CHECK_DEBUG) console.log(diffs.map((d, i) => `${((i + 1) * EVERY / fps).toFixed(1)}:${d}`).join(" "));
  // Có "gì mới" khi ít nhất 40 điểm ảnh (ảnh thu nhỏ 1/4) đổi rõ giữa 2 khung mẫu liền nhau.
  const MOVE = 40;
  const dead = [];
  let run = 0;
  diffs.forEach((d, i) => {
    if (d < MOVE) run++;
    else { if (run * EVERY / fps > DEAD_MAX) dead.push([(i - run) * EVERY / fps, i * EVERY / fps]); run = 0; }
  });
  if (run * EVERY / fps > DEAD_MAX) dead.push([(diffs.length - run) * EVERY / fps, diffs.length * EVERY / fps]);
  // Đoạn đứng hình ở 1.5 giây cuối (cảnh Follow đang mờ dần) không tính.
  const total = composition.durationInFrames / fps;

  // ---- NHỊP ĐỌC ----
  const pace = (voice?.scenes ?? []).map((v, i) => ({ i: i + 1, wps: v.words.length / Math.max(0.1, v.duration) })).filter((p) => p.wps > MAX_WPS);

  // ---- BÁO CÁO ----
  // Lỗi chỉ thoáng qua 1 khung mẫu (đang chuyển cảnh) không tính.
  const list = [...issues.values()].filter((x) => x.n >= 2);
  const fails = list.filter((x) => x.level === "FAIL");
  const warns = list.filter((x) => x.level === "WARN");
  console.log(`\n${script.id}: ${total.toFixed(1)}s, ${fps} hình/giây, đo ${audits.size} khung`);
  console.log(`  CHỮ        ${fails.length ? "FAIL" : warns.length ? "WARN" : "PASS"}`);
  for (const x of [...fails, ...warns]) console.log(`    ${x.level}  ${x.kind}: ${x.text}  ở ${x.t0.toFixed(1)}${x.t1 > x.t0 ? `–${x.t1.toFixed(1)}` : ""}s`);
  console.log(`  ĐỨNG HÌNH  ${dead.length ? "WARN" : "PASS"}  (dài nhất ${Math.max(0, ...dead.map(([a, b]) => b - a)).toFixed(1)}s, ngưỡng ${DEAD_MAX}s)`);
  for (const [a, b] of dead) console.log(`    WARN  không có gì mới từ ${a.toFixed(1)}s đến ${b.toFixed(1)}s`);
  console.log(`  NHỊP ĐỌC   ${pace.length ? "WARN" : "PASS"}  (tối đa ${MAX_WPS} chữ/giây)`);
  for (const p of pace) console.log(`    WARN  cảnh ${p.i}: ${p.wps.toFixed(2)} chữ/giây`);
  if (fails.length) failed = true;
}
process.exit(failed ? 1 : 0);
