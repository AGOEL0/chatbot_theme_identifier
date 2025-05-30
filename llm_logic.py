from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import numpy as np
import os
import easyocr
from dotenv import load_dotenv

# Set tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model_name="llama3-70b-8192", api_key=api_key)
parser = StrOutputParser()

prompt = PromptTemplate(
    template="""
    Answer the question as detailed as possible from the provided context.
    Make sure to provide all the details.
    If the answer is not in the provided context, just say "answer is not available in the context."

    Context:
    {context}

    Question:
    {question}
    """,
    input_variables=['context', 'question']
)

def get_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text

# Initialize easyocr reader once
reader = easyocr.Reader(['en'])

import numpy as np
from PIL import Image

def get_image_text(image_input):
    # if input is a PIL Image, convert to numpy array
    if isinstance(image_input, Image.Image):
        image_input = np.array(image_input)
    
    # if input is a file object, read bytes and convert to numpy array
    elif hasattr(image_input, "read"):
        from io import BytesIO
        image_bytes = image_input.read()
        image_input = np.array(Image.open(BytesIO(image_bytes)))
    
    # if input is bytes, convert to numpy array
    elif isinstance(image_input, bytes):
        from io import BytesIO
        image_input = np.array(Image.open(BytesIO(image_input)))
    
    # if input is string (filepath), just pass it as is to easyocr
    
    text_list = reader.readtext(image_input, detail=0)
    return ' '.join(text_list)

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

def get_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def setup_chain():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(lambda docs: "\n\n".join(doc.page_content for doc in docs)),
        'question': RunnablePassthrough()
    })
    return parallel_chain | prompt | model | parser

