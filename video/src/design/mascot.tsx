import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BASE_FPS } from "./frame";

// Mèo Adtek ở góc trái, miệng mở theo độ to của giọng đọc (không khớp từng âm, kiểu nhân vật ảo của streamer).
// 5 hình cùng một thân, chỉ khác miệng (public/mascot): m0 ngậm, m4 hé, m1 cười hé, m3 tròn chữ "o", m2 mở to.
// env: độ to giọng đọc của từng cảnh, 30 giá trị mỗi giây, từ 0 (im) tới 1 (to nhất); render.mjs --mascot đo sẵn.
export const MASCOT = { left: 24, top: 1224, height: 278 }; // ngay trên vùng tên kênh và caption của TikTok (dưới 1500)
const SPRITES = ["m0", "m4", "m1", "m3", "m2"];

export type MascotTrack = { from: number; lead: number; env: number[] }; // from, lead tính theo khung thật của video

export const Mascot: React.FC<{ tracks: MascotTrack[] }> = ({ tracks }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = fps / BASE_FPS;
  // Cảnh đang chạy và vị trí trong lời đọc (đơn vị 30 hình/giây). Đổi miệng mỗi 2 khung để không nhấp nháy.
  const tr = [...tracks].reverse().find((t) => f >= t.from + t.lead);
  const t30 = tr ? Math.floor((f - tr.from - tr.lead) / k / 2) * 2 : -1;
  const v = tr && t30 >= 0 && t30 < tr.env.length ? Math.max(tr.env[t30], tr.env[t30 + 1] ?? 0) : 0;
  const syll = Math.floor(t30 / 6) % 2; // đổi qua lại 2 kiểu miệng vừa để đỡ đơn điệu
  const mouth = v < 0.15 ? 0 : v < 0.4 ? 1 : v < 0.68 ? (syll ? 3 : 2) : 4;
  // Thở nhẹ và nhún đầu khi nói để nhân vật không đứng im.
  const bob = Math.sin(f / k / 18) * 4 + (mouth ? -3 * v : 0);
  const breathe = 1 + Math.sin(f / k / 24) * 0.012;
  const w = (MASCOT.height * 348) / 486;
  return (
    <div data-audit="skip" style={{ position: "absolute", left: MASCOT.left, top: MASCOT.top, width: w, height: MASCOT.height }}>
      <div style={{ position: "absolute", left: w * 0.12, right: w * 0.12, bottom: -6, height: 22, borderRadius: "50%", background: "rgba(0,0,0,0.28)", filter: "blur(6px)" }} />
      <div style={{ position: "absolute", inset: 0, transform: `translateY(${bob}px) scale(${breathe})`, transformOrigin: "50% 100%" }}>
        {SPRITES.map((s, i) => (
          <Img key={s} src={staticFile(`mascot/${s}.png`)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: i === mouth ? 1 : 0 }} />
        ))}
      </div>
    </div>
  );
};
