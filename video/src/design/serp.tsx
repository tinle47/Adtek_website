import React from "react";
import { Easing, Img, interpolate, staticFile } from "remotion";
import type { Visual } from "../types";
import { C, SANS, useFrame } from "./frame";

// Dựng lại trang kết quả Google trên điện thoại (chế độ tối) để trông như quay màn hình thật:
// gõ truy vấn, "Tổng quan do AI" hiện dần từng chữ, cuộn xuống kết quả tự nhiên rồi kết quả đó mờ đi.
// Chữ trong khối AI tóm tắt đúng nội dung bài blog. Kết quả tự nhiên là bài thật của Adtek, không giả nguồn trích dẫn.

export const G = {
  bg: "#1F1F1F",
  field: "#303134",
  text: "#E8EAED",
  sub: "#BDC1C6",
  faint: "#9AA0A6",
  link: "#8AB4F8",
  line: "#3C4043",
};
export const ROBOTO = '"Roboto", Arial, sans-serif';
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ease = Easing.bezier(0.33, 0, 0.2, 1);

export type SerpContent = Extract<Visual, { type: "serp" }>;

// Thời điểm (frame) của từng bước, tính từ đầu cảnh.
const T = { type: [6, 24], ai: 28, stream: [32, 74], more: 76, scroll: [84, 102], dim: 104 };

const PHONE_W = 540;
const BEZEL = 12;
const SCALE = (PHONE_W - BEZEL * 2) / 390; // thiết kế theo bề ngang 390 của iPhone
const SCROLL = 280;

const Icon = {
  search: (c: string) => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2.2" strokeLinecap="round">
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="M20 20l-4.6-4.6" />
    </svg>
  ),
  close: (c: string) => (
    <svg width="20" height="20" viewBox="0 0 24 24" stroke={c} strokeWidth="2" strokeLinecap="round">
      <path d="M6 6l12 12M18 6L6 18" />
    </svg>
  ),
  mic: (c: string) => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2" strokeLinecap="round">
      <rect x="9" y="3" width="6" height="11" rx="3" />
      <path d="M5.5 11a6.5 6.5 0 0013 0M12 17.5V21" />
    </svg>
  ),
  chevron: (c: string) => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2" strokeLinecap="round">
      <path d="M6 9l6 6 6-6" />
    </svg>
  ),
  sparkle: () => (
    <svg width="22" height="22" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="aiov" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#4C8DF6" />
          <stop offset="0.55" stopColor="#9B72F2" />
          <stop offset="1" stopColor="#D96570" />
        </linearGradient>
      </defs>
      <path d="M12 2C12.6 7 17 11.4 22 12C17 12.6 12.6 17 12 22C11.4 17 7 12.6 2 12C7 11.4 11.4 7 12 2Z" fill="url(#aiov)" />
    </svg>
  ),
};

const StatusBar: React.FC = () => (
  <div style={{ height: 44, display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 28px 0 34px", position: "relative" }}>
    <span style={{ fontSize: 15, fontWeight: 500, color: "#fff", fontFamily: "-apple-system, Roboto, sans-serif" }}>9:41</span>
    <div style={{ position: "absolute", left: "50%", top: 9, width: 112, height: 30, borderRadius: 16, background: "#000", transform: "translateX(-50%)" }} />
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 2 }}>
        {[4, 6, 8, 10].map((h) => (
          <div key={h} style={{ width: 3, height: h, borderRadius: 1, background: "#fff" }} />
        ))}
      </div>
      <svg width="16" height="12" viewBox="0 0 16 12" fill="#fff">
        <path d="M8 11.5l2.2-2.6a3 3 0 00-4.4 0zM3.4 6.6l1.4 1.6a4.6 4.6 0 016.4 0l1.4-1.6a6.7 6.7 0 00-9.2 0zM1 3.9l1.4 1.6a8.3 8.3 0 0111.2 0L15 3.9a10.4 10.4 0 00-14 0z" />
      </svg>
      <div style={{ width: 24, height: 12, borderRadius: 3.5, border: "1.2px solid rgba(255,255,255,0.5)", padding: 1.5, boxSizing: "border-box" }}>
        <div style={{ width: "75%", height: "100%", borderRadius: 1.5, background: "#fff" }} />
      </div>
    </div>
  </div>
);

