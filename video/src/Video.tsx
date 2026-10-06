import "@fontsource/be-vietnam-pro/400.css";
import "@fontsource/be-vietnam-pro/600.css";
import "@fontsource/be-vietnam-pro/700.css";
import "@fontsource/be-vietnam-pro/800.css";
import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, Sequence, continueRender, delayRender, staticFile } from "remotion";
import { Background, Brand, Captions, Progress } from "./components";
import { SceneView } from "./scenes";
import { timeline } from "./timing";
import type { VideoProps } from "./types";

// Chờ font tiếng Việt tải xong rồi mới chụp khung hình, tránh khung đầu bị font dự phòng.
const useFonts = () => {
  const [handle] = useState(() => delayRender("Tải font Be Vietnam Pro"));
  useEffect(() => {
    const sample = "Tiếng Việt ăâđêôơư";
    Promise.all([400, 600, 700, 800].map((w) => document.fonts.load(`${w} 40px "Be Vietnam Pro"`, sample))).then(() =>
      continueRender(handle),
    );
  }, [handle]);
};

export const Video: React.FC<VideoProps> = (props) => {
  useFonts();
  const scenes = timeline(props);
  return (
    <AbsoluteFill>
      <Background />
      {props.script.scenes.map((scene, i) => (
        <Sequence key={i} from={scenes[i].from} durationInFrames={scenes[i].frames}>
          <SceneView scene={scene} frames={scenes[i].frames} />
          <Captions words={scenes[i].words} />
          {scenes[i].audio && <Audio src={staticFile(scenes[i].audio!)} />}
        </Sequence>
      ))}
      <Brand />
      <Progress scenes={scenes} />
    </AbsoluteFill>
  );
};
