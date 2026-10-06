// Tạo giọng đọc bằng ElevenLabs (giọng nhân bản của anh Tin) kèm thời điểm từng chữ để khớp phụ đề.
// Cách dùng: node tools/voice.mjs <slug> [số video...]   ví dụ: node tools/voice.mjs aio-la-gi 1 2 3
// Cần biến môi trường ELEVENLABS_API_KEY và ELEVENLABS_VOICE_ID. Tùy chọn ELEVENLABS_MODEL.
// Kết quả: public/voice/<id>/<cảnh>.mp3 và manifest.json. Cảnh nào lời đọc không đổi thì dùng lại file cũ, không tốn thêm credit.
// Từ máy hay đọc sai khai báo trong tools/pronunciation.json (chữ gốc -> cách đọc). Máy đọc theo cách đọc, phụ đề vẫn hiện chữ gốc.
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const KEY = process.env.ELEVENLABS_API_KEY;
const VOICE = process.env.ELEVENLABS_VOICE_ID;
const MODEL = process.env.ELEVENLABS_MODEL || "eleven_v4"; // Eleven v4 hỗ trợ tiếng Việt và trả thời điểm từng chữ

if (!KEY || !VOICE) {
  console.error("Thiếu ELEVENLABS_API_KEY hoặc ELEVENLABS_VOICE_ID trong biến môi trường.");
  process.exit(1);
}

const [slug, ...nums] = process.argv.slice(2);
const dir = path.join(ROOT, "scripts", slug);
const files = nums.length ? nums.map((n) => `${n}.json`) : readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

// Từ điển phát âm: phân biệt hoa thường và chỉ thay nguyên chữ, nên "AI" không đụng tới "ai" hay "AIO".
const DICT = JSON.parse(readFileSync(path.join(ROOT, "tools", "pronunciation.json"), "utf8"));
const TERMS = Object.keys(DICT).sort((a, b) => b.length - a.length);
const esc = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const TERM_RE = TERMS.length ? new RegExp(`(?<![\\p{L}\\p{N}])(${TERMS.map(esc).join("|")})(?![\\p{L}\\p{N}])`, "gu") : null;

// Thay chữ gốc bằng cách đọc. map[i] = vị trí ký tự trong câu gốc ứng với ký tự thứ i của câu đọc.
function pronounce(text) {
  if (!TERM_RE) return { said: text, map: Array.from(text, (_, i) => i) };
  let said = "";
  const map = [];
  let last = 0;
  const keep = (from, to) => {
    for (let i = from; i < to; i++) map.push(i);
    said += text.slice(from, to);
  };
  for (const m of text.matchAll(TERM_RE)) {
    keep(last, m.index);
    const alias = DICT[m[0]];
    for (let k = 0; k < alias.length; k++) map.push(m.index + Math.floor((k * m[0].length) / alias.length));
    said += alias;
    last = m.index + m[0].length;
  }
  keep(last, text.length);
  return { said, map };
}

// Thời điểm từng chữ của câu gốc: lấy từ các ký tự đã đọc thuộc về chữ đó.
// Không dùng [...text] vì ElevenLabs trả thời điểm theo từng đơn vị UTF-16, giống text.length.
function toWords(text, map, { characters, character_start_times_seconds: s, character_end_times_seconds: e }) {
  const owner = new Array(text.length).fill(-1);
  const words = [];
  for (const m of text.matchAll(/\S+/g)) {
    for (let i = m.index; i < m.index + m[0].length; i++) owner[i] = words.length;
    words.push({ text: m[0], start: Infinity, end: 0 });
  }
  characters.forEach((ch, i) => {
    const w = words[owner[map[i]]];
    if (!w || /\s/.test(ch)) return;
    w.start = Math.min(w.start, s[i]);
    w.end = Math.max(w.end, e[i]);
  });
  // Chữ không có ký tự nào được đọc (hiếm) thì lấy theo chữ liền trước.
  words.forEach((w, i) => {
    if (w.start === Infinity) w.start = w.end = words[i - 1]?.end ?? 0;
  });
  return words;
}

const post = (body) =>
  fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`, {
    method: "POST",
    headers: { "xi-api-key": KEY, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

// Gửi đủ tùy chọn trước. Model mới có thể chưa nhận một số tùy chọn (lỗi 400/422):
// khi đó gửi lại bản tối giản, chỉ có lời đọc và model, để không dừng giữa chừng.
let minimal = false;
async function speak(text, previous_text, next_text) {
  const full = {
    text,
    model_id: MODEL,
    language_code: "vi",
    previous_text, // câu trước và sau giúp ngữ điệu liền mạch giữa các cảnh
    next_text,
    voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.2, use_speaker_boost: true },
  };
  let res = minimal ? null : await post(full);
  if (!res || res.status === 400 || res.status === 422) {
    if (res && !minimal) console.warn(`Model ${MODEL} không nhận đủ tùy chọn (${await res.text()}), chuyển sang bản tối giản.`);
    minimal = true;
    res = await post({ text, model_id: MODEL });
  }
  if (!res.ok) throw new Error(`ElevenLabs ${res.status}: ${await res.text()}`);
  return res.json();
}

for (const file of files) {
  const script = JSON.parse(readFileSync(path.join(dir, file), "utf8"));
  const out = path.join(ROOT, "public", "voice", script.id);
  mkdirSync(out, { recursive: true });
  const manifestPath = path.join(out, "manifest.json");
  const old = existsSync(manifestPath) ? JSON.parse(readFileSync(manifestPath, "utf8")) : { scenes: [] };
  const scenes = [];
  for (const [i, scene] of script.scenes.entries()) {
    const cached = old.scenes[i];
    const mp3 = path.join(out, `${i}.mp3`);
    const { said, map } = pronounce(scene.voice);
    // Sửa lời đọc hoặc sửa từ điển cho chữ có trong cảnh thì cảnh đó mới tạo lại giọng.
    if (cached?.text === scene.voice && (cached.said ?? cached.text) === said && existsSync(mp3)) {
      scenes.push(cached);
      continue;
    }
    const near = (j) => script.scenes[j] && pronounce(script.scenes[j].voice).said;
    const r = await speak(said, near(i - 1), near(i + 1));
    if (r.alignment.characters.join("") !== said) throw new Error(`${script.id} cảnh ${i + 1}: ElevenLabs trả thời điểm không khớp câu đã gửi.`);
    writeFileSync(mp3, Buffer.from(r.audio_base64, "base64"));
    const words = toWords(scene.voice, map, r.alignment);
    scenes.push({
      text: scene.voice,
      said,
      file: `voice/${script.id}/${i}.mp3`,
      duration: r.alignment.character_end_times_seconds.at(-1),
      words,
    });
    console.log(`${script.id} cảnh ${i + 1}: ${words.length} chữ`);
  }
  writeFileSync(manifestPath, JSON.stringify({ model: MODEL, scenes }, null, 1));
}
