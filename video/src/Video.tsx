import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useVideoConfig } from "remotion";
import { Audit } from "./design/audit";
import { Article, Follow, List, listDelays } from "./design/blocks";
import { BarChart, ColumnChart, Exhibit, Waffle, type TimedCol, type TimedNote } from "./design/charts";
import { BigNumber, Donut, Funnel, People, Slope, Trend, Versus } from "./design/charts2";
import { CHAT_NOTE_AT, ChatScreen } from "./design/chat";
import { BASE_FPS, Background, C, Caption, CueContext, Fade, Headline, LAYOUTS, LayoutContext, Logo, SANS, SiteFooter, clamp, cueTime, numbersIn, useFonts, useFrame, useLayout } from "./design/frame";
import { Shot } from "./design/shot";
import { Countdown, Race, SeaMap, Words, countdownCues, mapCues, raceCues, wordsCues } from "./design/formats";
import { Myth, QUIZ_REVEAL_AT, Quiz, mythStampAt } from "./design/hook";
import { GoogleSerp, PhoneNote, SERP_NOTE_AT } from "./design/serp";
import { timeline, type TimedScene } from "./timing";
import type { Scene, VideoProps, Visual, Word } from "./types";

const PHONE_H = 600;
// Cảnh đầu hiện sẵn trạng thái cuối của hiệu ứng: khung đầu tiên (cũng là ảnh bìa mặc định) đã có con số và câu hook.
const HOOK = 75;
const sfx = (name: string) => staticFile(`sfx/${name}.mp3`);
// Khung (tính từ đầu cảnh) lúc con số chính hiện ra, để đặt tiếng "bật".
const POP_AT: Partial<Record<Visual["type"], number>> = { bignumber: 34, versus: 40, people: 30, waffle: 40, donut: 30, slope: 30, trend: 30, funnel: 30, shot: 46 };
const NOTE = { left: 600, top: 350 }; // chú thích cạnh màn hình điện thoại, tính trong vùng hình

// Vùng hình minh họa: thiết kế gốc rộng 900px, mỗi khổ video đặt vị trí và thu nhỏ khác nhau.
const Stage: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => {
  const { stage } = useLayout();
  return (
    <div style={{ position: "absolute", left: stage.left, top: stage.top, width: 900, transform: `scale(${stage.scale})`, transformOrigin: "top left", ...style }}>
      {children}
    </div>
  );
};

type Chart = Extract<Visual, { type: "columns" | "hbars" }>;
type Group = { chart: Chart; first: number; last: number };

// Biểu đồ cột/thanh và các cảnh "continue" ngay sau nó tạo thành một nhóm: biểu đồ dựng một lần, cảnh sau chỉ thêm phần mới.
const chartGroups = (scenes: Scene[]): Group[] => {
  const groups: Group[] = [];
  scenes.forEach((s, i) => {
    const v = s.visual;
    if (v?.type === "columns" || v?.type === "hbars") groups.push({ chart: v, first: i, last: i });
    else if (v?.type === "continue" && groups.length && groups[groups.length - 1].last === i - 1) groups[groups.length - 1].last = i;
  });
  return groups;
};

// Mọi mốc trong ChartGroup tính theo 30 hình/giây (useFrame); k đổi sang khung thật cho Sequence.
const ChartGroup: React.FC<{ g: Group; sc: TimedScene[] }> = ({ g, sc: real }) => {
  const f = useFrame();
  const k = useVideoConfig().fps / BASE_FPS;
  const sc = real.map((s) => ({ ...s, from: s.from / k, frames: s.frames / k }));
  const shift = g.first === 0 ? HOOK : 0;
  const start = sc[g.first].from - shift;
  const end = sc[g.last].from + sc[g.last].frames;
  if (f < start || f > end) return null;
  const stepStart = (step = 0) => sc[Math.min(g.first + step, g.last)].from - (step === 0 ? shift : 0);
  const items = g.chart.type === "columns" ? g.chart.cols : g.chart.rows;
  // Phần tử cùng một bước hiện lần lượt cách nhau 12 frame.
  const order: Record<number, number> = {};
  // Thanh/cột hiện lúc giọng đọc tới giá trị của nó (cảnh đầu đang hiện sẵn trạng thái cuối thì giữ nhịp cũ).
  const voiceAt = (step: number, needle: number | undefined, fallback: number, after = -1) => {
    const idx = Math.min(g.first + step, g.last);
    if (idx === 0 || needle === undefined) return fallback;
    const start = sc[idx].from + sc[idx].lead;
    const t = cueTime(sc[idx].words, needle, (after - start) / BASE_FPS);
    return t === undefined ? fallback : Math.max(fallback, start + t * BASE_FPS - 2);
  };
  const timed: TimedCol[] = items.map((it) => {
    const step = it.step ?? 0;
    order[step] = (order[step] ?? -1) + 1;
    return { ...it, at: voiceAt(step, it.value, stepStart(step) + 6 + order[step] * 12) };
  });
  const lastAt = (step: number) => Math.max(...timed.filter((_, i) => (items[i].step ?? 0) === step).map((t) => t.at), stepStart(step));
  const notes: TimedNote[] = (g.chart.notes ?? []).map((n) => {
    const step = n.step ?? 0;
    const at = voiceAt(step, numbersIn(n.text)[0], lastAt(step) + 26, lastAt(step));
    return n.kind === "drop" ? { ...n, at } : { kind: "callout", target: n.at, text: n.text, at };
  });
  const o = interpolate(f, [end - 7, end], [1, 0], clamp);
  const pops = timed.filter((t) => t.at + 16 > 0).map((t, i) => (
    <Sequence key={i} from={Math.round((t.at + 16) * k)} durationInFrames={Math.round(10 * k)}>
      <Audio src={sfx("pop")} volume={0.32} />
    </Sequence>
  ));
  return (
    <>
    {pops}
    <Stage style={{ opacity: o }}>
      <Exhibit metric={g.chart.metric} unit={g.chart.unit} source={g.chart.source} appear={start}>
        {g.chart.type === "columns" ? (
          <ColumnChart cols={timed} max={g.chart.max} notes={notes} />
        ) : (
          <BarChart rows={timed} max={g.chart.max} notes={notes} />
        )}
      </Exhibit>
    </Stage>
    </>
  );
};

