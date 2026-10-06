// Tạo giọng đọc bằng ElevenLabs (giọng nhân bản của anh Tin) kèm thời điểm từng chữ để khớp phụ đề.
// Cách dùng: node tools/voice.mjs <slug> [số video...]   ví dụ: node tools/voice.mjs aio-la-gi 1 2 3
// Cần biến môi trường ELEVENLABS_API_KEY và ELEVENLABS_VOICE_ID. Tùy chọn ELEVENLABS_MODEL.
// Kết quả: public/voice/<id>/<cảnh>.mp3 và manifest.json. Cảnh nào lời đọc không đổi thì dùng lại file cũ, không tốn thêm credit.
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const KEY = process.env.ELEVENLABS_API_KEY;
const VOICE = process.env.ELEVENLABS_VOICE_ID;
const MODEL = process.env.ELEVENLABS_MODEL || "eleven_turbo_v2_5"; // dòng model hỗ trợ tiếng Việt

if (!KEY || !VOICE) {
  console.error("Thiếu ELEVENLABS_API_KEY hoặc ELEVENLABS_VOICE_ID trong biến môi trường.");
  process.exit(1);
}

const [slug, ...nums] = process.argv.slice(2);
const dir = path.join(ROOT, "scripts", slug);
const files = nums.length ? nums.map((n) => `${n}.json`) : readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

// Gộp thời điểm từng ký tự thành thời điểm từng chữ.
function toWords({ characters, character_start_times_seconds: s, character_end_times_seconds: e }) {
  const words = [];
  let cur = null;
  characters.forEach((ch, i) => {
    if (/\s/.test(ch)) {
      if (cur) words.push(cur);
      cur = null;
    } else if (cur) {
      cur.text += ch;
      cur.end = e[i];
    } else {
      cur = { text: ch, start: s[i], end: e[i] };
    }
  });
  if (cur) words.push(cur);
  return words;
}

async function speak(text, previous_text, next_text) {
  const res = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`,
    {
      method: "POST",
      headers: { "xi-api-key": KEY, "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        model_id: MODEL,
        language_code: "vi",
        apply_text_normalization: "on", // đọc "15%" thành "mười lăm phần trăm"
        previous_text, // câu trước và sau giúp ngữ điệu liền mạch giữa các cảnh
        next_text,
        voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.2, use_speaker_boost: true },
      }),
    },
  );
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
    if (cached?.text === scene.voice && existsSync(mp3)) {
      scenes.push(cached);
      continue;
    }
    const r = await speak(scene.voice, script.scenes[i - 1]?.voice, script.scenes[i + 1]?.voice);
    writeFileSync(mp3, Buffer.from(r.audio_base64, "base64"));
    const words = toWords(r.alignment);
    scenes.push({
      text: scene.voice,
      file: `voice/${script.id}/${i}.mp3`,
      duration: r.alignment.character_end_times_seconds.at(-1),
      words,
    });
    console.log(`${script.id} cảnh ${i + 1}: ${words.length} chữ`);
  }
  writeFileSync(manifestPath, JSON.stringify({ model: MODEL, scenes }, null, 1));
}
