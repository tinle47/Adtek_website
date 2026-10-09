import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Background, C, L, Logo, SANS, SERIF, clamp, ease, useFonts } from "./frame";

const prog = (f: number, at: number, len: number) => interpolate(f - at, [0, len], [0, 1], { ...clamp, easing: ease });
export const QUIZ_REVEAL_AT = 20; // khung lật đáp án, dùng chung cho âm thanh
export const MYTH_STAMP_AT = 26; // khung đóng dấu

// ---------- Đố số liệu: hỏi ở đầu video, lật đáp án ở gần cuối ----------
type Option = { label: string; text: string };
export const Quiz: React.FC<{ options: Option[]; answer: number; reveal?: boolean; tag?: string; note?: string; source?: string }> = ({
  options, answer, reveal, tag, note, source,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const flip = reveal ? spring({ frame: f - QUIZ_REVEAL_AT, fps, config: { damping: 12 }, durationInFrames: 20 }) : 0;
  const pulse = 1 + 0.03 * Math.max(0, Math.sin(Math.max(0, f - 30) / 5));
  return (
    <div style={{ width: 900, fontFamily: SANS, color: C.white }}>
      <div style={{ display: "flex", gap: 24 }}>
        {options.map((o, i) => {
          const enter = reveal ? 1 : prog(f, 4 + i * 8, 12);
          const right = i === answer;
          const lit = right ? flip : 0;
          return (
            <div
              key={i}
              style={{
                flex: 1,
                height: 250,
                borderRadius: 18,
                border: `3px solid ${lit > 0.5 ? C.orange : "rgba(255,255,255,0.35)"}`,
                background: lit > 0.5 ? C.orange : "rgba(255,255,255,0.06)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 14,
                opacity: enter * (reveal && !right ? 1 - 0.65 * flip : 1),
                transform: `translateY(${(1 - enter) * 30}px) scale(${1 + 0.08 * lit})`,
              }}
            >
              <div
                style={{
                  width: 64,
                  height: 64,
                  borderRadius: 32,
                  border: `3px solid ${lit > 0.5 ? C.navyDeep : C.orange}`,
                  color: lit > 0.5 ? C.navyDeep : C.orange,
                  fontSize: 34,
                  fontWeight: 700,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {lit > 0.5 ? "✓" : o.label}
              </div>
              <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 62, color: lit > 0.5 ? C.navyDeep : C.white }}>{o.text}</div>
            </div>
          );
        })}
      </div>
      {!reveal && tag && (
        <div style={{ marginTop: 40, display: "flex", justifyContent: "center", opacity: prog(f, 26, 10) }}>
          <div style={{ padding: "16px 34px", borderRadius: 40, background: C.white, color: C.navyDeep, fontSize: 32, fontWeight: 700, transform: `scale(${pulse})` }}>{tag}</div>
        </div>
      )}
      {reveal && note && (
        <div style={{ marginTop: 38, fontSize: 34, fontWeight: 700, borderLeft: `3px solid ${C.orange}`, paddingLeft: 18, opacity: prog(f, QUIZ_REVEAL_AT + 12, 12) }}>{note}</div>
      )}
      {source && <div style={{ marginTop: 22, fontSize: 19, color: C.muted, opacity: prog(f, 10, 12) }}>{source}</div>}
    </div>
  );
};

// ---------- Phá hiểu lầm: câu nhiều người tin, đóng dấu "SAI" ----------
export const Myth: React.FC<{ claim: string; verdict: string; note?: string; source?: string }> = ({ claim, verdict, note, source }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const card = prog(f, 0, 14);
  const stamp = spring({ frame: f - MYTH_STAMP_AT, fps, config: { damping: 11, stiffness: 180 }, durationInFrames: 16 });
  return (
    <div style={{ width: 900, fontFamily: SANS, color: C.white }}>
      <div style={{ position: "relative", padding: "46px 48px", borderRadius: 18, border: "2px solid rgba(255,255,255,0.3)", background: "rgba(255,255,255,0.05)", opacity: card }}>
        <div style={{ fontFamily: SERIF, fontSize: 120, lineHeight: 0.6, color: C.orange, height: 50 }}>“</div>
        <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 52, lineHeight: 1.25, opacity: 1 - 0.45 * stamp }}>{claim}</div>
        <div
          style={{
            position: "absolute",
            right: 40,
            bottom: -34,
            padding: "10px 34px",
            border: `6px solid ${C.orange}`,
            borderRadius: 12,
            color: C.orange,
            background: C.navyDeep,
            fontSize: 64,
            fontWeight: 800,
            letterSpacing: 4,
            opacity: stamp > 0.02 ? 1 : 0,
            transform: `rotate(-8deg) scale(${interpolate(stamp, [0, 1], [2.4, 1])})`,
          }}
        >
          {verdict}
        </div>
      </div>
      {note && <div style={{ marginTop: 70, fontSize: 34, fontWeight: 700, borderLeft: `3px solid ${C.orange}`, paddingLeft: 18, opacity: prog(f, MYTH_STAMP_AT + 18, 12) }}>{note}</div>}
      {source && <div style={{ marginTop: 22, fontSize: 19, color: C.muted, opacity: prog(f, MYTH_STAMP_AT + 18, 12) }}>{source}</div>}
    </div>
  );
};

// ---------- Ảnh bìa: 3 đến 5 chữ thật to để kênh nhìn rõ từng video ----------
// Video đố số liệu: ảnh bìa chỉ đặt câu hỏi và hiện các lựa chọn, không bao giờ lộ đáp án.
export const Cover: React.FC<{ title: string; accent: string; kicker?: string; options?: string[] }> = ({ title, accent, kicker, options }) => {
  useFonts();
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <Background />
      <Logo />
      <div style={{ position: "absolute", left: L.pad, right: L.pad, top: 520 }}>
        {kicker && <div style={{ fontFamily: SANS, fontSize: 30, fontWeight: 700, letterSpacing: 4, textTransform: "uppercase", color: C.muted, marginBottom: 34 }}>{kicker}</div>}
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 132, lineHeight: 1.05, color: C.white, letterSpacing: -1 }}>{title}</div>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 132, lineHeight: 1.05, color: C.orange, letterSpacing: -1, marginTop: 10 }}>{accent}</div>
        {options && (
          <div style={{ display: "flex", gap: 24, marginTop: 70 }}>
            {options.map((o, i) => (
              <div key={i} style={{ flex: 1, height: 190, borderRadius: 18, border: "3px solid rgba(255,255,255,0.45)", background: "rgba(255,255,255,0.06)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 10 }}>
                <div style={{ fontFamily: SANS, fontSize: 34, fontWeight: 700, color: C.orange }}>{String.fromCharCode(65 + i)}</div>
                <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 64, color: C.white }}>{o}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
