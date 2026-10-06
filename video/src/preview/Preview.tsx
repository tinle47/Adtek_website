import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  random,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CountUp, chunk, useEnter } from "../components";
import { FONT } from "../theme";
import { timeline, type TimedScene } from "../timing";
import type { VideoProps, Word } from "../types";
import { useFonts } from "../Video";
import { THEMES, type Theme, type ThemeId } from "./themes";

// Đoạn demo khoảng 15 giây để so sánh 3 hướng thiết kế trên cùng một nội dung (video 1 bài AIO).
type DemoScene = {
  kicker: string;
  headline: string;
  accent: string;
  narrative: [string, string]; // dòng dẫn cho hướng Data Story: chữ thường + cụm tô nền
  voice: string;
  visual: "search" | "compare" | "dots";
};

const DEMO: DemoScene[] = [
  {
    kicker: "AIO · Nghịch lý đầu tiên",
    headline: "Khách hàng vẫn tìm trên Google.",
    accent: "Nhưng ngừng bấm vào bạn.",
    narrative: ["Khi Google", "không có tóm tắt AI"],
    voice: "Khách hàng vẫn tìm trên Google. Nhưng họ đang ngừng bấm vào bạn.",
    visual: "search",
  },
  {
    kicker: "Pew Research · 900 người dùng",
    headline: "Khi Google hiện tóm tắt AI,",
    accent: "tỷ lệ bấm giảm gần nửa.",
    narrative: ["Khi Google", "có tóm tắt AI"],
    voice: "Khi Google hiện tóm tắt AI, tỷ lệ bấm vào kết quả giảm từ 15% xuống 8%.",
    visual: "compare",
  },
  {
    kicker: "Link nằm trong tóm tắt AI",
    headline: "Cứ 100 lượt tìm kiếm,",
    accent: "chỉ 1 lượt bấm vào link.",
    narrative: ["Bấm vào link", "nằm trong tóm tắt AI"],
    voice: "Còn link nằm ngay trong tóm tắt AI? Cứ 100 lượt tìm, chỉ 1 lượt được bấm.",
    visual: "dots",
  },
];

const PAD = 80;
const Y = { header: 140, head: 300, stage: 680, stageH: 560, caption: 1290, footer: 1800 };
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const props = { script: { scenes: DEMO }, voice: null } as unknown as VideoProps;
export const previewFrames = () => timeline(props).reduce((s, x) => s + x.frames, 0);

// ---------- Nền ----------
const Background: React.FC<{ t: Theme }> = ({ t }) => {
  const f = useCurrentFrame();
  if (t.id === "glow") {
    const pulse = 0.75 + Math.sin(f / 18) * 0.25;
    return (
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 30%, #0A3A86 0%, #002D72 30%, #001536 85%)" }}>
        {Array.from({ length: 70 }).map((_, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              left: random(`x${i}`) * 1080,
              top: random(`y${i}`) * 1920,
              width: 3,
              height: 3,
              borderRadius: 2,
              background: "#fff",
              opacity: 0.08 + 0.25 * Math.abs(Math.sin(f / 25 + i)),
            }}
          />
        ))}
        <div
          style={{
            position: "absolute",
            left: 540 - 520,
            top: Y.stage + Y.stageH / 2 - 520,
            width: 1040,
            height: 1040,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(255,144,20,0.16) 0%, rgba(255,144,20,0) 60%)",
            opacity: pulse,
          }}
        />
      </AbsoluteFill>
    );
  }
  if (t.id === "editorial") {
    return (
      <AbsoluteFill style={{ background: "#F6F1E9" }}>
        <AbsoluteFill
          style={{
            backgroundImage:
              "linear-gradient(rgba(0,45,114,0.035) 2px, transparent 2px), linear-gradient(90deg, rgba(0,45,114,0.035) 2px, transparent 2px)",
            backgroundSize: "60px 60px",
          }}
        />
        <div style={{ position: "absolute", left: -260, top: -260, width: 900, height: 900, borderRadius: "50%", background: "radial-gradient(circle, rgba(255,144,20,0.22), rgba(255,144,20,0) 65%)" }} />
        <div style={{ position: "absolute", right: -300, bottom: -200, width: 1000, height: 1000, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,45,114,0.10), rgba(0,45,114,0) 65%)" }} />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill
      style={{
        background: "#F4F5F8",
        backgroundImage:
          "linear-gradient(rgba(0,45,114,0.06) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(0,45,114,0.06) 1.5px, transparent 1.5px)",
        backgroundSize: "54px 54px",
      }}
    />
  );
};

