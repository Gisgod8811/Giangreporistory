# run_indexing.py
from src.rag_core import RAGCore

def main():
    print("--- BẮT ĐẦU GIAI ĐOẠN 3: EMBEDDING VÀ INDEXING ---")

    # Khởi tạo RAGCore, nó sẽ tự động tải model embedding
    rag_system = RAGCore()

    # Xây dựng cơ sở dữ liệu vector
    rag_system.build_vector_store()

    print("--- KẾT THÚC GIAI ĐOẠN 3 ---")
    print("Bộ não của hệ thống đã sẵn sàng để tìm kiếm!")

if __name__ == "__main__":
    main()