import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { Tone } from "../types";
import { SANS, clamp, ease } from "./frame";
import { W, count } from "./charts";

// Các biểu đồ chọn theo kiểu dữ liệu, mỗi loại một hiệu ứng riêng để video không lặp lại.
// Vẫn giữ chuẩn trình bày: màu phẳng, số ghi thẳng trên dữ liệu, một điểm nhấn cam, nguồn ở cuối.
const INK = { text: "#FFFFFF", soft: "#C9D5EA", source: "#8FA3C4", rule: "rgba(255,255,255,0.55)", cell: "rgba(255,255,255,0.14)" };
const TONE: Record<Tone, string> = { base: "#5E7DB3", main: "#D6E2F5", accent: "#FF9014" };

const prog = (f: number, at: number, len = 20) => interpolate(f - at, [0, len], [0, 1], { ...clamp, easing: ease });

const Source: React.FC<{ text: string; at: number }> = ({ text, at }) => {
  const f = useCurrentFrame();
  return <div style={{ marginTop: 28, fontSize: 19, color: INK.source, opacity: prog(f, at, 12) }}>{text}</div>;
};
const Metric: React.FC<{ metric: string; unit?: string }> = ({ metric, unit }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ fontSize: 30, lineHeight: 1.3, opacity: prog(f, 0, 12) }}>
      <b style={{ fontWeight: 700 }}>{metric}</b>
      {unit ? <span style={{ fontWeight: 400 }}>, {unit}</span> : null}
    </div>
  );
};
const Frame: React.FC<{ children: React.ReactNode }> = ({ children }) => <div style={{ width: W, color: INK.text, fontFamily: SANS }}>{children}</div>;

