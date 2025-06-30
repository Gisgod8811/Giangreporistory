# src/data_processor.py
import os
import re
import unicodedata
import json

# Các import cho phương pháp OCR
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract

# Các import cho các hàm khác
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import RAW_DATA_DIR, TXT_OUTPUT_DIR

# Cập nhật lại hàm clean_text
def clean_text(raw_text: str) -> str:
    text = raw_text
    unwanted_strings = [
        "TỬ VI NGHIỆM LÝ TOÀN THƯ THIÊN LƯƠNG",
        "TỬ VI NGHIỆM LÝ TOÀN THƯ 1",
        "TỬ VINGHIỆM LÝ TOÀN THƯ THIÊN LƯƠNG", # Thêm các biến thể từ OCR
        "TỬ VINGHIỆM LÝ TOÀN THƯ THIÊN LƯƠNG Số",
        "TỬ VINGHIỆM LÝ TOÀN THƯ THIÊN LƯƠNG Vũ",
        # Bạn có thể thêm các chuỗi footer khác vào đây nếu phát hiện
    ]
    for unwanted in unwanted_strings:
        text = text.replace(unwanted, "")
    
    # Giữ nguyên phần còn lại của hàm
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if not re.fullmatch(r'\s*\d+\s*', line)]
    text = "\n".join(cleaned_lines)
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Phiên bản cuối cùng, tăng chất lượng ảnh (DPI) để OCR chính xác hơn
def extract_and_clean_pdf(pdf_path: str) -> str | None:
    """
    Trích xuất văn bản bằng OCR, tối ưu bộ nhớ và tăng DPI để cải thiện độ chính xác.
    """
    print(f"  -> Đang trích xuất bằng phương pháp OCR (Tối ưu, DPI cao)...")
    
    # Cấu hình đường dẫn (giữ nguyên như cũ)
    poppler_path = r"E:\Poppler\poppler-24.08.0\Library\bin"
    # Không cần cấu hình Tesseract trong code nữa vì môi trường đã hoạt động tốt
    
    try:
        full_text = ""
        with fitz.open(pdf_path) as doc:
            num_pages = doc.page_count
            print(f"--> File có tổng cộng {num_pages} trang.")

        # Lặp qua từng trang để xử lý tuần tự
        for page_num in range(1, num_pages + 1):
            print(f"--> Đang xử lý trang {page_num}/{num_pages}...")
            
            # Chuyển DUY NHẤT MỘT trang thành ảnh với độ phân giải cao
            images = convert_from_path(
                pdf_path,
                poppler_path=poppler_path,
                first_page=page_num,
                last_page=page_num,
                dpi=300  # <-- THAM SỐ VÀNG: TĂNG ĐỘ PHÂN GIẢI ẢNH LÊN 300 DPI
            )
            
            if images:
                # lang='vie' sẽ sử dụng Tesseract đã được cấu hình đúng trong môi trường
                page_text = pytesseract.image_to_string(
                    images[0], 
                    lang='vie'
                )
                full_text += page_text + "\n"

        print("--> Đã hoàn tất OCR toàn bộ các trang.")
        print("--> Bắt đầu làm sạch văn bản...")
        cleaned_text = clean_text(full_text)
        print("--> Văn bản đã được làm sạch.")
        return cleaned_text
    
    except Exception as e:
        print(f"LỖI trong quá trình OCR: {e}")
        return None
def process_all_pdfs():
    print("--- BẮT ĐẦU GIAI ĐOẠN 1: TRÍCH XUẤT DỮ LIỆU ---")
    os.makedirs(TXT_OUTPUT_DIR, exist_ok=True)
    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"[!] KHÔNG TÌM THẤY FILE PDF NÀO trong: {RAW_DATA_DIR}")
        return
    for pdf_path in pdf_files:
        print(f"Đang xử lý file: {pdf_path.name}")
        cleaned_content = extract_and_clean_pdf(pdf_path)
        if cleaned_content:
            output_filename = pdf_path.stem + ".txt"
            output_path = TXT_OUTPUT_DIR / output_filename
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                print(f"-> ĐÃ LƯU THÀNH CÔNG VÀO: {output_path}")
            except Exception as e:
                print(f"-> Lỗi khi lưu file: {e}")
        print("-" * 20)
    print("--- HOÀN TẤT GIAI ĐOẠN 1 ---")    
