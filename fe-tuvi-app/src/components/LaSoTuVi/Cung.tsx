import React from "react";
import type { CungData } from "../../types/tuvi";

interface CungProps {
  data: CungData;
}

const colorMap: Record<string, string> = {
  chinh_tinh: "#d32f2f", // đỏ
  cat_tinh: "#388e3c",   // xanh lá
  sat_tinh: "#1976d2",   // xanh dương
  phu_tinh_khac: "#fbc02d" // vàng
};

const Cung: React.FC<CungProps> = ({ data }) => {
  return (
    <div className="cung-box" style={{ border: "1px solid #ccc", borderRadius: 8, padding: 12, margin: 8, minWidth: 220 }}>
      <div className="cung-header" style={{ borderBottom: "1px solid #eee", marginBottom: 8, paddingBottom: 4 }}>
        <strong>{data.cung}</strong>
      </div>

      {data.chinh_tinh.length > 0 && (
        <div className="sao-list" style={{ marginBottom: 4 }}>
          <span className="star chinh-tinh" style={{ color: colorMap.chinh_tinh, fontWeight: 600 }}>Chính tinh:</span>
          {data.chinh_tinh.join(", ")}
        </div>
      )}

      {data.cat_tinh.length > 0 && (
        <div className="sao-list" style={{ marginBottom: 4 }}>
          <span className="star cat-tinh" style={{ color: colorMap.cat_tinh, fontWeight: 600 }}>Cát tinh:</span>
          {data.cat_tinh.join(", ")}
        </div>
      )}

      {data.sat_tinh.length > 0 && (
        <div className="sao-list" style={{ marginBottom: 4 }}>
          <span className="star sat-tinh" style={{ color: colorMap.sat_tinh, fontWeight: 600 }}>Sát tinh:</span>
          {data.sat_tinh.join(", ")}
        </div>
      )}

      {data.phu_tinh_khac.length > 0 && (
        <div className="sao-list">
          <span className="star phu-tinh-khac" style={{ color: colorMap.phu_tinh_khac, fontWeight: 600 }}>Phụ tinh:</span>
          {data.phu_tinh_khac.join(", ")}
        </div>
      )}
    </div>
  );
};

export default Cung;
