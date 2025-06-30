# src/utils.py
# Các hàm tiện ích chung cho Tử Vi

def get_can_chi_nam(nam_al: int) -> str:
    """Tính Can Chi của năm Âm lịch."""
    can_list = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
    chi_list = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
    can = can_list[nam_al % 10]
    chi = chi_list[nam_al % 12]
    return f"{can} {chi}"

def gio_chi(gio_sinh: int) -> str:
    """Chuyển đổi giờ sinh số (0-23) sang tên Chi."""
    chi_gio = [
        (23, 1, "Tý"), (1, 3, "Sửu"), (3, 5, "Dần"), (5, 7, "Mão"), (7, 9, "Thìn"), (9, 11, "Tỵ"),
        (11, 13, "Ngọ"), (13, 15, "Mùi"), (15, 17, "Thân"), (17, 19, "Dậu"), (19, 21, "Tuất"), (21, 23, "Hợi")
    ]
    for start, end, chi in chi_gio:
        if start <= gio_sinh < end or (start == 23 and (gio_sinh == 23 or gio_sinh < 1)):
            return chi
    return "Tý"
