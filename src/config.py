# src/config.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Paths for Stage 1 & 2
TXT_OUTPUT_DIR = PROCESSED_DIR / "extracted_texts"
CHUNK_OUTPUT_FILE = PROCESSED_DIR / "chunks.json"

# Paths for Stage 3
VECTOR_STORE_PATH = PROCESSED_DIR / "vector_store"

# Model Configurations
GEMINI_MODEL_NAME = "gemini-2.0-flash" # <-- Sửa thành "gemini-2.0-flash" nếu bạn muốn
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Bảng trạng thái sao ở 12 cung
# M: Miếu, V: Vượng, Đ: Đắc, B: Bình, H: Hãm

TRANG_THAI_SAO = {
    # 14 Chính Tinh
    "Tử Vi":     {'Tý': 'B', 'Sửu': 'M', 'Dần': 'V', 'Mão': 'B', 'Thìn': 'Đ', 'Tỵ': 'M', 'Ngọ': 'M', 'Mùi': 'V', 'Thân': 'B', 'Dậu': 'B', 'Tuất': 'Đ', 'Hợi': 'B'},
    "Liêm Trinh": {'Tý': 'V', 'Sửu': 'B', 'Dần': 'Đ', 'Mão': 'B', 'Thìn': 'M', 'Tỵ': 'H', 'Ngọ': 'V', 'Mùi': 'M', 'Thân': 'Đ', 'Dậu': 'B', 'Tuất': 'M', 'Hợi': 'H'},
    "Thiên Đồng": {'Tý': 'V', 'Sửu': 'H', 'Dần': 'M', 'Mão': 'V', 'Thìn': 'B', 'Tỵ': 'H', 'Ngọ': 'H', 'Mùi': 'H', 'Thân': 'M', 'Dậu': 'V', 'Tuất': 'H', 'Hợi': 'Đ'},
    "Vũ Khúc":   {'Tý': 'B', 'Sửu': 'M', 'Dần': 'V', 'Mão': 'B', 'Thìn': 'M', 'Tỵ': 'Đ', 'Ngọ': 'V', 'Mùi': 'M', 'Thân': 'V', 'Dậu': 'B', 'Tuất': 'M', 'Hợi': 'Đ'},
    "Thái Dương": {'Tý': 'H', 'Sửu': 'H', 'Dần': 'M', 'Mão': 'M', 'Thìn': 'V', 'Tỵ': 'V', 'Ngọ': 'M', 'Mùi': 'Đ', 'Thân': 'H', 'Dậu': 'H', 'Tuất': 'H', 'Hợi': 'H'},
    "Thiên Cơ":   {'Tý': 'V', 'Sửu': 'H', 'Dần': 'M', 'Mão': 'M', 'Thìn': 'Đ', 'Tỵ': 'B', 'Ngọ': 'V', 'Mùi': 'H', 'Thân': 'M', 'Dậu': 'M', 'Tuất': 'Đ', 'Hợi': 'B'},
    "Thiên Phủ":  {'Tý': 'M', 'Sửu': 'V', 'Dần': 'M', 'Mão': 'B', 'Thìn': 'V', 'Tỵ': 'V', 'Ngọ': 'M', 'Mùi': 'V', 'Thân': 'M', 'Dậu': 'B', 'Tuất': 'V', 'Hợi': 'V'},
    "Thái Âm":   {'Tý': 'M', 'Sửu': 'M', 'Dần': 'H', 'Mão': 'H', 'Thìn': 'H', 'Tỵ': 'H', 'Ngọ': 'H', 'Mùi': 'H', 'Thân': 'V', 'Dậu': 'M', 'Tuất': 'M', 'Hợi': 'M'},
    "Tham Lang":  {'Tý': 'V', 'Sửu': 'M', 'Dần': 'B', 'Mão': 'B', 'Thìn': 'M', 'Tỵ': 'H', 'Ngọ': 'H', 'Mùi': 'M', 'Thân': 'B', 'Dậu': 'B', 'Tuất': 'M', 'Hợi': 'H'},
    "Cự Môn":     {'Tý': 'V', 'Sửu': 'B', 'Dần': 'V', 'Mão': 'M', 'Thìn': 'H', 'Tỵ': 'Đ', 'Ngọ': 'V', 'Mùi': 'B', 'Thân': 'V', 'Dậu': 'M', 'Tuất': 'H', 'Hợi': 'V'},
    "Thiên Tướng":{'Tý': 'Đ', 'Sửu': 'V', 'Dần': 'M', 'Mão': 'B', 'Thìn': 'V', 'Tỵ': 'Đ', 'Ngọ': 'Đ', 'Mùi': 'V', 'Thân': 'M', 'Dậu': 'B', 'Tuất': 'V', 'Hợi': 'Đ'},
    "Thiên Lương":{'Tý': 'M', 'Sửu': 'B', 'Dần': 'Đ', 'Mão': 'V', 'Thìn': 'M', 'Tỵ': 'H', 'Ngọ': 'M', 'Mùi': 'B', 'Thân': 'Đ', 'Dậu': 'V', 'Tuất': 'M', 'Hợi': 'H'},
    "Thất Sát":  {'Tý': 'M', 'Sửu': 'V', 'Dần': 'M', 'Mão': 'B', 'Thìn': 'B', 'Tỵ': 'B', 'Ngọ': 'M', 'Mùi': 'V', 'Thân': 'M', 'Dậu': 'B', 'Tuất': 'B', 'Hợi': 'B'},
    "Phá Quân":   {'Tý': 'M', 'Sửu': 'V', 'Dần': 'Đ', 'Mão': 'H', 'Thìn': 'Đ', 'Tỵ': 'H', 'Ngọ': 'M', 'Mùi': 'V', 'Thân': 'Đ', 'Dậu': 'H', 'Tuất': 'Đ', 'Hợi': 'H'},

    # Lục Sát Tinh
    "Kình Dương": {'Tý': 'H', 'Sửu': 'Đ', 'Dần': 'H', 'Mão': 'M', 'Thìn': 'Đ', 'Tỵ': 'H', 'Ngọ': 'H', 'Mùi': 'Đ', 'Thân': 'H', 'Dậu': 'M', 'Tuất': 'Đ', 'Hợi': 'H'},
    "Đà La":     {'Tý': 'H', 'Sửu': 'Đ', 'Dần': 'Đ', 'Mão': 'H', 'Thìn': 'Đ', 'Tỵ': 'H', 'Ngọ': 'H', 'Mùi': 'Đ', 'Thân': 'Đ', 'Dậu': 'H', 'Tuất': 'Đ', 'Hợi': 'H'},
    "Hỏa Tinh":   {'Tý': 'H', 'Sửu': 'Đ', 'Dần': 'M', 'Mão': 'Đ', 'Thìn': 'H', 'Tỵ': 'H', 'Ngọ': 'M', 'Mùi': 'Đ', 'Thân': 'H', 'Dậu': 'H', 'Tuất': 'M', 'Hợi': 'H'},
    "Linh Tinh":  {'Tý': 'H', 'Sửu': 'H', 'Dần': 'M', 'Mão': 'M', 'Thìn': 'Đ', 'Tỵ': 'H', 'Ngọ': 'M', 'Mùi': 'H', 'Thân': 'H', 'Dậu': 'M', 'Tuất': 'Đ', 'Hợi': 'H'},
    "Địa Không":  {'Tý': 'H', 'Sửu': 'H', 'Dần': 'Đ', 'Mão': 'H', 'Thìn': 'H', 'Tỵ': 'Đ', 'Ngọ': 'H', 'Mùi': 'H', 'Thân': 'Đ', 'Dậu': 'H', 'Tuất': 'H', 'Hợi': 'Đ'},
    "Địa Kiếp":   {'Tý': 'H', 'Sửu': 'H', 'Dần': 'Đ', 'Mão': 'H', 'Thìn': 'H', 'Tỵ': 'Đ', 'Ngọ': 'H', 'Mùi': 'H', 'Thân': 'Đ', 'Dậu': 'H', 'Tuất': 'H', 'Hợi': 'Đ'},

    # Lục Cát Tinh và các phụ tinh quan trọng khác
    "Văn Xương":  {'Tý': 'Đ', 'Sửu': 'M', 'Dần': 'Đ', 'Mão': 'B', 'Thìn': 'B', 'Tỵ': 'M', 'Ngọ': 'H', 'Mùi': 'H', 'Thân': 'Đ', 'Dậu': 'M', 'Tuất': 'H', 'Hợi': 'B'},
    "Văn Khúc":   {'Tý': 'Đ', 'Sửu': 'M', 'Dần': 'B', 'Mão': 'Đ', 'Thìn': 'B', 'Tỵ': 'M', 'Ngọ': 'B', 'Mùi': 'H', 'Thân': 'Đ', 'Dậu': 'M', 'Tuất': 'H', 'Hợi': 'B'},
    "Tả Phù":     {'Tý': 'B', 'Sửu': 'M', 'Dần': 'V', 'Mão': 'B', 'Thìn': 'M', 'Tỵ': 'V', 'Ngọ': 'B', 'Mùi': 'M', 'Thân': 'V', 'Dậu': 'B', 'Tuất': 'M', 'Hợi': 'V'},
    "Hữu Bật":    {'Tý': 'B', 'Sửu': 'M', 'Dần': 'V', 'Mão': 'B', 'Thìn': 'M', 'Tỵ': 'V', 'Ngọ': 'B', 'Mùi': 'M', 'Thân': 'V', 'Dậu': 'B', 'Tuất': 'M', 'Hợi': 'V'},
    "Thiên Khôi": {'Tý': 'V', 'Sửu': 'V', 'Dần': 'M', 'Mão': 'B', 'Thìn': 'B', 'Tỵ': 'B', 'Ngọ': 'M', 'Mùi': 'V', 'Thân': 'M', 'Dậu': 'B', 'Tuất': 'B', 'Hợi': 'B'},
    "Thiên Việt": {'Tý': 'B', 'Sửu': 'V', 'Dần': 'M', 'Mão': 'B', 'Thìn': 'B', 'Tỵ': 'B', 'Ngọ': 'M', 'Mùi': 'V', 'Thân': 'M', 'Dậu': 'V', 'Hợi': 'B', 'Tuất': 'B'},
    "Lộc Tồn":    {'Tý': 'B', 'Sửu': 'B', 'Dần': 'M', 'Mão': 'M', 'Thìn': 'B', 'Tỵ': 'V', 'Ngọ': 'M', 'Mùi': 'B', 'Thân': 'M', 'Dậu': 'M', 'Tuất': 'B', 'Hợi': 'V'},
    "Thiên Mã":   {'Tý': 'B', 'Sửu': 'B', 'Dần': 'V', 'Mão': 'B', 'Thìn': 'B', 'Tỵ': 'M', 'Ngọ': 'B', 'Mùi': 'B', 'Thân': 'V', 'Dậu': 'B', 'Tuất': 'B', 'Hợi': 'M'},
    "Hóa Lộc":    {'Tý': 'B', 'Sửu': 'Đ', 'Dần': 'M', 'Mão': 'M', 'Thìn': 'B', 'Tỵ': 'V', 'Ngọ': 'M', 'Mùi': 'Đ', 'Thân': 'M', 'Dậu': 'V', 'Tuất': 'B', 'Hợi': 'Đ'},
    "Hóa Quyền":  {'Tý': 'Đ', 'Sửu': 'Đ', 'Dần': 'M', 'Mão': 'V', 'Thìn': 'M', 'Tỵ': 'B', 'Ngọ': 'M', 'Mùi': 'Đ', 'Thân': 'M', 'Dậu': 'V', 'Tuất': 'B', 'Hợi': 'B'},
    "Hóa Khoa":   {'Tý': 'M', 'Sửu': 'Đ', 'Dần': 'B', 'Mão': 'M', 'Thìn': 'B', 'Tỵ': 'M', 'Ngọ': 'V', 'Mùi': 'Đ', 'Thân': 'V', 'Dậu': 'M', 'Tuất': 'B', 'Hợi': 'B'},
    "Hóa Kỵ":     {'Tý': 'Đ', 'Sửu': 'Đ', 'Dần': 'B', 'Mão': 'B', 'Thìn': 'H', 'Tỵ': 'H', 'Ngọ': 'B', 'Mùi': 'H', 'Thân': 'B', 'Dậu': 'B', 'Tuất': 'H', 'Hợi': 'Đ'},
    # Các sao khác sẽ mặc định là Bình Hòa (B) nếu không có trong danh sách này
}

