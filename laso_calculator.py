# laso_calculator.py
# Refactored: Uses modular TuViEngine from src.engine

import json
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, root_validator
from typing import Optional
import uvicorn
from lunardate import LunarDate
from fastapi.middleware.cors import CORSMiddleware
from src.engine import TuViEngine
from src.rag_core import RAGCore
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# --- Cấu hình Gemini ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel("gemini-2.0-flash")
else:
    llm = None
    print("Cảnh báo: Không tìm thấy GEMINI_API_KEY trong file .env. Chức năng phân tích Gemini sẽ không hoạt động.")

# --- Prompt Template cho Gemini (Bắc Phái Methodology) ---
PROMPT_TEMPLATE = """Bạn là một bậc thầy Tử Vi uyên bác, am tường sâu sắc cả hai trường phái Nam Tông và Bắc Tông, nhưng **lấy phương pháp luận của Tử Vi Bắc Phái làm trọng tâm** để luận giải. Sứ mệnh của bạn là đưa ra những phân tích sắc bén, logic, truy nguyên nhân quả và có giá trị dự báo cao cho đương số.

Hãy sử dụng hệ thống lý luận của Tử Vi Bắc Phái để phân tích chi tiết lá số sau đây:

**Dữ liệu lá số:**
{chart}

**YÊU CẦU PHÂN TÍCH:**

**1. Phương pháp luận giải (theo lăng kính Bắc Phái):**
* **Khởi Lập Thiên Bàn & Định Cách Cục:** Nhận định cục diện tổng quan của lá số, nhưng quan trọng nhất là xác định vị trí của **Tứ Hóa nguyên thủy (Hóa Lộc, Quyền, Khoa, Kỵ theo Can năm sinh)**. Đây là những "dấu ấn" nghiệp lực và tiềm năng bẩm sinh của đương số.
* **Luận Cung Mệnh và Cung Thân:** Phân tích sâu Mệnh Thân, nhưng phải luận giải ý nghĩa của các sao qua lăng kính "ý tượng" khi chúng được **Tứ Hóa nguyên thủy** kích hoạt hoặc khi chúng đứng trong cung vị có chứa Tứ Hóa. Ví dụ: "Thái Dương Hóa Kỵ" tại Tài Bạch sẽ có ý tượng gì? "Liêm Trinh Hóa Lộc" tại Quan Lộc mang ý nghĩa ra sao?
* **Sử dụng Tứ Hóa Phi Tinh và Cung Vị Chuyển Hoán:** Đây là cốt lõi của Bắc Phái.
    * Luận giải sự tương tác giữa các cung thông qua việc **"phi hóa"** từ Thiên Can của từng cung. Ví dụ: "Cung Quan Lộc phi Hóa Kỵ nhập cung Phụ Mẫu" có ý nghĩa gì đối với sự nghiệp?
    * Sử dụng phép **"Cung vị chuyển hoán"** (ví dụ: lấy cung Phu Thê làm cung Mệnh để luận về tính cách, hoàn cảnh của người phối ngẫu).
* **Phân Tích Vận Hạn (Đại Vận & Lưu Niên):**
    * Luận **Tứ Hóa của Đại Vận** (theo Can của cung Đại Vận) và **Tứ Hóa của Lưu Niên** (theo Can của năm xem).
    * Phân tích sự **"trùng첩" (xếp chồng)** và **"xung kích"** giữa các Hóa Kỵ (Kỵ gốc, Kỵ Đại Vận, Kỵ Lưu Niên) để tìm ra các sự kiện mấu chốt và **"ứng kỳ"** (thời điểm xảy ra sự việc) trong vận hạn.
* **Nguyên tắc cân bằng:** Phân tích phải logic, rõ ràng, nêu bật cả nhân và quả, chỉ ra cả cơ hội (nơi Hóa Lộc, Hóa Quyền đến) và thách thức (nơi Hóa Kỵ xung phá).

**2. Nội dung chi tiết cần luận giải (áp dụng phương pháp trên):**

* **Bản Mệnh & Cách Cục (Góc nhìn Bắc Phái):**
    * Luận giải ý nghĩa của Tứ Hóa nguyên thủy tại các cung. Điều này nói lên điều gì về "thiên mệnh" của đương số?
    * Phân tích tính cách, tiềm năng, và những vấn đề cốt lõi trong cuộc đời đương số qua Mệnh, Thân và sự phân bổ của Tứ Hóa.

* **Công danh & Sự nghiệp:**
    * Luận Cung Quan Lộc, sự liên kết của nó với Mệnh-Tài. Quan trọng hơn, phân tích **"Quan Lộc cung phi Hóa"** đi đâu để biết xu hướng sự nghiệp, và các cung khác phi hóa đến Quan Lộc ra sao để biết tác động từ bên ngoài.

* **Tài chính & Tiền bạc:**
    * Luận Cung Tài Bạch. Phân tích **"Tài Bạch cung phi Hóa"** để biết dòng tiền đi đâu, và cách đương số sử dụng tiền bạc. Hóa Lộc và Hóa Kỵ từ cung Tài sẽ chỉ ra cách kiếm tiền và nguyên nhân hao tán.

* **Tình duyên & Hôn nhân:**
    * Luận Cung Phu Thê. Phân tích **"Phu Thê cung phi Hóa"** để luận đoán về diễn biến tình cảm, nguyên nhân dẫn đến các sự kiện trong hôn nhân. Kỵ từ Phu Thê xung đi đâu sẽ là mấu chốt của các vấn đề.

* **Sức khỏe & Tật ách:**
    * Luận Cung Tật Ách. Phân tích **Hóa Kỵ** từ Mệnh, Tật Ách và các cung liên quan để chỉ ra các bệnh tật tiềm ẩn và nguyên nhân sâu xa.

* **Phân tích Vận Hạn (Ứng Dụng Sâu Bắc Phái):**
    * **Đại Hạn 10 năm:** Luận tác động của Tứ Hóa Đại Vận lên Thiên Bàn (lá số gốc).
    * **Lưu Niên (Năm hiện tại):** Dựa vào năm xem trong dữ liệu, luận giải chi tiết sự tương tác của Tứ Hóa Lưu Niên với Tứ Hóa Đại Vận và Tứ Hóa Gốc. Tìm điểm **"Kỵ xung"** và **"Lộc nhập"** để đưa ra dự báo chính xác cho năm đó.

**3. Tổng kết & Lời khuyên chiến lược:**
* Tổng hợp các "điểm Kỵ" và "điểm Lộc" quan trọng nhất của lá số.
* Đưa ra lời khuyên mang tính chiến lược, giúp đương số hiểu rõ "nhân quả" trong số phận của mình, từ đó chủ động cải thiện, nắm bắt cơ hội và né tránh rủi ro.

**ĐỊNH DẠNG ĐẦU RA:**

Hãy trả về kết quả phân tích dưới dạng một đối tượng JSON duy nhất với cấu trúc sau:

{{
  "tong_quan_ban_menh": {{
    "cach_cuc_va_tu_hoa_goc": "...",
    "tinh_cach_va_so_phan_qua_lang_kinh_bac_phai": "..."
  }},
  "cong_danh_su_nghiep": {{
    "xu_huong_su_nghiep_qua_phi_hoa": "...",
    "co_hoi_va_thach_thuc": "..."
  }},
  "tai_chinh_tien_bac": {{
    "dong_tien_va_cach_kiem_tieu": "...",
    "nguyen_nhan_thanh_bai_tai_chinh": "..."
  }},
  "tinh_duyen_hon_nhan": {{
    "dien_bien_tinh_cam_qua_phi_hoa": "...",
    "mau_chot_van_de_hon_nhan": "..."
  }},
  "suc_khoe_tat_ach": {{
    "nguyen_nhan_benh_tat_tiem_an": "...",
    "loi_khuyen_phong_ngua": "..."
  }},
  "phan_tich_van_han": {{
    "tong_quan_cac_dai_han": "...",
    "du_bao_chi_tiet_nam_hien_tai": "..."
  }},
  "tong_ket_va_loi_khuyen": {{
    "cac_diem_mau_chot_cua_la_so": "...",
    "loi_khuyen_chien_luoc_cai_van": "..."
  }}
}}
"""

