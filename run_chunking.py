# run_chunking.py (Phiên bản nâng cấp)
import os
import json
from src.config import TXT_OUTPUT_DIR, CHUNK_OUTPUT_FILE
from src.data_processor import create_semantic_chunks

def main():
    """
    Hàm chính để chạy toàn bộ quy trình chunking cho TẤT CẢ các file .txt.
    """
    print("--- BẮT ĐẦU GIAI ĐOẠN 2: CHUNKING DỮ LIỆU ---")

    txt_files = list(TXT_OUTPUT_DIR.glob("*.txt"))
    if not txt_files:
        print(f"LỖI: Không tìm thấy file .txt nào trong {TXT_OUTPUT_DIR}.")
        return

    all_chunks_with_metadata = []
    # Lặp qua tất cả các file .txt tìm được
    for source_txt_path in txt_files:
        print(f"\nĐang xử lý file: {source_txt_path.name}")
        try:
            with open(source_txt_path, 'r', encoding='utf-8') as f:
                text_content = f.read()

            # Tạo các chunk cho file hiện tại
            chunks = create_semantic_chunks(str(source_txt_path), text_content)
            all_chunks_with_metadata.extend(chunks) # Thêm chunk vào danh sách chung
        except Exception as e:
            print(f"Đã xảy ra lỗi khi xử lý file {source_txt_path.name}: {e}")

    if all_chunks_with_metadata:
        print(f"\nTổng cộng đã tạo được {len(all_chunks_with_metadata)} chunks từ {len(txt_files)} file.")
        print(f"Đang lưu tất cả chunks vào file: {CHUNK_OUTPUT_FILE}")
        CHUNK_OUTPUT_FILE.parent.mkdir(exist_ok=True)
        with open(CHUNK_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_chunks_with_metadata, f, indent=4, ensure_ascii=False)
        print("-> LƯU FILE CHUNKS.JSON THÀNH CÔNG!")
    else:
        print("Không tạo được chunk nào.")

    print("--- KẾT THÚC GIAI ĐOẠN 2 ---")

if __name__ == "__main__":
    main()