# Danh sách vòng Lộc Tồn (bỏ Lộc Tồn, Kình Dương, Đà La)
VONG_LOC_TON = [
    "Bác Sỹ", "Lực Sỹ", "Thanh Long", "Tiểu Hao", "Tướng Quân", "Tấu Thư", "Phi Liêm", "Hỷ Thần", "Bệnh Phù", "Đại Hao"
]

# Bảng tra cứu tam hợp cho Hỏa Tinh, Linh Tinh
HOA_LINH_TAM_HOP = {
    'Dần': ['Dần', 'Ngọ', 'Tuất'],
    'Ngọ': ['Dần', 'Ngọ', 'Tuất'],
    'Tuất': ['Dần', 'Ngọ', 'Tuất'],
    'Thân': ['Thân', 'Tý', 'Thìn'],
    'Tý': ['Thân', 'Tý', 'Thìn'],
    'Thìn': ['Thân', 'Tý', 'Thìn'],
    'Tỵ': ['Tỵ', 'Dậu', 'Sửu'],
    'Dậu': ['Tỵ', 'Dậu', 'Sửu'],
    'Sửu': ['Tỵ', 'Dậu', 'Sửu'],
    'Hợi': ['Hợi', 'Mão', 'Mùi'],
    'Mão': ['Hợi', 'Mão', 'Mùi'],
    'Mùi': ['Hợi', 'Mão', 'Mùi'],
}

