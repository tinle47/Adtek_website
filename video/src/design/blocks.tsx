import React from "react";
import { Img, staticFile } from "remotion";
import { C, SANS, SERIF, useEnter } from "./frame";

// Danh sách đánh số: số màu cam font có chân, kẻ mảnh giữa các ý, từng ý hiện lần lượt trong cảnh.
export const List: React.FC<{ items: string[]; frames: number }> = ({ items, frames }) => {
  const step = (frames * 0.7) / items.length;
  return (
    <div style={{ width: 900 }}>
      {items.map((it, i) => (
        <Item key={i} n={i + 1} text={it} delay={6 + i * step} last={i === items.length - 1} />
      ))}
    </div>
  );
};

const Item: React.FC<{ n: number; text: string; delay: number; last: boolean }> = ({ n, text, delay, last }) => {
  const p = useEnter(delay);
  return (
    <div
      style={{
        display: "flex",
        alignItems: "baseline",
        gap: 32,
        padding: "26px 0",
        borderBottom: last ? "none" : "1.5px solid rgba(255,255,255,0.18)",
        opacity: p,
        transform: `translateY(${(1 - p) * 14}px)`,
      }}
    >
      <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 48, color: C.orange, width: 40 }}>{n}</div>
      <div style={{ fontFamily: SANS, fontSize: 34, lineHeight: 1.35, color: C.white }}>{text}</div>
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
