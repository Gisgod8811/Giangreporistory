# src/an_sao.py
# Các hàm an sao chính tinh, phụ tinh, vòng, ...

import src.config as config

class SaoCalculator:
    def __init__(self):
        pass

    def an_chinh_tinh(self, dia_ban, ngay_sinh_al, cuc):
        # Bắc Tông: luôn dùng vòng địa chi Dần
        dia_chi = ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu']
        tu_vi_sao = ["Tử Vi", "Thiên Cơ", "Thái Dương", "Vũ Khúc", "Thiên Đồng", "Liêm Trinh"]
        thien_phu_sao = ["Thiên Phủ", "Thái Âm", "Tham Lang", "Cự Môn", "Thiên Tướng", "Thiên Lương", "Thất Sát", "Phá Quân"]
        so_cuc_map = {"Nhị": 2, "Tam": 3, "Tứ": 4, "Ngũ": 5, "Lục": 6}
        so_cuc = None
        for k in so_cuc_map:
            if k in cuc:
                so_cuc = so_cuc_map[k]
                break
        if so_cuc is None:
            return dia_ban
        # Bắc Tông: Tử Vi luôn an tại Dần, dịch chuyển theo bảng Bắc Tông
        tu_vi_table = [
            [0, 3, 6, 9, 0], [1, 4, 7, 10, 1], [2, 5, 8, 11, 2], [3, 6, 9, 0, 3], [4, 7, 10, 1, 4],
            [5, 8, 11, 2, 5], [6, 9, 0, 3, 6], [7, 10, 1, 4, 7], [8, 11, 2, 5, 8], [9, 0, 3, 6, 9],
            [10, 1, 4, 7, 10], [11, 2, 5, 8, 11], [0, 3, 6, 9, 0], [1, 4, 7, 10, 1], [2, 5, 8, 11, 2],
            [3, 6, 9, 0, 3], [4, 7, 10, 1, 4], [5, 8, 11, 2, 5], [6, 9, 0, 3, 6], [7, 10, 1, 4, 7],
            [8, 11, 2, 5, 8], [9, 0, 3, 6, 9], [10, 1, 4, 7, 10], [11, 2, 5, 8, 11], [0, 3, 6, 9, 0],
            [1, 4, 7, 10, 1], [2, 5, 8, 11, 2], [3, 6, 9, 0, 3], [4, 7, 10, 1, 4], [5, 8, 11, 2, 5],
        ]
        idx_ngay = (ngay_sinh_al - 1) % 30
        idx_cuc = so_cuc - 2
        tu_vi_pos = tu_vi_table[idx_ngay][idx_cuc]
        pos = tu_vi_pos
        for i, sao in enumerate(tu_vi_sao):
            cung_ten = dia_chi[pos]
            trang_thai = config.TRANG_THAI_SAO[sao][cung_ten]
            sao_object = {"ten": sao, "trang_thai": trang_thai}
            dia_ban[pos]["chinh_tinh"].append(sao_object)
            if i == 0:
                pos = (pos - 1) % 12
            elif i == 1:
                pos = (pos - 3) % 12
            elif i == 2:
                pos = (pos - 1) % 12
            elif i == 3:
                pos = (pos - 1) % 12
            elif i == 4:
                pos = (pos - 2) % 12
        # Thiên Phủ đối xứng Dần-Thân
        thien_phu_pos = (6 + tu_vi_pos) % 12
        pos = thien_phu_pos
        for i, sao in enumerate(thien_phu_sao):
            cung_ten = dia_chi[pos]
            trang_thai = config.TRANG_THAI_SAO[sao][cung_ten]
            sao_object = {"ten": sao, "trang_thai": trang_thai}
            dia_ban[pos]["chinh_tinh"].append(sao_object)
            if i < 6:
                pos = (pos + 1) % 12
            elif i == 6:
                pos = (pos + 3) % 12
        return dia_ban

    def an_hoa_linh(self, dia_ban, nam_chi, gio_sinh_chi):
        dia_chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        # 1. Xác định tam hợp của năm chi
        tam_hop = config.HOA_LINH_TAM_HOP[nam_chi]
        # 2. Cung khởi đầu là cung đầu tiên của tam hợp
        cung_khoi = tam_hop[0]
        idx_khoi = dia_chi.index(cung_khoi)
        # 3. Xác định chiều an
        chieu = config.HOA_LINH_CHIEU[gio_sinh_chi]
        # 4. An Hỏa Tinh
        if chieu == 'thuận':
            idx_hoa = (idx_khoi + 1) % 12
            idx_linh = (idx_khoi + 2) % 12
        else:
            idx_hoa = (idx_khoi - 1) % 12
            idx_linh = (idx_khoi - 2) % 12
        # 5. Lấy trạng thái và an vào dia_ban
        # Hỏa Tinh
        hoa_cung = dia_chi[idx_hoa]
        trang_thai_hoa = config.TRANG_THAI_SAO['Hỏa Tinh'][hoa_cung]
        sao_hoa = {"ten": "Hỏa Tinh", "trang_thai": trang_thai_hoa}
        dia_ban[idx_hoa]["sat_tinh"].append(sao_hoa)
        # Linh Tinh
        linh_cung = dia_chi[idx_linh]
        trang_thai_linh = config.TRANG_THAI_SAO['Linh Tinh'][linh_cung]
        sao_linh = {"ten": "Linh Tinh", "trang_thai": trang_thai_linh}
        dia_ban[idx_linh]["sat_tinh"].append(sao_linh)
        return dia_ban

    def an_vong_loc_ton(self, dia_ban, can_nam, am_duong_nam_nu):
        dia_chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        # Vị trí Lộc Tồn theo can năm
        loc_ton_dict = {
            "Giáp": "Dần", "Ất": "Mão", "Bính": "Tỵ", "Đinh": "Ngọ", "Mậu": "Thân",
            "Kỷ": "Dậu", "Canh": "Hợi", "Tân": "Tý", "Nhâm": "Thìn", "Quý": "Tỵ"
        }
        if can_nam not in loc_ton_dict:
            return dia_ban
        loc_ton_cung = loc_ton_dict[can_nam]
        idx_start = (dia_chi.index(loc_ton_cung) + 1) % 12  # Bắt đầu từ cung kế tiếp
        # Xác định chiều đi
        thuan = am_duong_nam_nu in ["Dương Nam", "Âm Nữ"]
        for i, sao in enumerate(config.VONG_LOC_TON):
            if thuan:
                idx = (idx_start + i) % 12
            else:
                idx = (idx_start - i) % 12
            cung_ten = dia_chi[idx]
            trang_thai = config.TRANG_THAI_SAO.get(sao, {c: 'B' for c in dia_chi})[cung_ten]
            sao_object = {"ten": sao, "trang_thai": trang_thai}
            dia_ban[idx]["phu_tinh_khac"].append(sao_object)
        return dia_ban

    def an_luu_tinh(self, dia_ban, nam_xem_can, nam_xem_chi):
        """
        An các Lưu tinh: L.Thái Tuế, L.Lộc Tồn, L.Kình Dương, L.Đà La, L.Thiên Mã, L.Tứ Hóa.
        """
        dia_chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        # Lưu Thái Tuế: tại cung trùng với chi năm xem
        for idx, cung in enumerate(dia_ban):
            if cung['ten_cung'] == nam_xem_chi:
                cung['luu_tinh'].append({'ten': 'L.Thái Tuế'})
        # Lưu Lộc Tồn, Lưu Kình Dương, Lưu Đà La: giống logic an Lộc Tồn theo can
        loc_ton_dict = {
            "Giáp": "Dần", "Ất": "Mão", "Bính": "Tỵ", "Đinh": "Ngọ", "Mậu": "Thân",
            "Kỷ": "Dậu", "Canh": "Hợi", "Tân": "Tý", "Nhâm": "Thìn", "Quý": "Tỵ"
        }
        # Lưu Lộc Tồn
        if nam_xem_can in loc_ton_dict:
            loc_ton_cung = loc_ton_dict[nam_xem_can]
            for cung in dia_ban:
                if cung['ten_cung'] == loc_ton_cung:
                    cung['luu_tinh'].append({'ten': 'L.Lộc Tồn'})
        # Lưu Kình Dương, Lưu Đà La (theo thứ tự sau Lộc Tồn, thuận chiều)
        if nam_xem_can in loc_ton_dict:
            idx_loc_ton = dia_chi.index(loc_ton_dict[nam_xem_can])
            idx_kinh = (idx_loc_ton + 1) % 12
            idx_da = (idx_loc_ton + 2) % 12
            dia_ban[idx_kinh]['luu_tinh'].append({'ten': 'L.Kình Dương'})
            dia_ban[idx_da]['luu_tinh'].append({'ten': 'L.Đà La'})
        # Lưu Thiên Mã: đối xung với Thái Tuế (cách 6 cung)
        idx_tt = dia_chi.index(nam_xem_chi)
        idx_ma = (idx_tt + 6) % 12
        dia_ban[idx_ma]['luu_tinh'].append({'ten': 'L.Thiên Mã'})
        # Lưu Tứ Hóa: Hóa Lộc, Hóa Quyền, Hóa Khoa, Hóa Kỵ (theo can năm xem)
        tu_hoa_dict = {
            'Giáp': ['L.Hóa Lộc', 'L.Hóa Quyền', 'L.Hóa Khoa', 'L.Hóa Kỵ'],
            'Ất': ['L.Hóa Khoa', 'L.Hóa Quyền', 'L.Hóa Lộc', 'L.Hóa Kỵ'],
            'Bính': ['L.Hóa Quyền', 'L.Hóa Khoa', 'L.Hóa Kỵ', 'L.Hóa Lộc'],
            'Đinh': ['L.Hóa Khoa', 'L.Hóa Kỵ', 'L.Hóa Quyền', 'L.Hóa Lộc'],
            'Mậu': ['L.Hóa Kỵ', 'L.Hóa Lộc', 'L.Hóa Khoa', 'L.Hóa Quyền'],
            'Kỷ': ['L.Hóa Lộc', 'L.Hóa Khoa', 'L.Hóa Quyền', 'L.Hóa Kỵ'],
            'Canh': ['L.Hóa Quyền', 'L.Hóa Lộc', 'L.Hóa Khoa', 'L.Hóa Kỵ'],
            'Tân': ['L.Hóa Khoa', 'L.Hóa Quyền', 'L.Hóa Kỵ', 'L.Hóa Lộc'],
            'Nhâm': ['L.Hóa Kỵ', 'L.Hóa Lộc', 'L.Hóa Khoa', 'L.Hóa Quyền'],
            'Quý': ['L.Hóa Lộc', 'L.Hóa Khoa', 'L.Hóa Quyền', 'L.Hóa Kỵ']
        }
        if nam_xem_can in tu_hoa_dict:
            hoa_names = tu_hoa_dict[nam_xem_can]
            # Gán vào 4 chính tinh: Tử Vi, Thiên Cơ, Thái Dương, Vũ Khúc (theo thứ tự)
            chinh_tinh_order = ['Tử Vi', 'Thiên Cơ', 'Thái Dương', 'Vũ Khúc']
            for hoa, tinh in zip(hoa_names, chinh_tinh_order):
                for cung in dia_ban:
                    for sao in cung['chinh_tinh']:
                        if sao['ten'] == tinh:
                            cung['luu_tinh'].append({'ten': hoa})
        return dia_ban

    # ...add other star placement methods here (an_luc_sat_tinh, an_luc_cat_tinh, etc.)...

# Có thể bổ sung các class/phân nhóm khác nếu cần
