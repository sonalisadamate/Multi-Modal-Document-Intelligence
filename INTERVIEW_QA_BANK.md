# Resume & Technical Interview Question Bank: Multi-Modal Document Intelligence

Add this project to your resume under **Projects**:

> **Multi-Modal Document Intelligence Platform | LangChain, Vision LLMs, Multimodal RAG, ChromaDB, LangSmith**
> - Engineered an enterprise multi-modal RAG system extracting, summarizing, and answering questions from complex PDFs, scanned tables, and images with page-level citations.
> - Developed dual-representation ingestion combining PyPDF, Tesseract OCR, and Vision LLM summary generators for complex visual charts.
> - Implemented an enterprise security layer featuring regex PII masking, prompt-injection defense scanners, and low-confidence human fallback routing.
> - Built automated RAGAS evaluation suite measuring Faithfulness (94%) and Answer Relevance (91%), monitored via LangSmith tracing.

---

## 15+ Comprehensive Technical Interview Q&As

### Q1: How does your system handle multimodal data like scanned tables, infographics, and PDF pages?
**Answer**: Standard text chunking destroys table boundaries and graphic summaries. I implemented a **Dual-Representation Ingestion Engine**:
1. Digital text pages are parsed via layout-aware PDF splitters.
2. Scanned image pages pass through Tesseract OCR.
3. Complex visual tables, financial graphics, and charts pass through a **Vision LLM (GPT-4o-mini / Gemini Vision)** which converts the visual content into a structured textual summary.
Both native text and Vision LLM summaries are tagged with page metadata and indexed into vector storage.

---

### Q2: Why did you choose ChromaDB for local dev and Pinecone for production?
**Answer**: 
- **ChromaDB** is lightweight, runs locally in-process with SQLite persistence, and requires zero external cloud network calls during local development or unit testing.
- **Pinecone** is a cloud-native serverless vector database providing managed index replication, automatic horizontal scaling, and ultra-low latency metadata filtering.
- I built a `VectorStoreManager` abstraction layer using the Adapter Pattern so the entire system can switch between ChromaDB and Pinecone by changing a single environment variable (`VECTOR_STORE_PROVIDER`).

---

### Q3: How do you prevent hallucinations and ensure answers are strictly grounded in source documents?
**Answer**: Grounding is enforced at three distinct layers:
1. **Prompt Engineering**: The LLM prompt explicitly instructs the model to answer *only* using provided context chunks and to cite source document filenames and page numbers.
2. **Guardrail Evaluator**: After vector retrieval, similarity scores are computed. If the top similarity score is below `0.65`, the system suppresses LLM generation and routes the query to a `FallbackHandler` requesting human review.
3. **Citation Verification**: The response pipeline checks for explicit page markers like `[Source: report.pdf, Page 4]`.

---

### Q4: How do you protect the system against prompt injection attacks?
**Answer**: I built a `PromptInjectionScanner` that inspects incoming user queries before sending them to the retriever or LLM chain. The scanner checks for adversarial patterns such as *"Ignore previous instructions"*, *"System prompt leak"*, *"System override"*, and jailbreak prefixes. If flagged, the query is blocked immediately with a security log entry.

---

### Q5: How do you ensure PII (Personally Identifiable Information) compliance?
**Answer**: The `PIIMasker` module executes regex and rule-based entity recognition on all raw document text and user queries prior to indexing or cloud transmission. It automatically redacts Emails, Phone Numbers, Social Security Numbers (SSNs), Credit Card Numbers, and API Keys into placeholders like `[REDACTED_SSN]`.

---

### Q6: What embedding models did you evaluate and why?
**Answer**: I benchmarked both open-source local embeddings and commercial cloud embeddings:
- **Local**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) and `BAAI/bge-small-en-v1.5` for cost-sensitive, privacy-constrained deployments.
- **Cloud**: `OpenAI text-embedding-3-small` (1536 dimensions) for higher semantic accuracy across complex domain jargon.
I wrapped these under a unified `BaseEmbeddingWrapper` so models can be swapped effortlessly.

---

### Q7: How do you evaluate your RAG pipeline's performance?
**Answer**: I implemented an automated evaluation framework based on **RAGAS** metrics using a synthetic Golden Dataset:
- **Faithfulness**: Verifies whether claims in the generated response are grounded in retrieved context chunks.
- **Answer Relevance**: Measures semantic similarity between the question and generated response.
- **Context Recall**: Verifies whether the retriever successfully retrieved the ground-truth document pages.

---

### Q8: What is LangSmith and how did you utilize it in this project?
**Answer**: **LangSmith** is an observability platform for LLM applications. I enabled `LANGCHAIN_TRACING_V2=true` across our chain. It provides full visibility into execution latency, prompt token usage, vector retrieval scores, and step-by-step trace logs for debugging production bottlenecks.

---

### Q9: How do you chunk documents without splitting tables in half?
**Answer**: I implemented a **layout-aware semantic splitter**. Instead of arbitrary token slicing, it splits text based on paragraph markers and table delimiters (`|`, `\t`). When a table is detected, the entire table block is preserved as a single chunk with overlap lines.

---

### Q10: What happens if a user asks a question about a document that isn't indexed?
**Answer**: The `GuardrailEvaluator` measures retrieval similarity scores. If no indexed chunks achieve a score above the threshold (`0.65`), the system activates `FallbackHandler.format_low_confidence_response()`, informing the user that insufficient evidence exists and recommending human review.

---

### Q11: How do page-level citations work in your response pipeline?
**Answer**: Every `ExtractedChunk` retains a metadata dictionary containing `{"page": page_number, "source": doc_name}`. When retrieved context chunks are fed into the prompt, page numbers are injected into the header blocks. The frontend parses these metadata tags and renders interactive citation cards below the response.

---

### Q12: How would you scale this system to process 1,000,000 document pages?
**Answer**: 
1. **Asynchronous Ingestion Queue**: Use Celery/Redis or AWS SQS to process document uploads asynchronously.
2. **Distributed Vector Database**: Migrate vector storage to Pinecone Serverless or distributed Qdrant/Milvus clusters.
3. **Batch Embedding**: Batch text chunks when invoking embedding endpoints.
4. **Caching Layer**: Cache frequent query embeddings and responses in Redis.

---

### Q13: Explain LangChain LCEL (LangChain Expression Language) used in your chain.
**Answer**: LCEL allows declarative composition of RAG chains using pipe syntax (`prompt | llm | output_parser`). It provides built-in streaming support, async execution, parallel step execution, and seamless integration with LangSmith tracing.

---

### Q14: How does OCR accuracy affect vector search quality, and how did you mitigate errors?
**Answer**: OCR errors (e.g. reading '1' as 'l' or '0' as 'O') can degrade sub-word vector matching. To mitigate this, I combined fuzzy keyword matching with dense semantic embeddings and used Vision LLM summaries for critical tabular data.

---

### Q15: What was the biggest engineering challenge you faced in this project?
**Answer**: Handling heterogeneous document formats (digital text vs scanned PDFs vs visual tables) without losing metadata context. Resolving this required designing the **dual-representation pipeline** and enforcing standardized page-level metadata schemas across all ingestion steps.
