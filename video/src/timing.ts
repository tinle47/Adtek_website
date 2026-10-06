import type { VideoProps, Word } from "./types";

export const FPS = 30;
const GAP = 0.35; // nghỉ sau mỗi câu, giây
const SEC_PER_WORD = 0.3; // tốc độ đọc ước tính khi chưa có giọng thật
const MIN_SCENE = 2.5;

export type TimedScene = { from: number; frames: number; words: Word[]; audio?: string };

// Chưa có giọng thật thì chia đều thời gian cho từng chữ để phụ đề vẫn chạy.
function estimateWords(text: string): { words: Word[]; duration: number } {
  const tokens = text.split(/\s+/).filter(Boolean);
  const duration = Math.max(MIN_SCENE - GAP, tokens.length * SEC_PER_WORD);
  const step = duration / tokens.length;
  return {
    duration,
    words: tokens.map((t, i) => ({ text: t, start: i * step, end: (i + 1) * step })),
  };
}

export function timeline({ script, voice }: VideoProps): TimedScene[] {
  let from = 0;
  return script.scenes.map((scene, i) => {
    const v = voice?.scenes[i];
    const { words, duration } = v ?? estimateWords(scene.voice);
    const frames = Math.round(Math.max(MIN_SCENE, duration + GAP) * FPS);
    const timed = { from, frames, words, audio: v?.file };
    from += frames;
    return timed;
  });
}

export const totalFrames = (props: VideoProps) =>
  timeline(props).reduce((sum, s) => sum + s.frames, 0);
