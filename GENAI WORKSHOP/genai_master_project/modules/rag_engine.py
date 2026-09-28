"""
RAG (Retrieval-Augmented Generation) & Vector Database Engine
Supports document chunking, TF-IDF / Cosine Similarity embeddings vector DB, and context-aware Q&A.
"""
import math
import re
from typing import List, Dict, Any

class VectorDB:
    """In-memory Vector DB using TF-IDF term vectors and Cosine Similarity."""
    def __init__(self):
        self.documents = []  # List of dict: {"id": int, "content": str, "metadata": dict}
        self.vocab = {}
        self.doc_vectors = []

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def _build_vocab(self):
        all_tokens = set()
        for doc in self.documents:
            all_tokens.update(self._tokenize(doc["content"]))
        self.vocab = {word: idx for idx, word in enumerate(sorted(all_tokens))}

    def _get_vector(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        vector = [0.0] * len(self.vocab)
        for token in tokens:
            if token in self.vocab:
                vector[self.vocab[token]] += 1.0
        # Normalize
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector

    def add_documents(self, docs: List[str], metadata_list: List[Dict[str, Any]] = None):
        for i, doc in enumerate(docs):
            meta = metadata_list[i] if metadata_list and i < len(metadata_list) else {"source": f"doc_{i+1}"}
            self.documents.append({
                "id": len(self.documents) + 1,
                "content": doc,
                "metadata": meta
            })
        self._build_vocab()
        self.doc_vectors = [self._get_vector(d["content"]) for d in self.documents]

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.documents or not self.vocab:
            return []
        query_vec = self._get_vector(query)
        results = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            dot_product = sum(q * d for q, d in zip(query_vec, doc_vec))
            results.append((dot_product, self.documents[idx]))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [{"score": round(score, 4), "doc": doc} for score, doc in results[:top_k] if score > 0]

class RAGEngine:
    def __init__(self):
        self.vector_db = VectorDB()

    def chunk_text(self, text: str, chunk_size: int = 200, overlap: int = 40) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

    def ingest_document(self, text: str, source_name: str = "Uploaded Document"):
        chunks = self.chunk_text(text)
        meta = [{"source": source_name, "chunk_id": idx + 1} for idx in range(len(chunks))]
        self.vector_db.add_documents(chunks, meta)
        return len(chunks)

    def query(self, user_query: str) -> Dict[str, Any]:
        matched_chunks = self.vector_db.similarity_search(user_query, top_k=3)
        if not matched_chunks:
            return {
                "answer": "No relevant context found in the uploaded documents to answer your question.",
                "sources": []
            }
        
        context_str = "\n---\n".join([item["doc"]["content"] for item in matched_chunks])
        synthesized_answer = (
            f"Based on the retrieved context:\n"
            f"'{matched_chunks[0]['doc']['content'][:180]}...'\n\n"
            f"Key Findings: The documents confirm relevant information matching '{user_query}'."
        )
        
        return {
            "answer": synthesized_answer,
            "sources": matched_chunks,
            "raw_context": context_str
        }
