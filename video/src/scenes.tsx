import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { CountUp, Highlight, Reveal, Source, useEnter } from "./components";
import { C, FONT, SAFE } from "./theme";
import type { Scene } from "./types";

type Of<T extends Scene["type"]> = Extract<Scene, { type: T }>;

// Khung nội dung chung: nằm giữa thanh logo và vùng phụ đề.
const Frame: React.FC<{ children: React.ReactNode; center?: boolean }> = ({ children, center }) => (
  <div
    style={{
      position: "absolute",
      left: SAFE.left,
      right: SAFE.right,
      top: SAFE.top,
      height: SAFE.captionTop - SAFE.top - 40,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: center ? "center" : "flex-start",
      textAlign: center ? "center" : "left",
      fontFamily: FONT,
      color: C.white,
    }}
  >
    {children}
  </div>
);

const Kicker: React.FC<{ text?: string; delay?: number }> = ({ text, delay = 0 }) =>
  text ? (
    <Reveal
      delay={delay}
      style={{ color: C.orange, fontWeight: 700, fontSize: 32, letterSpacing: 4, textTransform: "uppercase", marginBottom: 28 }}
    >
      {text}
    </Reveal>
  ) : null;

const Title: React.FC<{ text: string; delay?: number; size?: number }> = ({ text, delay = 0, size = 64 }) => (
  <Reveal delay={delay} style={{ fontWeight: 800, fontSize: size, lineHeight: 1.15, marginBottom: 48 }}>
    {text}
  </Reveal>
);

// Mở đầu: từng chữ bật lên lần lượt để giữ mắt người xem trong 2 giây đầu.
const Hook: React.FC<{ s: Of<"hook"> }> = ({ s }) => {
  const words = s.title.split(" ");
  const hl = new Set(s.highlight?.split(" "));
  return (
    <Frame>
      <Kicker text={s.kicker} />
      <div style={{ fontWeight: 800, fontSize: 112, lineHeight: 1.1 }}>
        {words.map((w, i) => (
          <Word key={i} delay={4 + i * 3} color={hl.has(w) ? C.orange : C.white}>
            {w}
          </Word>
        ))}
      </div>
    </Frame>
  );
};

const Word: React.FC<{ delay: number; color: string; children: React.ReactNode }> = ({ delay, color, children }) => {
  const p = useEnter(delay);
  return (
    <span
      style={{
        display: "inline-block",
        marginRight: 22,
        color,
        opacity: p,
        transform: `translateY(${(1 - p) * 30}px) scale(${0.9 + p * 0.1})`,
      }}
    >
      {children}
    </span>
  );
};

const Stat: React.FC<{ s: Of<"stat"> }> = ({ s }) => (
  <Frame>
    <Reveal style={{ fontWeight: 800, fontSize: 210, lineHeight: 1, color: C.orange, letterSpacing: -4 }}>
      <CountUp value={s.value} />
    </Reveal>
    <i style={{ display: "block", width: 120, height: 8, borderRadius: 4, background: C.white, margin: "40px 0" }} />
    <Reveal delay={8} style={{ fontWeight: 600, fontSize: 56, lineHeight: 1.25 }}>
      {s.label}
    </Reveal>
    <Source text={s.source} />
  </Frame>
);

