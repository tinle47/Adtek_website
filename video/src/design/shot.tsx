import React from "react";
import { Img, interpolate, staticFile } from "remotion";
import { C, SANS, clamp, ease, useFrame } from "./frame";

// Ảnh chụp thật bài báo hoặc báo cáo (tools/shot.mjs): khung trình duyệt, trang trượt dần tới câu có con số,
// bút dạ quang cam quét qua đúng con số, phần còn lại tối đi. Không phóng to cắt chữ, không sửa nội dung ảnh.
type Rect = { x: number; y: number; w: number; h: number };
const W = 900;
const BAR = 54; // thanh địa chỉ
const VIEW = 450; // chiều cao vùng xem ảnh

const prog = (f: number, at: number, len: number) => interpolate(f - at, [0, len], [0, 1], { ...clamp, easing: ease });

export const Shot: React.FC<{ image: string; width: number; height: number; highlight: Rect[]; url: string; source: string; note?: string }> = ({
  image, width, height, highlight, url, source, note,
}) => {
  const f = useFrame();
  const enter = prog(f, 0, 14);
  const pan = prog(f, 6, 40);
  const spot = prog(f, 58, 14);
  const s = W / width;
  const hy = Math.min(...highlight.map((r) => r.y));
  const hy2 = Math.max(...highlight.map((r) => r.y + r.h));
  // Trang trượt lên: câu có con số đi từ 72% xuống 42% chiều cao khung.
  const want = (k: number) => VIEW * k - ((hy + hy2) / 2) * s;
  const top = Math.min(0, Math.max(VIEW - height * s, interpolate(pan, [0, 1], [want(0.72), want(0.42)])));
  const ux = Math.min(...highlight.map((r) => r.x)), ux2 = Math.max(...highlight.map((r) => r.x + r.w));
  const domain = url.replace(/^https?:\/\//, "").split("/")[0].replace(/^www\./, "");
  return (
    <div style={{ width: W, fontFamily: SANS, opacity: enter, transform: `translateY(${(1 - enter) * 30}px)` }}>
      <div style={{ borderRadius: 18, overflow: "hidden", background: "#fff", boxShadow: "0 24px 60px rgba(0,0,0,0.35)" }}>
        <div style={{ height: BAR, background: "#EEF1F6", display: "flex", alignItems: "center", gap: 14, padding: "0 22px" }}>
          {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => (
            <div key={c} style={{ width: 13, height: 13, borderRadius: 7, background: c }} />
          ))}
          <div style={{ flex: 1, marginLeft: 12, height: 34, borderRadius: 17, background: "#fff", display: "flex", alignItems: "center", padding: "0 18px", fontSize: 21, color: "#3C4656" }}>
            {domain}
          </div>
        </div>
        <div style={{ position: "relative", width: W, height: VIEW, overflow: "hidden" }}>
          <div style={{ position: "absolute", left: 0, top, width: W, height: height * s }}>
            <Img src={staticFile(image)} style={{ width: "100%", height: "100%", display: "block" }} />
            <div
              style={{
                position: "absolute",
                left: ux * s - 10,
                top: hy * s - 8,
                width: (ux2 - ux) * s + 20,
                height: (hy2 - hy) * s + 16,
                borderRadius: 8,
                boxShadow: `0 0 0 3000px rgba(0,22,60,${0.5 * spot})`,
              }}
            />
            {highlight.map((r, i) => {
              const sweep = prog(f, 44 + i * 10, 14);
              return (
                <div
                  key={i}
                  style={{
                    position: "absolute",
                    left: r.x * s - 4,
                    top: r.y * s - 2,
                    width: (r.w * s + 8) * sweep,
                    height: r.h * s + 4,
                    background: "rgba(255,144,20,0.38)",
                    borderBottom: `4px solid ${C.orange}`,
                    mixBlendMode: "multiply",
                  }}
                />
              );
            })}
          </div>
        </div>
      </div>
      {note && (
        <div style={{ marginTop: 24, fontSize: 30, fontWeight: 700, color: C.white, opacity: prog(f, 62, 12), borderLeft: `3px solid ${C.orange}`, paddingLeft: 18 }}>{note}</div>
      )}
      <div style={{ marginTop: 16, fontSize: 19, color: C.muted, opacity: prog(f, 20, 12) }}>{source}</div>
    </div>
  );
};