// ---------- Khung cố định: logo + nhãn series, chân trang, thanh tiến độ ----------
const Header: React.FC<{ t: Theme }> = ({ t }) => (
  <div style={{ position: "absolute", left: PAD, right: PAD, top: Y.header }}>
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <Img src={staticFile(t.dark ? "logo-white.png" : "logo-adtek.png")} style={{ height: 58 }} />
      <div style={{ ...t.tag, fontSize: 22, fontWeight: 700, letterSpacing: 2, padding: "10px 22px", borderRadius: 30 }}>
        AIO · 01/03
      </div>
    </div>
    <div style={{ height: 1.5, background: t.line, marginTop: 28 }} />
  </div>
);

const Footer: React.FC<{ t: Theme }> = ({ t }) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: PAD,
          right: PAD,
          top: Y.footer,
          display: "flex",
          justifyContent: "space-between",
          fontSize: 22,
          letterSpacing: 1,
          color: t.muted,
        }}
      >
        <span>Tin Le · Founder Adtek</span>
        <span style={{ color: t.accent, fontWeight: 700 }}>adtek.agency</span>
      </div>
      <div style={{ position: "absolute", left: 0, bottom: 0, height: 8, width: `${(f / durationInFrames) * 100}%`, background: t.accent }} />
    </>
  );
};

// ---------- Tiêu đề 2 dòng: dòng thường + dòng nhấn ----------
const Headline: React.FC<{ t: Theme; s: DemoScene }> = ({ t, s }) => {
  const k = useEnter(0);
  const words = [...s.headline.split(" ").map((w) => ({ w, a: false })), ...s.accent.split(" ").map((w) => ({ w, a: true }))];
  const split = s.headline.split(" ").length;
  return (
    <div style={{ position: "absolute", left: PAD, right: PAD, top: Y.head, textAlign: t.align }}>
      <div style={{ opacity: k, color: t.accent, fontSize: 24, fontWeight: 700, letterSpacing: 4, textTransform: "uppercase", marginBottom: 26 }}>
        {s.kicker}
      </div>
      {[words.slice(0, split), words.slice(split)].map((part, j) => (
        <div key={j} style={{ fontSize: 62, fontWeight: 800, lineHeight: 1.2, letterSpacing: -0.5, textWrap: "balance" }}>
          {part.map((x, i) => (
            <HeadWord key={i} t={t} delay={4 + (i + j * split) * 2} accent={x.a}>
              {x.w}
            </HeadWord>
          ))}
        </div>
      ))}
    </div>
  );
};

const HeadWord: React.FC<{ t: Theme; delay: number; accent: boolean; children: React.ReactNode }> = ({ t, delay, accent, children }) => {
  const p = useEnter(delay);
  return (
    <span
      style={{
        display: "inline-block",
        marginRight: 16,
        opacity: p,
        transform: `translateY(${(1 - p) * 24}px)`,
        filter: `blur(${(1 - p) * 6}px)`,
        color: accent ? t.accent : t.text,
        textShadow: accent && t.glow ? "0 0 28px rgba(255,144,20,0.55)" : "none",
      }}
    >
      {children}
    </span>
  );
};