// So sánh hai con số bằng hai cột cao thấp.
const Compare: React.FC<{ s: Of<"compare"> }> = ({ s }) => {
  const frame = useCurrentFrame();
  const num = (v: string) => parseFloat(v.replace(/[^\d.]/g, "")) || 0;
  const max = Math.max(num(s.left.value), num(s.right.value));
  const grow = interpolate(frame, [6, 36], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const col = (side: { value: string; label: string }, color: string, delay: number) => (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-end" }}>
      <div style={{ fontWeight: 800, fontSize: 96, color, marginBottom: 20 }}>
        <CountUp value={side.value} delay={6} />
      </div>
      <div
        style={{
          width: "70%",
          height: 480 * (num(side.value) / max) * grow,
          background: color,
          borderRadius: "18px 18px 0 0",
        }}
      />
      <Reveal delay={delay} style={{ fontWeight: 600, fontSize: 38, marginTop: 24, textAlign: "center", lineHeight: 1.3 }}>
        {side.label}
      </Reveal>
    </div>
  );
  return (
    <Frame>
      {s.title && <Title text={s.title} />}
      <div style={{ display: "flex", width: "100%", gap: 40, alignItems: "flex-end" }}>
        {col(s.left, C.line, 10)}
        {col(s.right, C.orange, 14)}
      </div>
      <Source text={s.source} />
    </Frame>
  );
};

// Biểu đồ thanh ngang, thanh đầu tiên tô cam.
const Bars: React.FC<{ s: Of<"bars"> }> = ({ s }) => {
  const frame = useCurrentFrame();
  const max = Math.max(...s.items.map((it) => it.value));
  return (
    <Frame>
      <Title text={s.title} />
      {s.items.map((it, i) => {
        const delay = 10 + i * 12;
        const grow = interpolate(frame, [delay, delay + 24], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const color = i === 0 ? C.orange : C.line;
        return (
          <div key={i} style={{ width: "100%", marginBottom: 44 }}>
            <Reveal delay={delay} style={{ fontSize: 38, fontWeight: 600, marginBottom: 14 }}>
              {it.label}
            </Reveal>
            <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
              <div style={{ height: 64, width: `${(it.value / max) * 72 * grow}%`, background: color, borderRadius: 12 }} />
              <div style={{ fontSize: 52, fontWeight: 800, color, opacity: grow }}>
                <CountUp value={it.display ?? String(it.value)} delay={delay} duration={24} />
              </div>
            </div>
          </div>
        );
      })}
      <Source text={s.source} />
    </Frame>
  );
};

// Danh sách: từng ý hiện lần lượt, rải đều theo thời lượng cảnh.
const List: React.FC<{ s: Of<"list">; frames: number }> = ({ s, frames }) => {
  const step = (frames * 0.75) / s.items.length;
  return (
    <Frame>
      <Title text={s.title} />
      {s.items.map((it, i) => (
        <Reveal key={i} delay={8 + i * step} style={{ display: "flex", gap: 28, alignItems: "flex-start", marginBottom: 38 }}>
          <div
            style={{
              flex: "none",
              width: 76,
              height: 76,
              borderRadius: "50%",
              background: C.orange,
              color: C.navy,
              fontWeight: 800,
              fontSize: 40,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {i + 1}
          </div>
          <div style={{ fontSize: 46, fontWeight: 600, lineHeight: 1.3, paddingTop: 8 }}>{it}</div>
        </Reveal>
      ))}
    </Frame>
  );
};

const Statement: React.FC<{ s: Of<"statement"> }> = ({ s }) => (
  <Frame>
    <i style={{ display: "block", width: 120, height: 8, borderRadius: 4, background: C.orange, marginBottom: 48 }} />
    <Reveal style={{ fontWeight: 800, fontSize: 80, lineHeight: 1.2 }}>
      <Highlight text={s.text} highlight={s.highlight} />
    </Reveal>
  </Frame>
);

const Cta: React.FC<{ s: Of<"cta"> }> = ({ s }) => {
  const p = useEnter(0);
  return (
    <Frame center>
      <Img src={staticFile("logo-white.png")} style={{ height: 200, opacity: p, transform: `scale(${0.8 + p * 0.2})` }} />
      <Reveal delay={6} style={{ fontWeight: 800, fontSize: 70, lineHeight: 1.2, margin: "64px 0 40px" }}>
        {s.title}
      </Reveal>
      <Reveal
        delay={12}
        style={{
          background: C.orange,
          color: C.navy,
          fontWeight: 800,
          fontSize: 46,
          padding: "26px 48px",
          borderRadius: 60,
        }}
      >
        {s.action}
      </Reveal>
      <Reveal delay={18} style={{ marginTop: 44, fontSize: 36, color: C.muted, letterSpacing: 2 }}>
        adtek.agency
      </Reveal>
    </Frame>
  );
};

export const SceneView: React.FC<{ scene: Scene; frames: number }> = ({ scene, frames }) => {
  switch (scene.type) {
    case "hook":
      return <Hook s={scene} />;
    case "stat":
      return <Stat s={scene} />;
    case "compare":
      return <Compare s={scene} />;
    case "bars":
      return <Bars s={scene} />;
    case "list":
      return <List s={scene} frames={frames} />;
    case "statement":
      return <Statement s={scene} />;
    case "cta":
      return <Cta s={scene} />;
  }
};
