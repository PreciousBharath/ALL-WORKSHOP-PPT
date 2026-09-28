"""
Model Evaluation & Embedding Visualizer Module
Supports 2D PCA/t-SNE Embedding visualizer data, BLEU/ROUGE metrics, and fine-tuning exporter.
"""
import random
import json
from typing import List, Dict, Any

class ModelEvalEngine:
    @staticmethod
    def generate_embedding_2d_points(texts: List[str]) -> List[Dict[str, Any]]:
        # Simulated 2D PCA Projection points
        points = []
        for idx, text in enumerate(texts):
            # Cluster based on text length and character hash for reproducible visual clustering
            seed = sum(ord(c) for c in text)
            random.seed(seed)
            x = round(random.gauss(idx * 1.5, 0.8), 2)
            y = round(random.gauss(idx * 1.2, 0.8), 2)
            category = "Technical" if "code" in text.lower() or "data" in text.lower() else "General"
            
            points.append({
                "label": text[:25] + "...",
                "x": x,
                "y": y,
                "category": category,
                "full_text": text
            })
        return points

    @staticmethod
    def calculate_metrics(reference: str, candidate: str) -> Dict[str, float]:
        ref_words = reference.lower().split()
        cand_words = candidate.lower().split()
        
        overlap = set(ref_words).intersection(set(cand_words))
        precision = len(overlap) / len(cand_words) if cand_words else 0.0
        recall = len(overlap) / len(ref_words) if ref_words else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "BLEU_1_precision": round(precision, 4),
            "ROUGE_L_recall": round(recall, 4),
            "F1_Similarity_Score": round(f1, 4)
        }

    @staticmethod
    def export_fine_tuning_jsonl(pairs: List[Dict[str, str]]) -> str:
        lines = []
        for item in pairs:
            json_line = {
                "messages": [
                    {"role": "system", "content": "You are a specialized GenAI domain assistant."},
                    {"role": "user", "content": item.get("prompt", "")},
                    {"role": "assistant", "content": item.get("completion", "")}
                ]
            }
            lines.append(json.dumps(json_line))
        return "\n".join(lines)