// ---------- Phụ đề ----------
const Caption: React.FC<{ t: Theme; words: Word[] }> = ({ t, words }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const time = f / fps;
  const groups = chunk(words, 6);
  const g = groups.find((x) => time < x[x.length - 1].end) ?? groups[groups.length - 1];
  const on = (w: Word) => time >= w.start && time < w.end + 0.05;
  const box: React.CSSProperties =
    t.caption === "pill"
      ? { background: "#0B1B3F", color: "#fff", padding: "14px 26px", borderRadius: 14 }
      : t.caption === "highlight"
        ? { display: "inline", background: "#002D72", color: "#fff", padding: "6px 14px", boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone" }
        : { color: "rgba(255,255,255,0.92)" };
  return (
    <div style={{ position: "absolute", left: PAD + 20, right: PAD + 20, top: Y.caption + (t.caption === "highlight" ? 110 : 0), textAlign: "center" }}>
      <span style={{ display: "inline-block", fontSize: 38, fontWeight: 600, lineHeight: 1.55, ...box }}>
        {g.map((w, i) => (
          <span key={i} style={{ color: on(w) ? (t.caption === "highlight" ? "#FFB25C" : t.accent) : undefined }}>
            {w.text}
            {i < g.length - 1 ? " " : ""}
          </span>
        ))}
      </span>
    </div>
  );
};

// ---------- Hình minh họa ----------
const Card: React.FC<{ t: Theme; children: React.ReactNode }> = ({ t, children }) => {
  const p = useEnter(2);
  return (
    <div style={{ ...t.card, width: 880, padding: 48, position: "relative", opacity: p, transform: `scale(${0.96 + p * 0.04})` }}>
      {children}
    </div>
  );
};

const Magnifier: React.FC<{ color: string }> = ({ color }) => (
  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round">
    <circle cx="11" cy="11" r="7" />
    <path d="M20 20l-4-4" />
  </svg>
);

const Line: React.FC<{ t: Theme; w: string; h?: number; p?: number; color?: string }> = ({ t, w, h = 16, p = 1, color }) => (
  <div style={{ height: h, borderRadius: h / 2, background: color ?? t.dim, width: `calc(${w} * ${p})`, marginTop: 16 }} />
);

// Người dùng gõ tìm kiếm, tóm tắt AI hiện ra, các kết quả bên dưới mờ đi: không ai bấm.
const SearchMock: React.FC<{ t: Theme }> = ({ t }) => {
  const f = useCurrentFrame();
  const q = "aio là gì";
  const typed = q.slice(0, Math.floor(interpolate(f, [6, 24], [0, q.length], clamp)));
  const ov = useEnter(28);
  const res = useEnter(40);
  const fade = interpolate(f, [70, 84], [1, 0.3], clamp);
  const badge = useEnter(80);
  return (
    <Card t={t}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 20,
          height: 88,
          borderRadius: 44,
          padding: "0 32px",
          background: t.dark ? "rgba(255,255,255,0.06)" : "#F3EEE6",
          border: `1.5px solid ${t.line}`,
          fontSize: 34,
          color: t.text,
        }}
      >
        <Magnifier color={t.muted} />
        <span>
          {typed}
          <span style={{ opacity: f < 30 && f % 16 < 8 ? 1 : 0, color: t.accent }}>|</span>
        </span>
      </div>
      <div
        style={{
          marginTop: 32,
          opacity: ov,
          transform: `translateY(${(1 - ov) * 20}px)`,
          borderLeft: `6px solid ${t.accent}`,
          padding: "22px 28px 26px",
          borderRadius: 16,
          background: t.dark ? "rgba(255,144,20,0.08)" : "rgba(240,124,0,0.06)",
          boxShadow: t.glow ? "0 0 40px rgba(255,144,20,0.18)" : "none",
        }}
      >
        <div style={{ fontSize: 26, fontWeight: 700, color: t.accent, letterSpacing: 1 }}>✦ Tóm tắt AI</div>
        <Line t={t} w="95%" p={ov} />
        <Line t={t} w="82%" p={ov} />
        <Line t={t} w="58%" p={ov} />
      </div>
      <div style={{ opacity: res * fade, marginTop: 28 }}>
        {[0, 1].map((i) => (
          <div key={i} style={{ display: "flex", gap: 22, alignItems: "flex-start", marginTop: i ? 24 : 0 }}>
            <div style={{ width: 48, height: 48, borderRadius: 12, background: t.dim, flex: "none" }} />
            <div style={{ flex: 1 }}>
              <div style={{ height: 18, width: "62%", borderRadius: 9, background: t.muted, opacity: 0.55 }} />
              <Line t={t} w="90%" h={14} />
            </div>
          </div>
        ))}
      </div>
      <div
        style={{
          position: "absolute",
          right: 48,
          bottom: 60,
          opacity: badge,
          transform: `scale(${0.8 + badge * 0.2})`,
          ...t.chip,
          background: t.accent,
          color: "#fff",
          fontSize: 28,
          fontWeight: 800,
          padding: "12px 24px",
          borderRadius: 30,
          boxShadow: t.glow ? "0 0 30px rgba(255,144,20,0.6)" : "0 10px 24px rgba(240,124,0,0.3)",
        }}
      >
        0 lượt bấm
      </div>
    </Card>
  );
};

