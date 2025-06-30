# src/rag_core.py
import json
import faiss
import numpy as np
import os
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from src.config import VECTOR_STORE_PATH, GEMINI_MODEL_NAME

class RAGCore:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2'):
        """
        Khởi tạo hệ thống RAG và tải các tài nguyên cần thiết.
        """
        print("Đang tải mô hình embedding...")
        self.model = SentenceTransformer(embedding_model_name)
        print("Tải mô hình embedding thành công.")
        
        # Tải vector store ngay khi khởi tạo
        self.index = None
        self.chunks = []
        self.load_vector_store()
        
        # Cấu hình Gemini API
        print("Đang cấu hình Gemini API...")
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Không tìm thấy GEMINI_API_KEY trong file .env")
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel(GEMINI_MODEL_NAME)
        print("Cấu hình Gemini API thành công.")

    def load_vector_store(self):
        """Tải FAISS index và dữ liệu chunks từ file."""
        index_path = str(VECTOR_STORE_PATH / "faiss_index.bin")
        chunks_path = str(VECTOR_STORE_PATH / "chunks_data.json")

        if os.path.exists(index_path) and os.path.exists(chunks_path):
            print(f"Đang tải FAISS index từ: {index_path}")
            self.index = faiss.read_index(index_path)
            print("Tải FAISS index thành công.")
            
            print(f"Đang tải dữ liệu chunks từ: {chunks_path}")
            with open(chunks_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
            print(f"Tải thành công {len(self.chunks)} chunks.")
        else:
            print("LỖI: Không tìm thấy vector store. Vui lòng chạy `run_indexing.py` trước.")

    def search(self, query: str, k: int = 5):
        """Tìm kiếm các chunk liên quan nhất đến câu hỏi."""
        if self.index is None:
            return []
        
        query_vector = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        return [self.chunks[i] for i in indices[0]]

    def ask(self, query: str):
        """Thực hiện quy trình RAG hoàn chỉnh: tìm kiếm và sinh câu trả lời."""
        print(f"\nBắt đầu quy trình cho câu hỏi: '{query}'")
        retrieved_chunks = self.search(query)
        if not retrieved_chunks:
            return "Xin lỗi, tôi không tìm thấy thông tin nào liên quan trong sách để trả lời câu hỏi này."

        context = "\n\n---\n\n".join([chunk['page_content'] for chunk in retrieved_chunks])
        
        prompt_template = f"""Dựa vào những thông tin được trích lục từ sách tử vi dưới đây, hãy trả lời câu hỏi của người dùng một cách chi tiết, rõ ràng và tự nhiên.
        Lưu ý quan trọng:
        - Chỉ trả lời dựa trên thông tin được cung cấp.
        - Không được bịa đặt hay suy diễn thông tin không có trong văn bản.
        - Trình bày câu trả lời một cách mạch lạc, văn phong như một chuyên gia tử vi.
        --- THÔNG TIN TRÍCH LỤC ---
        {context}
        ---------------------------
        Câu hỏi của người dùng: "{query}"
        Câu trả lời của bạn:
        """
        
        print("Đang đưa thông tin cho Gemini để tạo câu trả lời...")
        response = self.llm.generate_content(prompt_template)
        print("Đã nhận được câu trả lời từ Gemini.")
        return response.text