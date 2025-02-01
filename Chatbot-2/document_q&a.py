import streamlit as st
import os
import time
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import StuffDocumentsChain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load API keys
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
google_api_key = os.getenv("GOOGLE_API_KEY")

# Streamlit UI
st.title("📄 Gemma Model - Document Q&A Chatbot")

# Initialize LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Prompt Template
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.

    <context>
    {context}
    <context>

    Question: {input}
    """
)

# Function for document embeddings
@st.cache_resource
def vector_embedding():
    st.write("🔄 Creating embeddings, please wait...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    pdf_directory = "./documents"  # Directory with PDF files

    # Load and process PDFs
    loader = PyPDFDirectoryLoader(pdf_directory)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs[:20])
    vectors = FAISS.from_documents(final_documents, embeddings)

    st.write("✅ Embeddings created successfully!")
    return vectors

# Button to generate document embeddings
if st.button("📂 Generate Document Embeddings"):
    st.session_state.vectors = vector_embedding()

# User input for question
prompt1 = st.text_input("🔍 Enter Your Question from Documents:")

if prompt1:
    if "vectors" not in st.session_state or st.session_state.vectors is None:
        st.warning("⚠️ Please click '📂 Generate Document Embeddings' first.")
    else:
        document_chain = StuffDocumentsChain.from_llm(llm, prompt)
        retriever = st.session_state.vectors.as_retriever()
        retrieval_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

        start = time.process_time()
        response = retrieval_chain.invoke({'query': prompt1})
        response_time = time.process_time() - start

        st.write("### 🤖 Answer:")
        st.write(response.get('result', '⚠️ No answer found.'))

        st.write(f"⏳ Response Time: {response_time:.2f} seconds")

        if "source_documents" in response:
            with st.expander("📄 Relevant Document Sections:"):
                for i, doc in enumerate(response["source_documents"]):
                    st.write(f"**Chunk {i+1}:**")
                    st.write(doc.page_content)
                    st.write("🔹" * 10)
