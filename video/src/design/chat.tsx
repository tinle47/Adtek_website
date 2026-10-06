import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import type { Visual } from "../types";
import { clamp, ease } from "./frame";
import { Phone } from "./serp";

// Màn hình chatbot trên điện thoại (chế độ tối): hỏi một câu, nhận danh sách, hỏi lại đúng câu đó, danh sách khác đi.
// Tên thương hiệu luôn bị làm mờ để không gán thứ hạng cho doanh nghiệp có thật.
export type ChatContent = Extract<Visual, { type: "chat" }>;

const K = { bg: "#212121", bubble: "#303030", text: "#ECECEC", faint: "#9B9B9B" };
// Thời điểm (frame) của từng bước, tính từ đầu cảnh.
const T = { q1: 8, a1: [18, 58], q2: 70, scroll: [74, 94], a2: [92, 132], note: 138 };
export const CHAT_NOTE_AT = T.note;

const fade = (f: number, at: number) => interpolate(f, [at, at + 8], [0, 1], clamp);

// Chuỗi ký tự giả có độ dài thay đổi theo mô tả, hiển thị mờ như tên bị che.
const fakeName = (seed: string) => "Lorem Ipsum Dolor Sitamet".slice(0, 9 + (seed.length % 9));

const Bubble: React.FC<{ text: string; at: number }> = ({ text, at }) => {
  const f = useCurrentFrame();
  const p = fade(f, at);
  return (
    <div style={{ display: "flex", justifyContent: "flex-end", padding: "0 16px", opacity: p, transform: `translateY(${(1 - p) * 10}px)` }}>
      <div style={{ maxWidth: 270, background: K.bubble, borderRadius: 20, padding: "10px 16px", fontSize: 16, lineHeight: "22px" }}>{text}</div>
    </div>
  );
};

// Câu trả lời hiện dần từng dòng như đang được tạo.
const Answer: React.FC<{ items: string[]; span: number[] }> = ({ items, span }) => {
  const f = useCurrentFrame();
  const lines = items.length + 1;
  const shown = interpolate(f, span, [0, lines], clamp);
  const o = (i: number) => interpolate(shown, [i, i + 1], [0, 1], clamp);
  return (
    <div style={{ padding: "16px 18px 8px", fontSize: 16, lineHeight: "24px" }}>
      <div style={{ opacity: o(0) }}>Một số agency được nhắc tới nhiều:</div>
      {items.map((d, i) => (
        <div key={i} style={{ display: "flex", gap: 8, marginTop: 10, opacity: o(i + 1) }}>
          <span>{i + 1}.</span>
          <div>
            <span style={{ fontWeight: 600, filter: "blur(5px)" }}>{fakeName(d + i)}</span>
            <span style={{ color: K.faint }}>: {d}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export const ChatScreen: React.FC<{ c: ChatContent; height: number }> = ({ c, height }) => {
  const f = useCurrentFrame();
  const scroll = interpolate(f, T.scroll, [0, 300], { ...clamp, easing: ease });
  return (
    <Phone height={height} bg={K.bg}>
      <div style={{ position: "relative", zIndex: 2, background: K.bg, height: 52, display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 18px", color: K.text }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
          <div style={{ width: 20, height: 2, background: K.text, borderRadius: 1 }} />
          <div style={{ width: 14, height: 2, background: K.text, borderRadius: 1 }} />
        </div>
        <div style={{ fontSize: 17, fontWeight: 500 }}>ChatGPT ›</div>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke={K.text} strokeWidth="1.8" strokeLinecap="round">
          <path d="M4 20h4l10.5-10.5a2.1 2.1 0 00-3-3L5 17v3z" />
        </svg>
      </div>
      <div style={{ transform: `translateY(${-scroll}px)`, color: K.text, paddingTop: 14 }}>
        <Bubble text={c.question} at={T.q1} />
        <Answer items={c.answers[0]} span={T.a1} />
        <div style={{ height: 18 }} />
        <Bubble text={c.question} at={T.q2} />
        <Answer items={c.answers[1]} span={T.a2} />
      </div>
    </Phone>
  );
};
