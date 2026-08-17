import os
import sys
import time
import streamlit as st

# Add project root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import get_settings
from src.ingestion.pdf_parser import PDFParser, ExtractedChunk
from src.ingestion.ocr_engine import OCREngine
from src.ingestion.vision_summarizer import VisionSummarizer
from src.vectorstore.store_manager import VectorStoreManager
from src.rag.retriever import MultimodalRetriever
from src.rag.chain import DocumentIntelligenceChain
from src.evaluation.ragas_evaluator import RAGASEvaluator

# Page Configuration
st.set_page_config(
    page_title="Multi-Modal Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT / Claude / Gemini Aesthetics
st.markdown("""
<style>
    /* Dark Theme & Custom Styling */
    .main {
        background-color: #0e1117;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stAppHeader {
        background-color: transparent;
    }
    .css-1d3 Sterling {
        background-color: #161b22;
    }
    
    /* Header Card */
    .header-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        color: #f9fafb;
    }
    .header-title {
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-subtitle {
        color: #9ca3af;
        font-size: 14px;
        margin-top: 4px;
    }

    /* Status Pill Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .badge-success { background-color: #064e3b; color: #34d399; border: 1px solid #059669; }
    .badge-info { background-color: #1e3a8a; color: #93c5fd; border: 1px solid #2563eb; }
    .badge-warning { background-color: #78350f; color: #fde047; border: 1px solid #d97706; }

    /* Citation Box */
    .citation-box {
        background-color: #1f2937;
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 4px;
        margin-top: 8px;
        font-size: 13px;
        color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "vector_store" not in st.session_state:
    st.session_state.settings = get_settings()
    st.session_state.vector_store = VectorStoreManager()
    st.session_state.retriever = MultimodalRetriever(vector_store=st.session_state.vector_store)
    st.session_state.chain = DocumentIntelligenceChain(retriever=st.session_state.retriever)
    st.session_state.messages = []
    st.session_state.indexed_files = []

    # Pre-index sample document for instant trial
    sample_chunk = ExtractedChunk(
        text="Enterprise Document Intelligence Platform architecture leverages Vision LLMs (GPT-4o/Gemini) for table processing, "
             "OpenAI text-embedding-3-small for semantic embeddings, ChromaDB for vector retrieval, and LangSmith for tracing. "
             "The system features PII masking, prompt injection scanner, and automated RAGAS evaluation framework achieving 92.4% faithfulness score.",
        page_number=1,
        doc_name="architecture_overview.pdf",
        chunk_type="text",
        metadata={"page": 1, "source": "architecture_overview.pdf", "content_type": "text"}
    )
    st.session_state.vector_store.add_chunks([sample_chunk])
    st.session_state.indexed_files.append("architecture_overview.pdf")

# Sidebar - Document Workspace & Settings
with st.sidebar:
    st.markdown("### 📁 Document Workspace")
    
    uploaded_files = st.file_uploader(
        "Upload PDFs, Scans, or Images",
        type=["pdf", "png", "jpg", "jpeg", "csv"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.indexed_files:
                with st.spinner(f"Indexing {uploaded_file.name}..."):
                    temp_path = os.path.join("./data", uploaded_file.name)
                    os.makedirs("./data", exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Select Ingestion Pipeline based on extension
                    if uploaded_file.name.endswith(".pdf"):
                        parser = PDFParser()
                        chunks = parser.parse_pdf(temp_path)
                    elif uploaded_file.name.endswith((".png", ".jpg", ".jpeg")):
                        ocr = OCREngine()
                        ocr_res = ocr.extract_text_from_image(temp_path)
                        vision = VisionSummarizer()
                        vision_res = vision.summarize_image(temp_path)
                        combined_text = f"{ocr_res['text']}\n\n{vision_res['summary']}"
                        chunks = [ExtractedChunk(
                            text=combined_text,
                            page_number=1,
                            doc_name=uploaded_file.name,
                            chunk_type="vision_summary",
                            metadata={"page": 1, "source": uploaded_file.name, "content_type": "image"}
                        )]
                    else:
                        content = str(uploaded_file.read().decode("utf-8", errors="ignore"))
                        chunks = [ExtractedChunk(
                            text=content, page_number=1, doc_name=uploaded_file.name,
                            chunk_type="text", metadata={"page": 1, "source": uploaded_file.name, "content_type": "text"}
                        )]

                    st.session_state.vector_store.add_chunks(chunks)
                    st.session_state.indexed_files.append(uploaded_file.name)
                    st.success(f"Indexed {uploaded_file.name} ({len(chunks)} chunks)")

    st.markdown("---")
    st.markdown("### ⚙️ System Architecture")
    st.markdown(f"**Vector Store**: `{st.session_state.settings.vector_store_provider.upper()}`")
    st.markdown(f"**Embedding Model**: `{st.session_state.settings.embedding_provider.upper()}`")
    st.markdown(f"**LLM Model**: `{st.session_state.settings.openai_model_name}`")
    st.markdown(f"**LangSmith Tracing**: `{'Active' if st.session_state.settings.langchain_tracing_v2 else 'Off'}`")

    st.markdown("---")
    if st.button("🧪 Run RAGAS Benchmark Evaluation"):
        with st.spinner("Executing RAGAS Evaluation Harness..."):
            evaluator = RAGASEvaluator()
            result = evaluator.evaluate_chain(lambda q: st.session_state.chain.run(q))
            st.session_state.benchmark_result = result
            st.success("Benchmark Complete!")

    if "benchmark_result" in st.session_state:
        res = st.session_state.benchmark_result
        st.markdown("#### 📊 RAGAS Metrics")
        st.metric("Overall RAGAS Score", f"{res.overall_ragas_score * 100:.1f}%")
        st.caption(f"Faithfulness: {res.faithfulness_score} | Relevance: {res.answer_relevance_score} | Recall: {res.context_recall_score}")

# Main Chat View
st.markdown("""
<div class="header-card">
    <div class="header-title">Multi-Modal Document Intelligence</div>
    <div class="header-subtitle">Extract, cite, summarize, and query complex PDFs, scans, tables, and visual charts.</div>
    <div style="margin-top: 12px;">
        <span class="badge badge-success">🛡️ PII Guarded</span>
        <span class="badge badge-info">⚡ Vector Search Active</span>
        <span class="badge badge-warning">🔍 Source-Only Citations</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citations" in message and message["citations"]:
            with st.expander("📍 Source Citations & Metadata"):
                for cit in message["citations"]:
                    st.markdown(
                        f"**{cit['source']}** (Page {cit['page']}) - Confidence: `{cit['confidence_score']:.2f}`\n\n"
                        f"> *\"{cit['snippet']}\"*"
                    )

# Chat Input Box
if prompt := st.chat_input("Ask a question about your uploaded documents..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Searching document vector store & verifying guardrails..."):
            response_data = st.session_state.chain.run(prompt)
            answer_text = response_data["answer"]
            citations = response_data.get("citations", [])

            st.markdown(answer_text)

            if citations:
                with st.expander("📍 Source Citations & Page Metadata"):
                    for cit in citations:
                        st.markdown(
                            f"**{cit['source']}** (Page {cit['page']}) - Similarity: `{cit['confidence_score']:.2f}`\n\n"
                            f"> *\"{cit['snippet']}\"*"
                        )

            # Record Assistant Message in State
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer_text,
                "citations": citations
            })
