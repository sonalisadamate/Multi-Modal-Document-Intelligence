import re
from typing import Dict, Any, List

class PromptInjectionScanner:
    """
    Guards against adversarial prompt injection, system prompt leakage, and jailbreak attempts.
    """
    def __init__(self):
        self.injection_rules: List[re.Pattern] = [
            re.compile(r'ignore\s+(all\s+)?(previous|above)\s+instructions', re.IGNORECASE),
            re.compile(r'disregard\s+(all\s+)?(previous|prior)\s+(rules|prompts|directions)', re.IGNORECASE),
            re.compile(r'you\s+are\s+now\s+(a|an)\s+(unrestricted|DAN|jailbroken)', re.IGNORECASE),
            re.compile(r'print\s+(your|the)\s+(system|initial)\s+prompt', re.IGNORECASE),
            re.compile(r'reveal\s+(your|the)\s+secret\s+instructions', re.IGNORECASE),
            re.compile(r'system\s+override\s*:', re.IGNORECASE),
            re.compile(r'bypass\s+(safety|guardrails|filters)', re.IGNORECASE),
            re.compile(r'<\s*system\s*>', re.IGNORECASE)
        ]

    def scan(self, user_query: str) -> Dict[str, Any]:
        """
        Scans user prompt for malicious injection patterns.
        Returns safety status dictionary.
        """
        if not user_query:
            return {"is_safe": True, "detected_patterns": []}

        detected = []
        for pattern in self.injection_rules:
            match = pattern.search(user_query)
            if match:
                detected.append(match.group(0))

        is_safe = len(detected) == 0
        return {
            "is_safe": is_safe,
            "detected_patterns": detected,
            "risk_score": 1.0 if not is_safe else 0.0,
            "reason": "Prompt injection pattern detected" if not is_safe else "Clean"
        }
