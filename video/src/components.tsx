import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, FONT, SAFE } from "./theme";
import type { TimedScene } from "./timing";
import type { Word } from "./types";

// Hiện dần từ dưới lên, dùng cho mọi phần tử trong cảnh. delay tính bằng frame.
export const useEnter = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping: 200 }, durationInFrames: 18 });
};

export const Reveal: React.FC<{ delay?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({
  delay = 0,
  style,
  children,
}) => {
  const p = useEnter(delay);
  return (
    <div style={{ opacity: p, transform: `translateY(${(1 - p) * 40}px)`, ...style }}>{children}</div>
  );
};

// Nền xanh có vòng tròn lớn trôi chậm, giống ảnh bìa blog.
export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 90) * 30;
  return (
    <AbsoluteFill style={{ background: C.navy, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          width: 1100,
          height: 1100,
          borderRadius: "50%",
          background: C.navyLight,
          left: 420 + drift,
          top: 1050 - drift,
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 420,
          height: 420,
          borderRadius: "50%",
          border: `3px solid ${C.navyLight}`,
          left: -160 - drift,
          top: 120 + drift,
        }}
      />
    </AbsoluteFill>
  );
};

export const Brand: React.FC = () => (
  <div
    style={{
      position: "absolute",
      left: SAFE.left,
      top: SAFE.top - 90,
      display: "flex",
      alignItems: "center",
      gap: 18,
      fontFamily: FONT,
      color: C.white,
      fontWeight: 700,
      fontSize: 26,
      letterSpacing: 6,
    }}
  >
    <Img src={staticFile("logo-white.png")} style={{ height: 44 }} />
    <i style={{ display: "block", width: 70, height: 6, borderRadius: 3, background: C.orange }} />
  </div>
);

// Thanh tiến độ chia đoạn theo cảnh, giống story.
export const Progress: React.FC<{ scenes: TimedScene[] }> = ({ scenes }) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE.left,
        right: SAFE.right,
        top: SAFE.top - 130,
        display: "flex",
        gap: 8,
      }}
    >
      {scenes.map((s, i) => {
        const p = interpolate(frame, [s.from, s.from + s.frames], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div key={i} style={{ flex: 1, height: 6, borderRadius: 3, background: "rgba(255,255,255,0.22)" }}>
            <div style={{ width: `${p * 100}%`, height: "100%", borderRadius: 3, background: C.orange }} />
          </div>
        );
      })}
    </div>
  );
};

// Phụ đề: mỗi lần hiện một cụm khoảng 5 chữ, chữ đang đọc tô cam.
export const chunk = (words: Word[], size = 5) => {
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

export const Captions: React.FC<{ words: Word[] }> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const groups = chunk(words);
  const group = groups.find((g) => t < g[g.length - 1].end) ?? groups[groups.length - 1];
  if (!group) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE.left,
        right: SAFE.right,
        top: SAFE.captionTop,
        height: SAFE.bottom - SAFE.captionTop,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          fontFamily: FONT,
          fontWeight: 700,
          fontSize: 50,
          lineHeight: 1.3,
          textAlign: "center",
          color: C.white,
          background: "rgba(0,20,60,0.72)",
          padding: "18px 30px",
          borderRadius: 18,
        }}
      >
        {group.map((w, i) => (
          <span key={i} style={{ color: t >= w.start && t < w.end + 0.05 ? C.orange : C.white }}>
            {w.text}{" "}
          </span>
        ))}
      </div>
    </div>
  );
};

// Số chạy từ 0 tới giá trị, giữ nguyên tiền tố/hậu tố. Ví dụ "61%", "75,000", "0.664", "<1%".
export const CountUp: React.FC<{ value: string; delay?: number; duration?: number }> = ({
  value,
  delay = 0,
  duration = 30,
}) => {
  const frame = useCurrentFrame();
  const m = value.match(/^(.*?)(\d[\d,]*(?:\.\d+)?)(.*)$/);
  if (!m) return <>{value}</>;
  const [, prefix, num, suffix] = m;
  const target = parseFloat(num.replace(/,/g, ""));
  const decimals = num.includes(".") ? num.split(".")[1].length : 0;
  const p = interpolate(frame - delay, [0, duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (x) => 1 - Math.pow(1 - x, 3),
  });
  const shown = (target * p).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return (
    <>
      {prefix}
      {shown}
      {suffix}
    </>
  );
};

// Tô cam một cụm từ trong câu.
export const Highlight: React.FC<{ text: string; highlight?: string }> = ({ text, highlight }) => {
  if (!highlight || !text.includes(highlight)) return <>{text}</>;
  const [before, after] = text.split(highlight);
  return (
    <>
      {before}
      <span style={{ color: C.orange }}>{highlight}</span>
      {after}
    </>
  );
};

export const Source: React.FC<{ text?: string }> = ({ text }) =>
  text ? (
    <Reveal delay={20} style={{ marginTop: 40, fontFamily: FONT, fontSize: 28, color: C.line }}>
      Nguồn: {text}
    </Reveal>
  ) : null;
