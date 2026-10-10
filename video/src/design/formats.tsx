import React, { useContext } from "react";
import { interpolate, useVideoConfig } from "remotion";
import type { Word } from "../types";
import sea from "../data/sea-map.json";
import { BASE_FPS, C, CueContext, CuedText, SANS, SERIF, SPRING, clamp, cueTime, ease, springAt, useFrame } from "./frame";

// Các dạng video mới (10/2026): chữ động, biểu đồ đua, bản đồ, đếm ngược. Mọi mốc đều theo giọng đọc
// (giọng nhắc tới dòng chữ, mốc thời gian, con số hay "hạng 3" thì phần đó mới hiện), không khớp thì chia đều theo cảnh.
const INK = { text: "#FFFFFF", soft: "#C9D5EA", source: "#8FA3C4", rule: "rgba(255,255,255,0.55)", cell: "rgba(255,255,255,0.14)", main: "#D6E2F5", base: "#5E7DB3" };
const prog = (f: number, at: number, len = 12) => interpolate(f - at, [0, len], [0, 1], { ...clamp, easing: ease });
const fmt = (v: number) => v.toLocaleString("en-US", { maximumFractionDigits: 1 });

// Mốc (khung 30 hình/giây, tính trong phần hình) lúc giọng đọc tới lần lượt từng needle. Mốc không khớp được
// nội suy giữa 2 mốc khớp gần nhất (hai đầu là start, end), nên bỏ qua vài tháng trong lời đọc vẫn trượt đều.
export const cueSeq = (words: Word[], offset: number, needles: (string | number)[], start: number, end: number) => {
  let after = -1;
  const found = needles.map((nd) => {
    const t = cueTime(words, nd, after);
    if (t === undefined) return undefined;
    after = t + 0.05;
    return offset + t * BASE_FPS - 2;
  });
  const n = needles.length;
  const out = found.map((v, i) => {
    if (v !== undefined) return v;
    let a = i - 1;
    while (a >= 0 && found[a] === undefined) a--;
    let b = i + 1;
    while (b < n && found[b] === undefined) b++;
    const va = a >= 0 ? found[a]! : start - (end - start) / Math.max(1, n - 1);
    const vb = b < n ? found[b]! : Math.max(end, va + 8 * (b - a));
    return va + ((vb - va) * (i - a)) / (b - a);
  });
  for (let i = 1; i < n; i++) out[i] = Math.max(out[i], out[i - 1] + 8);
  return out.map((v) => Math.max(0, v));
};
const useCueCtx = () => useContext(CueContext);

// ---------- Chữ động: từng dòng chữ to đập xuống đúng lúc giọng đọc ----------
// Cảnh không có tiêu đề, nên chữ chiếm cả vùng từ dưới logo tới trên phụ đề.
// Dòng đầu hiện ngay khi vào cảnh (không để màn hình trống lúc giọng đang đọc "Một:", "Hai:"), các dòng sau theo giọng.
export const wordsCues = (lines: string[], words: Word[], offset: number) => {
  const ats = cueSeq(words, offset, lines, 4, 40);
  ats[0] = Math.min(ats[0], offset + 4);
  for (let i = 1; i < ats.length; i++) ats[i] = Math.max(ats[i], ats[i - 1] + 6);
  return ats;
};
export const Words: React.FC<{ lines: string[]; emph?: string[]; source?: string }> = ({ lines, emph = [], source }) => {
  const f = useFrame();
  const { fps } = useVideoConfig();
  const { words, offset, hook } = useCueCtx();
  const ats = hook ? lines.map((_, i) => i * 3) : wordsCues(lines, words, offset);
  const long = Math.max(...lines.map((l) => l.length));
  const size = long > 16 ? 92 : long > 12 ? 108 : 124;
  // Tô cam những chữ nằm trong emph.
  const paint = (line: string) => {
    const hit = emph.find((e) => line.includes(e));
    if (!hit) return line;
    const i = line.indexOf(hit);
    return (
      <>
        {line.slice(0, i)}
        <span style={{ color: C.orange }}>{hit}</span>
        {line.slice(i + hit.length)}
      </>
    );
  };
  return (
    <div style={{ position: "relative", marginTop: -330, height: 980, width: 900, display: "flex", flexDirection: "column", justifyContent: "center", fontFamily: SERIF }}>
      {lines.map((l, i) => {
        const s = springAt(f, fps, ats[i], SPRING.snappy);
        return (
          <div
            key={i}
            style={{
              fontSize: size,
              fontWeight: 700,
              lineHeight: 1.08,
              letterSpacing: -1,
              color: C.white,
              opacity: Math.min(1, s * 1.5),
              transform: `translateY(${(1 - s) * -30}px) scale(${1.18 - 0.18 * s})`,
              transformOrigin: "left center",
              marginBottom: 14,
            }}
          >
            {paint(l)}
          </div>
        );
      })}
      {source && (
        <div style={{ marginTop: 30, fontFamily: SANS, fontSize: 22, color: INK.source, opacity: prog(f, ats[ats.length - 1] + 10) }}>{source}</div>
      )}
    </div>
  );
};

