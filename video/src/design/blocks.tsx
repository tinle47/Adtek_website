import React, { useContext } from "react";
import { Img, staticFile, useVideoConfig } from "remotion";
import type { Word } from "../types";
import { BASE_FPS, C, CueContext, SANS, SERIF, SPRING, cueTime, springAt, useEnter, useFrame } from "./frame";

// Danh sách đánh số: số màu cam font có chân, kẻ mảnh giữa các ý, từng ý hiện lần lượt trong cảnh.
export type ListItem = string | { text: string; detail?: string };

// Danh sách việc cần làm. Mỗi việc có thể kèm một dòng chi tiết (căn cứ hoặc cách làm), nguồn ghi ở cuối.
// Thời điểm hiện từng việc (listDelays) dùng chung cho tiếng "bật" trong Video.tsx. frames tính theo 30 hình/giây.
// Mỗi việc hiện lúc giọng đọc tới nó (khớp 2 chữ liền nhau của việc đó trong lời đọc); không khớp thì chia đều 70% thời lượng cảnh.
export const listDelays = (items: ListItem[], frames: number, words: Word[] = [], offset = 0) => {
  let after = -1;
  return items.map((it, i) => {
    const even = 6 + i * ((frames * 0.7) / items.length);
    const t = cueTime(words, typeof it === "string" ? it : it.text, after);
    if (t === undefined) return even;
    after = t + 0.1;
    return Math.max(i ? 6 : 0, offset + t * BASE_FPS - 2);
  });
};
// Dòng chi tiết của mỗi việc hiện khi giọng đọc tới nó (nếu lời đọc có nhắc), không thì hiện cùng việc đó.
const detailDelays = (items: ListItem[], delays: number[], words: Word[], offset: number) =>
  items.map((it, i) => {
    const detail = typeof it === "string" ? undefined : it.detail;
    const next = delays[i + 1] ?? Infinity;
    const t = detail ? cueTime(words, detail, (delays[i] - offset) / BASE_FPS, typeof it === "string" ? it : it.text) : undefined;
    const at = t === undefined ? delays[i] : offset + t * BASE_FPS - 2;
    return at < next ? Math.max(delays[i] + 8, at) : delays[i] + 8;
  });
export const List: React.FC<{ items: ListItem[]; frames: number; source?: string }> = ({ items, frames, source }) => {
  const { words, offset, hook } = useContext(CueContext);
  const delays = listDelays(items, frames, hook ? [] : words, offset);
  const details = detailDelays(items, delays, hook ? [] : words, offset);
  const p = useEnter(10);
  // Chữ dài thì thu gọn để danh sách không đè xuống phụ đề.
  const len = items.reduce((n, it) => n + (typeof it === "string" ? it.length : it.text.length + (it.detail?.length ?? 0)), 0);
  const compact = len > 220;
  return (
    <div style={{ width: 900 }}>
      {items.map((it, i) => (
        <Item key={i} n={i + 1} item={typeof it === "string" ? { text: it } : it} delay={delays[i]} detailAt={details[i]} last={i === items.length - 1} compact={compact} />
      ))}
      {source && <div style={{ marginTop: 22, fontFamily: SANS, fontSize: 19, lineHeight: 1.35, color: "#8FA3C4", opacity: p }}>{source}</div>}
    </div>
  );
};

const Item: React.FC<{ n: number; item: { text: string; detail?: string }; delay: number; detailAt: number; last: boolean; compact?: boolean }> = ({ n, item, delay, detailAt, last, compact }) => {
  const p = useEnter(delay);
  const d = useEnter(detailAt);
  const f = useFrame();
  const { fps } = useVideoConfig();
  // Số thứ tự bật lên có độ nảy, chữ trượt vào êm.
  const num = springAt(f, fps, delay, SPRING.playful);
  return (
    <div
      style={{
        display: "flex",
        alignItems: "baseline",
        gap: 32,
        padding: compact ? "14px 0" : item.detail ? "20px 0" : "26px 0",
        borderBottom: last ? "none" : "1.5px solid rgba(255,255,255,0.18)",
        opacity: p,
        transform: `translateY(${(1 - p) * 14}px)`,
      }}
    >
      <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 48, color: C.orange, width: 40, flex: "none", transform: `scale(${num})` }}>{n}</div>
      <div>
        <div style={{ fontFamily: SANS, fontSize: compact ? 30 : 34, lineHeight: 1.3, color: C.white }}>{item.text}</div>
        {item.detail && <div style={{ marginTop: 4, fontFamily: SANS, fontSize: compact ? 22 : 25, lineHeight: 1.3, color: "#C9D5EA", opacity: d, transform: `translateX(${(1 - d) * 16}px)` }}>{item.detail}</div>}
      </div>
    </div>
  );
};

