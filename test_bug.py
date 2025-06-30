# test_bug.py
from src.engine import TuViEngine
from src.utils import gio_chi

print("\n>>> BẮT ĐẦU KIỂM TRA LÁ SỐ BỊ LỖI <<<\n")

gioi_tinh = "nam"
ngay_al = 25
thang_al = 11
nam_al = 1999
gio_sinh = 14  # Giờ Mùi (13h-15h)
nam_xem = 2025

try:
    engine = TuViEngine(
        gioi_tinh=gioi_tinh,
        ngay_al=ngay_al,
        thang_al=thang_al,
        nam_al=nam_al,
        gio_sinh=gio_sinh,
        nam_xem=nam_xem
    )
    final_chart = engine.calculate()
    print("\n--- KẾT QUẢ TỪ ENGINE ---")
    print(f"Cung Mệnh tính được: {final_chart['thong_tin_duong_so'].get('cung_menh_tai')}")
    print(f"Cung Thân tính được: {final_chart['thong_tin_duong_so'].get('cung_than_tai')}")
    print(f"Cục tính được: {final_chart['thong_tin_duong_so'].get('menh_cuc')}")
    print(f"Chủ Mệnh: {final_chart['thong_tin_duong_so'].get('chu_menh')}")
    print(f"Chủ Thân: {final_chart['thong_tin_duong_so'].get('chu_than')}")
    print("\n--- KẾT QUẢ MONG MUỐN ---")
    print("Cung Mệnh phải là: Ngọ")
    print("Cung Thân phải là: Ngọ")
    print("Cục phải là: Hỏa Lục Cục")
    print("Chủ Mệnh phải là: Văn Khúc")
    print("Chủ Thân phải là: Thiên Lương")
except Exception as e:
    print(f"!!! ĐÃ XẢY RA LỖI NGHIÊM TRỌNG: {e}")