// ---------- Biểu đồ đua: các thanh vượt nhau qua từng mốc thời gian ----------
type Series = { name: string; values: (number | null)[] };
export const raceCues = (periods: string[], words: Word[], offset: number, frames: number) =>
  cueSeq(words, offset, periods.map((p) => (/^\d+$/.test(p) ? Number(p) : p)), 10, Math.max(40, frames * 0.8));
export const Race: React.FC<{ metric: string; unit?: string; source: string; periods: string[]; series: Series[]; frames: number; top?: number; note?: string }> = ({
  metric, unit, source, periods, series, frames, top = 6, note,
}) => {
  const f = useFrame();
  const { words, offset, hook } = useCueCtx();
  const ats = hook ? periods.map((_, i) => i) : raceCues(periods, words, offset, frames);
  // Vị trí thời gian liên tục: 0 = mốc đầu, 1 = mốc thứ hai...; giữa 2 mốc trượt êm.
  const pos = ats.length > 1 ? interpolate(f, ats, ats.map((_, i) => i), { ...clamp, easing: ease }) : 0;
  const at = (s: Series, i: number) => s.values[Math.max(0, Math.min(periods.length - 1, i))] ?? 0;
  const lo = Math.floor(pos), hi = Math.min(periods.length - 1, lo + 1), fr = pos - lo;
  const value = (s: Series) => at(s, lo) + (at(s, hi) - at(s, lo)) * fr;
  // Thứ hạng ở 2 mốc liền nhau, nội suy để thanh trượt lên xuống chứ không nhảy.
  const rank = (i: number) => {
    const sorted = [...series].sort((a, b) => at(b, i) - at(a, i));
    return new Map(sorted.map((s, k) => [s.name, k]));
  };
  const rLo = rank(lo), rHi = rank(hi);
  const ROW = 96, LABEL = 230, BAR = 900 - LABEL - 150;
  const max = Math.max(...series.map(value), 1e-9);
  const leader = [...series].sort((a, b) => value(b) - value(a))[0]?.name;
  const shown = series.filter((s) => Math.min(rLo.get(s.name)!, rHi.get(s.name)!) < top);
  return (
    <div style={{ width: 900, fontFamily: SANS, color: INK.text }}>
      <div style={{ fontSize: 30, lineHeight: 1.3, opacity: prog(f, 0) }}>
        <b>{metric}</b>
        {unit ? <span>, {unit}</span> : null}
      </div>
      <div style={{ position: "relative", height: top * ROW + 20, marginTop: 36 }}>
        {shown.map((s) => {
          const r = rLo.get(s.name)! + (rHi.get(s.name)! - rLo.get(s.name)!) * fr;
          const v = value(s);
          const w = (v / max) * BAR * prog(f, 2, 20);
          const lead = s.name === leader;
          return (
            <div key={s.name} style={{ position: "absolute", left: 0, top: r * ROW, display: "flex", alignItems: "center", height: ROW - 18, opacity: r > top - 0.5 ? Math.max(0, top - r) * 2 : 1 }}>
              <div style={{ width: LABEL, paddingRight: 20, textAlign: "right", fontSize: 30, fontWeight: lead ? 700 : 500, color: lead ? C.orange : INK.soft }}>{s.name}</div>
              <div style={{ width: Math.max(4, w), height: ROW - 30, background: lead ? C.orange : INK.main }} />
              <div style={{ marginLeft: 14, fontSize: 32, fontWeight: 700, color: lead ? C.orange : INK.text, fontVariantNumeric: "tabular-nums" }}>{fmt(v)}{unit === "%" ? "%" : ""}</div>
            </div>
          );
        })}
      </div>
      {note && <CuedText text={note} from={ats[ats.length - 1] + 20} style={{ fontSize: 34, fontWeight: 700, borderLeft: `3px solid ${C.orange}`, paddingLeft: 18, marginBottom: 18 }} />}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginTop: 6 }}>
        <div style={{ fontSize: 19, color: INK.source, maxWidth: 560, opacity: prog(f, 10) }}>{source}</div>
        <div style={{ fontFamily: SERIF, fontSize: 84, fontWeight: 700, color: "rgba(255,255,255,0.85)", lineHeight: 1, marginRight: 40 }}>{periods[Math.round(pos)]}</div>
      </div>
    </div>
  );
};

