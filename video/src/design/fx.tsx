import gsap from "gsap";
import React, { useMemo } from "react";
import { Lottie, type LottieAnimationData } from "@remotion/lottie";
import { Sequence, useVideoConfig } from "remotion";
import check from "../data/check-lottie.json";
import { BASE_FPS, C, SANS, SERIF, useEnter, useFrame, useLayout } from "./frame";

// Hiệu ứng thử nghiệm (render.mjs --fx, anh Tin chọn phương án 2 ngày 17/10/2026). Bản thường không dùng file này.
// GSAP ở đây chỉ làm "bộ tính đường cong": dựng một timeline dừng sẵn (paused) trên các đối tượng số thường,
// mỗi khung hình tua tới đúng giây của khung đó (seek) rồi đọc giá trị ra. Không để GSAP tự chạy theo đồng hồ thật,
// vì Remotion chụp từng khung riêng lẻ; tua tuyệt đối nên khung nào cũng ra đúng một kết quả.
const useStagger = (count: number, startFrame: number, stagger: number, duration: number, ease: string) => {
  const f = useFrame();
  const tl = useMemo(() => {
    const states = Array.from({ length: count }, () => ({ p: 0 }));
    const t = gsap.timeline({ paused: true });
    t.to(states, { p: 1, duration, ease, stagger }, startFrame / BASE_FPS);
    return { t, states };
  }, [count, startFrame, stagger, duration, ease]);
  tl.t.seek(Math.max(0, f / BASE_FPS), true);
  return tl.states.map((s) => s.p);
};

// Tiêu đề 2 dòng như Headline (frame.tsx) nhưng từng chữ trồi lên lần lượt; dòng cam bật nảy sau dòng trắng.
export const FxHeadline: React.FC<{ kicker: string; headline: string; accent: string; big?: boolean }> = ({ kicker, headline, accent, big }) => {
  const k = useEnter(0);
  const { head } = useLayout();
  const hw = headline ? headline.split(/\s+/) : [];
  const aw = accent ? accent.split(/\s+/) : [];
  const hp = useStagger(hw.length, 3, 0.045, 0.5, "back.out(1.6)");
  const ap = useStagger(aw.length, 3 + hw.length * 1.35 + 4, 0.05, 0.6, "back.out(2.2)");
  if (!headline && !accent && !kicker) return null;
  const line = (words: string[], ps: number[], color: string, pop: boolean) => (
    <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: big ? head.bigSize : head.size, lineHeight: 1.16, letterSpacing: -0.5, color }}>
      {words.map((w, i) => {
        const p = ps[i];
        return (
          <React.Fragment key={i}>
            <span
              style={{
                display: "inline-block",
                opacity: Math.min(1, Math.max(0, p * 1.6)),
                transform: `translateY(${(1 - p) * 34}px) scale(${pop ? 0.82 + 0.18 * p : 1})`,
                transformOrigin: "50% 80%",
              }}
            >
              {w}
            </span>
            {i < words.length - 1 ? " " : ""}
          </React.Fragment>
        );
      })}
    </div>
  );
  return (
    <div style={{ position: "absolute", left: head.left, width: head.width, top: big ? head.bigTop : head.top }}>
      <div style={{ fontFamily: SANS, fontSize: 22, fontWeight: 600, letterSpacing: 3, textTransform: "uppercase", color: C.muted, marginBottom: big ? 32 : 22, opacity: k }}>
        {kicker}
      </div>
      {line(hw, hp, C.white, false)}
      {big && <div style={{ height: 18 }} />}
      {line(aw, ap, C.orange, true)}
    </div>
  );
};

// Dấu tích vẽ dần (vòng cam rồi nét tích trắng) thay cho số thứ tự ở cảnh "Làm gì ngay".
// File Lottie tự vẽ (src/data/check-lottie.json, 24 khung ở 30 hình/giây), không lấy của bên thứ ba nên không vướng giấy phép.
// delay: khung (30 hình/giây) lúc việc đó hiện.
export const CheckMark: React.FC<{ delay: number; size?: number }> = ({ delay, size = 58 }) => {
  const { fps } = useVideoConfig();
  return (
    <div style={{ width: size, height: size, flex: "none", alignSelf: "flex-start" }}>
      <Sequence from={Math.round((delay * fps) / BASE_FPS)} layout="none">
        <Lottie animationData={check as LottieAnimationData} loop={false} style={{ width: size, height: size }} />
      </Sequence>
    </div>
  );
};