app = FastAPI(
    title="API Lập Lá Số Tử Vi (Logic Thuần Túy)",
    version="2.0.0",
    description="Phiên bản này sử dụng logic tính toán bằng Python thay vì LLM."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthInfo(BaseModel):
    user_id: str  # Thêm user_id để phân biệt người dùng
    gioi_tinh: str
    gio_sinh: int
    ngay_dl: Optional[int] = None
    thang_dl: Optional[int] = None
    nam_dl: Optional[int] = None
    ngay_al: Optional[int] = None
    thang_al: Optional[int] = None
    nam_al: Optional[int] = None
    nhuan: Optional[bool] = False
    thang_xem: Optional[int] = None  # Tháng xem vận hạn
    nam_xem: Optional[int] = None    # Năm xem vận hạn

    @root_validator(pre=True)
    def check_at_least_one_date_provided(cls, values):
        solar_provided = values.get('nam_dl') is not None
        lunar_provided = values.get('nam_al') is not None
        if not solar_provided and not lunar_provided:
            raise ValueError('Phải cung cấp ít nhất một loại ngày sinh (Dương lịch hoặc Âm lịch).')
        if not values.get('user_id'):
            raise ValueError('Thiếu user_id.')
        return values

USER_BIRTH_INFO_PATH = "user_birth_info.json"

def save_user_birth_info(info: BirthInfo, lunar_date: LunarDate):
    """Lưu thông tin sinh (cả dương lịch, âm lịch, leap, ...) vào file JSON theo user_id."""
    data = {
        "user_id": info.user_id,
        "gioi_tinh": info.gioi_tinh,
        "gio_sinh": info.gio_sinh,
        "ngay_dl": info.ngay_dl,
        "thang_dl": info.thang_dl,
        "nam_dl": info.nam_dl,
        "ngay_al": lunar_date.day,
        "thang_al": lunar_date.month,
        "nam_al": lunar_date.year,
        "nhuan": getattr(lunar_date, "leap", False)
    }
    file_path = f"user_birth_info_{info.user_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.post("/lap-la-so/", response_model=dict)
def create_astrological_chart_logic(info: BirthInfo):
    print(f"Nhận được yêu cầu: {info.model_dump_json(indent=2)}")
    try:
        if info.nam_dl:
            print(f"Phát hiện ngày Dương lịch. Đang đổi: {info.ngay_dl}/{info.thang_dl}/{info.nam_dl}")
            lunar_date = LunarDate.fromSolarDate(info.nam_dl, info.thang_dl, info.ngay_dl)
        else:
            print(f"Sử dụng ngày Âm lịch: {info.ngay_al}/{info.thang_al}/{info.nam_al}")
            lunar_date = LunarDate(info.nam_al, info.thang_al, info.ngay_al, info.nhuan)

        engine = TuViEngine(
            gioi_tinh=info.gioi_tinh,
            gio_sinh=info.gio_sinh,
            ngay_al=lunar_date.day,
            thang_al=lunar_date.month,
            nam_al=lunar_date.year
        )
        chart_data = engine.calculate()
        print("Tính toán lá số thành công bằng logic.")
        return chart_data

    except Exception as e:
        print(f"Lỗi nghiêm trọng trong quá trình tính toán: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Không thể tạo lá số. Lỗi: {str(e)}")

@app.post("/api/laso", response_model=dict)
def create_astrological_chart_tuvi(info: BirthInfo):
    """
    API /api/laso: Lập lá số Bắc Tông bằng logic Python (TuViEngine), không dùng Gemini/LLM.
    """
    print(f"[TuViEngine] Nhận được yêu cầu: {info.model_dump_json(indent=2)}")
    try:
        if info.nam_dl:
            print(f"Phát hiện ngày Dương lịch. Đang đổi: {info.ngay_dl}/{info.thang_dl}/{info.nam_dl}")
            lunar_date = LunarDate.fromSolarDate(info.nam_dl, info.thang_dl, info.ngay_dl)
        else:
            print(f"Sử dụng ngày Âm lịch: {info.ngay_al}/{info.thang_al}/{info.nam_al}")
            lunar_date = LunarDate(info.nam_al, info.thang_al, info.ngay_al, info.nhuan)
        engine = TuViEngine(
            gioi_tinh=info.gioi_tinh,
            gio_sinh=info.gio_sinh,
            ngay_al=lunar_date.day,
            thang_al=lunar_date.month,
            nam_al=lunar_date.year
        )
        chart_data = engine.calculate()
        print("[TuViEngine] Tính toán lá số thành công.")

        # Lưu thông tin sinh theo user_id
        birth_info_to_save = {
            "user_id": info.user_id,
            "gioi_tinh": info.gioi_tinh,
            "gio_sinh": info.gio_sinh,
            "ngay_dl": info.ngay_dl,
            "thang_dl": info.thang_dl,
            "nam_dl": info.nam_dl,
            "ngay_al": lunar_date.day,
            "thang_al": lunar_date.month,
            "nam_al": lunar_date.year,
            "nhuan": info.nhuan,
            "thang_xem": info.thang_xem,
            "nam_xem": info.nam_xem
        }
        file_path = f"user_birth_info_{info.user_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(birth_info_to_save, f, ensure_ascii=False, indent=2)

        response = {
            "chart": chart_data,
            "birth_info": birth_info_to_save
        }
        return response
    except Exception as e:
        print(f"[TuViEngine] Lỗi nghiêm trọng: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Không thể tạo lá số. Lỗi: {str(e)}")

@app.post("/api/luan_giai", response_model=dict)
def luan_giai_van_han(
    user_id: str = Body(...),
    thang_xem: Optional[int] = Body(None),
    nam_xem: Optional[int] = Body(None)
):
    """
    API /api/luan_giai: Luận giải vận hạn/lưu niên/lưu nguyệt dựa trên thông tin sinh đã lưu và tháng/năm xem.
    """
    try:
        file_path = f"user_birth_info_{user_id}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            birth_info = json.load(f)
        thang_xem_final = thang_xem if thang_xem is not None else birth_info.get("thang_xem")
        nam_xem_final = nam_xem if nam_xem is not None else birth_info.get("nam_xem")
        if not nam_xem_final:
            raise HTTPException(status_code=400, detail="Thiếu năm xem vận hạn (nam_xem)")
        engine = TuViEngine(
            gioi_tinh=birth_info["gioi_tinh"],
            gio_sinh=birth_info["gio_sinh"],
            ngay_al=birth_info["ngay_al"],
            thang_al=birth_info["thang_al"],
            nam_al=birth_info["nam_al"]
        )
        if hasattr(engine, "calculate_with_luu_nien"):
            ket_qua = engine.calculate_with_luu_nien(thang_xem=thang_xem_final, nam_xem=nam_xem_final)
        else:
            ket_qua = {"msg": "Chưa cài đặt hàm luận giải vận hạn trong engine."}
        return {
            "birth_info": birth_info,
            "thang_xem": thang_xem_final,
            "nam_xem": nam_xem_final,
            "luan_giai": ket_qua
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chưa có thông tin sinh cho user_id này. Hãy lập lá số trước.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi luận giải: {str(e)}")

rag = RAGCore()

@app.post("/api/phan_tich_laso", response_model=dict)
def analyze_laso_api(chart: dict = Body(...)):
    """
    API phân tích từng phần trong các cung từ dữ liệu lá số.
    Input: chart (dict) - dữ liệu lá số chuẩn từ /api/laso.
    Output: dict gồm phân tích từng phần và tổng kết Gemini.
    """
    try:
        # Phân tích từng phần trong các cung từ `dia_ban`
        cung_results = {}
        for cung in chart.get("dia_ban", []):
            cung_name = cung.get("ten_cung", "")
            cung_results[cung_name] = rag.analyze_chart_parts(cung)

        # Tổng kết Gemini
        summary = rag.analyze_chart_summary(chart)

        return {
            "phan_tich_tung_phan": cung_results,
            "tong_ket_gemini": summary
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/phan_tich_gemini", response_model=dict)
def analyze_gemini_api(chart: dict = Body(...)):
    """
    API phân tích tổng kết Gemini từ dữ liệu lá số.
    Input: chart (dict) - dữ liệu lá số chuẩn từ /api/laso.
    Output: dict gồm tổng kết Gemini.
    """
    try:
        # Kiểm tra xem Gemini đã được cấu hình chưa
        if llm is None:
            return {"error": "Gemini API chưa được cấu hình. Vui lòng kiểm tra GEMINI_API_KEY trong file .env"}
        
        # Chuẩn bị dữ liệu chart dưới dạng chuỗi JSON để đưa vào prompt
        chart_json = json.dumps(chart, ensure_ascii=False, indent=2)
        
        # Chuẩn bị prompt từ dữ liệu chart
        filled_prompt = PROMPT_TEMPLATE.format(chart=chart_json)
        print("[DEBUG] filled_prompt gửi Gemini:")
        print(filled_prompt[:500] + "..." if len(filled_prompt) > 500 else filled_prompt)

        # Gửi yêu cầu đến Gemini
        response = llm.generate_content(filled_prompt)
        print("[DEBUG] Đã nhận response từ Gemini!")

        # Làm sạch kết quả trả về
        raw_json_text = response.text.strip()
        
        # Loại bỏ markdown code blocks nếu có
        if '```json' in raw_json_text:
            raw_json_text = raw_json_text.split('```json', 1)[1]
        if '```' in raw_json_text:
            raw_json_text = raw_json_text.split('```', 1)[0]
        
        # Tìm JSON object chính nếu có text thừa
        start = raw_json_text.find('{')
        end = raw_json_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            cleaned_json = raw_json_text[start:end+1]
        else:
            cleaned_json = raw_json_text.strip()

        # Parse JSON và trả về
        try:
            result = json.loads(cleaned_json)
            return {
                "success": True,
                "analysis": result
            }
        except json.JSONDecodeError as json_error:
            print(f"[ERROR] Lỗi parse JSON: {json_error}")
            print(f"[DEBUG] Raw response: {raw_json_text}")
            return {
                "success": False,
                "error": "Không thể parse JSON từ Gemini",
                "raw_response": raw_json_text
            }

    except Exception as e:
        print(f"[ERROR] Lỗi khi gọi Gemini API: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    print("Khởi chạy máy chủ API tại http://0.0.0.0:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)

