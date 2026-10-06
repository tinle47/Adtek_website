import React from "react";
import { Composition } from "remotion";
import sample from "../scripts/aio-la-gi/1.json";
import { FPS, totalFrames } from "./timing";
import type { Script, VideoProps } from "./types";
import { Video } from "./Video";

// Một khuôn video dọc 1080x1920. Kịch bản và giọng đọc truyền vào qua props (tools/render.mjs).
export const Root: React.FC = () => (
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
);