// Hai cột 15% và 8%, nhãn chênh lệch hiện sau.
const Compare: React.FC<{ t: Theme }> = ({ t }) => {
  const f = useCurrentFrame();
  const grow = interpolate(f, [8, 34], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const delta = useEnter(40);
  const cols = [
    { v: 15, label: "Không có tóm tắt AI", color: t.dark ? "#9FB3D6" : "#8FA3C4" },
    { v: 8, label: "Có tóm tắt AI", color: t.accent },
  ];
  return (
    <Card t={t}>
      <div style={{ display: "flex", justifyContent: "space-around", alignItems: "flex-end", height: 420, position: "relative" }}>
        {cols.map((c, i) => (
          <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ fontSize: 84, fontWeight: 800, color: c.color, marginBottom: 18, textShadow: t.glow && i ? "0 0 28px rgba(255,144,20,0.6)" : "none" }}>
              <CountUp value={`${c.v}%`} delay={8} duration={26} />
            </div>
            <div
              style={{
                width: 200,
                height: 290 * (c.v / 15) * grow,
                borderRadius: "20px 20px 6px 6px",
                background: c.color,
                boxShadow: t.glow && i ? "0 0 40px rgba(255,144,20,0.5)" : "none",
              }}
            />
          </div>
        ))}
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: 190,
            transform: `translateX(-50%) scale(${0.8 + delta * 0.2})`,
            opacity: delta,
            fontSize: 34,
            fontWeight: 800,
            color: t.accent,
            border: `2px solid ${t.accent}`,
            borderRadius: 40,
            padding: "8px 22px",
            background: t.dark ? "rgba(255,144,20,0.1)" : "#fff",
          }}
        >
          ↓ 47%
        </div>
      </div>
      <div style={{ height: 1.5, background: t.line, margin: "0 0 24px" }} />
      <div style={{ display: "flex", justifyContent: "space-around" }}>
        {cols.map((c, i) => (
          <div key={i} style={{ ...t.chip, fontSize: 26, fontWeight: 600, padding: "10px 22px", borderRadius: 30 }}>
            {c.label}
          </div>
        ))}
      </div>
    </Card>
  );
};

