# Multi-Modal Document Intelligence Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-emerald.svg)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB%2FPinecone-purple.svg)](https://www.trychroma.com/)
[![Observability](https://img.shields.io/badge/Observability-LangSmith-orange.svg)](https://smith.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade **Multi-Modal Document Intelligence Platform** that ingests, extracts, summarizes, cites, and answers questions from complex PDFs, scanned images, financial tables, and visual infographics.

Built with **LangChain**, **Vision LLMs (GPT-4o-mini / Gemini)**, **Multimodal RAG**, **ChromaDB & Pinecone**, **Enterprise Security Guardrails**, **LangSmith Observability**, and an interactive **Claude/ChatGPT/Gemini-style Streamlit UI**.

---

## 🌟 Key Features

- 📄 **Layout-Aware PDF Ingestion**: Extracts digital text, structured tabular layouts, and section headers with page-level bounding box tags.
- 👁️ **Vision LLM Graphic & Table Summarizer**: Converts visual financial graphics, flowcharts, and complex tables into dense semantic summaries for indexing.
- 🔀 **Dual Vector Store Architecture**: Seamless abstraction supporting local persistent **ChromaDB** for dev/testing and cloud **Pinecone** for production.
- 🛡️ **Enterprise Security & Guardrails Layer**:
  - **PII Masking**: Redacts emails, phone numbers, SSNs, credit cards, and API keys.
  - **Prompt Injection Scanner**: Blocks adversarial prompt attacks and jailbreak attempts.
  - **Source-Only Grounding & Human Fallback**: Evaluates similarity confidence; triggers human fallback if scores fall below threshold.
- 📊 **RAGAS Evaluation Framework**: Automated test suite measuring **Faithfulness**, **Answer Relevance**, and **Context Recall**.
- 📡 **LangSmith Observability**: End-to-end tracing, latency monitoring, and token execution analytics.
- 💬 **Modern Chat Dashboard**: Claude/ChatGPT/Gemini aesthetics with expandable page citations, dark mode, and security status pills.

---

## 🏗️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                                  STREAMLIT UI                                     |
|                 Claude / ChatGPT / Gemini Modern Aesthetics                       |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                SECURITY GUARDRAILS                                |
|        1. Prompt Injection Scanner  |  2. PII Masker  |  3. Grounding Check       |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                               LANGCHAIN RAG PIPELINE                              |
|           LCEL Chain + Metadata Injector + Citation Formatter                    |
+-----------------------------------------------------------------------------------+
                        /                                   \
                       v                                     v
+------------------------------------+             +--------------------------------+
|       MULTIMODAL INGESTION         |             |          VECTOR STORE          |
| - Layout PDF Parser (PyPDF)        |             | - ChromaDB (Local Persistent)  |
| - Tesseract OCR (Scanned Docs)     |             | - Pinecone (Cloud Serverless)  |
| - Vision LLM (Tables & Charts)     |             | - OpenAI / HF Embeddings       |
+------------------------------------+             +--------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            OBSERVABILITY & EVALUATION                             |
|          LangSmith Tracing  |  RAGAS Metrics (Faithfulness, Relevance, Recall)     |
+-----------------------------------------------------------------------------------+
```

---

## ⚡ Quick Start & Installation

### 1. Clone & Setup Workspace
```bash
git clone https://github.com/sonalisadamate/Multi-Modal-Document-Intelligence.git
cd Multi-Modal-Document-Intelligence
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 4. Launch Streamlit Web UI
```bash
streamlit run frontend/app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Unit Tests & RAGAS Evaluation

### Execute PyTest Suite
```bash
pytest tests/
```

### Run RAGAS Benchmark Suite
```bash
python3 -m src.evaluation.ragas_evaluator
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
