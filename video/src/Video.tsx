import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Article, Follow, List } from "./design/blocks";
import { BarChart, ColumnChart, Exhibit, Waffle, type TimedCol, type TimedNote } from "./design/charts";
import { CHAT_NOTE_AT, ChatScreen } from "./design/chat";
import { Background, Caption, Fade, Headline, L, Logo, SiteFooter, clamp, useFonts } from "./design/frame";
import { GoogleSerp, PhoneNote, SERP_NOTE_AT } from "./design/serp";
import { timeline, type TimedScene } from "./timing";
import type { Scene, VideoProps, Visual } from "./types";

const PHONE_H = 600;
const NOTE = { left: L.pad + 600, top: 1010 };

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

const ChartGroup: React.FC<{ g: Group; sc: TimedScene[] }> = ({ g, sc }) => {
  const f = useCurrentFrame();
  const start = sc[g.first].from;
  const end = sc[g.last].from + sc[g.last].frames;
  if (f < start || f > end) return null;
  const stepStart = (step = 0) => sc[Math.min(g.first + step, g.last)].from;
  const items = g.chart.type === "columns" ? g.chart.cols : g.chart.rows;
  // Phần tử cùng một bước hiện lần lượt cách nhau 12 frame.
  const order: Record<number, number> = {};
  const timed: TimedCol[] = items.map((it) => {
    const step = it.step ?? 0;
    order[step] = (order[step] ?? -1) + 1;
    return { ...it, at: stepStart(step) + 6 + order[step] * 12 };
  });
  const lastAt = (step: number) => Math.max(...timed.filter((_, i) => (items[i].step ?? 0) === step).map((t) => t.at), stepStart(step));
  const notes: TimedNote[] = (g.chart.notes ?? []).map((n) => {
    const at = lastAt(n.step ?? 0) + 26;
    return n.kind === "drop" ? { ...n, at } : { kind: "callout", target: n.at, text: n.text, at };
  });
  const o = interpolate(f, [end - 7, end], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: L.pad, top: L.stage, opacity: o }}>
      <Exhibit metric={g.chart.metric} unit={g.chart.unit} source={g.chart.source} appear={start}>
        {g.chart.type === "columns" ? (
          <ColumnChart cols={timed} max={g.chart.max} notes={notes} />
        ) : (
          <BarChart rows={timed} max={g.chart.max} notes={notes} />
        )}
      </Exhibit>
    </div>
  );
};

// Hình minh họa riêng của một cảnh (biểu đồ cột/thanh được vẽ ở ChartGroup).
const SceneVisual: React.FC<{ v?: Visual; frames: number }> = ({ v, frames }) => {
  if (!v) return null;
  const stage: React.CSSProperties = { position: "absolute", left: L.pad, top: L.stage };
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
    case "list":
      return (
        <div style={stage}>
          <List items={v.items} frames={frames} />
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
          <Follow note={v.note ?? "Số liệu marketing có nguồn, mỗi ngày."} />
        </div>
      );
    default:
      return null;
  }
};

export const Video: React.FC<VideoProps> = (props) => {
  useFonts();
  const sc = timeline(props);
  const scenes = props.script.scenes;
  return (
    <AbsoluteFill>
      <Background />
      <Logo />
      {chartGroups(scenes).map((g) => (
        <ChartGroup key={g.first} g={g} sc={sc} />
      ))}
      {scenes.map((s, i) => {
        const frames = sc[i].frames + (i === scenes.length - 1 ? 10 : 0);
        return (
          <Sequence key={i} from={sc[i].from} durationInFrames={frames}>
            <Fade frames={frames}>
              <Headline kicker={s.kicker} headline={s.headline} accent={s.accent} big={!s.visual} />
              <SceneVisual v={s.visual} frames={sc[i].frames} />
            </Fade>
            <Caption words={sc[i].words} />
            {sc[i].audio && <Audio src={staticFile(sc[i].audio!)} />}
          </Sequence>
        );
      })}
      <SiteFooter />
    </AbsoluteFill>
  );
};
