import React from "react";
import { Composition, Still } from "remotion";
import { LAYOUTS } from "./design/frame";
import { Cover } from "./design/hook";
import sample from "../scripts/aio-la-gi/1.json";
import { FPS, totalFrames } from "./timing";
import type { Script, VideoProps } from "./types";
import { Video } from "./Video";

// Một khuôn video dọc 1080x1920. Kịch bản và giọng đọc truyền vào qua props (tools/render.mjs).
const CoverStill: React.FC<VideoProps> = ({ script }) => {
  const c = script.cover ?? { title: script.scenes[0].headline, accent: script.scenes[0].accent };
  return <Cover title={c.title} accent={c.accent} kicker={c.kicker} options={c.options} />;
};

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
    calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props), fps: props.fps ?? FPS, width: LAYOUTS[props.format ?? "9:16"].w, height: LAYOUTS[props.format ?? "9:16"].h })}
  />
  {/* Ảnh bìa riêng cho từng video (out/<id>-cover.png). */}
  <Still id="Cover" component={CoverStill} width={1080} height={1920} defaultProps={{ script: sample as Script, voice: null } satisfies VideoProps} />
  </>
);
