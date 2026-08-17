# Mid-Level AI Engineer Interview Guide: Multi-Modal Document Intelligence

This guide equips you to explain the **Multi-Modal Document Intelligence** project during technical interviews with confidence, clarity, and architectural authority.

---

## 1. High-Level Project Elevator Pitch (30-60 Seconds)

> "I designed and built an enterprise-grade **Multi-Modal Document Intelligence Platform** that processes complex unstructured PDFs, scanned images, financial tables, and infographics to deliver accurate, grounded Q&A with page-level citations.
> 
> Key architectural highlights include a **dual-representation multimodal ingestion engine** using PyPDF, OCR, and Vision LLMs (GPT-4o-mini/Gemini), a **unified vector store abstraction** over ChromaDB and Pinecone, a **multi-layered enterprise security suite** (PII masking + prompt injection scanning), and an automated **RAGAS evaluation framework** integrated with **LangSmith observability**."

---

## 2. Technical Architecture & System Design

```
+-----------------------------------------------------------------------------------+
|                                  USER INTERFACE                                   |
|                Streamlit Chat UI (Claude / ChatGPT / Gemini style)                 |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                  SECURITY LAYER                                   |
|   1. Prompt Injection Scanner  -->  2. PII Anonymizer  -->  3. Grounding Evaluator|
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              LANGCHAIN RAG PIPELINE                               |
|        LCEL Chain + Page Metadata Injector + Citation Formatting Engine          |
+-----------------------------------------------------------------------------------+
                        /                                   \
                       v                                     v
+------------------------------------+             +--------------------------------+
|       MULTIMODAL INGESTION         |             |        VECTOR STORE            |
| - Digital Text: Layout PDF Parser  |             | - Dev: ChromaDB (HNSW Cosine)  |
| - Scanned Docs: Tesseract OCR      |             | - Prod: Pinecone Cloud         |
| - Charts/Tables: Vision LLM Summaries |          | - Embeddings: OpenAI / HF      |
+------------------------------------+             +--------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            OBSERVABILITY & EVALUATION                             |
|          LangSmith Tracing  |  RAGAS Metrics (Faithfulness, Relevance, Recall)     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Deep Dive into Key Technical Decisions & Trade-Offs

### A. Multimodal Strategy: Dual-Representation vs Direct Image Indexing
- **The Challenge**: Standard text RAG fails on charts, scanned tables, and infographics because text extractors output corrupted raw strings. Direct visual embedding (CLIP/ColPali) is computationally expensive for large documents.
- **Our Solution**: Used a **Dual-Representation Strategy**. Native text is parsed via layout-aware PDF splitters. Visual elements (charts, tables, scans) pass through Vision LLMs (GPT-4o-mini / Gemini Vision) to generate dense, semantic textual summaries.
- **Trade-off**: Slightly higher ingestion latency for images in exchange for significantly faster vector search and superior compatibility with standard dense retrievers.

### B. Vector Store Choice: ChromaDB vs Pinecone
- **Development / On-Premise**: Local `ChromaDB` persistent storage with HNSW index for low-latency offline execution and zero cloud cost.
- **Production Enterprise**: `Pinecone` serverless vector database providing managed multi-region replication, horizontal scaling, and low-latency filtering.
- **Abstraction Design**: Implemented `VectorStoreManager` wrapping both providers behind a single unified API (`add_chunks`, `similarity_search`).

### C. Enterprise Security & Guardrail Strategy
- **Prompt Injection Defense**: Scans input prompts using regex heuristic rules against system prompt leaks, jailbreaks, and instructions override attempts.
- **PII Masking**: Redacts sensitive data (SSN, Phone, Email, Credit Cards) before indexing or LLM transmission to maintain SOC2 / GDPR compliance.
- **Confidence-Based Human Fallback**: Evaluates retrieval similarity scores. If top match is below `0.65`, the system triggers graceful fallback to human document analysts instead of hallucinating.

### D. Observability & Evaluation Strategy
- **LangSmith Tracing**: Set `LANGCHAIN_TRACING_V2=true` to capture complete LLM execution graphs, prompt tokens, latent vector scores, and chain execution latency.
- **RAGAS Evaluation Framework**: Automated evaluation suite measuring:
  1. **Faithfulness**: Verifying facts in the answer strictly exist in retrieved context chunks.
  2. **Answer Relevance**: Measuring how well the response directly answers the user prompt.
  3. **Context Recall**: Verifying retriever fetches the expected source document pages.

---

## 4. How to Position Yourself as a Mid-Level AI Engineer

| Junior AI Engineer Focus | Mid-Level AI Engineer Focus (Your Positioning) |
| :--- | :--- |
| Focuses on calling standard API wrappers (`llm.predict`). | Focuses on **system architecture, data pipelines, trade-offs, and security**. |
| Accepts hallucinations without evaluation. | Implements **RAGAS benchmarks, confidence thresholds, and grounding checks**. |
| Indexes raw text without metadata. | Implements **layout-aware chunking, page citations, and bounding box tags**. |
| Ignores security & compliance. | Implements **PII redactors, prompt injection scanners, and fallback handlers**. |
| Uses single hardcoded vector DB. | Builds **abstract vector store managers (ChromaDB + Pinecone)**. |
