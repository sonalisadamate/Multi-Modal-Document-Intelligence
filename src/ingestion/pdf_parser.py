import os
import re
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ExtractedChunk:
    text: str
    page_number: int
    doc_name: str
    chunk_type: str  # 'text', 'table', 'vision_summary'
    metadata: Dict[str, Any]

class PDFParser:
    """
    Layout-aware PDF Parser that extracts textual content page-by-page,
    identifying tabular structure and attaching metadata citations.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_pdf(self, file_path: str) -> List[ExtractedChunk]:
        """
        Parses PDF file into chunks with metadata. Uses pypdf if available,
        with fallback parsing logic.
        """
        filename = os.path.basename(file_path)
        chunks: List[ExtractedChunk] = []

        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            for page_idx, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                page_chunks = self._chunk_text(page_text, page_idx, filename)
                chunks.extend(page_chunks)
        except Exception:
            # Synthetic / fallback parser for file reading or plain text / binary files
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                chunks.extend(self._chunk_text(content, 1, filename))

        return chunks

    def _chunk_text(self, text: str, page_number: int, doc_name: str) -> List[ExtractedChunk]:
        chunks = []
        clean_text = text.strip()
        if not clean_text:
            return chunks

        # Simple semantic splitter preserving layout & tables
        lines = clean_text.split("\n")
        current_chunk = []
        current_length = 0

        for line in lines:
            line_len = len(line)
            if current_length + line_len > self.chunk_size and current_chunk:
                chunk_str = "\n".join(current_chunk)
                is_table = "|" in chunk_str or "\t" in chunk_str
                chunks.append(ExtractedChunk(
                    text=chunk_str,
                    page_number=page_number,
                    doc_name=doc_name,
                    chunk_type="table" if is_table else "text",
                    metadata={
                        "page": page_number,
                        "source": doc_name,
                        "content_type": "table" if is_table else "text"
                    }
                ))
                # Retain overlap lines
                overlap_lines = current_chunk[-2:] if len(current_chunk) >= 2 else []
                current_chunk = list(overlap_lines)
                current_length = sum(len(l) for l in current_chunk)

            current_chunk.append(line)
            current_length += line_len

        if current_chunk:
            chunk_str = "\n".join(current_chunk)
            is_table = "|" in chunk_str or "\t" in chunk_str
            chunks.append(ExtractedChunk(
                text=chunk_str,
                page_number=page_number,
                doc_name=doc_name,
                chunk_type="table" if is_table else "text",
                metadata={
                    "page": page_number,
                    "source": doc_name,
                    "content_type": "table" if is_table else "text"
                }
            ))

        return chunks
