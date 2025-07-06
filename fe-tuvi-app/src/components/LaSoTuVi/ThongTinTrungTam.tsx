import React from "react";
import type { ThongTinDuongSo } from "../../types/tuvi";

interface ThongTinTrungTamProps {
  data: ThongTinDuongSo;
}

const ThongTinTrungTam: React.FC<ThongTinTrungTamProps> = ({ data }) => {
  return (
    <div className="thong-tin-trung-tam">
      <h2>Thông Tin Đương Số</h2>
      <ul className="info-list">
        <li><strong>Giới tính:</strong> {data.gioi_tinh}</li>
        <li><strong>Ngày sinh (DL):</strong> {data.ngay_sinh_duong_lich}</li>
        <li><strong>Giờ sinh:</strong> {data.gio_sinh}</li>
        <li><strong>Ngày sinh (AL):</strong> {data.ngay_sinh_am_lich}</li>
        <li><strong>Năm sinh:</strong> {data.nam_sinh}</li>
        <li><strong>Cục:</strong> {data.cuc}</li>
      </ul>
    </div>
  );
};

export default ThongTinTrungTam;
