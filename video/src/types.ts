// Kịch bản một video: scripts/<slug>/<số>.json.
// Mỗi cảnh: dòng dẫn nhỏ (kicker), tiêu đề 2 dòng (headline trắng + accent cam), lời đọc (voice, cũng là phụ đề)
// và một hình minh họa (visual). Không có visual thì cảnh là câu chốt, tiêu đề lớn hơn.

// "step" của cột/thanh/chú thích: 0 = hiện ở cảnh này, 1 = hiện ở cảnh kế tiếp (cảnh đó dùng visual "continue").
type Step = { step?: number };
export type Tone = "base" | "main" | "accent"; // nhóm đối chiếu, nhóm chính, điểm nhấn duy nhất

export type ChartNote =
  | ({ kind: "drop"; from: number; to: number; text: string } & Step) // mũi tên từ cột cao xuống cột thấp
  | ({ kind: "callout"; at: number; text: string } & Step); // chữ đậm + đường dẫn trên một cột/thanh

type VsItem = { label: string; value: number; display?: string; suffix?: string };

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
  | { type: "list"; items: (string | { text: string; detail?: string })[]; source?: string } // việc cần làm, mỗi việc có căn cứ
  // Chọn biểu đồ theo kiểu dữ liệu (xem README): mỗi loại có hiệu ứng riêng.
  | { type: "bignumber"; value: number; display?: string; prefix?: string; suffix?: string; label: string; context?: string; source: string } // 1 con số gây sốc
  | { type: "versus"; metric: string; unit?: string; source: string; items: [VsItem, VsItem]; winner: 0 | 1; note?: string } // 2 con số đối đầu
  | { type: "slope"; metric: string; unit?: string; source: string; from: string; to: string; series: { label: string; a: number; b: number; display?: [string, string]; tone: Tone }[]; min?: number } // trước và sau, 1 đến 3 nhóm
  | { type: "trend"; metric: string; unit?: string; source: string; points: { label: string; value: number; display?: string }[]; min?: number; note?: string } // xu hướng 3 mốc trở lên
  | { type: "donut"; metric: string; unit?: string; source: string; parts: { label: string; value: number; display?: string; tone: Tone }[]; center?: string; centerLabel?: string } // các phần trong một tổng
  | { type: "people"; metric: string; unit?: string; source: string; lit: number; legend: [string, string] } // x trên 10 người
  | { type: "funnel"; metric: string; unit?: string; source: string; stages: { label: string; value: number; display?: string }[] } // rơi rụng qua từng bước
  | { type: "article"; image: string; title: string; url: string } // thẻ bài blog (không dùng cho kênh TikTok độc lập)
  | { type: "shot"; image: string; width: number; height: number; highlight: { x: number; y: number; w: number; h: number }[]; url: string; source: string; note?: string } // ảnh chụp thật bài báo, báo cáo (tools/shot.mjs)
  | { type: "quiz"; options: { label: string; text: string }[]; answer: number; reveal?: boolean; tag?: string; note?: string; source?: string } // đố số liệu: hỏi ở cảnh đầu, cảnh sau reveal: true để lật đáp án
  | { type: "myth"; claim: string; verdict: string; note?: string; source?: string } // phá hiểu lầm: câu nhiều người tin, đóng dấu
  | { type: "follow"; note?: string; ask?: string } // ask: câu hỏi kêu gọi bình luận // cảnh cuối kêu gọi theo dõi kênh
  | { type: "continue" }; // giữ biểu đồ của cảnh trước, hiện thêm phần có step tương ứng

export type Scene = { kicker: string; headline: string; accent: string; voice: string; visual?: Visual };

export type Script = {
  id: string;
  cover?: { title: string; accent: string; kicker?: string; options?: string[] }; // ảnh bìa 3 đến 5 chữ; video đố số liệu thì là câu hỏi + lựa chọn, không lộ đáp án
  post_url?: string; // bài blog liên quan nếu có, không đưa vào caption
  caption: string;
  hashtags: string[];
  scenes: Scene[];
};

// Kết quả của tools/voice.mjs: giọng đọc và thời điểm từng chữ cho mỗi cảnh.
export type Word = { text: string; start: number; end: number };
export type VoiceScene = { file: string; duration: number; words: Word[] };
export type Voice = { scenes: VoiceScene[] } | null;

export type VideoProps = { script: Script; voice: Voice };
