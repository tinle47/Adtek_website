import type { Scene, VideoProps, Word } from "./types";

export const FPS = 30; // mặc định; kịch bản xuất 60 hình/giây truyền fps qua props
const GAP = 0.25; // nghỉ sau mỗi câu, giây
const SEC_PER_WORD = 0.3; // tốc độ đọc ước tính khi chưa có giọng thật
const MIN_SCENE = 2.5;
// Màn hình điện thoại có diễn biến riêng (gõ, trả lời, cuộn, chú thích) nên cần tối thiểu từng này giây.
const MIN_BY_VISUAL: Record<string, number> = { serp: 5.5, chat: 6 };

// from, frames tính theo khung thật của video. lead: số khung (đơn vị 30 hình/giây) chờ trước khi giọng bắt đầu.
export type TimedScene = { from: number; frames: number; words: Word[]; audio?: string; lead: number };

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

const minSeconds = (scene: Scene) => MIN_BY_VISUAL[scene.visual?.type ?? ""] ?? MIN_SCENE;
// Cảnh lật đáp án đố số liệu: giọng chờ đến sau tiếng "ding" (khớp QUIZ_VOICE_AT trong design/hook.tsx).
export const leadFrames = (scene: Scene) => (scene.visual?.type === "quiz" && scene.visual.reveal ? 27 : 0);

export function timeline({ script, voice, fps = FPS }: VideoProps): TimedScene[] {
  let from = 0;
  return script.scenes.map((scene, i) => {
    const v = voice?.scenes[i];
    const { words, duration } = v ?? estimateWords(scene.voice);
    const lead = leadFrames(scene);
    const frames = Math.round((Math.max(minSeconds(scene), duration + GAP) + lead / FPS) * fps);
    const timed = { from, frames, words, audio: v?.file, lead };
    from += frames;
    return timed;
  });
}

export const totalFrames = (props: VideoProps) =>
  timeline(props).reduce((sum, s) => sum + s.frames, 0) + Math.round(10 * (props.fps ?? FPS) / FPS);
