import React from "react";
import type { LaSoData } from "../../types/tuvi";
import ThongTinTrungTam from "./ThongTinTrungTam";
import Cung from "./Cung";
import "./LaSoTuVi.css";

interface LaSoTuViProps {
  data: LaSoData;
}

const LaSoTuVi: React.FC<LaSoTuViProps> = ({ data }) => {
  if (!data?.dia_ban || !Array.isArray(data.dia_ban)) {
    return <div className="error-message">Dữ liệu lá số không hợp lệ hoặc thiếu thông tin các cung.</div>;
  }

  return (
    <div className="la-so-grid">
      {/* Render 12 cung xung quanh */}
      {data.dia_ban.map((cung, idx) => {
        // Xác định vị trí grid cho từng cung (theo thứ tự kim đồng hồ, bắt đầu từ góc trên bên trái)
        const gridPositions = [
          { gridColumn: '1', gridRow: '1' }, // 0
          { gridColumn: '2', gridRow: '1' }, // 1
          { gridColumn: '3', gridRow: '1' }, // 2
          { gridColumn: '4', gridRow: '1' }, // 3
          { gridColumn: '4', gridRow: '2' }, // 4
          { gridColumn: '4', gridRow: '3' }, // 5
          { gridColumn: '4', gridRow: '4' }, // 6
          { gridColumn: '3', gridRow: '4' }, // 7
          { gridColumn: '2', gridRow: '4' }, // 8
          { gridColumn: '1', gridRow: '4' }, // 9
          { gridColumn: '1', gridRow: '3' }, // 10
          { gridColumn: '1', gridRow: '2' }  // 11
        ];
        return (
          <div key={idx} style={{ position: 'relative', ...gridPositions[idx], zIndex: 1 }}>
            <Cung data={cung} />
          </div>
        );
      })}
      <div className="center-info">
        <ThongTinTrungTam data={data.thong_tin_duong_so} />
      </div>
    </div>
  );
};

export default LaSoTuVi;
