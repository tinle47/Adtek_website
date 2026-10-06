import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";

// Biểu đồ theo chuẩn trình bày của McKinsey: màu phẳng, cột vuông, không lưới, không bóng,
// số ghi thẳng trên dữ liệu, chú thích bằng đường kẻ mảnh và chữ đậm nhỏ, một điểm nhấn duy nhất.
export type Variant = "light" | "dark";

export const INK = {
  light: {
    text: "#14171F",
    soft: "#4A5160",
    source: "#7A8190",
    rule: "#14171F",
    base: "#A9BEDF", // nhóm đối chiếu
    main: "#002D72", // nhóm chính
    cell: "#DCE4F1",
    accent: "#FF9014", // điểm nhấn duy nhất
  },
  dark: {
    text: "#FFFFFF",
    soft: "#C9D5EA",
    source: "#8FA3C4",
    rule: "rgba(255,255,255,0.55)",
    base: "#5E7DB3",
    main: "#D6E2F5",
    cell: "rgba(255,255,255,0.14)",
    accent: "#FF9014",
  },
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ease = Easing.bezier(0.33, 0, 0.2, 1);
const prog = (f: number, at: number, len = 20) => interpolate(f - at, [0, len], [0, 1], { ...clamp, easing: ease });

// Khung "exhibit": tên chỉ số in đậm + đơn vị in thường, biểu đồ, dòng nguồn.
export const Exhibit: React.FC<{
  v: Variant;
  metric: string;
  unit: string;
  source: string;
  appear: number;
  children: React.ReactNode;
}> = ({ v, metric, unit, source, appear, children }) => {
  const f = useCurrentFrame();
  const c = INK[v];
  const p = prog(f, appear, 12);
  return (
    <div
      style={{
        width: 920,
        padding: v === "light" ? "44px 48px 36px" : "8px 0 0",
        background: v === "light" ? "#FFFFFF" : "transparent",
        opacity: p,
        color: c.text,
      }}
    >
      <div style={{ fontSize: 30, lineHeight: 1.3, textAlign: "left" }}>
        <b style={{ fontWeight: 700 }}>{metric}</b>, <span style={{ fontWeight: 400 }}>{unit}</span>
      </div>
      <div style={{ marginTop: 36 }}>{children}</div>
      <div style={{ marginTop: 28, fontSize: 19, color: c.source, textAlign: "left" }}>{source}</div>
    </div>
  );
};

export type Column = { label: string; value: number; tone: "base" | "main" | "accent"; at: number };

// Biểu đồ cột: cột mọc từ đường nền, số hiện sau khi cột mọc xong. Cột mới thêm vào theo thời điểm "at".
export const ColumnChart: React.FC<{
  v: Variant;
  cols: Column[];
  max: number;
  slots: number; // số chỗ dành sẵn để cột mới thêm vào không làm xô lệch cột cũ
  notes?: React.ReactNode;
}> = ({ v, cols, max, slots, notes }) => {
  const f = useCurrentFrame();
  const c = INK[v];
  const W = 824;
  const H = 300;
  const BW = 132;
  const slot = W / slots;
  return (
    <div style={{ position: "relative", width: W, height: H + 110 }}>
      {cols.map((col, i) => {
        const g = prog(f, col.at, 22);
        const label = prog(f, col.at + 16, 8);
        const h = (col.value / max) * H * g;
        const x = slot * i + (slot - BW) / 2;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: H - h, width: BW, height: h, background: c[col.tone] }} />
            <div
              style={{
                position: "absolute",
                left: x - 20,
                width: BW + 40,
                top: H - h - 50,
                textAlign: "center",
                fontSize: 36,
                fontWeight: col.tone === "accent" ? 700 : 400,
                color: col.tone === "accent" ? c.accent : c.text,
                opacity: label,
              }}
            >
              {col.value}
            </div>
            <div
              style={{
                position: "absolute",
                left: slot * i,
                width: slot,
                top: H + 18,
                textAlign: "center",
                fontSize: 25,
                lineHeight: 1.3,
                color: c.soft,
                whiteSpace: "pre-line",
                opacity: prog(f, col.at, 10),
              }}
            >
              {col.label}
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: H, height: 1.5, background: c.rule }} />
      {notes}
    </div>
  );
};

// Chú thích: đường kẻ mảnh vẽ dần + chữ đậm nhỏ. points là toạ độ trong khung biểu đồ.
export const Note: React.FC<{
  v: Variant;
  at: number;
  points: [number, number][];
  text: React.ReactNode;
  textAt: { left: number; top: number; width?: number; align?: "left" | "right" | "center" };
  arrow?: boolean;
}> = ({ v, at, points, text, textAt, arrow }) => {
  const f = useCurrentFrame();
  const c = INK[v];
  const draw = prog(f, at, 16);
  const txt = prog(f, at + 10, 10);
  const len = points.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - points[i][0], p[1] - points[i][1]), 0);
  const end = points[points.length - 1];
  return (
    <>
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width="1" height="1">
        <polyline
          points={points.map((p) => p.join(",")).join(" ")}
          fill="none"
          stroke={c.text}
          strokeWidth={2}
          strokeDasharray={len}
          strokeDashoffset={len * (1 - draw)}
        />
        {arrow && draw > 0.98 && <polygon points={`${end[0] - 7},${end[1] - 12} ${end[0] + 7},${end[1] - 12} ${end[0]},${end[1]}`} fill={c.text} />}
      </svg>
      <div
        style={{
          position: "absolute",
          left: textAt.left,
          top: textAt.top,
          width: textAt.width ?? 300,
          textAlign: textAt.align ?? "left",
          fontSize: 25,
          lineHeight: 1.3,
          color: c.text,
          opacity: txt,
        }}
      >
        {text}
      </div>
    </>
  );
};

// Biểu đồ ô vuông 10x10: mỗi ô là 1 lượt, ô nhấn hiện sau cùng. Chú giải đặt bên phải.
export const Waffle: React.FC<{ v: Variant; at: number; lit: number; legend: [string, string] }> = ({ v, at, lit, legend }) => {
  const f = useCurrentFrame();
  const c = INK[v];
  const S = 38;
  const G = 6;
  const litP = prog(f, at + 34, 10);
  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 44 }}>
      <div style={{ display: "grid", gridTemplateColumns: `repeat(10, ${S}px)`, gap: G }}>
        {Array.from({ length: 100 }).map((_, i) => {
          const row = Math.floor(i / 10);
          const on = i < lit;
          return (
            <div
              key={i}
              style={{
                width: S,
                height: S,
                background: on && litP > 0 ? c.accent : c.cell,
                opacity: prog(f, at + row * 2, 8) * (on ? 0.35 + 0.65 * litP : 1),
              }}
            />
          );
        })}
      </div>
      <div style={{ paddingTop: 4, fontSize: 25, lineHeight: 1.35, color: c.text }}>
        {[
          [c.accent, legend[0], litP],
          [c.cell, legend[1], prog(f, at + 18, 10)],
        ].map(([color, text, o], i) => (
          <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start", marginBottom: 26, opacity: o as number }}>
            <div style={{ width: 22, height: 22, marginTop: 5, flex: "none", background: color as string, outline: v === "light" && i ? "1px solid #C5CFDF" : "none" }} />
            <div style={{ fontWeight: i ? 400 : 700 }}>{text as string}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
