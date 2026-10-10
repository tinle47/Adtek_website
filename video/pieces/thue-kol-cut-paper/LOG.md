# Log: thue-kol-cut-paper

## Run 1 - 2026-10-10

- Trial re-telling of `scripts/thue-kol-khach-co-tin/1.json` in cut paper, for side-by-side comparison with the Remotion version.
- Check-ins done by self-review (client approved the trial): story table in `brief.md`; look frames `check/look-draft-*.jpg`, `check/look-fixes.jpg`, `check/look.jpg`; storyboard `check/storyboard.jpg`; stamp close-up `check/stamp-crop.jpg`; cover `check/cover.png`.
- Voice: the approved takes, placed by `tools/make-voice.mjs` (no TTS, no whisper); word times from manifest.json.

### Fixes from self-review (before and after the first export)
- SAI stamp was small, translucent and hidden behind the KOL's raised bottle: bigger (400x180, 160px), on a paper backing, the KOL's arm moved out of it.
- Hook: the buyer read as content, not doubtful: added a "?" thought bubble that vanishes on the stamp.
- Hearts covered the LIVE tag (draw order).
- Bars: the buyer's head overlapped the 51% bar: moved down.
- Drop shot was an empty wall: added a 5-star meter that fills to a red line at 3.6 (true scale).
- Finale: buyer's phone hit the banner, audience covered the Follow button, the KOL's clapping arms crossed his face, the "+" overlapped "Follow": all moved.
- To-do: "kể cả lời chê" finished writing 0.4s before the cut: starts earlier.
- Review: story arc failed "peak has the highest cut rate" (peak act was set to the whole trust section): the peak is the bin + 50 stretch (0.34 cuts/s).
- Two cut-timing bugs: CUT() rounded up an extra 8th because voice times are stored at 3 decimals (bars cut 0.27s late); toFixed(4) put the drop cut one frame late (34.6667 > 1040/30). Shot times now snap to exact frames.
- Drop wall lavender had the same luminance as the mint bars wall (cut invisible to the grey diff): darker lavender.

### Final numbers (review.mjs on renders/final.mp4)
- 63.17s, 1895 frames, 30fps, 1080x1920. 9 hard cuts, all on the 112.5 BPM 8th grid (0 frames error); no morphs; no flat frames.
- Story arc 5/5 PASS: the stamp (gift) p90 -8.2 dBFS vs next -12.9; peak (bin + 50) 0.34 cuts/s; hush median -120 dB, 1.0s at <= -40 dBFS before the stamp.
- Text PASS (0 cut-off/overlap, 0 under the phone UI). Dead beats PASS (0). Loudness -14.5 LUFS, true peak -1.5 dBFS.
- Narration density FAIL on line 1 only: 3.98 words/s (Vietnamese counts syllables as words; approved take, not re-recorded). Word hits PASS.
- Render: final export 452s wall clock (frames 113s, score + stems 87s, x264 encodes the rest) on 4 cores; review 234s.

### Per-shot PASS (contact sheets vs FRAME.md + cut-paper checklist)
| shot | character acting | full world | paper/pattern | 3+ life | text on paper | verdict |
|---|---|---|---|---|---|---|
| 1 stage | KOL performs, buyer doubts then smiles | curtain stage | stripes, wood | bunting, hearts, sparkles, LIVE | banner, stamp | PASS |
| 2 survey | buyer ticks | sky gingham, desk | gingham, wood grain | cat, mug steam, clock, falling photo | clipboard | PASS |
| 3 versus | buyer rides up, KOL sweats | mustard stripes | stripes, dots | bunting, confetti, crowd hearts | tags, columns | PASS |
| 4 shoppers | 10 shoppers react | shop shelves | stripes, gingham floor | lamps, products, basket | tag | PASS |
| 5 age20 | close-up, delighted | dorm wall | dots, stripes | fairy lights, poster, sticky notes, stars | tags | PASS |
| 6 bars | buyer with magnifier | mint stripes | stripes, crayon | plant, review card, photo | labels on wall | PASS |
| 7 drop | buyer flicks product | lavender stripes | stripes, wood | clock, fly, dust puff | tag, star meter | PASS |
| 8 fifty | buyer thumbs up | peach dots | dots, wood | plant, confetti, card stack | tags | PASS |
| 9 todo | seller acts each step | cork board, table | cork, lines, wood | QR, polaroid, gift, bubbles | notepad | PASS (weakest) |
| 10 finale | buyer on stage, KOL claps | curtain stage | stripes, wood | bunting, audience, stars | banner, bubble, button | PASS |

### Weakest shot
- 9 (what to do now): 13.6s on one locked framing; the table props are small (~120-170px) and the seller is a small bust, so the frame is mostly a text notepad. Next run: push in on each prop as its step is read, or give each step its own 3s shot.