// Thẻ bài blog ở cảnh cuối: ảnh bìa thật, đường dẫn, tiêu đề.
export const Article: React.FC<{ image: string; title: string; url: string }> = ({ image, title, url }) => {
  const p = useEnter(2);
  return (
    <div style={{ width: 900, opacity: p, transform: `translateY(${(1 - p) * 24}px)` }}>
      <Img src={staticFile(image)} style={{ width: 900, height: 473, objectFit: "cover", display: "block", borderRadius: 6 }} />
      <div style={{ marginTop: 26, fontFamily: SANS, fontSize: 24, letterSpacing: 1, color: C.muted }}>{url}</div>
      <div style={{ marginTop: 10, fontFamily: SERIF, fontWeight: 600, fontSize: 40, lineHeight: 1.2, color: C.white }}>{title}</div>
    </div>
  );
};

// Cảnh cuối kêu gọi theo dõi kênh: ảnh đại diện, tên kênh, lời hứa nội dung, nút Follow (điểm nhấn cam duy nhất).
export const Follow: React.FC<{ note: string; ask?: string }> = ({ note, ask }) => {
  const frame = useFrame();
  const p = useEnter(2);
  const b = useEnter(10);
  const pulse = 1 + 0.04 * Math.max(0, Math.sin(Math.max(0, frame - 24) / 6));
  return (
    <div style={{ width: 900, opacity: p, transform: `translateY(${(1 - p) * 24}px)`, display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div style={{ width: 170, height: 170, borderRadius: "50%", background: C.navyDeep, border: "3px solid rgba(255,255,255,0.85)", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Img src={staticFile("logo-white.png")} style={{ height: 86 }} />
      </div>
      <div style={{ marginTop: 24, fontFamily: SERIF, fontWeight: 600, fontSize: 56, color: C.white }}>Adtek</div>
      <div style={{ marginTop: 4, fontFamily: SANS, fontSize: 26, letterSpacing: 2, textTransform: "uppercase", color: C.muted }}>Growth Marketing Agency</div>
      <div style={{ marginTop: 10, fontFamily: SANS, fontWeight: 600, fontSize: 30, color: C.white }}>@adtek.growth.marketing</div>
      <div style={{ marginTop: 28, width: 600, borderTop: "1.5px solid rgba(255,255,255,0.18)" }} />
      {ask ? (
        // Câu hỏi để người xem bình luận: bình luận là tín hiệu giúp video được đẩy tiếp.
        <div style={{ position: "relative", marginTop: 30, padding: "22px 34px", borderRadius: 22, border: `3px solid ${C.orange}`, fontFamily: SANS, fontWeight: 700, fontSize: 34, lineHeight: 1.35, color: C.white, textAlign: "center", maxWidth: 800 }}>
          {ask}
          <div style={{ position: "absolute", left: 70, bottom: -18, width: 30, height: 30, background: "#00245F", borderRight: `3px solid ${C.orange}`, borderBottom: `3px solid ${C.orange}`, transform: "rotate(45deg)" }} />
        </div>
      ) : (
        <div style={{ marginTop: 26, fontFamily: SANS, fontSize: 32, lineHeight: 1.4, color: C.white, textAlign: "center", maxWidth: 760 }}>{note}</div>
      )}
      <div
        style={{
          marginTop: 34,
          padding: "20px 90px",
          borderRadius: 8,
          background: C.orange,
          fontFamily: SANS,
          fontWeight: 700,
          fontSize: 38,
          color: C.navyDeep,
          opacity: b,
          transform: `scale(${(0.9 + 0.1 * b) * pulse})`,
        }}
      >
        + Follow
      </div>
    </div>
  );
};
