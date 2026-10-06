// Kịch bản một video: scripts/<slug>/<số>.json.
// Mỗi cảnh: dòng dẫn nhỏ (kicker), tiêu đề 2 dòng (headline trắng + accent cam), lời đọc (voice, cũng là phụ đề)
// và một hình minh họa (visual). Không có visual thì cảnh là câu chốt, tiêu đề lớn hơn.

// "step" của cột/thanh/chú thích: 0 = hiện ở cảnh này, 1 = hiện ở cảnh kế tiếp (cảnh đó dùng visual "continue").
type Step = { step?: number };
export type Tone = "base" | "main" | "accent"; // nhóm đối chiếu, nhóm chính, điểm nhấn duy nhất

export type ChartNote =
  | ({ kind: "drop"; from: number; to: number; text: string } & Step) // mũi tên từ cột cao xuống cột thấp
  | ({ kind: "callout"; at: number; text: string } & Step); // chữ đậm + đường dẫn trên một cột/thanh

export type Visual =
  | {
      type: "serp"; // màn hình Google trên điện thoại
      query: string;
      answer: { text: string; bold?: boolean }[];
      result: { site: string; url: string; title: string; snippet: string };
      questions: string[];
      note: [string, string]; // chú thích ngoài điện thoại: phần đậm + phần thường
    }
  | {
      type: "chat"; // màn hình chatbot trên điện thoại, hỏi 2 lần ra 2 câu trả lời khác nhau
      question: string;
      answers: [string[], string[]]; // mô tả từng mục, tên thương hiệu luôn bị làm mờ
      note: [string, string];
    }
  | {
      type: "columns";
      metric: string;
      unit: string;
      source: string;
      max: number;
      cols: ({ label: string; value: number; display?: string; tone: Tone } & Step)[];
      notes?: ChartNote[];
    }
  | {
      type: "hbars";
      metric: string;
      unit: string;
      source: string;
      max: number;
      rows: ({ label: string; value: number; display?: string; tone: Tone } & Step)[];
      notes?: ChartNote[];
    }
  | { type: "waffle"; metric: string; unit: string; source: string; lit: number; legend: [string, string] }
  | { type: "list"; items: string[] }
  | { type: "article"; image: string; title: string; url: string } // thẻ bài blog ở cảnh cuối
  | { type: "continue" }; // giữ biểu đồ của cảnh trước, hiện thêm phần có step tương ứng

export type Scene = { kicker: string; headline: string; accent: string; voice: string; visual?: Visual };

export type Script = {
  id: string;
  post_url: string;
  caption: string;
  hashtags: string[];
  music?: string | false; // nhạc nền trong public/, mặc định music/nhe-nhang.mp3, false để tắt
  scenes: Scene[];
};

// Kết quả của tools/voice.mjs: giọng đọc và thời điểm từng chữ cho mỗi cảnh.
export type Word = { text: string; start: number; end: number };
export type VoiceScene = { file: string; duration: number; words: Word[] };
export type Voice = { scenes: VoiceScene[] } | null;

export type VideoProps = { script: Script; voice: Voice };
