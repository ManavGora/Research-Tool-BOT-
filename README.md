# GenAI Research Tool 📈

It is a Streamlit-based POC web application that allows users to input news article URLs and PDF documents for text analysis. It processes the provided content, creates embeddings, and enables users to query the data using an OpenAI language model. The results include answers to the queries and relevant sources.

<br>
<img src="https://github.com/ManavGora/Research-Tool-BOT-/blob/main/Architecture.png"/>
<br>


## Features

- Accepts up to 3 URLs and 3 PDF files for content analysis.
- Extracts text from the provided URLs and PDFs.
- Creates embeddings using OpenAI embeddings and stores them in a FAISS index.
- Allows users to input queries and retrieves answers along with the sources from the processed data.

## Prerequisites

- Python 3.8+
- Streamlit
- LangChain
- OpenAI API Key
- PyMuPDF (fitz)
- FAISS
- dotenv

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ManavGora/Research-Tool-BOT-
   cd Research-Tool-BOT-

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   ```bash
   pip install -r requirements.txt

4. Create a '.env' file in the root directory and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key

5. Run the Streamlit app:
   ```bash
   streamlit run main.py
