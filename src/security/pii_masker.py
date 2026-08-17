import re
from typing import Dict, List, Tuple

class PIIMasker:
    """
    Production PII Masker using regular expressions and rule-based entity recognition.
    Redacts sensitive personal information prior to indexing into vector databases or LLM prompts.
    """
    def __init__(self):
        self.patterns: Dict[str, Tuple[re.Pattern, str]] = {
            "EMAIL": (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), "[REDACTED_EMAIL]"),
            "PHONE": (re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'), "[REDACTED_PHONE]"),
            "SSN": (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), "[REDACTED_SSN]"),
            "CREDIT_CARD": (re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'), "[REDACTED_CREDIT_CARD]"),
            "API_KEY": (re.compile(r'\b(?:sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16})\b'), "[REDACTED_API_KEY]")
        }

    def mask(self, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Masks PII elements in text and returns the sanitized text alongside redact statistics.
        """
        if not text:
            return "", {}
        
        redacted_text = text
        redaction_counts = {}

        for pii_type, (pattern, replacement) in self.patterns.items():
            matches = pattern.findall(redacted_text)
            if matches:
                redaction_counts[pii_type] = len(matches)
                redacted_text = pattern.sub(replacement, redacted_text)

        return redacted_text, redaction_counts

    def has_pii(self, text: str) -> bool:
        """Checks if text contains any PII patterns."""
        for pattern, _ in self.patterns.values():
            if pattern.search(text):
                return True
        return False