const AddressBar: React.FC = () => (
  <div style={{ height: 56, display: "flex", alignItems: "center", gap: 12, padding: "0 14px", borderBottom: `1px solid ${G.line}` }}>
    <div style={{ flex: 1, height: 40, borderRadius: 20, background: G.field, display: "flex", alignItems: "center", gap: 10, padding: "0 14px" }}>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke={G.faint} strokeWidth="2.4" strokeLinecap="round">
        <path d="M4 7h10M18 7h2M4 17h2M10 17h10" />
        <circle cx="16" cy="7" r="2" />
        <circle cx="8" cy="17" r="2" />
      </svg>
      <span style={{ fontSize: 15, color: G.text }}>google.com</span>
    </div>
    <div style={{ width: 22, height: 22, borderRadius: 5, border: `2px solid ${G.text}`, fontSize: 12, fontWeight: 500, color: G.text, display: "flex", alignItems: "center", justifyContent: "center" }}>
      3
    </div>
    <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ width: 4, height: 4, borderRadius: 2, background: G.text }} />
      ))}
    </div>
  </div>
);

// Khung iPhone: viền, thanh trạng thái, màn hình thiết kế theo bề ngang 390 rồi phóng to. Đáy mờ dần vào nền.
export const Phone: React.FC<{ height: number; bg: string; children: React.ReactNode }> = ({ height, bg, children }) => {
  const f = useFrame();
  const enter = interpolate(f, [0, 12], [0, 1], { ...clamp, easing: ease });
  return (
    <div
      style={{
        width: PHONE_W,
        height,
        padding: `${BEZEL}px ${BEZEL}px 0`,
        boxSizing: "border-box",
        borderRadius: "64px 64px 0 0",
        background: "#0C0C0E",
        boxShadow: "inset 0 0 0 2px #2B2B30",
        opacity: enter,
        transform: `translateY(${(1 - enter) * 50}px)`,
        WebkitMaskImage: "linear-gradient(to bottom, #000 82%, transparent 100%)",
        maskImage: "linear-gradient(to bottom, #000 82%, transparent 100%)",
      }}
    >
      <div style={{ borderRadius: "52px 52px 0 0", overflow: "hidden", height: height - BEZEL, background: bg }}>
        <div style={{ width: 390, height: height / SCALE, transform: `scale(${SCALE})`, transformOrigin: "0 0", fontFamily: ROBOTO, color: G.text, position: "relative" }}>
          <div style={{ position: "relative", zIndex: 2, background: bg }}>
            <StatusBar />
          </div>
          {children}
        </div>
      </div>
    </div>
  );
};

