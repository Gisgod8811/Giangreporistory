export interface ThongTinDuongSo {
  gioi_tinh: string;
  ngay_sinh_duong_lich: string;
  gio_sinh: string;
  ngay_sinh_am_lich: string;
  nam_sinh: string;
  cuc: string;
}

export interface CungData {
  cung: string;
  chinh_tinh: string[];
  cat_tinh: string[];
  sat_tinh: string[];
  phu_tinh_khac: string[];
}

export interface LaSoData {
  thong_tin_duong_so: ThongTinDuongSo;
  dia_ban: CungData[];
}

export interface BirthInfo {
  gioi_tinh: string;
  gio_sinh: number;
  ngay_dl?: number;
  thang_dl?: number;
  nam_dl?: number;
  ngay_al?: number;
  thang_al?: number;
  nam_al?: number;
}