# Bảng tra chiều an Hỏa Tinh, Linh Tinh theo giờ sinh (giờ dương/giờ âm)
HOA_LINH_CHIEU = {
    'Tý': 'thuận', 'Sửu': 'thuận', 'Dần': 'thuận', 'Mão': 'thuận', 'Thìn': 'thuận', 'Tỵ': 'thuận',
    'Ngọ': 'nghịch', 'Mùi': 'nghịch', 'Thân': 'nghịch', 'Dậu': 'nghịch', 'Tuất': 'nghịch', 'Hợi': 'nghịch'
}

# Chủ Mệnh và Chủ Thân (chuẩn hóa theo yêu cầu)
CHU_MENH_DICT = {
    'Tý': 'Tang Môn', 'Sửu': 'Thiên Cơ', 'Dần': 'Thiên Lương', 'Mão': 'Thiên Đồng',
    'Thìn': 'Văn Xương', 'Tỵ': 'Văn Khúc', 'Ngọ': 'Thiên Tướng', 'Mùi': 'Thiên Phủ',
    'Thân': 'Thái Dương', 'Dậu': 'Thái Âm', 'Tuất': 'Tham Lang', 'Hợi': 'Cự Môn'
}
CHU_THAN_DICT = {
    'Tý': 'Lộc Tồn', 'Sửu': 'Bác Sỹ', 'Dần': 'Lực Sỹ', 'Mão': 'Thanh Long',
    'Thìn': 'Tiểu Hao', 'Tỵ': 'Tướng Quân', 'Ngọ': 'Tấu Thư', 'Mùi': 'Phi Liêm',
    'Thân': 'Hỷ Thần', 'Dậu': 'Bệnh Phù', 'Tuất': 'Đại Hao', 'Hợi': 'Phục Binh'
}