export const GoogleSerp: React.FC<{ c: SerpContent; height: number }> = ({ c, height }) => {
  const f = useFrame();
  const typed = c.query.slice(0, Math.round(interpolate(f, T.type, [0, c.query.length], clamp)));
  const caret = f < T.type[1] + 4 && f % 16 < 9;
  const ai = interpolate(f, [T.ai, T.ai + 8], [0, 1], clamp);
  const words = c.answer.flatMap((seg) => seg.text.split(" ").map((w) => ({ w, bold: seg.bold })));
  const shown = Math.floor(interpolate(f, T.stream, [0, words.length], clamp));
  const more = interpolate(f, [T.more, T.more + 8], [0, 1], clamp);
  const scroll = interpolate(f, T.scroll, [0, SCROLL], { ...clamp, easing: ease });
  const dim = interpolate(f, [T.dim, T.dim + 10], [1, 0.32], clamp) * interpolate(f, [T.ai + 4, T.ai + 12], [0, 1], clamp);

  return (
    <Phone height={height} bg={G.bg}>
          <div style={{ position: "relative", zIndex: 2, background: G.bg }}>
            <AddressBar />
          </div>
          <div style={{ transform: `translateY(${-scroll}px)` }}>
            {/* Ô tìm kiếm + tab */}
            <div style={{ padding: "12px 14px" }}>
              <div style={{ height: 48, borderRadius: 24, background: G.field, display: "flex", alignItems: "center", gap: 12, padding: "0 16px" }}>
                {Icon.search(G.faint)}
                <span style={{ flex: 1, fontSize: 16, color: G.text }}>
                  {typed}
                  <span style={{ opacity: caret ? 1 : 0, color: G.link }}>|</span>
                </span>
                {Icon.close(G.faint)}
                <div style={{ width: 1, height: 24, background: G.line }} />
                {Icon.mic(G.faint)}
              </div>
            </div>
            <div style={{ display: "flex", gap: 22, padding: "0 18px", fontSize: 14, color: G.sub, borderBottom: `1px solid ${G.line}` }}>
              {["Tất cả", "Hình ảnh", "Video", "Tin tức", "Mua sắm"].map((tab, i) => (
                <div key={tab} style={{ padding: "10px 0 9px", color: i ? G.sub : G.text, fontWeight: i ? 400 : 500, borderBottom: i ? "none" : `3px solid ${G.text}` }}>
                  {tab}
                </div>
              ))}
            </div>

            {/* Tổng quan do AI */}
            <div style={{ padding: "18px 18px 14px", opacity: ai }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 16, fontWeight: 500 }}>
                {Icon.sparkle()}
                Tổng quan do AI
              </div>
              <div style={{ marginTop: 12, fontSize: 16, lineHeight: "24px", minHeight: 144 }}>
                {words.slice(0, shown).map((x, i) => (
                  <span key={i} style={{ fontWeight: x.bold ? 500 : 400 }}>
                    {x.w}{" "}
                  </span>
                ))}
              </div>
              <div
                style={{
                  marginTop: 12,
                  opacity: more,
                  height: 40,
                  borderRadius: 20,
                  background: G.field,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 6,
                  fontSize: 14,
                  fontWeight: 500,
                }}
              >
                Hiện thêm {Icon.chevron(G.text)}
              </div>
            </div>
            <div style={{ height: 8, background: "#151515", opacity: ai }} />

            {/* Kết quả tự nhiên: bài thật của Adtek */}
            <div style={{ padding: "16px 18px", opacity: dim }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ width: 28, height: 28, borderRadius: 14, background: "#fff", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Img src={staticFile("logo-adtek.png")} style={{ width: 18 }} />
                </div>
                <div>
                  <div style={{ fontSize: 14, color: G.text }}>{c.result.site}</div>
                  <div style={{ fontSize: 12, color: G.faint }}>{c.result.url}</div>
                </div>
              </div>
              <div style={{ marginTop: 10, fontSize: 20, lineHeight: "26px", color: G.link }}>{c.result.title}</div>
              <div style={{ marginTop: 6, fontSize: 14, lineHeight: "22px", color: G.sub }}>{c.result.snippet}</div>
            </div>
            <div style={{ height: 8, background: "#151515", opacity: ai }} />

            {/* Mọi người cũng hỏi */}
            <div style={{ padding: "16px 18px", opacity: dim }}>
              <div style={{ fontSize: 18, fontWeight: 500, marginBottom: 6 }}>Mọi người cũng hỏi</div>
              {c.questions.map((q) => (
                <div key={q} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 0", borderBottom: `1px solid ${G.line}`, fontSize: 15 }}>
                  {q}
                  {Icon.chevron(G.faint)}
                </div>
              ))}
            </div>
          </div>
    </Phone>
  );
};

export const SERP_NOTE_AT = T.dim;

// Chú thích kiểu McKinsey đặt ngoài điện thoại: đường kẻ ngắn + phần chữ đậm + phần chữ thường.
export const PhoneNote: React.FC<{ top: number; left: number; note: [string, string]; at: number }> = ({ top, left, note, at }) => {
  const f = useFrame();
  const draw = interpolate(f, [at, at + 12], [0, 1], { ...clamp, easing: ease });
  const txt = interpolate(f, [at + 8, at + 18], [0, 1], clamp);
  return (
    <div style={{ position: "absolute", left, top, width: 290, color: C.white, fontFamily: SANS }}>
      <div style={{ height: 2, width: 40 * draw, background: C.white, position: "absolute", left: -48, top: 16 }} />
      <div style={{ fontSize: 26, lineHeight: 1.35, opacity: txt }}>
        <b>{note[0]}</b> {note[1]}
      </div>
    </div>
  );
};
