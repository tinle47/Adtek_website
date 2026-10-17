import React, { useMemo } from "react";
import { ThreeCanvas } from "@remotion/three";
import { Edges, PerspectiveCamera } from "@react-three/drei";
import { interpolate } from "remotion";
import { Color, DoubleSide, ExtrudeGeometry, type Shape } from "three";
import { SVGLoader } from "three/examples/jsm/loaders/SVGLoader.js";
import { clamp, ease, useFrame } from "./frame";

// Bản đồ Đông Nam Á dạng 3D (render.mjs --fx3d, bản thử theo phương án 2 của anh Tin, 17/10/2026).
// Giữ đúng quy tắc "không bóp méo dữ liệu": mọi nước nổi cùng một độ dày, con số vẫn nằm trong nhãn 2D phía trên,
// không mã hóa dữ liệu bằng chiều cao hay phối cảnh. 3D chỉ dùng cho cú lướt máy quay lúc vào cảnh:
// máy quay nghiêng 50 độ rồi về thẳng từ trên xuống trong 12 khung đầu, sau đó đứng yên để nhãn 2D nằm đúng chỗ.
// Mọi chuyển động tính theo khung hình (useFrame của frame.tsx), không dùng useFrame của React Three Fiber.

type Country = { d: string; cx: number; cy: number };
export type Map3DProps = {
  width: number; // kích thước khung (điểm ảnh), cùng tỷ lệ với bản đồ
  height: number;
  map: { width: number; height: number; countries: Record<string, Country> };
  // màu mặt trên đã trộn sẵn độ mờ (giống fill và fillOpacity của bản 2D)
  colors: Record<string, string>;
};

const DEPTH = 10; // độ dày mọi nước như nhau
const FOV = 30;
const FLY = 12; // số khung (30 hình/giây) của cú lướt máy quay

const shapesOf = (d: string): Shape[] => {
  const data = new SVGLoader().parse(`<svg xmlns="http://www.w3.org/2000/svg"><path d="${d}"/></svg>`);
  return data.paths.flatMap((p) => SVGLoader.createShapes(p));
};

const CountryMesh: React.FC<{ d: string; color: string }> = ({ d, color }) => {
  const geo = useMemo(() => new ExtrudeGeometry(shapesOf(d), { depth: DEPTH, bevelEnabled: false }), [d]);
  // Mặt trên đúng màu bản 2D; cạnh tối hơn để thấy độ nổi.
  const side = useMemo(() => new Color(color).multiplyScalar(0.55).getStyle(), [color]);
  return (
    <mesh geometry={geo}>
      <meshBasicMaterial attach="material-0" color={color} side={DoubleSide} />
      <meshBasicMaterial attach="material-1" color={side} side={DoubleSide} />
      <Edges color="#ffffff" transparent opacity={0.35} threshold={20} />
    </mesh>
  );
};

export const Map3D: React.FC<Map3DProps> = ({ width, height, map, colors }) => {
  const f = useFrame();
  const t = interpolate(f, [0, FLY], [1, 0], { ...clamp, easing: ease }); // 1 = đang nghiêng, 0 = thẳng từ trên xuống
  // Khoảng cách để mặt trên lấp vừa khung khi nhìn thẳng xuống: cao hiển thị = 2 * D * tan(FOV/2) = chiều cao bản đồ.
  const D = map.height / 2 / Math.tan(((FOV / 2) * Math.PI) / 180);
  const tilt = ((50 * Math.PI) / 180) * t;
  const dist = D * (1 + 0.35 * t);
  return (
    <ThreeCanvas width={Math.round(width)} height={Math.round(height)} style={{ position: "absolute", left: 0, top: 0, width, height }}>
      <ambientLight intensity={1} />
      <PerspectiveCamera
        makeDefault
        fov={FOV}
        aspect={width / height}
        near={10}
        far={dist * 4}
        position={[0, -dist * Math.sin(tilt), DEPTH + dist * Math.cos(tilt)]}
        rotation={[tilt, 0, 0]}
      />
      {/* Đường viền SVG có trục y hướng xuống: lật y và dời tâm bản đồ về gốc tọa độ; xoay nhẹ quanh trục đứng lúc lướt vào. */}
      <group rotation={[0, 0, (-10 * Math.PI * t) / 180]}>
        <group scale={[1, -1, 1]} position={[-map.width / 2, map.height / 2, 0]}>
          {Object.entries(map.countries).map(([iso, c]) => (
            <CountryMesh key={iso} d={c.d} color={colors[iso]} />
          ))}
        </group>
      </group>
    </ThreeCanvas>
  );
};
