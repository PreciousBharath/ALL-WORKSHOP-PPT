"""
GenAI Safety, Guardrails & PII Masking Engine
Implements PII redaction (Email, Phone, SSN, Credit Card) and Prompt Injection detection.
"""
import re
from typing import Dict, Any, List

class SafetyGuardrailsEngine:
    PII_PATTERNS = {
        "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "PHONE": r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
        "CREDIT_CARD": r'\b(?:\d[ -]*?){13,16}\b'
    }

    INJECTION_KEYPHRASES = [
        "ignore previous instructions",
        "bypass safety",
        "system prompt override",
        "you are now unfiltered",
        "jailbreak mode",
        "dan prompt"
    ]

    @classmethod
    def redact_pii(cls, text: str) -> Dict[str, Any]:
        redacted_text = text
        detected_types = []
        
        for pii_type, pattern in cls.PII_PATTERNS.items():
            matches = re.findall(pattern, redacted_text)
            if matches:
                detected_types.append(pii_type)
                redacted_text = re.sub(pattern, f"[{pii_type}_REDACTED]", redacted_text)

        return {
            "original_text": text,
            "redacted_text": redacted_text,
            "pii_detected": detected_types,
            "has_pii": len(detected_types) > 0
        }

    @classmethod
    def analyze_prompt_injection(cls, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        matched_flags = [phrase for phrase in cls.INJECTION_KEYPHRASES if phrase in prompt_lower]
        
        risk_score = min(1.0, len(matched_flags) * 0.45)
        is_safe = risk_score < 0.3

        return {
            "prompt": prompt,
            "is_safe": is_safe,
            "risk_score": round(risk_score, 2),
            "matched_injection_patterns": matched_flags,
            "recommendation": "Allow Request" if is_safe else "BLOCK REQUEST: Potential Prompt Injection / System Override Detected"
        }
