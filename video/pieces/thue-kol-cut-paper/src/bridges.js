
// =====================================================================
//  ERAS, CAMERAS, BRIDGES (read by kit/morph.js). A narrated beat-cut: every shot boundary is a hard cut on a
//  sentence end, snapped to the 8th grid, so BRIDGES stays empty. ERA_BG: each shot's wall colour.
// =====================================================================
const ERA_BG = ['#a8406f', '#cfe2ee', '#e3b55a', '#6fb7ae', '#4c6fb5', '#a9d9c6', '#9f8cc6', '#f3d6be', '#c9a46a', '#a8406f'];
// a small shake on the stamp; otherwise locked-off framings (scale changes come from the shots themselves)
function pieceCam(era, t) {
  if (era === 0) { const d = t - TIMELINE.cues.sai; if (d >= 0 && d < 0.3) { const a = 14 * Math.exp(-d * 14) * (B % 2 ? 1 : -1); return { z: 1, tx: a, ty: -a * 0.6 }; } }
  return null;
}
const BRIDGES = [];
