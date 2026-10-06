// Kịch bản một video: scripts/<slug>/<số>.json. Mỗi cảnh có "voice" là lời đọc (cũng là phụ đề).
export type Scene =
  | { type: "hook"; voice: string; kicker?: string; title: string; highlight?: string }
  | { type: "stat"; voice: string; value: string; label: string; source?: string }
  | {
      type: "compare";
      voice: string;
      title?: string;
      left: { value: string; label: string };
      right: { value: string; label: string };
      source?: string;
    }
  | {
      type: "bars";
      voice: string;
      title: string;
      items: { label: string; value: number; display?: string }[];
      source?: string;
    }
  | { type: "list"; voice: string; title: string; items: string[] }
  | { type: "statement"; voice: string; text: string; highlight?: string }
  | { type: "cta"; voice: string; title: string; action: string };

export type Script = {
  id: string;
  post_url: string;
  caption: string;
  hashtags: string[];
  scenes: Scene[];
};

// Kết quả của tools/voice.mjs: giọng đọc và thời điểm từng chữ cho mỗi cảnh.
export type Word = { text: string; start: number; end: number };
export type VoiceScene = { file: string; duration: number; words: Word[] };
export type Voice = { scenes: VoiceScene[] } | null;

export type VideoProps = { script: Script; voice: Voice };
