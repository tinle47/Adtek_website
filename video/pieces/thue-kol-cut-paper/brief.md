# Brief: Thuê KOL, khách có tin? (cut paper trial)

A re-telling of the approved Remotion video `scripts/thue-kol-khach-co-tin/1.json` in the animate skill's cut-paper style, to compare side by side. No new facts or numbers: everything on screen comes from 1.json.

## Spec

- 1080x1920, **30fps**, 63.17s = 1895 frames. Grid: 112.5 BPM (an 8th = 8 frames), so every cut is a whole frame.
- Style: cut paper (torn paper, drop shadows, grain, crayon, patterns, characters with faces). Text in Inter (the style's handwriting fonts are not installed; Inter has every Vietnamese diacritic), navy #00245F ink on torn paper tags.
- Format: voice-led beat-cut, a myth bust (claim, stamp, proof, what to do, ask). The voice is the clock: each scene cuts 0.15s before its line, on the 8th grid. No morphs.
- Voice: the 6 approved ElevenLabs takes, unchanged. `tools/make-voice.mjs` writes `voice/voice.wav` and `voice.json` in the skill's voice.mjs format, with word times from `public/voice/thue-kol-khach-co-tin/manifest.json` (no TTS, no whisper).
- Device (one sentence): the ordinary buyer in the orange shirt starts in the KOL's audience with a "?" and ends on the same stage with the mic, while the banner that asked the question now says "Review thật, bán hàng thật."
- Colour: Adtek orange = real buyers and their reviews (her shirt, her column, the lit phones, the stars, the review numbers). The KOL is purple and gold, never orange. Navy = every word and the Follow button.

## Story table (voice times)

| # | t (s) | shot | what happens | sound |
|---|---|---|---|---|
| 1 | 0.00-4.53 | stage | Frame 0: the hook banner "Thuê KOL nổi tiếng / là khách sẽ tin?" complete; the KOL performs under a ring light, live hearts; the buyer doubts ("?"). 2.6: the score stops. 3.66 "Sai.": the SAI stamp slams under the banner, the spotlight dies, the KOL sweats, the buyer smiles | glossy pad, glitter; silence 2.6-3.6; the loudest hit (stab + sub) on the stamp |
| 2 | 4.53-9.33 | survey | Q&Me clipboard ticks itself: 200 người, 20 đến 49 tuổi, Hà Nội và TP.HCM, 09/2026; the KOL's pinned photo falls on "ngược lại" | pencil ticks |
| 3 | 9.33-16.00 | versus | 54%: the buyer's orange column rises (true scale, 11.5px per point) with her on it; 13%: the KOL's column barely leaves the floor; crowd holds orange hearts | her motif (rising fifth), his two falling notes |
| 4 | 16.00-22.13 | shoppers | 10 shoppers, the buyer among them; on "78%" 8 phones light orange: "78% chọn mua theo review, khoảng 8/10 người" | 8 plucks, one per phone |
| 5 | 22.13-25.07 | age20 | extreme close-up of a 20-year-old; "Ở tuổi 20", then "87%" with stars | chime |
| 6 | 25.07-34.67 | bars | "Review nào đáng tin?": 69% real photo/video (orange), 60% detail, 51% stars, each on its spoken number; the buyer reads a review with a magnifier | 8th groove, a slap per bar |
| 7 | 34.67-37.33 | drop | "Dưới 3.6 sao bị loại": a 5-star meter fills to a red line at 3.6; the buyer flicks a 2-star product into the bin | whoosh, bin thud |
| 8 | 37.33-40.53 | fifty | "74% cần từ 50 đánh giá mới tin": review cards stack up on 2s; "50 đánh giá" lands on "50" | card ticks, chime (busiest stretch, 16ths) |
| 9 | 40.53-54.13 | todo | "Làm gì ngay?" checklist on a cork board, each item ticked on its words; the seller (navy) acts each out: QR on the parcel, a photo, a crossed-out gift, a reply to a complaint | warm, a chime per step |
| 10 | 54.13-63.17 | finale | the same stage, changed: the buyer has the mic and the spotlight, the KOL claps in the audience; "Bạn tin review của KOL hay người mua thật?", "Comment cho Adtek", "Follow Adtek" | her motif, a held chord |

## Claims on screen (all from 1.json, already fact-checked upstream)

- Q&Me, How Vietnamese consumers trust online reviews, 09/2026: 200 people aged 20 to 49, Hà Nội and TP.HCM; 54% trust ordinary buyers more than KOL, 13% lean to celebrities; 78% say online reviews strongly influence purchase (about 8/10), 87% at age 20; real photo/video 69%, detail 60%, star rating 51%; under 3.6 stars dropped; 74% need at least 50 reviews.
- Google Business Profile Help: do not offer incentives for reviews (treated as fake reviews); ask for reviews via link/QR; reply to reviews.
- Every number on screen carries a source strip ("Nguồn: Q&Me, ... 09/2026" / "Nguồn: Google Business Profile Help; Q&Me, 09/2026").