// 100 chấm, chỉ 1 chấm sáng: 1% lượt bấm.
const Dots: React.FC<{ t: Theme }> = ({ t }) => {
  const f = useCurrentFrame();
  const LIT = 44;
  const lit = useEnter(44);
  const pulse = 1 + Math.sin(f / 6) * 0.08 * lit;
  const label = useEnter(50);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: t.align === "left" ? "flex-start" : "center" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(10, 34px)", gap: 20 }}>
        {Array.from({ length: 100 }).map((_, i) => {
          const r = Math.floor(i / 10);
          const c = i % 10;
          const p = interpolate(f - (r + c) * 1.2, [0, 10], [0, 1], clamp);
          const on = i === LIT && lit > 0.05;
          return (
            <div
              key={i}
              style={{
                width: 34,
                height: 34,
                borderRadius: "50%",
                opacity: p,
                transform: `scale(${on ? 1.35 * pulse : 0.6 + p * 0.4})`,
                background: on ? t.accent : t.dim,
                boxShadow: on ? (t.glow ? "0 0 36px 10px rgba(255,144,20,0.6)" : `0 0 0 8px rgba(240,124,0,0.18)`) : "none",
              }}
            />
          );
        })}
      </div>
      <div style={{ marginTop: 44, opacity: label, transform: `translateY(${(1 - label) * 16}px)`, display: "flex", alignItems: "baseline", gap: 18 }}>
        <span style={{ fontSize: 76, fontWeight: 800, color: t.accent, textShadow: t.glow ? "0 0 28px rgba(255,144,20,0.55)" : "none" }}>1/100</span>
        <span style={{ fontSize: 30, color: t.muted }}>lượt bấm vào link trong tóm tắt AI</span>
      </div>
    </div>
  );
};

// ---------- Hướng Data Story: tiêu đề cố định + một biểu đồ thêm dần từng lớp ----------
const DataTitle: React.FC<{ t: Theme }> = ({ t }) => {
  const p = useEnter(0);
  return (
    <div style={{ position: "absolute", left: PAD, right: PAD, top: Y.head - 20, textAlign: "center", opacity: p }}>
      <div style={{ fontSize: 60, fontWeight: 800, color: t.text, letterSpacing: -1, lineHeight: 1.1 }}>GOOGLE CÓ TÓM TẮT AI</div>
      <div style={{ fontSize: 30, color: t.muted, marginTop: 14 }}>Tỷ lệ lượt tìm kiếm có bấm vào kết quả</div>
    </div>
  );
};

const Narrative: React.FC<{ t: Theme; s: DemoScene }> = ({ t, s }) => {
  const p = useEnter(0);
  const reveal = interpolate(useCurrentFrame(), [6, 20], [0, 100], clamp);
  return (
    <div style={{ position: "absolute", left: PAD, right: PAD, top: Y.head + 150, textAlign: "center", fontSize: 36, color: t.text, opacity: p }}>
      {s.narrative[0]}{" "}
      <span
        style={{
          background: t.accent,
          color: "#fff",
          fontWeight: 700,
          padding: "6px 16px",
          clipPath: `inset(0 ${100 - reveal}% 0 0)`,
          display: "inline-block",
        }}
      >
        {s.narrative[1]}
      </span>
    </div>
  );
};

