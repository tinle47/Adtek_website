import "@fontsource/be-vietnam-pro/400.css";
import "@fontsource/be-vietnam-pro/600.css";
import "@fontsource/be-vietnam-pro/700.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/source-serif-4/600.css";
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { Word } from "../types";

// Khung video Adtek: nền navy phẳng, logo góc trái, tiêu đề font có chân căn trái, phụ đề giữa, không hiệu ứng phát sáng.
export const C = {
  navy: "#002D72",
  navyDeep: "#00225A",
  orange: "#FF9014",
  white: "#FFFFFF",
  muted: "#8FA3C4",
};
export const SANS = '"Be Vietnam Pro", sans-serif';
export const SERIF = '"Source Serif 4", serif';

// Bố cục dọc 1080x1920. Trên 260 và dưới 1500 là vùng giao diện TikTok che, chỉ để logo và tên miền.
export const L = { pad: 90, logo: 150, head: 300, stage: 660, caption: 1350, footer: 1800 };

export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const ease = Easing.bezier(0.33, 0, 0.2, 1);

// Chờ đủ font (kể cả dấu tiếng Việt) rồi mới chụp khung hình.
export const useFonts = () => {
  const [handle] = useState(() => delayRender("Tải font"));
  useEffect(() => {
    const sample = "Tiếng Việt ăâđêôơư";
    Promise.all([
      ...[400, 600, 700].map((w) => document.fonts.load(`${w} 40px "Be Vietnam Pro"`, sample)),
      document.fonts.load(`600 60px "Source Serif 4"`, sample),
      ...[400, 500].map((w) => document.fonts.load(`${w} 16px "Roboto"`, sample)),
    ]).then(() => continueRender(handle));
  }, [handle]);
};

// Hiện dần từ dưới lên. delay tính bằng frame.
export const useEnter = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping: 200 }, durationInFrames: 18 });
};

export const Background: React.FC = () => (
  <AbsoluteFill style={{ background: `linear-gradient(180deg, ${C.navy} 0%, ${C.navyDeep} 100%)` }} />
);

export const Logo: React.FC = () => (
  <Img src={staticFile("logo-white.png")} style={{ position: "absolute", left: L.pad, top: L.logo, height: 66 }} />
);

export const SiteFooter: React.FC = () => (
  <div style={{ position: "absolute", right: L.pad, top: L.footer, fontFamily: SANS, fontSize: 22, fontWeight: 600, letterSpacing: 1, color: C.muted }}>
    adtek.agency
  </div>
);

// Tiêu đề 2 dòng: dòng trắng + dòng cam. Cảnh không có hình minh họa (câu chốt) dùng cỡ lớn và đặt thấp hơn.
export const Headline: React.FC<{ kicker: string; headline: string; accent: string; big?: boolean }> = ({
  kicker,
  headline,
  accent,
  big,
}) => {
  const k = useEnter(0);
  const a = useEnter(4);
  const b = useEnter(10);
  const line = (p: number, color: string, text: string) => (
    <div
      style={{
        fontFamily: SERIF,
        fontWeight: 600,
        fontSize: big ? 84 : 64,
        lineHeight: 1.16,
        letterSpacing: -0.5,
        color,
        textWrap: "pretty",
        opacity: p,
        transform: `translateY(${(1 - p) * 18}px)`,
      }}
    >
      {text}
    </div>
  );
  return (
    <div style={{ position: "absolute", left: L.pad, right: L.pad, top: big ? 640 : L.head }}>
      <div style={{ fontFamily: SANS, fontSize: 22, fontWeight: 600, letterSpacing: 3, textTransform: "uppercase", color: C.muted, marginBottom: big ? 32 : 22, opacity: k }}>
        {kicker}
      </div>
      {line(a, C.white, headline)}
      {big && <div style={{ height: 18 }} />}
      {line(b, C.orange, accent)}
    </div>
  );
};

// Phụ đề: mỗi lần một cụm khoảng 6 chữ, chữ đang đọc tô cam.
const chunk = (words: Word[], size = 6) => {
  const out: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    if (cur.length >= size || /[.,:;?!]$/.test(w.text)) {
      out.push(cur);
      cur = [];
    }
  }
  if (cur.length) out.push(cur);
  return out;
};

export const Caption: React.FC<{ words: Word[] }> = ({ words }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const groups = chunk(words);
  const g = groups.find((x) => t < x[x.length - 1].end) ?? groups[groups.length - 1];
  if (!g) return null;
  return (
    <div style={{ position: "absolute", left: L.pad + 20, right: L.pad + 20, top: L.caption, textAlign: "center", fontFamily: SANS, fontSize: 38, fontWeight: 600, lineHeight: 1.5, color: "rgba(255,255,255,0.92)" }}>
      {g.map((w, i) => (
        <span key={i} style={{ color: t >= w.start && t < w.end + 0.05 ? C.orange : undefined }}>
          {w.text}
          {i < g.length - 1 ? " " : ""}
        </span>
      ))}
    </div>
  );
};

// Mờ dần ở cuối cảnh để chuyển cảnh êm.
export const Fade: React.FC<{ frames: number; children: React.ReactNode }> = ({ frames, children }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ opacity: interpolate(f, [frames - 7, frames], [1, 0], clamp) }}>{children}</AbsoluteFill>;
};
