import React from "react";
import { Composition } from "remotion";
import sample from "../scripts/aio-la-gi/1.json";
import { FPS, totalFrames } from "./timing";
import type { Script, VideoProps } from "./types";
import { Video } from "./Video";
import { Preview, previewFrames } from "./preview/Preview";
import type { ThemeId } from "./preview/themes";
import { Combo, comboFrames } from "./preview/Combo";

// Một khuôn video dọc 1080x1920. Kịch bản và giọng đọc truyền vào qua props (tools/render.mjs).
export const Root: React.FC = () => (
  <>
  <Composition
    id="Infographic"
    component={Video}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={300}
    defaultProps={{ script: sample as Script, voice: null } satisfies VideoProps}
    calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props) })}
  />
  {/* 3 hướng thiết kế để chọn, cùng nội dung demo */}
  {(["glow", "editorial", "data"] as ThemeId[]).map((theme) => (
    <Composition
      key={theme}
      id={`Preview-${theme}`}
      component={Preview}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={previewFrames() + 10}
      defaultProps={{ theme }}
    />
  ))}
  {/* Hướng A + C, biểu đồ chuẩn McKinsey vẽ trên navy, thử 3 font có chân cho tiêu đề */}
  {(["playfair", "source", "noto"] as const).map((serif) => (
    <Composition
      key={serif}
      id={`Combo-${serif}`}
      component={Combo}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={comboFrames()}
      defaultProps={{ variant: "dark" as const, serif }}
    />
  ))}
  </>
);