// Hình minh họa riêng của một cảnh (biểu đồ cột/thanh được vẽ ở ChartGroup).
const SceneVisual: React.FC<{ v?: Visual; frames: number }> = ({ v, frames }) => {
  if (!v) return null;
  const stage: React.CSSProperties = { position: "relative" };
  switch (v.type) {
    case "serp":
      return (
        <>
          <div style={stage}>
            <GoogleSerp c={v} height={PHONE_H} />
          </div>
          <PhoneNote {...NOTE} note={v.note} at={SERP_NOTE_AT} />
        </>
      );
    case "chat":
      return (
        <>
          <div style={stage}>
            <ChatScreen c={v} height={PHONE_H} />
          </div>
          <PhoneNote {...NOTE} note={v.note} at={CHAT_NOTE_AT} />
        </>
      );
    case "waffle":
      return (
        <div style={stage}>
          <Exhibit metric={v.metric} unit={v.unit} source={v.source} appear={0}>
            <Waffle at={4} lit={v.lit} legend={v.legend} />
          </Exhibit>
        </div>
      );
    case "bignumber":
      return <div style={stage}><BigNumber {...v} /></div>;
    case "versus":
      return <div style={stage}><Versus {...v} /></div>;
    case "slope":
      return <div style={stage}><Slope {...v} /></div>;
    case "trend":
      return <div style={stage}><Trend {...v} /></div>;
    case "donut":
      return <div style={stage}><Donut {...v} /></div>;
    case "people":
      return <div style={stage}><People {...v} /></div>;
    case "funnel":
      return <div style={stage}><Funnel {...v} /></div>;
    case "shot":
      return <div style={stage}><Shot {...v} /></div>;
    case "quiz":
      return <div style={stage}><Quiz {...v} /></div>;
    case "myth":
      return <div style={stage}><Myth {...v} /></div>;
    case "words":
      return <Words {...v} />;
    case "race":
      return <Race {...v} frames={frames} />;
    case "map":
      return <SeaMap {...v} frames={frames} />;
    case "countdown":
      return <Countdown {...v} frames={frames} />;
    case "list":
      return (
        <div style={stage}>
          <List items={v.items} frames={frames} source={v.source} />
        </div>
      );
    case "article":
      return (
        <div style={stage}>
          <Article image={v.image} title={v.title} url={v.url} />
        </div>
      );
    case "follow":
      return (
        <div style={stage}>
          <Follow note={v.note ?? "Số liệu marketing có nguồn, mỗi ngày."} ask={v.ask} />
        </div>
      );
    default:
      return null;
  }
};

