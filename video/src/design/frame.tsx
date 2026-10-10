import "@fontsource/be-vietnam-pro/400.css";
import "@fontsource/be-vietnam-pro/600.css";
import "@fontsource/be-vietnam-pro/700.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/source-serif-4/600.css";
import React, { createContext, useContext, useEffect, useState } from "react";
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
import { cueTime } from "../cue";
export { cueTime, numbersIn } from "../cue";

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

// Mọi mốc thời gian trong phần thiết kế tính theo khung của video 30 hình/giây. Xuất 60 hình/giây thì
// useFrame trả về số khung đã quy đổi (có thể lẻ, ví dụ 12.5), nên hiệu ứng giữ nguyên nhịp mà mượt gấp đôi.
export const BASE_FPS = 30;
export const useFrame = () => useCurrentFrame() * (BASE_FPS / useVideoConfig().fps);

// Lò xo (thông số lấy từ bộ animate): snappy cho thẻ nhỏ, nút; smooth cho tiêu đề, khung; heavy cho số to;
// playful nảy rõ, dùng cho con dấu, biểu tượng. Có độ nảy nhẹ và dừng tự nhiên thay vì trượt đều rồi khựng lại.
export const SPRING = {
  snappy: { stiffness: 320, damping: 30 },
  smooth: { stiffness: 170, damping: 26 },
  heavy: { stiffness: 90, damping: 19 },
  playful: { stiffness: 260, damping: 14 },
};
// Lò xo bắt đầu ở khung `at` (đơn vị 30 hình/giây), f lấy từ useFrame, fps là fps thật của video.
export const springAt = (f: number, fps: number, at: number, config: Partial<typeof SPRING.smooth>, durationInFrames?: number) =>
  spring({ frame: (f - at) * (fps / BASE_FPS), fps, config, durationInFrames: durationInFrames && durationInFrames * (fps / BASE_FPS) });

// ---------- Giọng đọc là đồng hồ (học từ bộ animate) ----------
// Con số, ý trong danh sách, con dấu "SAI" hiện đúng lúc giọng đọc tới nó, thay vì hiện hết trong 2 giây đầu
// rồi đứng yên suốt phần còn lại của cảnh (người xem lướt đi khi màn hình đứng yên quá 4 giây).
// words: lời đọc của cảnh; offset: khung (30 hình/giây) lúc giọng bắt đầu, tính theo khung của phần hình;
// hook: cảnh đầu đang hiện sẵn trạng thái cuối, chỉ những hiệu ứng cho phép (con dấu, nhấn lựa chọn) mới đợi giọng.
type Cue = { words: Word[]; offset: number; hook: boolean };
export const CueContext = createContext<Cue>({ words: [], offset: 0, hook: false });
// cue(needle, fallback): khung hiện phần tử = muộn hơn giữa mốc mặc định và lúc giọng đọc tới (sớm 2 khung cho kịp mắt).
export const useCue = () => {
  const { words, offset, hook } = useContext(CueContext);
  // floor: mốc sớm nhất được phép (mặc định là fallback).
  return (needle: string | number | undefined, fallback: number, o: { after?: number; inHook?: boolean; floor?: number } = {}) => {
    if (needle === undefined || (hook && !o.inHook)) return fallback;
    const t = cueTime(words, needle, o.after === undefined ? -1 : (o.after - offset) / BASE_FPS);
    return t === undefined ? fallback : Math.max(o.floor ?? fallback, offset + t * BASE_FPS - 2);
  };
};

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
  const f = useFrame();
  const { fps } = useVideoConfig();
  return springAt(f, fps, delay, SPRING.smooth);
};

export const Background: React.FC = () => (
  <AbsoluteFill style={{ background: `linear-gradient(180deg, ${C.navy} 0%, ${C.navyDeep} 100%)` }} />
);

export const Logo: React.FC = () => (
  <Img src={staticFile("logo-white.png")} style={{ position: "absolute", left: L.pad, top: L.logo, height: 66 }} />
);

export const SiteFooter: React.FC = () => (
  <div data-audit="skip" style={{ position: "absolute", right: L.pad, top: L.footer, fontFamily: SANS, fontSize: 22, fontWeight: 600, letterSpacing: 1, color: C.muted }}>
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
// frames là số khung thật của cảnh.
export const Fade: React.FC<{ frames: number; children: React.ReactNode }> = ({ frames, children }) => {
  const f = useCurrentFrame();
  const fade = 7 * (useVideoConfig().fps / BASE_FPS);
  return <AbsoluteFill style={{ opacity: interpolate(f, [frames - fade, frames], [1, 0], clamp) }}>{children}</AbsoluteFill>;
};
