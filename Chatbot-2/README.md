# Chatbot-2: Document Q&A Chatbot

## Overview
**Chatbot-2** is a **Document Q&A Chatbot** built with Streamlit and LangChain. It allows users to upload PDF documents and interact with them using an AI-powered question-answering model. The chatbot processes the documents, creates embeddings, and retrieves the most relevant information to answer users' queries.

## Features
- **Document Upload**: Upload your PDF documents to the `./documents` folder.
- **Embeddings Creation**: Generates embeddings from the uploaded documents using Google Generative AI.
- **Question Answering**: Interact with the chatbot to get answers based on the content of the uploaded documents.
- **Relevant Sections**: Displays the most relevant sections from the documents to support the answer.

## Prerequisites
- Python 3.9 or higher
- `.env` file with `GROQ_API_KEY` and `GOOGLE_API_KEY`

## Installation
### 1. Clone the repository

git clone https://github.com/Ashmitagurung/Chatbot-Projects.git
cd chatbot-2

### 2. Create a virtual environment (optional)

python3 -m venv venv
source venv/bin/activate

### 3. Install required dependencies
pip install -r requirements.txt

### 3. Install required dependencies

pip install -r requirements.txt

### 4. Set up API keys
Create a .env file in the root directory of the project with the following contents:

GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_google_api_key

Replace your_groq_api_key and your_google_api_key with your actual API keys.

### 5. Upload your PDFs
Upload your PDF documents to the ./documents folder in the repository.`

## Usage
### 1. Run the application:

streamlit run document_q&a.py
Access the chatbot through the local server (usually http://localhost:8501).

### 2. Generate Document Embeddings:
Click the "📂 Generate Document Embeddings" button to create embeddings for your uploaded documents.

### 3. Ask Questions:
Enter your questions in the text input box, and the chatbot will provide the most relevant answer based on the documents.

### 4. View Relevant Document Sections:
The chatbot will display the sections of the documents that were used to generate the answer.
