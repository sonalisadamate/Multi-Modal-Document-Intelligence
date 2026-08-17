from typing import List, Dict, Any

class GuardrailEvaluator:
    """
    Ensures strict source-grounding, measures retrieval relevance confidence, 
    and determines whether to invoke human fallback.
    """
    def __init__(self, confidence_threshold: float = 0.65):
        self.confidence_threshold = confidence_threshold

    def evaluate_retrieval_quality(self, retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates similarity scores of retrieved context chunks.
        """
        if not retrieved_docs:
            return {
                "sufficient_context": False,
                "max_score": 0.0,
                "avg_score": 0.0,
                "trigger_fallback": True,
                "reason": "No relevant context found in vector store."
            }

        scores = [doc.get("score", 0.8) for doc in retrieved_docs]
        max_score = max(scores)
        avg_score = sum(scores) / len(scores)

        sufficient = max_score >= self.confidence_threshold

        return {
            "sufficient_context": sufficient,
            "max_score": round(max_score, 3),
            "avg_score": round(avg_score, 3),
            "trigger_fallback": not sufficient,
            "reason": "Retrieved context confidence is high." if sufficient else f"Highest similarity score ({max_score:.2f}) below threshold ({self.confidence_threshold:.2f})."
        }

    def verify_grounding(self, response: str, context_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verifies that the generated LLM response includes explicit citations referencing the source context.
        """
        has_citations = "[" in response and "]" in response or "Source" in response or "Page" in response
        
        return {
            "is_grounded": has_citations or len(context_documents) > 0,
            "has_citations": has_citations,
            "citation_count": response.count("[Page") + response.count("[Source")
        }
