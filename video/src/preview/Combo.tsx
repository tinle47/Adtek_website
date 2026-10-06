import React from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from "remotion";
import { FONT } from "../theme";
import { timeline } from "../timing";
import type { VideoProps } from "../types";
import { useFonts } from "../Video";
import { ColumnChart, Exhibit, Note, Waffle, type Variant } from "./Exhibit";
import { Background, Caption, Fade, Footer, Header, Headline, PAD, SearchMock, clamp, type DemoScene } from "./Preview";
import { THEMES } from "./themes";

// Hướng A + C: khung Navy Glow, biểu đồ chuẩn McKinsey biến đổi dần qua từng câu thoại.
const scene = (kicker: string, headline: string, accent: string, voice: string) =>
  ({ kicker, headline, accent, voice, narrative: ["", ""], visual: "search" }) as DemoScene;

const SCENES = [
  scene("AIO · Nghịch lý đầu tiên", "Khách hàng vẫn tìm trên Google.", "Nhưng ngừng bấm vào bạn.", "Khách hàng vẫn tìm trên Google. Nhưng họ đang ngừng bấm vào bạn."),
  scene("Pew Research · 900 người dùng", "Khi Google hiện tóm tắt AI,", "tỷ lệ bấm giảm gần nửa.", "Khi Google hiện tóm tắt AI, tỷ lệ bấm vào kết quả giảm từ 15% xuống 8%."),
  scene("Link nằm trong tóm tắt AI", "Link ngay trong tóm tắt AI?", "Còn thấp hơn.", "Còn link nằm ngay trong tóm tắt AI? Chỉ khoảng 1% lượt được bấm."),
  scene("Quy ra 100 lượt tìm kiếm", "Cứ 100 lượt tìm kiếm,", "chỉ 1 lượt bấm vào link.", "Nghĩa là cứ 100 lượt tìm kiếm, chỉ 1 lượt bấm vào link trong tóm tắt AI."),
];

const props = { script: { scenes: SCENES }, voice: null } as unknown as VideoProps;
export const comboFrames = () => timeline(props).reduce((s, x) => s + x.frames, 0) + 10;

const STAGE_TOP = 590;
const SOURCE = "Nguồn: Pew Research Center, 07/2025; 900 người dùng tại Mỹ";

const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ position: "absolute", left: PAD, right: PAD, top: STAGE_TOP, display: "flex", justifyContent: "center" }}>{children}</div>
);

// Biểu đồ cột sống xuyên cảnh 2 và 3: cảnh 3 chỉ thêm cột và chú thích, không dựng lại.
const ClickChart: React.FC<{ v: Variant; from: number; to: number; s2: number }> = ({ v, from, to, s2 }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [to - 7, to], [1, 0], clamp);
  if (f < from || f > to) return null;
  const slot = 824 / 3;
  const mid = (i: number) => slot * i + slot / 2;
  return (
    <Stage>
      <div style={{ opacity: o }}>
        <Exhibit v={v} metric="Tỷ lệ lượt tìm kiếm có bấm vào kết quả" unit="%" source={SOURCE} appear={from}>
          <div style={{ paddingTop: 60 }}>
            <ColumnChart
              v={v}
              max={15}
              slots={3}
              cols={[
                { label: "Không có\ntóm tắt AI", value: 15, tone: "base", at: from + 6 },
                { label: "Có\ntóm tắt AI", value: 8, tone: "main", at: from + 18 },
                { label: "Link nằm trong\ntóm tắt AI", value: 1, tone: "accent", at: s2 + 8 },
              ]}
              notes={
                <>
                  <Note
                    v={v}
                    at={from + 44}
                    arrow
                    points={[[mid(0) + 72, 0], [mid(1), 0], [mid(1), 80]]}
                    text={<b>Giảm 47%</b>}
                    textAt={{ left: mid(1) + 16, top: 8, width: 220 }}
                  />
                  <Note
                    v={v}
                    at={s2 + 30}
                    points={[[mid(2), 226], [mid(2), 184]]}
                    text={<b>Chỉ khoảng 1 trong 100 lượt tìm kiếm</b>}
                    textAt={{ left: mid(2) - 130, top: 112, width: 260, align: "center" }}
                  />
                </>
              }
            />
          </div>
        </Exhibit>
      </div>
    </Stage>
  );
};

export const Combo: React.FC<{ variant: Variant }> = ({ variant: v }) => {
  useFonts();
  const t = THEMES.glow;
  const sc = timeline(props);
  const end = (i: number) => sc[i].from + sc[i].frames;
  return (
    <AbsoluteFill style={{ fontFamily: FONT, color: t.text }}>
      <Background t={t} />
      <Header t={t} />
      <ClickChart v={v} from={sc[1].from} to={end(2)} s2={sc[2].from} />
      {SCENES.map((s, i) => {
        const last = i === SCENES.length - 1;
        return (
          <Sequence key={i} from={sc[i].from} durationInFrames={sc[i].frames + (last ? 10 : 0)}>
            <Fade frames={sc[i].frames + (last ? 10 : 0)}>
              <Headline t={t} s={s} />
              {i === 0 && (
                <Stage>
                  <SearchMock t={t} />
                </Stage>
              )}
              {i === 3 && (
                <Stage>
                  <Exhibit v={v} metric="Lượt bấm vào link trong tóm tắt AI" unit="trên 100 lượt tìm kiếm" source={SOURCE} appear={0}>
                    <Waffle v={v} at={4} lit={1} legend={["1 lượt bấm vào link trong tóm tắt AI", "99 lượt không bấm"]} />
                  </Exhibit>
                </Stage>
              )}
            </Fade>
            <Caption t={t} words={sc[i].words} top={1310} />
          </Sequence>
        );
      })}
      <Footer t={t} />
    </AbsoluteFill>
  );
};
