import os
import streamlit as st
import pickle
import time
import fitz  # PyMuPDF for PDF extraction
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv() 

st.title("Research Tool 📈")
st.sidebar.title("Input Data")

# Input URLs and PDFs
urls = []
pdfs = []

for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

for i in range(3):
    pdf = st.sidebar.file_uploader(f"PDF {i+1}", type="pdf")
    if pdf:
        pdfs.append(pdf)

process_data_clicked = st.sidebar.button("Process Data")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

if process_data_clicked:
    data = []

    # Load and process URLs
    if urls:
        loader = UnstructuredURLLoader(urls=urls)
        main_placeholder.text("Data Loading from URLs...Started...✅✅✅")
        url_data = loader.load()
        data.extend(url_data)
    
    # Load and process PDFs
    if pdfs:
        for pdf in pdfs:
            pdf_reader = fitz.open(stream=pdf.read(), filetype="pdf")
            for page_num in range(len(pdf_reader)):
                page = pdf_reader.load_page(page_num)
                text = page.get_text()
                data.append(text)
        main_placeholder.text("Data Loading from PDFs...Started...✅✅✅")

    # Split data into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)

    # Create embeddings and save to FAISS index
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore_openai, f)

# Handle user queries
query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            
            st.header("Answer")
            st.write(result["answer"])
            
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")
                for source in sources_list:
                    st.write(source)
