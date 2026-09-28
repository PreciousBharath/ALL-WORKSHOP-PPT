"""
Prompt Engineering Studio - Prompt Analyzer Engine
Calculates complexity, clarity, specificity, quality scores, word/char counts,
and structural element detection for prompts.
"""

import re
import math

class PromptAnalyzer:
    """
    Analyzes prompt text across quantitative and qualitative metrics.
    """

    def __init__(self):
        pass

    def analyze(self, text: str) -> dict:
        """Analyze a single prompt text and return comprehensive metric breakdown."""
        if not text or not text.strip():
            return self._empty_analysis()

        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = max(len(sentences), 1)

        # Estimated tokens (roughly 1.3 tokens per word for English)
        estimated_tokens = max(math.ceil(word_count * 1.3), word_count)
        
        # Reading time (Average 200 words per minute)
        reading_time_sec = round((word_count / 200.0) * 60, 1)

        # Syllable & Complexity Estimation
        syllables = sum(self._count_syllables(w) for w in words)
        avg_words_per_sentence = word_count / sentence_count
        avg_syllables_per_word = (syllables / word_count) if word_count > 0 else 1.0

        # Flesch Reading Ease Formula: 206.835 - 1.015(total words/total sentences) - 84.6(total syllables/total words)
        flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        complexity_score = min(max(round(100 - max(flesch_score, 0), 1), 10), 100)

        # Specificity Score Calculation
        specific_keywords = [
            "specific", "format", "step-by-step", "example", "constraint", 
            "context", "role", "output", "avoid", "ensure", "include", 
            "must", "should", "structure", "bullet", "table", "code", "objective"
        ]
        text_lower = text.lower()
        matched_kw_count = sum(1 for kw in specific_keywords if kw in text_lower)
        specificity_score = min(round(30 + (matched_kw_count * 8) + min(word_count * 0.4, 30), 1), 98)

        # Clarity Score Calculation
        # Penalize extremely long sentences, reward clear sectioning
        has_headers = bool(re.search(r'#{1,4}\s|\n[A-Z\s]{4,}:', text))
        has_bullets = bool(re.search(r'^\s*[-*•\d+.]\s', text, re.MULTILINE))
        clarity_bonus = (20 if has_headers else 0) + (15 if has_bullets else 0)
        clarity_score = min(round(50 + clarity_bonus + (10 if avg_words_per_sentence < 25 else -10), 1), 98)

        # Structural Elements Check
        structural_elements = {
            "Role Definition": bool(re.search(r'role|persona|act as|engineer|architect|expert|specialist', text_lower)),
            "Context & Background": bool(re.search(r'context|background|audience|scenario', text_lower)),
            "Clear Goal / Task": bool(re.search(r'objective|goal|task|explain|create|write|implement|provide', text_lower)),
            "Output Format": bool(re.search(r'format|structure|markdown|bullet|code block|table|json|html', text_lower)),
            "Constraints & Rules": bool(re.search(r'constraint|avoid|do not|ensure|rule|must', text_lower)),
            "Examples / Few-Shot": bool(re.search(r'example|template|sample|e\.g\.', text_lower))
        }

        element_match_count = sum(1 for v in structural_elements.values() if v)

        # Overall Quality Score
        quality_score = min(round(
            (specificity_score * 0.35) + 
            (clarity_score * 0.35) + 
            ((element_match_count / 6.0 * 100) * 0.30), 1
        ), 99)

        return {
            "word_count": word_count,
            "char_count": char_count,
            "char_count_no_spaces": char_count_no_spaces,
            "sentence_count": sentence_count,
            "estimated_tokens": estimated_tokens,
            "reading_time_sec": reading_time_sec,
            "complexity_score": complexity_score,
            "specificity_score": specificity_score,
            "clarity_score": clarity_score,
            "quality_score": quality_score,
            "structural_elements": structural_elements
        }

    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count in a word."""
        word = word.lower()
        if len(word) <= 3:
            return 1
        word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
        word = re.sub(r'^y', '', word)
        syllables = len(re.findall(r'[aeiouy]{1,2}', word))
        return max(syllables, 1)

    def _empty_analysis(self) -> dict:
        return {
            "word_count": 0,
            "char_count": 0,
            "char_count_no_spaces": 0,
            "sentence_count": 0,
            "estimated_tokens": 0,
            "reading_time_sec": 0,
            "complexity_score": 0,
            "specificity_score": 0,
            "clarity_score": 0,
            "quality_score": 0,
            "structural_elements": {
                "Role Definition": False,
                "Context & Background": False,
                "Clear Goal / Task": False,
                "Output Format": False,
                "Constraints & Rules": False,
                "Examples / Few-Shot": False
            }
        }
