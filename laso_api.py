# laso_api.py (Phiên bản linh hoạt, tự đổi lịch bằng thư viện)
# Chạy file này bằng lệnh: python laso_api.py

import os
import json
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, root_validator
from typing import Optional
import uvicorn
import google.generativeai as genai
from dotenv import load_dotenv
from lunardate import LunarDate # Import thư viện đổi lịch
from fastapi.middleware.cors import CORSMiddleware

# --- Cấu hình ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong file .env.")
genai.configure(api_key=api_key)
llm = genai.GenerativeModel("gemini-2.0-flash")
app = FastAPI(title="API Lập Lá Số Tử Vi", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thay đổi thành domain cụ thể nếu muốn bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Định nghĩa cấu trúc dữ liệu đầu vào linh hoạt ---
class BirthInfo(BaseModel):
    gioi_tinh: str
    gio_sinh: int
    # Thông tin dương lịch (tùy chọn)
    ngay_dl: Optional[int] = None
    thang_dl: Optional[int] = None
    nam_dl: Optional[int] = None
    # Thông tin âm lịch (tùy chọn)
    ngay_al: Optional[int] = None
    thang_al: Optional[int] = None
    nam_al: Optional[int] = None
    nhuan: Optional[bool] = False # Tháng nhuận?
    # Thông tin xem vận hạn (tùy chọn)
    nam_xem: Optional[int] = None
    thang_xem: Optional[int] = None
    @root_validator(pre=True)
    def check_at_least_one_date_provided(cls, values):
        solar_provided = values.get('nam_dl') is not None
        lunar_provided = values.get('nam_al') is not None
        if not solar_provided and not lunar_provided:
            raise ValueError('Phải cung cấp ít nhất một loại ngày sinh (Dương lịch hoặc Âm lịch).')
        return values

# --- Prompt Template ---
PROMPT_TEMPLATE = """Bạn là một engine tính toán Tử Vi tự động, không có cảm xúc. Nhiệm vụ của bạn là nhận thông tin đầu vào (bao gồm ngày Âm lịch đã được tính sẵn) và trả về một đối tượng JSON duy nhất chứa toàn bộ dữ liệu của lá số.

**THÔNG TIN ĐẦU VÀO:**
* **Giới tính:** {gioi_tinh}
* **Ngày sinh dương lịch:** {ngay_dl} tháng {thang_dl} năm {nam_dl}
* **Giờ sinh:** {gio_sinh} giờ
* **Ngày sinh âm lịch:** Ngày {ngay_al} tháng {thang_al} năm {can_chi_nam}

**QUY TẮC THỰC HIỆN (BẮT BUỘC TUÂN THỦ NGHIÊM NGẶT):**

Dựa trên các quy tắc phổ thông của Tử Vi Đẩu Số, hãy thực hiện tuần tự các bước sau để lập một lá số hoàn chỉnh:

1.  **Tính toán cơ bản:** Xác định Can Chi năm, tháng, ngày, giờ. Tìm Ngũ hành nạp âm và Cục của lá số.
2.  **An Cung:** An cung Mệnh, cung Thân, và 12 cung chức năng.
3.  **An Sao chi tiết:** An tất cả các sao sau đây vào đúng 12 cung của địa bàn:
    * **14 Chính tinh:** (Tử Vi, Thiên Phủ, ...)
    * **Lục Sát Tinh:** Địa Không, Địa Kiếp, Kình Dương, Đà La, Hỏa Tinh, Linh Tinh.
    * **Lục Cát Tinh:** Văn Xương, Văn Khúc, Tả Phù, Hữu Bật, Thiên Khôi, Thiên Việt.
    * **Tứ Hóa:** Hóa Lộc, Hóa Quyền, Hóa Khoa, Hóa Kỵ theo Can năm sinh.
    * **Vòng Lộc Tồn:** Lộc Tồn, Bác Sỹ, Lực Sỹ, Thanh Long, Tiểu Hao, Tướng Quân, Tấu Thư, Phi Liêm, Hỷ Thần, Bệnh Phù, Đại Hao, Phục Binh, Quan Phủ.
    * **Vòng Thái Tuế:** Thái Tuế, Thiếu Dương, Tang Môn, Thiếu Âm, Quan Phù, Tử Phù, Tuế Phá, Long Đức, Bạch Hổ, Phúc Đức, Điếu Khách, Trực Phù.
    * **Vòng Tràng Sinh:** Tràng Sinh, Mộc Dục, Quan Đới, Lâm Quan, Đế Vượng, Suy, Bệnh, Tử, Mộ, Tuyệt, Thai, Dưỡng.
    * **Các sao đôi quan trọng:** Long Trì, Phượng Các; Ân Quang, Thiên Quý; Tam Thai, Bát Tọa; Thiên Quan, Thiên Phúc; Thiên Hình, Thiên Diêu; Thiên Khốc, Thiên Hư; Cô Thần, Quả Tú.
    * **Các sao đơn quan trọng khác:** Thiên Mã, Hồng Loan, Thiên Hỷ, Đào Hoa, Hoa Cái, Kiếp Sát, Phá Toái, Đẩu Quân, Thiên Không, Thiên Y, Thiên Trù, Lưu Hà.

**ĐỊNH DẠNG ĐẦU RA (CỰC KỲ QUAN TRỌNG):**
* Chỉ trả về **duy nhất một đối tượng JSON**, không có bất kỳ văn bản giải thích nào khác.
* Cấu trúc JSON phải như sau:
    * Một object chính.
    * Key `thong_tin_duong_so` chứa các thông tin cơ bản.
    * Key `dia_ban` chứa một mảng (array) gồm đúng 12 object, mỗi object đại diện cho một cung từ Tý đến Hợi.
    * Trong mỗi cung, các sao phải được phân loại vào các mảng: `chinh_tinh`, `cat_tinh`, `sat_tinh`, `phu_tinh_khac`.


Hãy bắt đầu tính toán và trả về đối tượng JSON.
"""

def get_can_chi_nam(nam_al):
    can_list = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    can = can_list[(nam_al + 6) % 10]
    chi = chi_list[(nam_al + 8) % 12]
    return f"{can} {chi}"

def ensure_full_json_structure(chart_data):
    # Bổ sung các trường còn thiếu cho thong_tin_duong_so
    thong_tin_keys = [
        "ho_ten", "gioi_tinh", "duong_lich", "am_lich", "gio_sinh", "nam_xem", "tuoi", "am_duong_nghia", "ban_menh", "menh_cuc", "chu_menh", "chu_than"
    ]
    if "thong_tin_duong_so" not in chart_data:
        chart_data["thong_tin_duong_so"] = {}
    for key in thong_tin_keys:
        chart_data["thong_tin_duong_so"].setdefault(key, "")

    # Bổ sung các trường còn thiếu cho từng cung trong dia_ban
    cung_keys = [
        "ten_cung", "can_chi", "dai_han", "vong_trang_sinh", "vong_luu", "luu_nien",
        "cung_chuc_nang", "chinh_tinh", "cat_tinh", "sat_tinh", "phu_tinh_khac"
    ]
    if "dia_ban" not in chart_data or not isinstance(chart_data["dia_ban"], list):
        chart_data["dia_ban"] = []
    for cung in chart_data["dia_ban"]:
        for key in cung_keys:
            if key in ["cung_chuc_nang", "chinh_tinh", "cat_tinh", "sat_tinh", "phu_tinh_khac"]:
                cung.setdefault(key, [])
            else:
                cung.setdefault(key, "")
    return chart_data

# --- API Endpoint ---
@app.post("/lap-la-so/", response_model=dict)
def create_astrological_chart(info: BirthInfo):
    print("=== ĐÃ VÀO HÀM create_astrological_chart ===")
    print(f"Nhận được yêu cầu lập lá số cho: {info.model_dump_json(indent=2)}")
    try:
        # --- LOGIC CHUYỂN ĐỔI NGÀY THÔNG MINH ---
        if info.nam_dl:  # Nếu nhập dương lịch, chuyển sang âm lịch
            print(f"Phát hiện ngày Dương lịch. Đang đổi: {info.ngay_dl}/{info.thang_dl}/{info.nam_dl}")
            # Kiểm tra dữ liệu ngày tháng năm hợp lệ
            if not (1 <= info.thang_dl <= 12 and 1 <= info.ngay_dl <= 31):
                raise ValueError("Ngày hoặc tháng dương lịch không hợp lệ!")
            lunar_date = LunarDate.fromSolarDate(info.nam_dl, info.thang_dl, info.ngay_dl)
        else:  # Nếu nhập âm lịch, giữ nguyên
            print(f"Đang dùng ngày Âm lịch: {info.ngay_al}/{info.thang_al}/{info.nam_al}")
            lunar_date = LunarDate(info.nam_al, info.thang_al, info.ngay_al)

        # Lấy thông tin âm lịch để gửi cho Gemini
        full_info = {
            "gioi_tinh": info.gioi_tinh,
            "gio_sinh": info.gio_sinh,
            "ngay_dl": info.ngay_dl if info.ngay_dl else lunar_date.toSolarDate().day,
            "thang_dl": info.thang_dl if info.thang_dl else lunar_date.toSolarDate().month,
            "nam_dl": info.nam_dl if info.nam_dl else lunar_date.toSolarDate().year,
            "ngay_al": lunar_date.day,
            "thang_al": lunar_date.month,
            "can_chi_nam": get_can_chi_nam(lunar_date.year)
        }
        print(f"[DEBUG] full_info gửi Gemini: {full_info}")
        # ---------------------------------------------
        # Bước B: Điền thông tin đầy đủ vào prompt lập số
        try:
            filled_prompt = PROMPT_TEMPLATE.format(**full_info)
        except Exception as prompt_exc:
            print(f"[ERROR] Lỗi khi format prompt: {prompt_exc}")
            print(f"[DEBUG] full_info: {full_info}")
            raise HTTPException(status_code=500, detail=f"Lỗi format prompt: {prompt_exc}")
        print("[DEBUG] filled_prompt gửi Gemini:")
        print(filled_prompt)
        print("Đang gửi yêu cầu lập lá số chi tiết đến Gemini...")
        print("[DEBUG] Chuẩn bị gọi Gemini...")
        try:
            response = llm.generate_content(filled_prompt)
            print("[DEBUG] Đã nhận response từ Gemini!")
        except Exception as gemini_exc:
            print(f"[ERROR] Lỗi khi gọi Gemini API: {gemini_exc}")
            raise HTTPException(status_code=500, detail=f"Lỗi khi gọi Gemini API: {gemini_exc}")
        print(f"[DEBUG] Gemini raw response object: {response}")
        raw_json_text = response.text.strip()
        # Làm sạch kết quả trả về
        if '```json' in raw_json_text:
            raw_json_text = raw_json_text.split('```json', 1)[1]
        if '```' in raw_json_text:
            raw_json_text = raw_json_text.split('```', 1)[0]
        raw_json_text = raw_json_text.strip()
        # Lấy phần JSON object đầu tiên nếu có ký tự thừa
        start = raw_json_text.find('{')
        end = raw_json_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            cleaned_json = raw_json_text[start:end+1]
        else:
            cleaned_json = raw_json_text
        print("=== RAW JSON TEXT NHẬN ĐƯỢC TỪ GEMINI ===")
        print(cleaned_json)
        try:
            chart_data = json.loads(cleaned_json)
        except Exception as e:
            print("[WARN] Parse lỗi, thử tự động thêm dấu { } bao quanh...")
            try:
                fallback_json = '{' + cleaned_json.strip().lstrip(',').lstrip('\n').lstrip() + '}'
                print("[DEBUG] Fallback JSON thử parse:")
                print(fallback_json)
                chart_data = json.loads(fallback_json)
            except Exception as e2:
                print("LỖI PARSE JSON, raw_json_text nhận được:")
                print(raw_json_text)
                raise HTTPException(status_code=500, detail=f"Không thể tạo lá số. Lỗi: {str(e2)}")
        chart_data = ensure_full_json_structure(chart_data)
        print("Parse JSON lá số thành công.")
        return chart_data
    except Exception as e:
        print(f"Lỗi nghiêm trọng: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể tạo lá số. Lỗi: {str(e)}")

# --- Bộ nhớ tạm để lưu thông tin sinh theo user_id (demo, production nên dùng DB) ---
user_birthinfo_store = {}

class LuuNienRequest(BaseModel):
    user_id: str
    nam_xem: int
    thang_xem: Optional[int] = None  # Nếu chỉ xem lưu niên thì không cần tháng

@app.post("/api/laso", response_model=dict)
def save_birth_info(user_id: str, info: BirthInfo):
    """
    Nhận thông tin sinh, trả về lá số Bắc Tông chuẩn, đồng thời lưu vào bộ nhớ tạm theo user_id.
    Nếu có nhập nam_xem/thang_xem thì trả về luôn cả luận vận hạn/lưu niên/lưu nguyệt.
    """
    chart_data = create_astrological_chart(info)
    user_birthinfo_store[user_id] = info.model_dump()
    # Nếu có nhập năm/tháng xem thì trả về luôn luận vận hạn/lưu niên/lưu nguyệt
    if info.nam_xem:
        from src.cung import CungCalculator
        calc = CungCalculator()
        # Lấy birth_info dạng dict, bổ sung các trường cần thiết
        birth_info = info.model_dump()
        # Nếu thiếu ngày/tháng/năm âm thì tự động chuyển đổi
        if not birth_info.get('ngay_al') and birth_info.get('ngay_dl'):
            from lunardate import LunarDate
            lunar = LunarDate.fromSolarDate(birth_info['nam_dl'], birth_info['thang_dl'], birth_info['ngay_dl'])
            birth_info['ngay_al'] = lunar.day
            birth_info['thang_al'] = lunar.month
            birth_info['nam_al'] = lunar.year
        # Chuyển đổi giờ sinh số sang chi nếu cần
        GIO_CHI_LIST = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        if 'gio_sinh' in birth_info and birth_info['gio_sinh'] is not None:
            birth_info['gio_chi'] = GIO_CHI_LIST[birth_info['gio_sinh'] % 12]
        # Gọi luận vận hạn/lưu niên/lưu nguyệt
        van_han = calc.luan_van_han_luu_nien(
            info.nam_xem,
            info.thang_xem if info.thang_xem else 1,
            birth_info
        )
        chart_data['luu_niên'] = van_han
    return chart_data

@app.post("/api/luu_nien", response_model=dict)
def luan_van_han(req: LuuNienRequest):
    """
    Nhận user_id + năm/tháng xem, trả về luận vận hạn/lưu niên/lưu nguyệt chuẩn Bắc Tông (Python),
    phân tích chi tiết các sao, đại hạn, đánh giá tổng quan tốt/xấu, và (tùy chọn) giải thích AI.
    """
    info_dict = user_birthinfo_store.get(req.user_id)
    if not info_dict:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin sinh cho user_id này. Hãy lập lá số trước.")
    from src.cung import CungCalculator
    calc = CungCalculator()
    birth_info = dict(info_dict)
    if not birth_info.get('ngay_al') and birth_info.get('ngay_dl'):
        from lunardate import LunarDate
        lunar = LunarDate.fromSolarDate(birth_info['nam_dl'], birth_info['thang_dl'], birth_info['ngay_dl'])
        birth_info['ngay_al'] = lunar.day
        birth_info['thang_al'] = lunar.month
        birth_info['nam_al'] = lunar.year
    GIO_CHI_LIST = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    if 'gio_sinh' in birth_info and birth_info['gio_sinh'] is not None:
        birth_info['gio_chi'] = GIO_CHI_LIST[birth_info['gio_sinh'] % 12]
    # Tính luận vận hạn/lưu niên/lưu nguyệt Bắc Tông
    result_bt = calc.calculate_with_luu_niên(birth_info, req.nam_xem, req.thang_xem if req.thang_xem else 1)
    # Phân tích chi tiết các sao tại cung lưu niên/lưu nguyệt
    dia_ban = birth_info.get('dia_ban', [])
    cung_luu_nien = result_bt['luu_niên']['cung_luu_nien']
    cung_luu_nguyet = result_bt['luu_niên']['cung_luu_nguyet']
    sao_luu_nien = next((c for c in dia_ban if c.get('ten_cung') == cung_luu_nien), {})
    sao_luu_nguyet = next((c for c in dia_ban if c.get('ten_cung') == cung_luu_nguyet), {})
    # Đánh giá tổng quan
    def danh_gia_cung(cung):
        chinh_tinh = set(cung.get('chinh_tinh', []))
        cat_tinh = set(cung.get('cat_tinh', []))
        sat_tinh = set(cung.get('sat_tinh', []))
        diem = len(cat_tinh) - len(sat_tinh)
        if 'Tử Vi' in chinh_tinh or 'Thiên Phủ' in chinh_tinh:
            diem += 2
        if 'Địa Không' in sat_tinh or 'Địa Kiếp' in sat_tinh:
            diem -= 2
        if diem >= 2:
            return 'Tốt', diem
        elif diem <= -2:
            return 'Xấu', diem
        else:
            return 'Trung bình', diem
    danh_gia_nien, diem_nien = danh_gia_cung(sao_luu_nien)
    danh_gia_nguyet, diem_nguyet = danh_gia_cung(sao_luu_nguyet)
    # Gợi ý hành động
    goi_y = []
    if danh_gia_nien == 'Xấu' or danh_gia_nguyet == 'Xấu':
        goi_y.append('Cẩn trọng sức khỏe, tài chính, đề phòng tiểu nhân.')
    if danh_gia_nien == 'Tốt' or danh_gia_nguyet == 'Tốt':
        goi_y.append('Năm/tháng thuận lợi để phát triển sự nghiệp, học tập, kết hôn.')
    if not goi_y:
        goi_y.append('Năm/tháng bình ổn, nên giữ vững mục tiêu, tránh thay đổi lớn.')
    # (Tùy chọn) Gọi Gemini để lấy giải thích AI
    result_ai = None
    try:
        prompt = f"Hãy giải thích chi tiết luận vận hạn/lưu niên/lưu nguyệt Bắc Tông cho năm {req.nam_xem}, tháng {req.thang_xem if req.thang_xem else 1} dựa trên thông tin sau:\n{result_bt}"
        response = llm.generate_content(prompt)
        result_ai = response.text.strip()
    except Exception as e:
        result_ai = f"Không thể lấy giải thích AI: {e}"
    return {
        "thong_tin_sinh": birth_info,
        "tuoi_am": req.nam_xem - birth_info.get('nam_al', 0) + 1,
        "can_luong": result_bt.get('can_luong'),
        "luu_niên": result_bt['luu_niên'],
        "sao_luu_nien": sao_luu_nien,
        "sao_luu_nguyet": sao_luu_nguyet,
        "danh_gia_luu_nien": danh_gia_nien,
        "danh_gia_luu_nguyet": danh_gia_nguyet,
        "goi_y": goi_y,
        "luan_giai_ai": result_ai
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)