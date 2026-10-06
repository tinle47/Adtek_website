import "@fontsource/noto-serif-display/600.css";
import "@fontsource/playfair-display/600.css";
import "@fontsource/source-serif-4/600.css";
import React, { useEffect, useState } from "react";
import { AbsoluteFill, Img, continueRender, delayRender, staticFile } from "remotion";
import { useEnter } from "../components";
import { FONT } from "../theme";

// Khung sạch cho hướng A + C: nền navy phẳng, chỉ có logo, tiêu đề font có chân căn trái, không hiệu ứng phát sáng.
export const SERIFS = {
  playfair: '"Playfair Display", serif',
  source: '"Source Serif 4", serif',
  noto: '"Noto Serif Display", serif',
};
export type SerifId = keyof typeof SERIFS;

export const L = { pad: 90, logo: 150, head: 300, stage: 660, caption: 1350 };
const NAVY = "#002D72";
const ORANGE = "#FF9014";

export const useSerif = (id: SerifId) => {
  const [handle] = useState(() => delayRender(`Tải font ${id}`));
  useEffect(() => {
    document.fonts.load(`600 60px ${SERIFS[id]}`, "Tiếng Việt ăâđêôơư").then(() => continueRender(handle));
  }, [handle, id]);
};

export const CleanBackground: React.FC = () => (
  <AbsoluteFill style={{ background: `linear-gradient(180deg, ${NAVY} 0%, #00225A 100%)` }} />
);

export const Logo: React.FC = () => (
  <Img src={staticFile("logo-white.png")} style={{ position: "absolute", left: L.pad, top: L.logo, height: 54 }} />
);

export const SiteFooter: React.FC = () => (
  <div style={{ position: "absolute", right: L.pad, top: 1800, fontFamily: FONT, fontSize: 22, fontWeight: 600, letterSpacing: 1, color: "#8FA3C4" }}>
    adtek.agency
  </div>
);

// Tiêu đề 2 dòng: dòng thường màu trắng, dòng nhấn màu cam phẳng. Hiện dần theo dòng, không làm mờ, không phát sáng.
export const SerifHeadline: React.FC<{ serif: SerifId; kicker: string; headline: string; accent: string }> = ({
  serif,
  kicker,
  headline,
  accent,
}) => {
  const k = useEnter(0);
  const a = useEnter(4);
  const b = useEnter(10);
  const line = (p: number, color: string, text: string) => (
    <div
      style={{
        fontFamily: SERIFS[serif],
        fontWeight: 600,
        fontSize: 64,
        lineHeight: 1.16,
        letterSpacing: -0.5,
        color,
        textWrap: "pretty",
        opacity: p,
        transform: `translateY(${(1 - p) * 18}px)`,
      }}
    >
      {text}
    </div>
  );
  return (
    <div style={{ position: "absolute", left: L.pad, right: L.pad, top: L.head }}>
      <div style={{ fontFamily: FONT, fontSize: 22, fontWeight: 600, letterSpacing: 3, textTransform: "uppercase", color: "#8FA3C4", marginBottom: 22, opacity: k }}>
        {kicker}
      </div>
      {line(a, "#FFFFFF", headline)}
      {line(b, ORANGE, accent)}
    </div>
  );
};
