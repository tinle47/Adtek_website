import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import type { Tone } from "../types";
import { SANS, clamp, ease } from "./frame";

// Biểu đồ theo chuẩn trình bày của McKinsey, vẽ trên nền navy: màu phẳng, cột vuông, không lưới, không bóng,
// số ghi thẳng trên dữ liệu, chú thích bằng đường kẻ mảnh và chữ đậm nhỏ, chỉ một điểm nhấn màu cam.
const INK = {
  text: "#FFFFFF",
  soft: "#C9D5EA",
  source: "#8FA3C4",
  rule: "rgba(255,255,255,0.55)",
  cell: "rgba(255,255,255,0.14)",
};
const TONE: Record<Tone, string> = { base: "#5E7DB3", main: "#D6E2F5", accent: "#FF9014" };
export const W = 900; // bề ngang vùng biểu đồ

const prog = (f: number, at: number, len = 20) => interpolate(f - at, [0, len], [0, 1], { ...clamp, easing: ease });
// Số đếm tăng dần theo tiến độ p (0 đến 1), giữ đúng số chữ số thập phân của giá trị cuối.
export const count = (v: number, p: number, display?: string) => {
  if (display && p >= 0.999) return display;
  const d = (String(v).split(".")[1] ?? "").length;
  return (v * p).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
};

// Tên chỉ số in đậm + đơn vị in thường, biểu đồ, dòng nguồn.
export const Exhibit: React.FC<{ metric: string; unit: string; source: string; appear: number; children: React.ReactNode }> = ({
  metric,
  unit,
  source,
  appear,
  children,
}) => {
  const f = useCurrentFrame();
  return (
    <div style={{ width: W, opacity: prog(f, appear, 12), color: INK.text, fontFamily: SANS }}>
      <div style={{ fontSize: 30, lineHeight: 1.3 }}>
        <b style={{ fontWeight: 700 }}>{metric}</b>, <span style={{ fontWeight: 400 }}>{unit}</span>
      </div>
      <div style={{ marginTop: 36 }}>{children}</div>
      <div style={{ marginTop: 28, fontSize: 19, color: INK.source }}>{source}</div>
    </div>
  );
};

// Đường kẻ mảnh vẽ dần, có thể có mũi tên ở cuối.
const Line: React.FC<{ at: number; points: [number, number][]; arrow?: boolean }> = ({ at, points, arrow }) => {
  const f = useCurrentFrame();
  const draw = prog(f, at, 16);
  const len = points.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - points[i][0], p[1] - points[i][1]), 0);
  const end = points[points.length - 1];
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width="1" height="1">
      <polyline points={points.map((p) => p.join(",")).join(" ")} fill="none" stroke={INK.text} strokeWidth={2} strokeDasharray={len} strokeDashoffset={len * (1 - draw)} />
      {arrow && draw > 0.98 && <polygon points={`${end[0] - 7},${end[1] - 12} ${end[0] + 7},${end[1] - 12} ${end[0]},${end[1]}`} fill={INK.text} />}
    </svg>
  );
};

const NoteText: React.FC<{ at: number; style: React.CSSProperties; children: React.ReactNode }> = ({ at, style, children }) => {
  const f = useCurrentFrame();
  return <div style={{ position: "absolute", fontSize: 25, lineHeight: 1.3, fontWeight: 700, color: INK.text, opacity: prog(f, at + 10, 10), ...style }}>{children}</div>;
};

// ---------- Biểu đồ cột ----------
export type TimedCol = { label: string; value: number; display?: string; tone: Tone; at: number };
export type TimedNote =
  | { kind: "drop"; from: number; to: number; text: string; at: number }
  | { kind: "callout"; at: number; target: number; text: string };

