# src/cung.py
# Các hàm xử lý cung, cục, mệnh/thân

class CungCalculator:
    def __init__(self):
        pass

    # Phiên bản đúng trong file src/cung.py
    def an_cung_menh_than(self, thang_sinh_al: int, gio_sinh_chi: str) -> tuple[str, str]:
        """
        An cung Mệnh và Thân theo chuẩn Bắc Tông (Trung Hoa cổ truyền):
        - Tháng 1 tại Dần, đếm thuận đến tháng sinh trên vòng tháng (DIA_CHI_THANG)
        - Tìm vị trí cung tháng sinh trên vòng địa chi Dần (DIA_CHI_DAN)
        - Đếm NGHỊCH (Mệnh) và THUẬN (Thân) theo giờ sinh trên DIA_CHI_DAN
        """
        DIA_CHI_THANG = ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu']
        DIA_CHI_DAN = ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu']
        GIO_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        # Bước 1: Xác định cung tháng sinh trên vòng tháng
        index_cung_thang_sinh = (thang_sinh_al - 1) % 12
        cung_thang_sinh = DIA_CHI_THANG[index_cung_thang_sinh]
        # Bước 2: Tìm vị trí cung tháng sinh trên vòng địa chi Dần
        index_cung_thang_sinh_in_DIA_CHI_DAN = DIA_CHI_DAN.index(cung_thang_sinh)
        # Bước 3: Đếm NGHỊCH (Mệnh) và THUẬN (Thân) trên DIA_CHI_DAN
        index_gio_sinh = GIO_CHI.index(gio_sinh_chi)
        index_cung_menh = (index_cung_thang_sinh_in_DIA_CHI_DAN - index_gio_sinh) % 12
        cung_menh = DIA_CHI_DAN[index_cung_menh]
        index_cung_than = (index_cung_thang_sinh_in_DIA_CHI_DAN + index_gio_sinh) % 12
        cung_than = DIA_CHI_DAN[index_cung_than]
        print("\n--- DEBUG an_cung_menh_than (Bắc Tông) ---")
        print(f"Tháng âm lịch: {thang_sinh_al}, Giờ sinh chi: {gio_sinh_chi}")
        print(f"Cung tháng sinh: {cung_thang_sinh} (index {index_cung_thang_sinh_in_DIA_CHI_DAN} trong DIA_CHI_DAN)")
        print(f"Index giờ sinh: {index_gio_sinh} ({gio_sinh_chi})")
        print(f"Index Mệnh: {index_cung_menh} ({cung_menh})")
        print(f"Index Thân: {index_cung_than} ({cung_than})")
        print("-----------------------------")
        return (cung_menh, cung_than)

    def xac_dinh_cuc(self, cung_menh_chi, nam_can):
        """
        Xác định Cục dựa trên cung mệnh và can năm, theo quy tắc truyền thống.
        """
        can_dan_dict = {
            "Giáp": "Bính", "Kỷ": "Bính",
            "Ất": "Mậu", "Canh": "Mậu",
            "Bính": "Canh", "Tân": "Canh",
            "Đinh": "Nhâm", "Nhâm": "Nhâm",
            "Mậu": "Giáp", "Quý": "Giáp"
        }
        ngu_hanh_list = ["Kim", "Thủy", "Hỏa", "Thổ", "Mộc"]
        dia_chi = ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu']
        can_dan = can_dan_dict.get(nam_can, None)
        if can_dan is None:
            return ""
        hanh_bat_dau = {
            "Bính": 2,  # Hỏa
            "Mậu": 3,   # Thổ
            "Canh": 0,  # Kim
            "Nhâm": 1,  # Thủy
            "Giáp": 4   # Mộc
        }
        start_idx = hanh_bat_dau[can_dan]
        hanh_12_cung = []
        for i in range(12):
            hanh_12_cung.append(ngu_hanh_list[(start_idx + i) % 5])
        try:
            idx = dia_chi.index(cung_menh_chi)
        except ValueError:
            return ""
        hanh_cung_menh = hanh_12_cung[idx]
        so_cuc = {
            "Thủy": "Nhị",
            "Mộc": "Tam",
            "Kim": "Tứ",
            "Thổ": "Ngũ",
            "Hỏa": "Lục"
        }
        ten_cuc = f"{hanh_cung_menh} {so_cuc.get(hanh_cung_menh, '')} Cục"
        return ten_cuc

    def tinh_dai_han(self, tuoi_am, cuc, gioi_tinh, cung_menh, nam_chi):
        """
        Tính đại hạn cho từng cung dựa trên tuổi khởi hạn (theo Cục), chiều đi (theo Âm/Dương Nam/Nữ của NĂM SINH), và cung mệnh.
        Trả về dict {ten_cung: 'start-end'}
        """
        dia_chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        khoi_han_dict = {
            'Nhị': 2,
            'Tam': 3,
            'Tứ': 4,
            'Ngũ': 5,
            'Lục': 6
        }
        so_cuc = None
        for k in khoi_han_dict:
            if k in cuc:
                so_cuc = k
                break
        tuoi_khoi = khoi_han_dict.get(so_cuc, 0)
        # Xác định âm/dương của năm sinh
        duong_chi = ['Tý', 'Dần', 'Thìn', 'Ngọ', 'Thân', 'Tuất']
        am_chi = ['Sửu', 'Mão', 'Tỵ', 'Mùi', 'Dậu', 'Hợi']
        nam_chi = nam_chi.strip()
        if nam_chi in duong_chi:
            nam_am_duong = 'duong'
        elif nam_chi in am_chi:
            nam_am_duong = 'am'
        else:
            nam_am_duong = ''
        gioi_tinh = gioi_tinh.lower()
        # Quy tắc truyền thống
        # Dương Nam, Âm Nữ: thuận chiều (step=1)
        # Âm Nam, Dương Nữ: nghịch chiều (step=-1)
        if (gioi_tinh == 'nam' and nam_am_duong == 'duong') or (gioi_tinh == 'nu' and nam_am_duong == 'am'):
            step = 1
        else:
            step = -1
        start_idx = dia_chi.index(cung_menh)
        dai_han = {}
        for i in range(12):
            idx = (start_idx + i * step) % 12
            ten_cung = dia_chi[idx]
            start = tuoi_khoi + i * 10
            end = start + 10
            dai_han[ten_cung] = f"{start}-{end}"
        return dai_han

    def tinh_chu_menh_than(self, nam_chi, than_chi):
        """
        Trả về (chu_menh, chu_than) dựa vào nam_chi và than_chi.
        """
        from src.config import CHU_MENH_DICT, CHU_THAN_DICT
        chu_menh = CHU_MENH_DICT.get(nam_chi, "")
        chu_than = CHU_THAN_DICT.get(than_chi, "")
        return chu_menh, chu_than

    def an_cung_chuc_nang(self, dia_ban, cung_menh_chi, am_duong_nam_nu):
        """
        Gán tên cung chức năng cho từng cung trong dia_ban theo quy tắc Bắc Tông.
        - dia_ban: list 12 dict, mỗi dict có 'ten_cung'.
        - cung_menh_chi: tên cung Mệnh (ví dụ: 'Dần').
        - am_duong_nam_nu: 'Dương Nam', 'Âm Nam', 'Dương Nữ', 'Âm Nữ'.
        Trả về dia_ban đã thêm trường 'cung_chuc_nang' cho từng cung.
        """
        chuc_nang_thuan = [
            "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc", "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"
        ]
        chuc_nang_nghich = [
            "Mệnh", "Huynh Đệ", "Phu Thê", "Tử Tức", "Tài Bạch", "Tật Ách", "Thiên Di", "Nô Bộc", "Quan Lộc", "Điền Trạch", "Phúc Đức", "Phụ Mẫu"
        ]
        # Tìm vị trí cung Mệnh
        idx_menh = next((i for i, c in enumerate(dia_ban) if c.get('ten_cung') == cung_menh_chi), None)
        if idx_menh is None:
            return dia_ban
        # Xác định chiều đi
        if am_duong_nam_nu in ["Dương Nam", "Âm Nữ"]:
            chuc_nang_list = chuc_nang_thuan
            step = 1
        else:
            chuc_nang_list = chuc_nang_nghich
            step = -1
        # Gán tên chức năng cho từng cung
        for i in range(12):
            idx = (idx_menh + i * step) % 12
            dia_ban[idx]['cung_chuc_nang'] = chuc_nang_list[i]
        return dia_ban

    def tinh_can_luong(self, ngay_al, thang_al, nam_can, nam_chi, gio_chi):
        """
        Tính cân lượng theo bảng Lục Thập Hoa Giáp Cân Lượng chuẩn Bắc Tông.
        Tham số:
            - ngay_al: ngày âm lịch (1-30)
            - thang_al: tháng âm lịch (1-12)
            - nam_can: can năm sinh (Giáp, Ất, ...)
            - nam_chi: chi năm sinh (Tý, Sửu, ...)
            - gio_chi: chi giờ sinh (Tý, Sửu, ...)
        Trả về chuỗi mô tả cân lượng và số lượng lạng.
        """
        # Bảng cân lượng chuẩn Bắc Tông (Lục Thập Hoa Giáp Cân Lượng)
        # Dưới đây là bảng rút gọn, bạn nên thay bằng bảng đầy đủ nếu có
        # Mỗi mục là (can, chi, thang, ngay, gio): số lạng
        # Thực tế bảng chuẩn là cộng từng phần: năm, tháng, ngày, giờ
        # Dưới đây là các bảng lookup chuẩn hóa (theo sách cổ truyền)
        can_luong_nam = {
            'Giáp': 1.2, 'Ất': 1.0, 'Bính': 0.9, 'Đinh': 0.7, 'Mậu': 1.6,
            'Kỷ': 0.8, 'Canh': 1.5, 'Tân': 0.7, 'Nhâm': 1.5, 'Quý': 0.8
        }
        can_luong_chi = {
            'Tý': 0.7, 'Sửu': 0.8, 'Dần': 0.9, 'Mão': 1.0, 'Thìn': 1.1, 'Tỵ': 1.2,
            'Ngọ': 1.3, 'Mùi': 1.4, 'Thân': 1.5, 'Dậu': 1.6, 'Tuất': 1.7, 'Hợi': 1.8
        }
        can_luong_thang = [0, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]  # 1-12
        can_luong_ngay = [0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]  # 1-30
        can_luong_gio = {
            'Tý': 1.6, 'Sửu': 0.5, 'Dần': 1.0, 'Mão': 0.6, 'Thìn': 1.1, 'Tỵ': 0.5,
            'Ngọ': 1.6, 'Mùi': 0.6, 'Thân': 1.0, 'Dậu': 0.6, 'Tuất': 1.1, 'Hợi': 0.5
        }
        # Lấy giá trị từng phần
        nam_l = can_luong_nam.get(nam_can, 0)
        chi_l = can_luong_chi.get(nam_chi, 0)
        thang_l = can_luong_thang[thang_al] if 1 <= thang_al <= 12 else 0
        ngay_l = can_luong_ngay[ngay_al] if 1 <= ngay_al <= 30 else 0
        gio_l = can_luong_gio.get(gio_chi, 0)
        so_luong = nam_l + chi_l + thang_l + ngay_l + gio_l
        return f"Cân lượng: {so_luong:.2f} lạng", so_luong

    def is_leap_lunar_year(self, year_gregorian):
        """
        Kiểm tra năm dương lịch có phải là năm nhuận âm lịch không.
        Trả về (is_leap, leap_month):
            - is_leap: True nếu là năm nhuận âm lịch, False nếu không
            - leap_month: số tháng nhuận (1-12) nếu có, None nếu không
        """
        from lunardate import LunarDate
        # Thử từng tháng xem có tháng nhuận không
        for m in range(1, 13):
            try:
                # Nếu tháng nhuận tồn tại, LunarDate sẽ không raise exception
                LunarDate(year_gregorian, m, 1, True)
                return True, m
            except ValueError:
                continue
        return False, None

    def luan_van_han_luu_nien(self, year_gregorian, month_gregorian, birth_info):
        """
        Luận vận hạn/lưu niên/lưu nguyệt cho năm/tháng dương lịch cụ thể.
        birth_info: dict gồm các thông tin sinh (năm, tháng, ngày, giờ, can, chi, giới tính...)
        Trả về dict kết quả luận giải Bắc Tông:
            - Thông tin năm nhuận
            - Cung lưu niên (năm xem)
            - Cung lưu nguyệt (tháng xem)
            - Gợi ý vận hạn chính
        """
        # Kiểm tra năm nhuận
        is_leap, leap_month = self.is_leap_lunar_year(year_gregorian)
        # Xác định chi năm xem
        DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        chi_nam_xem = DIA_CHI[(year_gregorian + 8) % 12]  # 1900 là Canh Tý
        # Xác định cung lưu niên: Đếm thuận từ cung Mệnh theo số tuổi (năm xem - năm sinh âm lịch + 1)
        cung_menh = birth_info.get('cung_menh')
        tuoi_am = year_gregorian - birth_info.get('nam_sinh_dl') + 1
        dia_ban = birth_info.get('dia_ban', [])
        idx_menh = next((i for i, c in enumerate(dia_ban) if c.get('ten_cung') == cung_menh), 0)
        idx_luu_nien = (idx_menh + (tuoi_am - 1)) % 12
        cung_luu_nien = dia_ban[idx_luu_nien]['ten_cung'] if dia_ban else DIA_CHI[idx_luu_nien]
        # Xác định cung lưu nguyệt: Đếm thuận từ cung lưu niên theo số tháng xem (tháng 1 tại cung lưu niên)
        idx_luu_nguyet = (idx_luu_nien + (month_gregorian - 1)) % 12
        cung_luu_nguyet = dia_ban[idx_luu_nguyet]['ten_cung'] if dia_ban else DIA_CHI[idx_luu_nguyet]
        # Gợi ý vận hạn chính (có thể mở rộng theo sao, đại hạn...)
        van_han = f"Năm {year_gregorian} ({chi_nam_xem}), tháng {month_gregorian}: Lưu niên tại {cung_luu_nien}, lưu nguyệt tại {cung_luu_nguyet}."
        if is_leap and month_gregorian == leap_month:
            van_han += " Tháng này là tháng nhuận, nên tham khảo thêm luận giải đặc biệt."
        result = {
            'is_leap_year': is_leap,
            'leap_month': leap_month,
            'chi_nam_xem': chi_nam_xem,
            'cung_luu_nien': cung_luu_nien,
            'cung_luu_nguyet': cung_luu_nguyet,
            'van_han': van_han
        }
        return result

    def calculate_with_luu_niên(self, birth_info, year_xem, month_xem):
        """
        Tích hợp luận vận hạn/lưu niên/lưu nguyệt vào engine tổng:
        - birth_info: dict thông tin sinh (có thể thiếu can/chi năm, chi giờ, sẽ tự động bổ sung)
        - year_xem: năm dương lịch cần xem
        - month_xem: tháng dương lịch cần xem
        Trả về dict kết quả đầy đủ: lá số gốc + luận vận hạn/lưu niên/lưu nguyệt
        """
        # Bổ sung tự động chuyển đổi dương lịch sang âm lịch nếu thiếu
        if (('ngay_al' not in birth_info or birth_info.get('ngay_al') is None) and
            all(k in birth_info and birth_info[k] is not None for k in ['ngay_dl', 'thang_dl', 'nam_dl'])):
            try:
                from lunardate import LunarDate
                lunar = LunarDate.fromSolarDate(birth_info['nam_dl'], birth_info['thang_dl'], birth_info['ngay_dl'])
                birth_info['ngay_al'] = lunar.day
                birth_info['thang_al'] = lunar.month
                birth_info['nam_al'] = lunar.year
            except Exception as e:
                birth_info['can_luong_debug'] = f'Lỗi chuyển đổi âm lịch: {e}'
        # Chuyển đổi giờ sinh số sang chi nếu cần (bất kể birth_info có trường gio_chi hay không)
        GIO_CHI_LIST = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        if 'gio_sinh' in birth_info and birth_info['gio_sinh'] is not None:
            birth_info['gio_chi'] = GIO_CHI_LIST[birth_info['gio_sinh'] % 12]
        # Bổ sung tự động can/chi năm nếu thiếu
        CAN_LIST = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
        CHI_LIST = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        if 'nam_al' in birth_info:
            if birth_info.get('nam_can') is None:
                can_idx = (birth_info['nam_al'] + 6) % 10
                birth_info['nam_can'] = CAN_LIST[can_idx]
            if birth_info.get('nam_chi') is None:
                chi_idx = (birth_info['nam_al'] + 8) % 12
                birth_info['nam_chi'] = CHI_LIST[chi_idx]
        # Tính cân lượng nếu đủ thông tin và không có giá trị None
        can_luong = None
        can_luong_keys = ['ngay_al', 'thang_al', 'nam_can', 'nam_chi', 'gio_chi']
        missing_keys = [k for k in can_luong_keys if k not in birth_info or birth_info[k] is None]
        if not missing_keys:
            can_luong = self.tinh_can_luong(
                birth_info['ngay_al'],
                birth_info['thang_al'],
                birth_info['nam_can'],
                birth_info['nam_chi'],
                birth_info['gio_chi']
            )
        else:
            birth_info['can_luong_debug'] = f'Thiếu trường: {missing_keys}'
        # Luận vận hạn/lưu niên/lưu nguyệt
        van_han_info = self.luan_van_han_luu_nien(year_xem, month_xem, birth_info)
        # Kết hợp kết quả
        result = dict(birth_info)
        if can_luong:
            result['can_luong'] = can_luong[0]
            result['so_luong'] = can_luong[1]
        result['luu_niên'] = van_han_info
        return result
