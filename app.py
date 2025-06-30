# app.py
import streamlit as st
from src.rag_core import RAGCore

# Dùng cache của streamlit để chỉ tải hệ thống RAG một lần duy nhất
@st.cache_resource
def load_rag_system():
    """Tải toàn bộ hệ thống RAG và trả về đối tượng RAGCore."""
    try:
        return RAGCore()
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi khởi tạo hệ thống RAG: {e}")
        return None

# --- Giao diện chính của ứng dụng ---
st.set_page_config(page_title="Hỏi Đáp Tử Vi", page_icon="🔮")
st.title("🔮 Hệ thống Hỏi Đáp Tử Vi")
st.write("Chào mừng bạn! Hãy đặt câu hỏi về các luận giải trong sách tử vi đã được nạp.")

# Tải hệ thống RAG
with st.spinner("Đang khởi tạo hệ thống và tải 'bộ não' AI... Vui lòng chờ trong giây lát."):
    rag_system = load_rag_system()

# Chỉ hiển thị phần còn lại nếu hệ thống tải thành công
if rag_system and rag_system.index is not None:
    st.success("Hệ thống đã sẵn sàng!")

    # Tạo ô nhập câu hỏi
    query = st.text_input("Nhập câu hỏi của bạn tại đây:", "")

    if query:
        with st.spinner("Đang tìm kiếm thông tin và tạo câu trả lời..."):
            answer = rag_system.ask(query)
            st.subheader("Câu trả lời cho bạn:")
            st.markdown(answer)

            with st.expander("Xem các đoạn văn bản tham khảo mà AI đã đọc"):
                retrieved_chunks = rag_system.search(query)
                for i, chunk in enumerate(retrieved_chunks):
                    st.info(f"Nguồn tham khảo {i+1} (Mục: {chunk['metadata']['section']})")
                    st.write(chunk['page_content'])
else:
    st.error("Không thể tải 'bộ não' của hệ thống. Vui lòng kiểm tra lại file index hoặc chạy lại `run_indexing.py`.")