const DataChart: React.FC<{ t: Theme; scenes: TimedScene[] }> = ({ t, scenes }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const BAR = 540;
  const rows = [
    { label: "Không có\ntóm tắt AI", v: 15, color: "#8FA3C4" },
    { label: "Có\ntóm tắt AI", v: 8, color: "#002D72" },
    { label: "Link trong\ntóm tắt AI", v: 1, color: t.accent },
  ];
  const step = (i: number, d = 8) => interpolate(f - scenes[i].from - d, [0, 24], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const note1 = step(1, 36);
  const note2 = step(2, 36);
  return (
    <div style={{ position: "absolute", left: PAD, right: PAD, top: Y.stage - 110 }}>
      <div style={{ position: "relative", marginLeft: 260, width: BAR + 120, height: 64, fontSize: 24, color: t.muted }}>
        {[0, 5, 10, 15].map((v) => (
          <span key={v} style={{ position: "absolute", left: (v / 15) * BAR, transform: "translateX(-50%)" }}>
            {v}%
          </span>
        ))}
      </div>
      <div style={{ position: "relative" }}>
        {[0, 5, 10, 15].map((v) => (
          <div key={v} style={{ position: "absolute", left: 260 + (v / 15) * BAR, top: 0, bottom: 0, width: 1.5, background: t.line, opacity: 0.5 }} />
        ))}
        {rows.map((r, i) => {
          const p = step(i);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", height: 150, opacity: Math.min(1, p * 3) }}>
              <div style={{ width: 240, paddingRight: 20, textAlign: "right", fontSize: 32, fontWeight: 700, color: t.text, whiteSpace: "pre-line", lineHeight: 1.2 }}>
                {r.label}
              </div>
              <div style={{ height: 84, width: Math.max(6, (r.v / 15) * BAR * p), background: r.color, borderRadius: "0 10px 10px 0" }} />
              <div style={{ marginLeft: 18, fontSize: 44, fontWeight: 800, color: i === 2 ? t.accent : t.text }}>
                {f >= scenes[i].from ? <CountUp value={`${r.v}%`} delay={scenes[i].from + 8} duration={24} /> : null}
              </div>
            </div>
          );
        })}
        <div
          style={{
            position: "absolute",
            right: 0,
            top: 190,
            opacity: note1,
            transform: `translateX(${(1 - note1) * 30}px)`,
            background: t.accent,
            color: "#fff",
            fontSize: 30,
            fontWeight: 800,
            padding: "8px 18px",
          }}
        >
          ↓ 47%
        </div>
      </div>
      <div
        style={{
          marginTop: 30,
          marginLeft: 260,
          opacity: note2,
          transform: `translateY(${(1 - note2) * 20}px)`,
          borderLeft: `5px solid ${t.accent}`,
          paddingLeft: 20,
          fontSize: 30,
          color: t.text,
          lineHeight: 1.35,
        }}
      >
        <b>Chỉ 1 trong 100</b> lượt tìm kiếm có người
        <br />
        bấm vào link nằm trong tóm tắt AI
      </div>
      <div style={{ marginTop: 34, fontSize: 22, color: t.muted, opacity: f / fps > 0.5 ? 1 : 0 }}>Nguồn: Pew Research Center, 2025</div>
    </div>
  );
};

// ---------- Ghép cảnh ----------
const Fade: React.FC<{ frames: number; children: React.ReactNode }> = ({ frames, children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [frames - 7, frames], [1, 0], clamp);
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const VISUAL = { search: SearchMock, compare: Compare, dots: Dots };

export const Preview: React.FC<{ theme: ThemeId }> = ({ theme }) => {
  useFonts();
  const t = THEMES[theme];
  const scenes = timeline(props);
  const data = t.id === "data";
  return (
    <AbsoluteFill style={{ fontFamily: FONT, color: t.text }}>
      <Background t={t} />
      <Header t={t} />
      {data && <DataTitle t={t} />}
      {data && <DataChart t={t} scenes={scenes} />}
      {DEMO.map((s, i) => {
        const V = VISUAL[s.visual];
        const last = i === DEMO.length - 1;
        return (
          <Sequence key={i} from={scenes[i].from} durationInFrames={scenes[i].frames}>
            <Fade frames={last ? scenes[i].frames + 10 : scenes[i].frames}>
              {data ? <Narrative t={t} s={s} /> : <Headline t={t} s={s} />}
              {!data && (
                <div
                  style={{
                    position: "absolute",
                    left: PAD,
                    right: PAD,
                    top: Y.stage,
                    height: Y.stageH,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: t.align === "left" ? "flex-start" : "center",
                  }}
                >
                  <V t={t} />
                </div>
              )}
            </Fade>
            <Caption t={t} words={scenes[i].words} />
          </Sequence>
        );
      })}
      <Footer t={t} />
    </AbsoluteFill>
  );
};
