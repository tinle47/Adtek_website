import type React from "react";

// 3 hướng thiết kế cho cùng một bộ cảnh. Chỉ khác màu, nền, kiểu thẻ và kiểu phụ đề.
export type ThemeId = "glow" | "editorial" | "data";

export type Theme = {
  id: ThemeId;
  name: string;
  dark: boolean;
  text: string;
  accent: string;
  muted: string;
  dim: string; // chấm, thanh, đường kẻ ở trạng thái chưa nhấn
  line: string;
  align: "center" | "left";
  glow: boolean;
  card: React.CSSProperties;
  chip: React.CSSProperties;
  tag: React.CSSProperties; // nhãn series góc phải trên
  caption: "plain" | "pill" | "highlight";
};

const ORANGE = "#FF9014";

export const THEMES: Record<ThemeId, Theme> = {
  // Từ Khoa ADS, Phương Thảo Analytics: nền tối, điểm sáng phát quang, nét mảnh.
  glow: {
    id: "glow",
    name: "Navy Glow",
    dark: true,
    text: "#FFFFFF",
    accent: ORANGE,
    muted: "#9FB3D6",
    dim: "rgba(159,179,214,0.22)",
    line: "rgba(159,179,214,0.28)",
    align: "center",
    glow: true,
    card: {
      border: "1.5px solid rgba(255,144,20,0.55)",
      background: "rgba(0,18,56,0.55)",
      borderRadius: 28,
      boxShadow: "0 0 60px rgba(255,144,20,0.18), inset 0 0 40px rgba(255,144,20,0.05)",
    },
    chip: { border: "1.5px solid rgba(159,179,214,0.4)", color: "#D6E2F5", background: "transparent" },
    tag: { border: "1.5px solid rgba(255,144,20,0.6)", color: ORANGE, background: "rgba(255,144,20,0.08)" },
    caption: "plain",
  },
  // Từ Tổng Tài AI, Origin AI: nền kem, thẻ trắng, chữ navy, điểm nhấn cam.
  editorial: {
    id: "editorial",
    name: "Editorial Cream",
    dark: false,
    text: "#0B1B3F",
    accent: "#F07C00",
    muted: "#5B6475",
    dim: "rgba(0,45,114,0.12)",
    line: "rgba(0,45,114,0.14)",
    align: "left",
    glow: false,
    card: {
      background: "#FFFFFF",
      borderRadius: 28,
      boxShadow: "0 24px 60px rgba(0,45,114,0.10), 0 2px 8px rgba(0,45,114,0.05)",
    },
    chip: { background: "rgba(240,124,0,0.10)", color: "#C46200", border: "none" },
    tag: { background: "#F07C00", color: "#FFFFFF", border: "none" },
    caption: "pill",
  },
  // Từ Visual Capitalist, Barron's: nền giấy kẻ ô, một biểu đồ xuyên suốt, phụ đề tô nền.
  data: {
    id: "data",
    name: "Data Story",
    dark: false,
    text: "#0B1B3F",
    accent: "#F07C00",
    muted: "#5B6475",
    dim: "rgba(0,45,114,0.16)",
    line: "rgba(0,45,114,0.25)",
    align: "center",
    glow: false,
    card: {},
    chip: { background: "#002D72", color: "#FFFFFF", border: "none" },
    tag: { background: "#002D72", color: "#FFFFFF", border: "none" },
    caption: "highlight",
  },
};