// ---------- Bản đồ Đông Nam Á: từng nước sáng lên kèm con số khi giọng đọc tới ----------
type MapItem = { iso3: string; name: string; value: number; display?: string };
type Country = { d: string; cx: number; cy: number };
const MAP = sea as { width: number; height: number; countries: Record<string, Country> };
// Vị trí nhãn tránh đè nhau (Malaysia và Singapore sát nhau, Indonesia trải dài).
const LABEL_AT: Record<string, [number, number]> = { VNM: [575, 120], THA: [250, 150], PHL: [770, 150], MYS: [300, 330], SGP: [250, 455], IDN: [560, 560] };
export const mapCues = (items: MapItem[], words: Word[], offset: number, frames: number) =>
  cueSeq(words, offset, items.map((it) => it.value), 10, Math.max(40, frames * 0.75));
export const SeaMap: React.FC<{ metric: string; unit?: string; source: string; items: MapItem[]; frames: number; highlight?: string }> = ({
  metric, unit, source, items, frames, highlight = "VNM",
}) => {
  const f = useFrame();
  const { fps } = useVideoConfig();
  const { words, offset, hook } = useCueCtx();
  const ats = hook ? items.map(() => 0) : mapCues(items, words, offset, frames);
  const when = new Map(items.map((it, i) => [it.iso3, ats[i]]));
  // Bản đồ cao tối đa 520px để nguồn không đè phụ đề; căn giữa vùng hình.
  const scale = 520 / MAP.height;
  const mw = MAP.width * scale;
  return (
    <div style={{ width: 900, fontFamily: SANS, color: INK.text }}>
      <div style={{ fontSize: 30, lineHeight: 1.3, opacity: prog(f, 0) }}>
        <b>{metric}</b>
        {unit ? <span>, {unit}</span> : null}
      </div>
      <div style={{ position: "relative", width: mw, height: MAP.height * scale, marginTop: 16, marginLeft: (900 - mw) / 2 }}>
        <svg width={mw} height={MAP.height * scale} viewBox={`0 0 ${MAP.width} ${MAP.height}`} style={{ position: "absolute", left: 0, top: 0 }}>
          {Object.entries(MAP.countries).map(([iso, c]) => {
            const t = when.get(iso);
            const lit = t === undefined ? 0 : prog(f, t, 10);
            const hi = iso === highlight;
            const fill = t === undefined ? "rgba(255,255,255,0.08)" : hi ? C.orange : INK.main;
            return (
              <path key={iso} d={c.d} fill={fill} fillOpacity={t === undefined ? 1 : 0.18 + 0.82 * lit} stroke="rgba(255,255,255,0.35)" strokeWidth={0.8} />
            );
          })}
          {/* Singapore quá nhỏ ở cỡ này: đánh dấu bằng chấm tròn */}
          {when.has("SGP") && <circle cx={MAP.countries.SGP.cx} cy={MAP.countries.SGP.cy} r={7 * prog(f, when.get("SGP")!, 10)} fill={INK.main} />}
        </svg>
        {items.map((it, i) => {
          const pop = springAt(f, fps, ats[i], SPRING.playful);
          const [x, y] = LABEL_AT[it.iso3] ? LABEL_AT[it.iso3].map((v) => v * (mw / 900)) : [MAP.countries[it.iso3].cx * scale, MAP.countries[it.iso3].cy * scale];
          const hi = it.iso3 === highlight;
          return (
            <div
              key={it.iso3}
              style={{
                position: "absolute", left: x, top: y, transform: `translate(-50%, -50%) scale(${pop})`,
                padding: "8px 16px", borderRadius: 10, background: hi ? C.orange : C.navyDeep, border: `2px solid ${hi ? C.orange : "rgba(255,255,255,0.5)"}`,
                textAlign: "center", whiteSpace: "nowrap",
              }}
            >
              <div style={{ fontSize: 22, fontWeight: 600, color: hi ? C.navyDeep : INK.soft }}>{it.name}</div>
              <div style={{ fontSize: hi ? 42 : 34, fontWeight: 700, lineHeight: 1.1, color: hi ? C.navyDeep : C.white }}>{it.display ?? fmt(it.value)}</div>
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 10, fontSize: 19, color: INK.source, opacity: prog(f, 10) }}>{source}</div>
    </div>
  );
};

// ---------- Đếm ngược top 5: hạng 5 về hạng 1, hạng 1 lật cuối cùng ----------
type Rank = { rank: number; label: string; value?: number | null; display?: string; note?: string };
// Hạng nào hiện lúc giọng đọc "Hạng N"; hạng 1 lật kèm tiếng ding (Video.tsx dùng chung mốc này).
export const countdownCues = (items: Rank[], words: Word[], offset: number, frames: number) => {
  const order = [...items].sort((a, b) => b.rank - a.rank);
  const ats = cueSeq(words, offset, order.map((it) => `hạng ${it.rank}`), 10, Math.max(40, frames * 0.8));
  return new Map(order.map((it, i) => [it.rank, ats[i]]));
};
export const Countdown: React.FC<{ metric: string; source: string; items: Rank[]; frames: number; teaser?: boolean }> = ({ metric, source, items, frames, teaser }) => {
  const f = useFrame();
  const { fps } = useVideoConfig();
  const { words, offset, hook } = useCueCtx();
  // teaser (cảnh mở đầu): chưa lật ô nào, hạng 1 nhấp nháy chờ.
  const when = teaser ? new Map(items.map((it) => [it.rank, Infinity])) : hook ? new Map(items.map((it) => [it.rank, 0])) : countdownCues(items, words, offset, frames);
  const rows = [...items].sort((a, b) => a.rank - b.rank);
  const ROW = 96;
  return (
    <div style={{ width: 900, fontFamily: SANS, color: INK.text }}>
      <div style={{ fontSize: 30, lineHeight: 1.3, opacity: prog(f, 0) }}>
        <b>{metric}</b>
      </div>
      <div style={{ display: "grid", gap: 12, marginTop: 24 }}>
        {rows.map((it) => {
          const t = when.get(it.rank) ?? 0;
          const flip = Number.isFinite(t) ? springAt(f, fps, t, it.rank === 1 ? { stiffness: 200, damping: 12 } : SPRING.snappy) : 0;
          const open = f >= t;
          const first = it.rank === 1;
          const wait = 1 + 0.03 * Math.max(0, Math.sin(f / 5)); // ô "?" nhấp nháy khi chờ
          return (
            <div
              key={it.rank}
              style={{
                display: "flex", alignItems: "center", gap: 26, height: ROW, padding: "0 28px", borderRadius: 16,
                background: open && first ? C.orange : "rgba(255,255,255,0.06)",
                border: `2px solid ${open && first ? C.orange : "rgba(255,255,255,0.22)"}`,
                transform: `scale(${open ? 0.96 + 0.04 * flip : first ? wait : 1})`,
              }}
            >
              <div style={{ fontFamily: SERIF, fontSize: 56, fontWeight: 700, width: 54, color: open && first ? C.navyDeep : C.orange }}>{it.rank}</div>
              {open ? (
                <div style={{ opacity: Math.min(1, flip * 1.4), transform: `translateX(${(1 - flip) * 30}px)` }}>
                  <div style={{ fontSize: first ? 42 : 34, fontWeight: 700, lineHeight: 1.15, color: first ? C.navyDeep : C.white }}>
                    {it.label}
                    {it.display ? <span style={{ fontWeight: 500 }}> · {it.display}</span> : null}
                  </div>
                  {it.note && <div style={{ fontSize: 22, color: first ? C.navyDeep : INK.soft, marginTop: 4 }}>{it.note}</div>}
                </div>
              ) : (
                <div style={{ fontSize: 44, fontWeight: 700, color: "rgba(255,255,255,0.35)" }}>?</div>
              )}
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 22, fontSize: 19, color: INK.source }}>{source}</div>
    </div>
  );
};
