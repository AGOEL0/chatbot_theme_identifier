# app.py

import streamlit as st
from llm_logic import get_pdf_text, get_image_text, get_text_chunks, get_vector_store, setup_chain

# ----- Streamlit UI -----

st.set_page_config(page_title="🎨 Colorful PDF & Image Q&A Chatbot", layout="wide", page_icon="✨")

# Custom CSS for styling and animation
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #f6f9fc, #e9f1ff);
    }
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #ff6ec4, #7873f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    .sidebar .block-container {
        background: linear-gradient(145deg, #e0e5ec, #f9f9f9);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
    }
    .file-list-item {
        margin-bottom: 0.3rem;
        padding: 0.4rem;
        border-radius: 8px;
        background-color: #ffe8f1;
        color: #d81b60;
        font-weight: 600;
        font-size: 0.95rem;
        transition: background-color 0.3s;
    }
    .file-list-item:hover {
        background-color: #ffd6e6;
    }
    .footer-text {
        font-size: 0.85rem;
        color: #666;
        margin-top: 2rem;
        text-align: center;
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✨ PDF & Image Q&A Chatbot ✨</h1>', unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.header("🌟 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDFs and Images",
        accept_multiple_files=True,
        type=["pdf", "png", "jpg", "jpeg"],
        help="Upload PDFs, PNGs, JPGs"
    )
    
    if uploaded_files:
        st.markdown("**📋 Uploaded Files:**")
        for file in uploaded_files:
            file_icon = "📄" if file.type == "application/pdf" else "🖼️"
            st.markdown(f'<div class="file-list-item">{file_icon} {file.name}</div>', unsafe_allow_html=True)
    else:
        st.info("⚠️ No files uploaded yet.")
    
    st.header("💬 Ask a Question")
    user_question = st.text_input("Type your question here...")
    
    process_btn = st.button("🚀 Process & Answer")

# Main content area
status_placeholder = st.empty()
answer_placeholder = st.empty()
raw_text_expander = st.expander("🔍 Show Extracted Raw Text")

if uploaded_files and process_btn:
    with st.spinner("✨ Processing your documents... Please wait!"):
        raw_text = ""
        for idx, file in enumerate(uploaded_files):
            if file.type == "application/pdf":
                raw_text += get_pdf_text(file) + "\n"
                status_placeholder.success(f"✅ Processed PDF: {file.name} ({idx+1}/{len(uploaded_files)})")
            elif file.type.startswith("image/"):
                raw_text += get_image_text(file) + "\n"
                status_placeholder.success(f"🖼️ Processed Image: {file.name} ({idx+1}/{len(uploaded_files)})")
    if raw_text.strip() == "":
        status_placeholder.error("❌ No text could be extracted from the uploaded files.")
    else:
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        status_placeholder.success("🎉 Documents processed and vector store built!")

        with raw_text_expander:
            st.text_area("📜 Extracted Text", raw_text, height=300)

        if user_question.strip():
            with st.spinner("🤖 Generating answer..."):
                chain = setup_chain()
                answer = chain.invoke(user_question)
                answer_placeholder.markdown("### 🧠 **Answer:**")
                answer_placeholder.success(answer)
        else:
            answer_placeholder.info("✏️ Please type a question to get an answer.")

elif process_btn:
    status_placeholder.warning("⚠️ Please upload at least one file before processing.")

# Footer note
st.markdown('<div class="footer-text">🚀 Built with ❤️ using Streamlit + LangChain | Designed for a delightful experience ✨</div>', unsafe_allow_html=True)
