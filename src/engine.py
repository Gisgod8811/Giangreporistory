# src/engine.py
# Class TuViEngine: chỉ điều phối tổng thể, gọi các module con

from src.utils import get_can_chi_nam, gio_chi
from src.an_sao import SaoCalculator
from src.cung import CungCalculator

class TuViEngine:
    def __init__(self, gioi_tinh, gio_sinh, ngay_al, thang_al, nam_al, nam_xem=None):
        self.gioi_tinh = gioi_tinh
        self.gio_sinh = gio_sinh
        self.ngay_al = ngay_al
        self.thang_al = thang_al
        self.nam_al = nam_al
        self.nam_xem = nam_xem if nam_xem is not None else nam_al
        self.can_chi_nam = get_can_chi_nam(nam_al)
        self.can_chi_nam_xem = get_can_chi_nam(self.nam_xem)
        self.sao_calculator = SaoCalculator()
        self.cung_calculator = CungCalculator()

    def calculate(self):
        can_nam, chi_nam = self.can_chi_nam.split()
        can_nam_xem, chi_nam_xem = self.can_chi_nam_xem.split()
        # 3. An cung Mệnh, Thân
        cung_menh, cung_than = self.cung_calculator.an_cung_menh_than(self.thang_al, gio_chi(self.gio_sinh))
        # 4. Khởi tạo địa bàn 12 cung Bắc Tông (Dần khởi đầu)
        dia_chi = ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu']
        dia_ban = [{"ten_cung": chi, "chinh_tinh": [], "cat_tinh": [], "sat_tinh": [], "phu_tinh_khac": [], "luu_tinh": []} for chi in dia_chi]
        # 5. An cung chức năng
        # Xác định âm dương nam nữ
        duong_chi = ['Tý', 'Dần', 'Thìn', 'Ngọ', 'Thân', 'Tuất']
        am_chi = ['Sửu', 'Mão', 'Tỵ', 'Mùi', 'Dậu', 'Hợi']
        if (self.gioi_tinh.lower() == 'nam' and chi_nam in duong_chi):
            am_duong_nam_nu = 'Dương Nam'
        elif (self.gioi_tinh.lower() == 'nam' and chi_nam in am_chi):
            am_duong_nam_nu = 'Âm Nam'
        elif (self.gioi_tinh.lower() == 'nữ' and chi_nam in duong_chi):
            am_duong_nam_nu = 'Dương Nữ'
        else:
            am_duong_nam_nu = 'Âm Nữ'
        dia_ban = self.cung_calculator.an_cung_chuc_nang(dia_ban, cung_menh, am_duong_nam_nu)
        # 6. Xác định Cục
        cuc = self.cung_calculator.xac_dinh_cuc(cung_menh, can_nam)
        # 7. An 14 chính tinh
        dia_ban = self.sao_calculator.an_chinh_tinh(dia_ban, self.ngay_al, cuc)
        # 8. Tính đại hạn cho từng cung
        tuoi_am = self.nam_al
        dai_han_data = self.cung_calculator.tinh_dai_han(tuoi_am, cuc, self.gioi_tinh, cung_menh, chi_nam)
        for cung in dia_ban:
            cung['dai_han'] = dai_han_data.get(cung['ten_cung'], "")
        # 9. Chủ Mệnh & Chủ Thân
        chu_menh, chu_than = self.cung_calculator.tinh_chu_menh_than(chi_nam, cung_than)
        # 10. Cân lượng
        # Sửa: truyền đúng thứ tự và đủ 5 tham số (ngay_al, thang_al, can_nam, chi_nam, gio_chi)
        can_luong_str, can_luong_val = self.cung_calculator.tinh_can_luong(
            self.ngay_al,
            self.thang_al,
            can_nam,
            chi_nam,
            gio_chi(self.gio_sinh)
        )
        # An Lưu Tinh
        dia_ban = self.sao_calculator.an_luu_tinh(dia_ban, can_nam_xem, chi_nam_xem)
        final_chart = {
            "thong_tin_duong_so": {
                "gioi_tinh": self.gioi_tinh,
                "am_lich": f"{self.ngay_al}/{self.thang_al}/{self.nam_al}",
                "can_chi_nam": self.can_chi_nam,
                "gio_sinh_chi": f"Giờ {gio_chi(self.gio_sinh)}",
                "menh_cuc": cuc,
                "cung_menh_tai": cung_menh,
                "cung_than_tai": cung_than,
                "chu_menh": chu_menh,
                "chu_than": chu_than,
                "am_duong_nam_nu": am_duong_nam_nu,
                "can_luong": can_luong_str
            },
            "dia_ban": dia_ban
        }
        return final_chart
