# chatbot_theme_identifier
✨ A colorful Streamlit app to upload PDFs &amp; images, extract text (PDF &amp; OCR), and ask natural language questions using LangChain + LLM (Groq). Uses HuggingFace embeddings + FAISS for vector search. Beautiful animated UI, supports multi-file upload, and runs locally with easy setup! 🚀

🚀 Features
✅ Upload multiple PDF, PNG, JPG, JPEG files
✅ Extract text from PDFs using PyPDF2
✅ Extract text from images using pytesseract (OCR)
✅ Store and search text chunks using FAISS vector store
✅ Ask questions and get detailed answers using LangChain + LLM
✅ Beautiful animated Streamlit UI with colorful gradients and sidebar file browser

🏗 Tech Stack
Python 🐍
Streamlit 🌈
LangChain 🔗
Groq LLM (llama3-70b-8192)
HuggingFace Embeddings
FAISS (vector search)
PyPDF2 (PDF parsing)
pytesseract + Tesseract OCR (image text extraction)

⚙️ Setup Instructions

1️⃣ Clone this repo:
git clone https://github.com/yourusername/pdf-image-qa-chatbot.git
cd pdf-image-qa-chatbot

2️⃣ Install dependencies:
pip install -r requirements.txt

3️⃣ Install Tesseract OCR (for image text extraction):

Download Windows installer: https://github.com/UB-Mannheim/tesseract/wiki

Install to: C:\Program Files\Tesseract-OCR

Add C:\Program Files\Tesseract-OCR to your system PATH

Or set directly in code:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

4️⃣ Run the app:
streamlit run app.py
