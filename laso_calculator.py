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
import os

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

if __name__ == "__main__":
    print("Khởi chạy máy chủ API tại http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)

