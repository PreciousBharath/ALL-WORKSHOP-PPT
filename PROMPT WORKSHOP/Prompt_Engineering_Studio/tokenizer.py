"""
Prompt Engineering Studio - Tokenization Engine
Uses tiktoken (or fallback tokenization) to tokenize text, count tokens,
and compute detailed token statistics and tables.
"""

import re
import pandas as pd

class PromptTokenizer:
    """
    Handles LLM tokenization analysis using OpenAI tiktoken (cl100k_base) 
    or robust regex fallback.
    """

    def __init__(self):
        self.encoder = None
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.encoder = None

    def tokenize(self, text: str) -> dict:
        """
        Tokenizes the input text and produces structured token breakdown & statistics.
        """
        if not text or not text.strip():
            return {
                "tokens_list": [],
                "token_df": pd.DataFrame(),
                "total_tokens": 0,
                "avg_token_len": 0,
                "unique_tokens": 0,
                "repeated_tokens": 0,
                "repeat_ratio": 0.0
            }

        tokens_data = []

        if self.encoder:
            try:
                token_ids = self.encoder.encode(text)
                for idx, tid in enumerate(token_ids, start=1):
                    t_bytes = self.encoder.decode_bytes([tid])
                    t_str = t_bytes.decode('utf-8', errors='replace')
                    tokens_data.append({
                        "Token #": idx,
                        "Token": t_str,
                        "Token ID": tid,
                        "Length": len(t_str),
                        "Bytes": str(t_bytes)
                    })
            except Exception:
                tokens_data = self._fallback_tokenize(text)
        else:
            tokens_data = self._fallback_tokenize(text)

        df = pd.DataFrame(tokens_data)
        
        total_tokens = len(df)
        if total_tokens > 0:
            token_strings = df["Token"].tolist()
            avg_token_len = round(sum(df["Length"]) / total_tokens, 2)
            unique_tokens = len(set(token_strings))
            repeated_tokens = total_tokens - unique_tokens
            repeat_ratio = round((repeated_tokens / total_tokens) * 100, 1)
        else:
            avg_token_len = 0
            unique_tokens = 0
            repeated_tokens = 0
            repeat_ratio = 0.0

        return {
            "tokens_list": df["Token"].tolist() if not df.empty else [],
            "token_df": df,
            "total_tokens": total_tokens,
            "avg_token_len": avg_token_len,
            "unique_tokens": unique_tokens,
            "repeated_tokens": repeated_tokens,
            "repeat_ratio": repeat_ratio
        }

    def _fallback_tokenize(self, text: str) -> list:
        """Fallback tokenization using sub-word/whitespace regex splitting."""
        pattern = r'\w+|\s+|[^\w\s]'
        raw_tokens = re.findall(pattern, text)
        data = []
        for idx, tok in enumerate(raw_tokens, start=1):
            data.append({
                "Token #": idx,
                "Token": tok,
                "Token ID": 1000 + idx,
                "Length": len(tok),
                "Bytes": str(tok.encode('utf-8'))
            })
        return data
