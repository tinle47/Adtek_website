import React from "react";
import { Img, staticFile, useCurrentFrame } from "remotion";
import { C, SANS, SERIF, useEnter } from "./frame";

// Danh sách đánh số: số màu cam font có chân, kẻ mảnh giữa các ý, từng ý hiện lần lượt trong cảnh.
export type ListItem = string | { text: string; detail?: string };

// Danh sách việc cần làm. Mỗi việc có thể kèm một dòng chi tiết (căn cứ hoặc cách làm), nguồn ghi ở cuối.
export const List: React.FC<{ items: ListItem[]; frames: number; source?: string }> = ({ items, frames, source }) => {
  const step = (frames * 0.7) / items.length;
  const p = useEnter(10);
  // Chữ dài thì thu gọn để danh sách không đè xuống phụ đề.
  const len = items.reduce((n, it) => n + (typeof it === "string" ? it.length : it.text.length + (it.detail?.length ?? 0)), 0);
  const compact = len > 220;
  return (
    <div style={{ width: 900 }}>
      {items.map((it, i) => (
        <Item key={i} n={i + 1} item={typeof it === "string" ? { text: it } : it} delay={6 + i * step} last={i === items.length - 1} compact={compact} />
      ))}
      {source && <div style={{ marginTop: 22, fontFamily: SANS, fontSize: 19, lineHeight: 1.35, color: "#8FA3C4", opacity: p }}>{source}</div>}
    </div>
  );
};

const Item: React.FC<{ n: number; item: { text: string; detail?: string }; delay: number; last: boolean; compact?: boolean }> = ({ n, item, delay, last, compact }) => {
  const p = useEnter(delay);
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
      <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 48, color: C.orange, width: 40, flex: "none" }}>{n}</div>
      <div>
        <div style={{ fontFamily: SANS, fontSize: compact ? 30 : 34, lineHeight: 1.3, color: C.white }}>{item.text}</div>
        {item.detail && <div style={{ marginTop: 4, fontFamily: SANS, fontSize: compact ? 22 : 25, lineHeight: 1.3, color: "#C9D5EA" }}>{item.detail}</div>}
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
  const frame = useCurrentFrame();
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