# --- HÀM CHẠY TOÀN BỘ QUY TRÌNH (KHÔNG THAY ĐỔI) ---
# Thay thế hàm create_semantic_chunks cũ bằng phiên bản cuối cùng này
def create_semantic_chunks(source_filepath: str, source_text: str):
    """
    Phiên bản cuối cùng, dùng Regex để tìm tất cả các tiêu đề và vị trí của chúng,
    sau đó mới tiến hành cắt văn bản. Rất hiệu quả với dữ liệu OCR bị làm phẳng.
    """
    print("Bắt đầu chia văn bản theo ngữ nghĩa (Phiên bản cuối cùng)...")

    # Regex để tìm một dòng có ít nhất 2 từ và toàn bộ là VIẾT HOA.
    # Đây được coi là một tiêu đề mục lớn.
    regex_pattern = r'\b[A-ZÀ-ỸÁ-Ỹ]{2,}(?:\s+[A-ZÀ-ỸÁ-Ỹ]{2,})+\b'

    # Tìm tất cả các tiêu đề và vị trí bắt đầu của chúng
    headings = []
    for match in re.finditer(regex_pattern, source_text):
        # Chỉ lấy các tiêu đề có vẻ hợp lệ (không quá dài)
        if len(match.group(0).split()) < 15:
            headings.append((match.group(0).strip(), match.start()))

    final_chunks = []
    sub_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", ", ", " ", ""]
    )

    if not headings:
        print("Không tìm thấy tiêu đề nào, toàn bộ văn bản sẽ được xử lý như một mục.")
        sub_chunks = sub_splitter.split_text(source_text)
        for sub_chunk in sub_chunks:
            if len(sub_chunk.strip()) > 50:
                final_chunks.append({
                    "page_content": sub_chunk.strip(),
                    "metadata": {
                        "source": os.path.basename(source_filepath),
                        "section": "Nội dung chung"
                    }
                })
    else:
        print(f"Tìm thấy {len(headings)} tiêu đề mục lớn.")
        # Xử lý phần văn bản trước tiêu đề đầu tiên
        first_heading_start = headings[0][1]
        if first_heading_start > 0:
            initial_content = source_text[:first_heading_start].strip()
            sub_chunks = sub_splitter.split_text(initial_content)
            for sub_chunk in sub_chunks:
                 if len(sub_chunk.strip()) > 50:
                    final_chunks.append({
                        "page_content": sub_chunk.strip(),
                        "metadata": {"source": os.path.basename(source_filepath), "section": "Phần mở đầu"}
                    })

        # Lặp qua các tiêu đề để cắt và xử lý từng mục
        for i in range(len(headings)):
            title = headings[i][0]
            start_pos = headings[i][1]
            # Vị trí kết thúc của mục này là vị trí bắt đầu của mục tiếp theo
            end_pos = headings[i+1][1] if i + 1 < len(headings) else len(source_text)
            
            section_content = source_text[start_pos:end_pos].strip()
            
            # Xóa chính cái tiêu đề khỏi phần nội dung để tránh lặp lại
            content_without_title = section_content.replace(title, "", 1).strip()

            sub_chunks = sub_splitter.split_text(content_without_title)
            for sub_chunk in sub_chunks:
                if len(sub_chunk.strip()) > 50:
                    final_chunks.append({
                        "page_content": sub_chunk.strip(),
                        "metadata": {
                            "source": os.path.basename(source_filepath),
                            "section": title
                        }
                    })

    print(f"-> Đã tạo thành công {len(final_chunks)} chunks có ý nghĩa.")
    return final_chunks