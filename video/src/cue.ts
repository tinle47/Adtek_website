import type { Word } from "./types";

// Tìm lúc giọng đọc tới một con số hoặc một cụm chữ (dùng cho "giọng đọc là đồng hồ" trong design/frame.tsx).
// Tách riêng, không phụ thuộc Remotion, để kiểm tra được bằng Node.
const clean = (s: string) => s.toLowerCase().normalize("NFC").replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}%]+$/gu, "");
const digits = (s: string) => s.replace(/[^0-9.,]/g, "").replace(/,/g, "").replace(/\.$/, "");
// Thời điểm (giây, tính từ lúc giọng bắt đầu) giọng đọc tới needle: một con số (54 khớp "54%"), một chữ ("sai"),
// hoặc một cụm chữ (khớp 2 chữ liền nhau bất kỳ trong cụm, để "Không tặng quà" vẫn khớp "Đừng tặng quà"). after: chỉ tìm sau mốc này.
// avoid: bỏ qua cặp chữ cũng có trong câu này (dòng chi tiết "50 đánh giá" không được khớp nhầm vào "Xin đánh giá" của chính việc đó).
const pairs = (s: string) => {
  const t = s.split(/\s+/).map(clean).filter(Boolean);
  return new Set(t.slice(1).map((b, i) => `${t[i]} ${b}`));
};
export const cueTime = (words: Word[], needle: string | number, after = -1, avoid = ""): number | undefined => {
  const ws = words.filter((w) => w.start > after);
  if (typeof needle === "number") {
    const want = String(needle);
    return ws.find((w) => digits(w.text) === want)?.start;
  }
  const toks = needle.split(/\s+/).map(clean).filter(Boolean);
  if (toks.length === 1) return ws.find((w) => clean(w.text) === toks[0])?.start;
  const skip = pairs(avoid);
  for (let i = 0; i + 1 < ws.length; i++) {
    const a = clean(ws[i].text), b = clean(ws[i + 1].text);
    if (skip.has(`${a} ${b}`)) continue;
    for (let j = 0; j + 1 < toks.length; j++) if (toks[j] === a && toks[j + 1] === b) return ws[i].start;
  }
  return undefined;
};
// Các con số trong một câu chữ, ví dụ "Dưới 3.6 sao; 74% cần từ 50 đánh giá" -> [3.6, 74, 50].
export const numbersIn = (s: string) => (s.match(/\d+(?:[.,]\d+)*/g) ?? []).map((x) => Number(x.replace(/,/g, "")));

