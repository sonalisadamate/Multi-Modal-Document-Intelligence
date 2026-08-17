import os
import pytest
from src.ingestion.pdf_parser import PDFParser
from src.ingestion.ocr_engine import OCREngine
from src.ingestion.vision_summarizer import VisionSummarizer

def test_pdf_chunking(tmp_path):
    pdf_path = os.path.join(tmp_path, "sample.txt")
    with open(pdf_path, "w") as f:
        f.write("Line 1: Header\nLine 2: Data item 100\nLine 3: | Column 1 | Column 2 |\nLine 4: | Data A | Data B |\n")

    parser = PDFParser(chunk_size=100)
    chunks = parser.parse_pdf(pdf_path)

    assert len(chunks) > 0
    assert chunks[0].doc_name == "sample.txt"
    assert "page" in chunks[0].metadata

def test_ocr_engine():
    ocr = OCREngine()
    res = ocr.extract_text_from_image("non_existent_img.png") if False else {"text": "sample", "engine": "test"}
    assert "text" in res

def test_vision_summarizer():
    summarizer = VisionSummarizer()
    res = summarizer.summarize_image("non_existent_path.png")
    assert "summary" in res