// ---------- Số lớn: một con số gây sốc, đếm từ 0 ----------
export const BigNumber: React.FC<{ value: number; display?: string; prefix?: string; suffix?: string; label: string; context?: string; source: string }> = ({
  value, display, prefix, suffix, label, context, source,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = prog(f, 4, 34);
  const pop = spring({ frame: f - 36, fps, config: { damping: 12, stiffness: 160 }, durationInFrames: 20 });
  return (
    <Frame>
      <div style={{ display: "flex", alignItems: "baseline", gap: 14, marginTop: 30, transform: `scale(${1 + 0.04 * pop * (1 - pop) * 4})`, transformOrigin: "left bottom" }}>
        {prefix && <span style={{ fontSize: 80, fontWeight: 700, color: TONE.accent }}>{prefix}</span>}
        <span style={{ fontSize: 210, lineHeight: 0.95, fontWeight: 700, color: TONE.accent, fontVariantNumeric: "tabular-nums", letterSpacing: -4 }}>{count(value, p, display)}</span>
        {suffix && <span style={{ fontSize: 76, fontWeight: 700, color: TONE.accent }}>{suffix}</span>}
      </div>
      <div style={{ marginTop: 18, height: 4, width: 520 * prog(f, 30, 16), background: TONE.accent }} />
      <div style={{ marginTop: 28, fontSize: 40, lineHeight: 1.3, fontWeight: 600, opacity: prog(f, 24, 12) }}>{label}</div>
      {context && <div style={{ marginTop: 14, fontSize: 30, lineHeight: 1.35, color: INK.soft, opacity: prog(f, 40, 12) }}>{context}</div>}
      <Source text={source} at={44} />
    </Frame>
  );
};

// ---------- Đối đầu: hai con số so sánh trực tiếp ----------
type VsItem = { label: string; value: number; display?: string; suffix?: string };
export const Versus: React.FC<{ metric: string; unit?: string; source: string; items: [VsItem, VsItem]; winner: 0 | 1; note?: string }> = ({
  metric, unit, source, items, winner, note,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = prog(f, 8, 30);
  const win = spring({ frame: f - 40, fps, config: { damping: 14 }, durationInFrames: 22 });
  return (
    <Frame>
      <Metric metric={metric} unit={unit} />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 2px 1fr", gap: 40, marginTop: 50, alignItems: "end" }}>
        {[0, 1].map((i) => {
          const it = items[i];
          const w = i === winner;
          const slide = interpolate(prog(f, 6 + i * 6, 18), [0, 1], [i ? 60 : -60, 0]);
          return (
            <React.Fragment key={i}>
              {i === 1 && <div style={{ background: INK.rule, height: 260 * prog(f, 4, 16), alignSelf: "center" }} />}
              <div style={{ textAlign: i ? "left" : "right", transform: `translateX(${slide}px)`, opacity: prog(f, 6 + i * 6, 12) }}>
                <div
                  style={{
                    fontSize: 128,
                    lineHeight: 1,
                    fontWeight: 700,
                    color: w ? TONE.accent : TONE.main,
                    fontVariantNumeric: "tabular-nums",
                    transform: `scale(${w ? 1 + 0.12 * win : 1 - 0.08 * win})`,
                    transformOrigin: i ? "left bottom" : "right bottom",
                    opacity: w ? 1 : 1 - 0.35 * win,
                  }}
                >
                  {count(it.value, p, it.display)}
                  {it.suffix && <span style={{ fontSize: 60 }}>{it.suffix}</span>}
                </div>
                <div style={{ marginTop: 20, fontSize: 28, lineHeight: 1.3, color: INK.soft }}>{it.label}</div>
              </div>
            </React.Fragment>
          );
        })}
      </div>
      {note && (
        <div style={{ marginTop: 46, fontSize: 32, fontWeight: 700, color: INK.text, opacity: prog(f, 48, 12), borderLeft: `3px solid ${TONE.accent}`, paddingLeft: 18 }}>{note}</div>
      )}
      <Source text={source} at={20} />
    </Frame>
  );
};

// ---------- Đường dốc: trước và sau của 1 đến 3 nhóm ----------
type SlopeSeries = { label: string; a: number; b: number; display?: [string, string]; tone: Tone };
export const Slope: React.FC<{ metric: string; unit?: string; source: string; from: string; to: string; series: SlopeSeries[] }> = ({
  metric, unit, source, from, to, series,
}) => {
  const f = useCurrentFrame();
  const H = 380;
  const X0 = 230;
  const X1 = 620;
  const vals = series.flatMap((s) => [s.a, s.b]);
  const lo = Math.min(...vals);
  const hi = Math.max(...vals);
  const pad = (hi - lo || hi || 1) * 0.12;
  const y = (v: number) => H - ((v - (lo - pad)) / (hi + pad - (lo - pad))) * H;
  // Đẩy nhãn hai đầu ra xa nhau nếu quá gần.
  const spread = (ys: number[]) => {
    const idx = ys.map((v, i) => [v, i]).sort((p, q) => p[0] - q[0]);
    for (let k = 1; k < idx.length; k++) if (idx[k][0] - idx[k - 1][0] < 52) idx[k][0] = idx[k - 1][0] + 52;
    const out = [...ys];
    idx.forEach(([v, i]) => (out[i] = v));
    return out;
  };
  const la = spread(series.map((s) => y(s.a)));
  const lb = spread(series.map((s) => y(s.b)));
  return (
    <Frame>
      <Metric metric={metric} unit={unit} />
      <div style={{ position: "relative", width: W, height: H + 70, marginTop: 40 }}>
        {[X0, X1].map((x, k) => (
          <React.Fragment key={k}>
            <div style={{ position: "absolute", left: x - 1, top: -10, width: 2, height: (H + 20) * prog(f, 2, 14), background: INK.rule }} />
            <div style={{ position: "absolute", left: x - 120, width: 240, top: H + 26, textAlign: "center", fontSize: 26, color: INK.soft, opacity: prog(f, 4, 10) }}>{k ? to : from}</div>
          </React.Fragment>
        ))}
        <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          {series.map((s, i) => {
            const at = 12 + i * 10;
            const d = prog(f, at, 26);
            const x2 = X0 + (X1 - X0) * d;
            const y2 = y(s.a) + (y(s.b) - y(s.a)) * d;
            const color = TONE[s.tone];
            return (
              <g key={i}>
                <line x1={X0} y1={y(s.a)} x2={x2} y2={y2} stroke={color} strokeWidth={s.tone === "accent" ? 7 : 5} strokeLinecap="round" opacity={d > 0 ? 1 : 0} />
                <circle cx={X0} cy={y(s.a)} r={11 * prog(f, at - 4, 8)} fill={color} />
                <circle cx={X1} cy={y(s.b)} r={13 * prog(f, at + 24, 8)} fill={color} />
              </g>
            );
          })}
        </svg>
        {series.map((s, i) => {
          const at = 12 + i * 10;
          const accent = s.tone === "accent";
          const style = { position: "absolute" as const, fontSize: 34, fontWeight: accent ? 700 : 400, color: accent ? TONE.accent : INK.text };
          return (
            <React.Fragment key={i}>
              <div style={{ ...style, left: 0, width: X0 - 30, top: la[i] - 24, textAlign: "right", opacity: prog(f, at, 10) }}>{s.display?.[0] ?? s.a.toLocaleString("en-US")}</div>
              <div style={{ ...style, left: X1 + 30, width: W - X1 - 30, top: lb[i] - 24, opacity: prog(f, at + 26, 10) }}>
                {count(s.b, prog(f, at + 6, 22), s.display?.[1])} <span style={{ fontSize: 26, fontWeight: 600, color: accent ? TONE.accent : INK.soft }}>{s.label}</span>
              </div>
            </React.Fragment>
          );
        })}
      </div>
      <Source text={source} at={20} />
    </Frame>
  );
};

// ---------- Đường xu hướng: 3 điểm thời gian trở lên ----------
type Pt = { label: string; value: number; display?: string };
export const Trend: React.FC<{ metric: string; unit?: string; source: string; points: Pt[]; min?: number; note?: string }> = ({ metric, unit, source, points, min = 0, note }) => {
  const f = useCurrentFrame();
  const H = 340;
  const PADX = 60;
  const hi = Math.max(...points.map((p) => p.value));
  const x = (i: number) => PADX + (i * (W - 2 * PADX)) / (points.length - 1);
  const y = (v: number) => H - ((v - min) / (hi - min)) * (H - 40);
  const draw = prog(f, 10, 40);
  const pts = points.map((p, i) => [x(i), y(p.value)] as const);
  const path = pts.map((p, i) => `${i ? "L" : "M"}${p[0]},${p[1]}`).join(" ");
  const total = pts.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);
  const last = points.length - 1;
  return (
    <Frame>
      <Metric metric={metric} unit={unit} />
      <div style={{ position: "relative", width: W, height: H + 70, marginTop: 60 }}>
        <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          <defs>
            <linearGradient id="trendFill" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stopColor={TONE.accent} stopOpacity={0.35} />
              <stop offset="1" stopColor={TONE.accent} stopOpacity={0} />
            </linearGradient>
            <clipPath id="trendClip">
              <rect x={0} y={-40} width={PADX + (W - 2 * PADX) * draw + 2} height={H + 80} />
            </clipPath>
          </defs>
          <line x1={0} x2={W} y1={H} y2={H} stroke={INK.rule} strokeWidth={1.5} />
          <path d={`${path} L${pts[last][0]},${H} L${pts[0][0]},${H} Z`} fill="url(#trendFill)" clipPath="url(#trendClip)" opacity={prog(f, 20, 30)} />
          <path d={path} fill="none" stroke={TONE.accent} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={total} strokeDashoffset={total * (1 - draw)} />
          {pts.map((p, i) => {
            const t = 10 + (40 * i) / last;
            return <circle key={i} cx={p[0]} cy={p[1]} r={(i === last ? 14 : 9) * prog(f, t, 8)} fill={i === last ? TONE.accent : INK.text} />;
          })}
        </svg>
        {points.map((p, i) => {
          const t = 10 + (40 * i) / last;
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: x(i) - 110, width: 220, top: y(p.value) - 62, textAlign: "center", fontSize: i === last ? 40 : 30, fontWeight: i === last ? 700 : 400, color: i === last ? TONE.accent : INK.text, opacity: prog(f, t + 4, 10) }}>
                {p.display ?? p.value.toLocaleString("en-US")}
              </div>
              <div style={{ position: "absolute", left: x(i) - 110, width: 220, top: H + 20, textAlign: "center", fontSize: 25, color: INK.soft, opacity: prog(f, 6, 10) }}>{p.label}</div>
            </React.Fragment>
          );
        })}
      </div>
      {note && <div style={{ marginTop: 10, fontSize: 30, fontWeight: 700, opacity: prog(f, 54, 12), borderLeft: `3px solid ${TONE.accent}`, paddingLeft: 18 }}>{note}</div>}
      <Source text={source} at={20} />
    </Frame>
  );
};

