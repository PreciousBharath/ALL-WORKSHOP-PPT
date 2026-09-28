"""
Prompt Engineering Studio - ASCII Character Analyzer Engine
Parses prompt text to build ASCII breakdown tables, character category statistics, 
and distribution metrics.
"""

import pandas as pd
import string

class ASCIIAnalyzer:
    """
    Analyzes ASCII codes, hex representations, and character classifications for prompts.
    """

    def __init__(self):
        pass

    def analyze(self, text: str) -> dict:
        """
        Builds character-level ASCII table and character category statistics.
        """
        if not text:
            return {
                "ascii_df": pd.DataFrame(),
                "total_chars": 0,
                "printable_chars": 0,
                "non_printable_chars": 0,
                "categories": {}
            }

        data = []
        categories = {
            "Uppercase": 0,
            "Lowercase": 0,
            "Digits": 0,
            "Spaces & Whitespace": 0,
            "Punctuation & Symbols": 0,
            "Control / Other": 0
        }

        for idx, char in enumerate(text, start=1):
            ascii_code = ord(char)
            hex_val = hex(ascii_code).upper()
            bin_val = bin(ascii_code)

            if char in string.ascii_uppercase:
                cat = "Uppercase"
            elif char in string.ascii_lowercase:
                cat = "Lowercase"
            elif char in string.digits:
                cat = "Digits"
            elif char.isspace():
                cat = "Spaces & Whitespace"
            elif char in string.punctuation:
                cat = "Punctuation & Symbols"
            else:
                cat = "Control / Other"

            categories[cat] += 1

            # Display representation
            display_char = "' '" if char == ' ' else ("\\n" if char == '\n' else ("\\t" if char == '\t' else char))

            data.append({
                "Pos": idx,
                "Char": display_char,
                "ASCII (Dec)": ascii_code,
                "Hex": hex_val,
                "Binary": bin_val,
                "Category": cat
            })

        df = pd.DataFrame(data)

        return {
            "ascii_df": df,
            "total_chars": len(text),
            "categories": categories
        }