export const ColumnChart: React.FC<{ cols: TimedCol[]; max: number; notes: TimedNote[] }> = ({ cols, max, notes }) => {
  const f = useCurrentFrame();
  const H = 300;
  const slot = W / cols.length;
  const BW = Math.min(150, slot * 0.5);
  const mid = (i: number) => slot * i + slot / 2;
  const top = (i: number) => H - (cols[i].value / max) * H;
  return (
    <div style={{ position: "relative", width: W, height: H + 110, marginTop: 60 }}>
      {cols.map((c, i) => {
        const g = prog(f, c.at, 22);
        const h = (c.value / max) * H * g;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: mid(i) - BW / 2, top: H - h, width: BW, height: h, background: TONE[c.tone] }} />
            <div
              style={{
                position: "absolute",
                left: mid(i) - BW,
                width: BW * 2,
                top: H - h - 50,
                textAlign: "center",
                fontSize: 36,
                fontWeight: c.tone === "accent" ? 700 : 400,
                color: c.tone === "accent" ? TONE.accent : INK.text,
                opacity: prog(f, c.at + 16, 8),
              }}
            >
              {count(c.value, g, c.display)}
            </div>
            <div style={{ position: "absolute", left: slot * i, width: slot, top: H + 18, textAlign: "center", fontSize: 25, lineHeight: 1.3, color: INK.soft, whiteSpace: "pre-line", opacity: prog(f, c.at, 10) }}>
              {c.label}
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: H, height: 1.5, background: INK.rule }} />
      {notes.map((n, k) => {
        if (n.kind === "drop") {
          const y = top(n.from);
          return (
            <React.Fragment key={k}>
              <Line at={n.at} arrow points={[[mid(n.from) + BW / 2 + 8, y], [mid(n.to), y], [mid(n.to), top(n.to) - 58]]} />
              <NoteText at={n.at} style={{ left: mid(n.to) + 16, top: y + 8, width: 240 }}>
                {n.text}
              </NoteText>
            </React.Fragment>
          );
        }
        const y = top(n.target);
        const x = mid(n.target);
        // Cột thấp: chữ đặt phía trên cột. Cột cao: chữ đặt bên trái cột, nối bằng đường ngang.
        return y >= 170 ? (
          <React.Fragment key={k}>
            <Line at={n.at} points={[[x, y - 56], [x, y - 98]]} />
            <NoteText at={n.at} style={{ left: x - 140, top: y - 172, width: 280, textAlign: "center" }}>
              {n.text}
            </NoteText>
          </React.Fragment>
        ) : (
          <React.Fragment key={k}>
            <Line at={n.at} points={[[x - BW / 2 - 8, y + 34], [x - BW / 2 - 48, y + 34]]} />
            <NoteText at={n.at} style={{ left: x - BW / 2 - 56 - 240, top: y + 18, width: 240, textAlign: "right" }}>
              {n.text}
            </NoteText>
          </React.Fragment>
        );
      })}
    </div>
  );
};

// ---------- Biểu đồ thanh ngang ----------
export type TimedRow = TimedCol;

export const BarChart: React.FC<{ rows: TimedRow[]; max: number; notes: TimedNote[] }> = ({ rows, max, notes }) => {
  const f = useCurrentFrame();
  const LABEL = 300;
  const BAR = W - LABEL - 24 - 120;
  const ROW = 116;
  return (
    <div style={{ position: "relative", width: W, height: rows.length * ROW + (notes.length ? 80 : 0) }}>
      {rows.map((r, i) => {
        const g = prog(f, r.at, 22);
        const show = prog(f, r.at, 10);
        return (
          <div key={i} style={{ position: "absolute", top: i * ROW, left: 0, width: W, height: ROW, display: "flex", alignItems: "center" }}>
            <div style={{ width: LABEL + 24, flex: "none", boxSizing: "border-box", paddingRight: 24, textAlign: "right", fontSize: 26, lineHeight: 1.3, color: INK.soft, opacity: show }}>{r.label}</div>
            <div style={{ height: 64, flex: "none", width: (r.value / max) * BAR * g, background: TONE[r.tone] }} />
            <div style={{ marginLeft: 16, fontSize: 34, fontWeight: r.tone === "accent" ? 700 : 400, color: r.tone === "accent" ? TONE.accent : INK.text, opacity: prog(f, r.at + 16, 8) }}>
              {count(r.value, g, r.display)}
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: LABEL + 24 - 2, top: 12, height: rows.length * ROW - 24, width: 1.5, background: INK.rule }} />
      {notes.map((n, k) => (
        <NoteText key={k} at={n.at} style={{ left: LABEL + 24, top: rows.length * ROW + 10, width: BAR + 120, borderLeft: `2px solid ${INK.text}`, paddingLeft: 16 }}>
          {n.text}
        </NoteText>
      ))}
    </div>
  );
};

// ---------- Biểu đồ ô vuông 10x10 ----------
export const Waffle: React.FC<{ at: number; lit: number; legend: [string, string] }> = ({ at, lit, legend }) => {
  const f = useCurrentFrame();
  const S = 38;
  const G = 6;
  const litP = prog(f, at + 34, 10);
  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 44 }}>
      <div style={{ display: "grid", gridTemplateColumns: `repeat(10, ${S}px)`, gap: G }}>
        {Array.from({ length: 100 }).map((_, i) => {
          const on = i < lit;
          return (
            <div
              key={i}
              style={{
                width: S,
                height: S,
                background: on && litP > 0 ? TONE.accent : INK.cell,
                opacity: prog(f, at + Math.floor(i / 10) * 2, 8) * (on ? 0.35 + 0.65 * litP : 1),
              }}
            />
          );
        })}
      </div>
      <div style={{ paddingTop: 4, fontSize: 25, lineHeight: 1.35, color: INK.text, width: 410 }}>
        {[
          [TONE.accent, legend[0], litP, 700],
          [INK.cell, legend[1], prog(f, at + 18, 10), 400],
        ].map(([color, text, o, weight], i) => (
          <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start", marginBottom: 26, opacity: o as number }}>
            <div style={{ width: 22, height: 22, marginTop: 5, flex: "none", background: color as string }} />
            <div style={{ fontWeight: weight as number }}>{text as string}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