// ---------- Vòng tròn: các phần trong một tổng ----------
type Part = { label: string; value: number; display?: string; tone: Tone };
export const Donut: React.FC<{ metric: string; unit?: string; source: string; parts: Part[]; center?: string; centerLabel?: string }> = ({
  metric, unit, source, parts, center, centerLabel,
}) => {
  const f = useCurrentFrame();
  const R = 160;
  const SW = 64;
  const Cc = 2 * Math.PI * R;
  const total = parts.reduce((s, p) => s + p.value, 0);
  let acc = 0;
  return (
    <Frame>
      <Metric metric={metric} unit={unit} />
      <div style={{ display: "flex", alignItems: "center", gap: 56, marginTop: 44 }}>
        <div style={{ position: "relative", width: (R + SW / 2) * 2, height: (R + SW / 2) * 2, flex: "none" }}>
          <svg width={(R + SW / 2) * 2} height={(R + SW / 2) * 2} style={{ transform: "rotate(-90deg)" }}>
            <circle cx={R + SW / 2} cy={R + SW / 2} r={R} fill="none" stroke={INK.cell} strokeWidth={SW} />
            {parts.map((p, i) => {
              const len = (p.value / total) * Cc;
              const off = acc;
              acc += len;
              const g = prog(f, 8 + i * 14, 22);
              return (
                <circle key={i} cx={R + SW / 2} cy={R + SW / 2} r={R} fill="none" stroke={TONE[p.tone]} strokeWidth={SW}
                  strokeDasharray={`${Math.max(0, len * g - 3)} ${Cc}`} strokeDashoffset={-off} />
              );
            })}
          </svg>
          {center && (
            <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", textAlign: "center", opacity: prog(f, 30, 12) }}>
              <div>
                <div style={{ fontSize: 64, fontWeight: 700, color: TONE.accent, lineHeight: 1 }}>{center}</div>
                {centerLabel && <div style={{ fontSize: 24, color: INK.soft, marginTop: 8, maxWidth: 200 }}>{centerLabel}</div>}
              </div>
            </div>
          )}
        </div>
        <div style={{ display: "grid", gap: 26 }}>
          {parts.map((p, i) => (
            <div key={i} style={{ display: "flex", gap: 16, alignItems: "baseline", opacity: prog(f, 12 + i * 14, 10) }}>
              <div style={{ width: 22, height: 22, flex: "none", background: TONE[p.tone], transform: "translateY(2px)" }} />
              <div>
                <div style={{ fontSize: 40, fontWeight: 700, color: p.tone === "accent" ? TONE.accent : INK.text, lineHeight: 1.1 }}>
                  {count(p.value, prog(f, 8 + i * 14, 22), p.display)}
                </div>
                <div style={{ fontSize: 26, color: INK.soft, lineHeight: 1.3 }}>{p.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <Source text={source} at={20} />
    </Frame>
  );
};

// ---------- Hình người: x trên 10 người ----------
const Person: React.FC<{ color: string; size: number }> = ({ color, size }) => (
  <svg width={size} height={size * 1.6} viewBox="0 0 40 64">
    <circle cx={20} cy={11} r={10} fill={color} />
    <path d="M4 62 V36 a16 16 0 0 1 32 0 V62 Z" fill={color} />
  </svg>
);
export const People: React.FC<{ metric: string; unit?: string; source: string; lit: number; legend: [string, string] }> = ({ metric, unit, source, lit, legend }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Frame>
      <Metric metric={metric} unit={unit} />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "26px 34px", marginTop: 46, width: 600 }}>
        {Array.from({ length: 10 }).map((_, i) => {
          const s = spring({ frame: f - 4 - i * 2, fps, config: { damping: 14 }, durationInFrames: 16 });
          const on = i < lit && f > 30 + i * 4;
          return (
            <div key={i} style={{ transform: `scale(${s})`, transformOrigin: "center bottom" }}>
              <Person color={on ? TONE.accent : INK.cell} size={72} />
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 40, display: "grid", gap: 14, fontSize: 30 }}>
        <div style={{ display: "flex", gap: 14, alignItems: "baseline", opacity: prog(f, 30 + lit * 4, 10) }}>
          <b style={{ color: TONE.accent, fontSize: 44 }}>{lit}/10</b>
          <span style={{ fontWeight: 600 }}>{legend[0]}</span>
        </div>
        <div style={{ color: INK.soft, opacity: prog(f, 36 + lit * 4, 10) }}>{legend[1]}</div>
      </div>
      <Source text={source} at={20} />
    </Frame>
  );
};

// ---------- Phễu: rơi rụng qua từng bước ----------
type Stage = { label: string; value: number; display?: string };
export const Funnel: React.FC<{ metric: string; unit?: string; source: string; stages: Stage[] }> = ({ metric, unit, source, stages }) => {
  const f = useCurrentFrame();
  const top = stages[0].value;
  const ROW = Math.min(104, 440 / stages.length);
  const LABEL = 270;
  const AREA = W - LABEL - 20;
  const last = stages.length - 1;
  return (
    <Frame>
      <Metric metric={metric} unit={unit} />
      <div style={{ marginTop: 40, display: "grid", gap: 12 }}>
        {stages.map((s, i) => {
          const at = 6 + i * 12;
          const g = prog(f, at, 18);
          const w = Math.max(6, (s.value / top) * AREA); // đúng tỷ lệ, không làm tròn lên cho vừa chữ
          const inside = w >= 130;
          const accent = i === last;
          const fill = accent ? TONE.accent : i === 0 ? TONE.base : TONE.main;
          const ink = i === 0 && !accent ? INK.text : "#00225A";
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", height: ROW, opacity: g, transform: `translateY(${(1 - g) * -30}px)` }}>
              <div style={{ width: LABEL, flex: "none", paddingRight: 20, textAlign: "right", fontSize: 26, lineHeight: 1.25, color: INK.soft }}>{s.label}</div>
              <div style={{ position: "relative", width: AREA, height: ROW, flex: "none" }}>
                <div style={{ position: "absolute", left: (AREA - w) / 2, width: w, height: ROW, background: fill, display: "grid", placeItems: "center" }}>
                  {inside && <span style={{ fontSize: accent ? 44 : 34, fontWeight: 700, color: ink }}>{count(s.value, prog(f, at, 22), s.display)}</span>}
                </div>
                {!inside && (
                  <div style={{ position: "absolute", left: (AREA + w) / 2 + 16, top: 0, height: ROW, display: "flex", alignItems: "center", fontSize: accent ? 44 : 34, fontWeight: 700, color: accent ? TONE.accent : INK.text }}>
                    {count(s.value, prog(f, at, 22), s.display)}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
      <Source text={source} at={20} />
    </Frame>
  );
};
