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
