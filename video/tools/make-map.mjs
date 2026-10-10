// Tạo đường viền bản đồ Đông Nam Á (src/data/sea-map.json) từ Natural Earth 1:50m (gói world-atlas, phạm vi công cộng).
// Chạy 1 lần: node tools/make-map.mjs. Video chỉ đọc file JSON đã tạo, không cần thư viện bản đồ lúc dựng.
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { geoMercator, geoPath, geoCentroid } from "d3-geo";
import { feature } from "topojson-client";

const ROOT = path.resolve(import.meta.dirname, "..");
const topo = JSON.parse(readFileSync(path.join(ROOT, "node_modules/world-atlas/countries-50m.json"), "utf8"));
const all = feature(topo, topo.objects.countries).features;
// Mã số ISO 3166-1 của các nước Đông Nam Á; 6 nước đầu là các nước có số liệu trong e-Conomy SEA.
const ISO = { VNM: "704", IDN: "360", THA: "764", PHL: "608", MYS: "458", SGP: "702", LAO: "418", KHM: "116", MMR: "104", BRN: "096", TLS: "626" };
const W = 900, H = 640;
const pick = (code) => all.find((f) => f.id === code);
const main = ["VNM", "IDN", "THA", "PHL", "MYS", "SGP"].map((k) => pick(ISO[k]));
const proj = geoMercator().fitExtent([[20, 20], [W - 20, H - 20]], { type: "FeatureCollection", features: main });
const gp = geoPath(proj);
const out = { width: W, height: H, countries: {} };
for (const [iso3, code] of Object.entries(ISO)) {
  const f = pick(code);
  if (!f) throw new Error(`thiếu ${iso3}`);
  const [cx, cy] = proj(geoCentroid(f));
  out.countries[iso3] = { d: gp(f), cx: Math.round(cx), cy: Math.round(cy) };
}
writeFileSync(path.join(ROOT, "src/data/sea-map.json"), JSON.stringify(out));
console.log("src/data/sea-map.json", Object.keys(out.countries).join(" "), Math.round(JSON.stringify(out).length / 1024), "KB");
