import React from "react";
import { AbsoluteFill, interpolate, useVideoConfig } from "remotion";
import type { Word } from "../types";
import { C, SANS, SPRING, clamp, springAt, useFrame } from "./frame";

// Khung mở đầu kiểu chữ TikTok (anh Tin chốt hướng A và C, 11/10/2026): hơn một nửa người xem lướt đi trong 2 giây đầu,
// nên khung đầu tiên chỉ có 1 câu hook thật to giữa màn hình (chữ trắng đậm viền đen, ý chính màu cam), giọng đọc đúng câu đó,
// rồi chữ bung ra để biểu đồ của cảnh 1 hiện lên. Kịch bản bật bằng trường "hook" (không có thì giữ kiểu cũ).

// Khung (30 hình/giây) lúc thẻ hook rời đi: hết câu đầu tiên của lời đọc, trong khoảng 1.5 đến 3 giây.
export const openerEnd = (words: Word[], lead: number) => {
  const first = words.find((w) => /[.?!]$/.test(w.text)) ?? words[Math.min(words.length, 8) - 1];
  const t = first ? lead + first.end * 30 + 6 : 60;
  return Math.round(Math.min(90, Math.max(45, t)));
};

const OUT = 8; // số khung chữ bung ra và mờ đi

const outline = (w: number): React.CSSProperties => ({
  WebkitTextStroke: `${w}px #000000`,
  paintOrder: "stroke fill",
  textShadow: "0 6px 0 rgba(0,0,0,0.55)",
});

export const Opener: React.FC<{ text: string; accent?: string; options?: string[]; end: number }> = ({ text, accent, options, end }) => {
  const f = useFrame();
  const { fps } = useVideoConfig();
  if (f > end + OUT) return null;
  // Khung đầu đã đủ chữ (to hơn 12%), lò xo co về đúng cỡ; sau đó chữ phóng chậm để màn hình không đứng yên.
  const land = springAt(f, fps, 0, SPRING.snappy);
  const drift = interpolate(f, [0, end], [0, 0.04], clamp);
  const exit = interpolate(f, [end - 2, end + OUT], [0, 1], clamp);
  const scale = 1.12 - 0.12 * land + drift + exit * 0.3;
  // Cỡ chữ theo số ký tự (chữ đậm rộng khoảng 0.56 cỡ chữ), chừa chỗ cho lúc chữ phóng to 12% ở khung đầu.
  // Câu dài thì xuống 2 hàng cân nhau: câu chính từ 15 ký tự (to nhất 150), ý cam từ 19 ký tự (to nhất 0.8 câu chính).
  const fit = (chars: number, max: number) => Math.round(Math.min(max, 820 / (chars * 0.56)));
  const lines = (t: string, from: number) => (t.length >= from ? Math.ceil(t.length / 2) + 1 : t.length);
  const size = fit(lines(text, 15), 150);
  const accentSize = accent ? fit(lines(accent, 19), Math.round(size * 0.8)) : 0;
  return (
    <AbsoluteFill style={{ opacity: 1 - exit, alignItems: "center", justifyContent: "center", paddingBottom: 260 }}>
      <div style={{ width: 940, textAlign: "center", transform: `scale(${scale})`, fontFamily: SANS, fontWeight: 700, lineHeight: 1.12, letterSpacing: -1 }}>
        <div style={{ fontSize: size, color: C.white, textWrap: "balance", ...outline(14) }}>{text}</div>
        {accent && <div style={{ fontSize: accentSize, color: C.orange, marginTop: 18, textWrap: "balance", ...outline(12) }}>{accent}</div>}
        {options && (
          <div style={{ display: "flex", gap: 22, marginTop: 56, justifyContent: "center" }}>
            {options.map((o, i) => {
              const p = springAt(f, fps, 3 + i * 3, SPRING.playful);
              return (
                <div key={i} style={{ flex: 1, padding: "26px 10px", borderRadius: 22, background: C.white, border: "5px solid #000000", transform: `scale(${0.85 + 0.15 * p})` }}>
                  <div style={{ fontSize: 36, color: C.orange }}>{String.fromCharCode(65 + i)}</div>
                  <div style={{ fontSize: o.length > 8 ? 40 : 52, color: C.navyDeep }}>{o}</div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
