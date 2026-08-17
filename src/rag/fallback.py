from typing import Dict, Any, List

class FallbackHandler:
    """
    Handles graceful degradation and human fallback routing when 
    security risks or low confidence scores are encountered.
    """
    def format_security_block_response(self, query: str, reason: str, detected_patterns: List[str]) -> Dict[str, Any]:
        return {
            "query": query,
            "answer": (
                "⚠️ **Security Policy Violation**: Your query contains patterns flagged by our Prompt Injection "
                "Guardrail Scanner. The request has been safely blocked to prevent system prompt leakage or unauthorized overrides."
            ),
            "citations": [],
            "security": {
                "prompt_injection_safe": False,
                "reason": reason,
                "detected_patterns": detected_patterns
            },
            "metrics": {
                "latency_seconds": 0.005,
                "confidence_score": 0.0,
                "status": "BLOCKED_BY_GUARDRAIL"
            },
            "action_required": "Please rephrase your request using standard business language."
        }

    def format_low_confidence_response(self, query: str, reason: str, confidence_score: float) -> Dict[str, Any]:
        return {
            "query": query,
            "answer": (
                "🤖 **Human Fallback Triggered**: The document intelligence system could not locate high-confidence "
                "supporting evidence in the uploaded documents for your question (Confidence Score: "
                f"`{confidence_score:.2f}`).\n\n"
                "**Recommended Actions**:\n"
                "1. Upload additional relevant PDF pages or visual scans.\n"
                "2. Forward this inquiry to a human document analyst."
            ),
            "citations": [],
            "security": {
                "prompt_injection_safe": True
            },
            "metrics": {
                "latency_seconds": 0.01,
                "confidence_score": confidence_score,
                "status": "LOW_CONFIDENCE_FALLBACK"
            },
            "action_required": "Human Analyst Review Recommended"
        }