export const Video: React.FC<VideoProps> = (props) => {
  useFonts();
  const { fps } = useVideoConfig();
  const sc = timeline({ ...props, fps });
  const scenes = props.script.scenes;
  // Đổi mốc 30 hình/giây sang khung thật của video (60 hình/giây thì nhân 2).
  const at = (x: number) => Math.round((x * fps) / BASE_FPS);
  return (
    <LayoutContext.Provider value={LAYOUTS[props.format ?? "9:16"]}>
    <AbsoluteFill>
      <Background />
      <Logo />
      {chartGroups(scenes).map((g) => (
        <ChartGroup key={g.first} g={g} sc={sc} />
      ))}
      {scenes.map((s, i) => {
        const frames = sc[i].frames + (i === scenes.length - 1 ? at(10) : 0);
        const reveal = s.visual?.type === "quiz" && s.visual.reveal;
        // Khung con dấu "SAI" đóng xuống, tính từ đầu cảnh (cảnh đầu đã lùi HOOK khung); âm là đã đóng sẵn ở khung đầu.
        const shift = i === 0 ? HOOK : 0;
        const stamp = s.visual?.type === "myth" ? mythStampAt(sc[i].words, sc[i].lead + shift, s.visual.verdict) - shift : -1;
        return (
          <Sequence key={i} from={sc[i].from} durationInFrames={frames}>
            <Fade frames={frames}>
              <Sequence from={i === 0 ? -at(HOOK) : 0} layout="none">
                {/* Cảnh lật đáp án: tiêu đề (thường chứa đáp án) chỉ hiện cùng lúc thẻ lật, không lộ trong khoảng lặng. */}
                <Sequence from={reveal ? at(QUIZ_REVEAL_AT) : 0} layout="none">
                  <Headline kicker={s.kicker} headline={s.headline} accent={s.accent} big={!s.visual} />
                </Sequence>
                <CueContext.Provider value={{ words: sc[i].words, offset: sc[i].lead + (i === 0 ? HOOK : 0), hook: i === 0 }}>
                  <Stage>
                    <SceneVisual v={s.visual} frames={(sc[i].frames * BASE_FPS) / fps} />
                  </Stage>
                </CueContext.Provider>
              </Sequence>
            </Fade>
            {/* Cảnh lật đáp án không có tiếng chuyển cảnh: giữ khoảng lặng trước tiếng "ding". */}
            {i > 0 && !reveal && <Audio src={sfx("whoosh")} volume={0.28} />}
            {i > 0 && s.visual && POP_AT[s.visual.type] !== undefined && (
              <Sequence from={at(POP_AT[s.visual.type]!)} layout="none">
                <Audio src={sfx("pop")} volume={0.35} />
              </Sequence>
            )}
            {s.visual?.type === "list" &&
              listDelays(s.visual.items, (sc[i].frames * BASE_FPS) / fps, i === 0 ? [] : sc[i].words, sc[i].lead).map((d, j) => (
                <Sequence key={j} from={at(d + 2)} layout="none">
                  <Audio src={sfx("pop")} volume={0.22} />
                </Sequence>
              ))}
            {i > 0 &&
              formatPops(s.visual, sc[i].words, sc[i].lead, (sc[i].frames * BASE_FPS) / fps).map(([d, kind], j) => (
                <Sequence key={`f${j}`} from={at(d + 2)} layout="none">
                  <Audio src={sfx(kind)} volume={kind === "ding" ? 0.7 : 0.25} />
                </Sequence>
              ))}
            {reveal && (
              <Sequence from={at(QUIZ_REVEAL_AT)} layout="none">
                <Audio src={sfx("ding")} volume={0.75} />
              </Sequence>
            )}
            {stamp >= 0 && (
              <Sequence from={at(stamp)} layout="none">
                <Audio src={sfx("pop")} volume={0.45} />
              </Sequence>
            )}
            <Sequence from={at(sc[i].lead)} layout="none">
              {!props.carousel && <Caption words={sc[i].words} />}
              {sc[i].audio && <Audio src={staticFile(sc[i].audio!)} />}
            </Sequence>
            {props.carousel && <SlideBadge n={i + 1} total={scenes.length} />}
          </Sequence>
        );
      })}
      <SiteFooter />
      {props.audit && <Audit />}
    </AbsoluteFill>
    </LayoutContext.Provider>
  );
};

// Tiếng "bật" khi từng phần của các dạng mới hiện ra (dòng chữ, mốc thời gian, nước, hạng); hạng 1 là tiếng ding.
const formatPops = (v: Visual | undefined, words: Word[], lead: number, frames: number): [number, "pop" | "ding"][] => {
  if (!v) return [];
  if (v.type === "words") return wordsCues(v.lines, words, lead).map((d) => [d, "pop"]);
  if (v.type === "race") return raceCues(v.periods, words, lead, frames).slice(1).map((d) => [d, "pop"]);
  if (v.type === "map") return mapCues(v.items, words, lead, frames).map((d) => [d, "pop"]);
  if (v.type === "countdown" && !v.teaser) return [...countdownCues(v.items, words, lead, frames)].map(([r, d]) => [d, r === 1 ? "ding" : "pop"]);
  return [];
};

// Bản ảnh lướt (TikTok photo mode): số trang ở góc phải, trang đầu có lời nhắc lướt sang.
const SlideBadge: React.FC<{ n: number; total: number }> = ({ n, total }) => {
  const { logo, caption, w } = useLayout();
  return (
    <>
      <div style={{ position: "absolute", right: logo.left, top: logo.top + 8, padding: "8px 20px", borderRadius: 30, background: "rgba(255,255,255,0.12)", color: "#FFFFFF", fontFamily: SANS, fontSize: 28, fontWeight: 700 }}>
        {n}/{total}
      </div>
      {n === 1 && (
        <div style={{ position: "absolute", left: 0, width: w, top: caption.top, display: "flex", justifyContent: "center" }}>
          <div style={{ padding: "16px 34px", borderRadius: 40, background: C.orange, color: C.navyDeep, fontFamily: SANS, fontSize: 32, fontWeight: 700 }}>Lướt để xem tiếp →</div>
        </div>
      )}
    </>
  );
};
