"""
Mock metrics computation for LLM evaluation.
Provides stub implementations of BLEU, ROUGE, and BERTScore without external dependencies.
"""

import random
import re
import math
from typing import Dict, List, Any, Optional
from collections import Counter


class MetricsCalculator:
    """Mock implementation of common NLP metrics for LLM evaluation."""
    
    def __init__(self, enable_real_metrics: bool = False):
        """
        Initialize metrics calculator.
        
        Args:
            enable_real_metrics: If True, use real metric implementations (requires additional dependencies)
        """
        self.enable_real_metrics = enable_real_metrics
        self.random_seed = 42
        random.seed(self.random_seed)
    
    def compute_all_metrics(self, reference: str, candidate: str) -> Dict[str, float]:
        """
        Compute all available metrics for a reference-candidate pair.
        
        Args:
            reference: Reference text (ground truth or prompt)
            candidate: Candidate text (model output)
            
        Returns:
            Dictionary of metric names to values
        """
        # Pre-tokenize once for efficiency
        ref_words = self._tokenize(reference.lower())
        cand_words = self._tokenize(candidate.lower())
        
        metrics = {}
        
        if self.enable_real_metrics:
            # Real implementations would go here
            # metrics.update(self._compute_real_bleu(reference, candidate))
            # metrics.update(self._compute_real_rouge(reference, candidate))
            # metrics.update(self._compute_real_bert_score(reference, candidate))
            pass
        
        # Only use quality_score from Excel data - no automatic metric calculation
        metrics.update({
            'quality_score': None,  # Will be filled from Excel data, not computed
        })
        
        return metrics
    
    def compute_all_metrics_with_quality(self, reference: str, candidate: str, 
                                       quality_score: float = None) -> Dict[str, float]:
        """
        Compute all metrics including human quality score.
        
        Args:
            reference: Reference text (ground truth or prompt)
            candidate: Candidate text (model output)
            quality_score: Human evaluation score 1-10 (optional)
            
        Returns:
            Dictionary of metric names to values
        """
        # Get base metrics (without quality_score)
        metrics = self.compute_all_metrics(reference, candidate)
        
        # Add human quality score if provided
        if quality_score is not None:
            # Validate score range
            if 0 <= quality_score <= 10:
                metrics['quality_score'] = round(float(quality_score), 1)
            else:
                print(f"Warning: Quality score {quality_score} out of range (0-10), skipping")
                metrics['quality_score'] = None
        else:
            metrics['quality_score'] = None
        
        return metrics
    
    def _mock_bleu_score_fast(self, ref_words: List[str], cand_words: List[str]) -> float:
        """Fast BLEU score using pre-tokenized words."""
        if not cand_words:
            return 0.0
        
        # Simple word overlap with cached counters
        ref_set = set(ref_words)
        cand_set = set(cand_words)
        overlap = len(ref_set & cand_set)
        precision = overlap / len(cand_set) if cand_set else 0.0
        
        # Add minimal randomness for realism
        noise = (hash(tuple(cand_words[:3])) % 100) / 1000.0 - 0.05
        bleu = max(0.0, min(1.0, precision * 0.7 + 0.2 + noise))
        return round(bleu, 4)
    
    def _mock_rouge_l_score_fast(self, ref_words: List[str], cand_words: List[str]) -> float:
        """Fast ROUGE-L score using pre-tokenized words."""
        if not ref_words or not cand_words:
            return 0.0
        
        # Fast set-based approximation
        ref_set = set(ref_words)
        cand_set = set(cand_words)
        common = ref_set & cand_set
        
        if not common:
            return 0.0
        
        precision = len(common) / len(cand_set)
        recall = len(common) / len(ref_set)
        f1 = 2 * precision * recall / (precision + recall)
        
        # Add noise
        noise = (hash(tuple(sorted(common)[:2])) % 100) / 1250.0 - 0.04
        rouge_l = max(0.0, min(1.0, f1 * 0.8 + 0.15 + noise))
        return round(rouge_l, 4)
    
    def _mock_bert_score_fast(self, ref_words: List[str], cand_words: List[str]) -> float:
        """Fast BERTScore using pre-tokenized words."""
        if not ref_words or not cand_words:
            return 0.3
        
        # Fast heuristic based on overlap and length
        overlap_ratio = len(set(ref_words) & set(cand_words)) / len(set(ref_words) | set(cand_words))
        length_sim = 1 - abs(len(ref_words) - len(cand_words)) / max(len(ref_words), len(cand_words))
        
        base_score = (overlap_ratio * 0.6 + length_sim * 0.4)
        noise = (hash(tuple(cand_words[-2:])) % 100) / 2000.0
        bert_score = max(0.3, min(0.95, base_score * 0.6 + 0.3 + noise))
        return round(bert_score, 4)
    
    def _mock_semantic_similarity_fast(self, ref_words: List[str], cand_words: List[str]) -> float:
        """Fast semantic similarity using pre-tokenized words."""
        if not ref_words or not cand_words:
            return 0.0
        
        ref_set = set(ref_words)
        cand_set = set(cand_words)
        jaccard = len(ref_set & cand_set) / len(ref_set | cand_set)
        
        noise = (hash(tuple(sorted(ref_set)[:2])) % 100) / 1000.0 - 0.05
        similarity = max(0.0, min(1.0, jaccard * 0.8 + 0.1 + noise))
        return round(similarity, 4)
        """
        Mock BLEU score based on n-gram overlap with some randomness.
        Real BLEU would use proper n-gram precision and brevity penalty.
        """
        # Simple word-level overlap
        ref_words = self._tokenize(reference.lower())
        cand_words = self._tokenize(candidate.lower())
        
        if not cand_words:
            return 0.0
        
        # Calculate word overlap
        ref_counter = Counter(ref_words)
        cand_counter = Counter(cand_words)
        
        overlap = sum((ref_counter & cand_counter).values())
        precision = overlap / len(cand_words) if cand_words else 0.0
        
        # Add some realistic randomness and adjust range
        noise = random.uniform(-0.1, 0.1)
        bleu = max(0.0, min(1.0, precision * 0.7 + 0.2 + noise))
        
        return round(bleu, 4)
    
    def _mock_rouge_l_score(self, reference: str, candidate: str) -> float:
        """
        Mock ROUGE-L score based on longest common subsequence.
        Real ROUGE-L would use proper LCS calculation.
        """
        ref_words = self._tokenize(reference.lower())
        cand_words = self._tokenize(candidate.lower())
        
        if not ref_words or not cand_words:
            return 0.0
        
        # Simple LCS approximation using set intersection
        common_words = set(ref_words) & set(cand_words)
        
        if not common_words:
            return 0.0
        
        # Mock F1-style calculation
        precision = len(common_words) / len(set(cand_words))
        recall = len(common_words) / len(set(ref_words))
        
        if precision + recall == 0:
            return 0.0
        
        f1 = 2 * precision * recall / (precision + recall)
        
        # Add noise and adjust
        noise = random.uniform(-0.08, 0.08)
        rouge_l = max(0.0, min(1.0, f1 * 0.8 + 0.15 + noise))
        
        return round(rouge_l, 4)
    
    def _mock_bert_score(self, reference: str, candidate: str) -> float:
        """
        Mock BERTScore based on semantic similarity heuristics.
        Real BERTScore would use BERT embeddings and cosine similarity.
        """
        ref_words = self._tokenize(reference.lower())
        cand_words = self._tokenize(candidate.lower())
        
        if not ref_words or not cand_words:
            return 0.0
        
        # Mock semantic similarity based on:
        # 1. Word overlap
        # 2. Length similarity
        # 3. Some randomness to simulate semantic understanding
        
        overlap_ratio = len(set(ref_words) & set(cand_words)) / len(set(ref_words) | set(cand_words))
        length_sim = 1 - abs(len(ref_words) - len(cand_words)) / max(len(ref_words), len(cand_words))
        
        # Base score from overlap and length
        base_score = (overlap_ratio * 0.6 + length_sim * 0.4)
        
        # Add semantic noise (simulating BERT's understanding)
        semantic_noise = random.uniform(-0.05, 0.1)
        
        # BERTScore typically ranges from 0.3 to 0.95
        bert_score = max(0.3, min(0.95, base_score * 0.6 + 0.3 + semantic_noise))
        
        return round(bert_score, 4)
    
    def _exact_match(self, reference: str, candidate: str) -> float:
        """Exact string match (normalized)."""
        ref_norm = self._normalize_text(reference)
        cand_norm = self._normalize_text(candidate)
        return 1.0 if ref_norm == cand_norm else 0.0
    
    def _mock_semantic_similarity(self, reference: str, candidate: str) -> float:
        """Mock semantic similarity using word overlap and heuristics."""
        ref_words = set(self._tokenize(reference.lower()))
        cand_words = set(self._tokenize(candidate.lower()))
        
        if not ref_words or not cand_words:
            return 0.0
        
        jaccard = len(ref_words & cand_words) / len(ref_words | cand_words)
        
        # Add some noise to simulate semantic understanding
        noise = random.uniform(-0.1, 0.15)
        similarity = max(0.0, min(1.0, jaccard * 0.8 + 0.1 + noise))
        
        return round(similarity, 4)
    
    def _length_ratio(self, reference: str, candidate: str) -> float:
        """Calculate length ratio (candidate/reference)."""
        ref_len = len(self._tokenize(reference))
        cand_len = len(self._tokenize(candidate))
        
        if ref_len == 0:
            return 0.0 if cand_len == 0 else float('inf')
        
        return round(cand_len / ref_len, 4)
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple word tokenization."""
        return re.findall(r'\b\w+\b', text.lower())
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        # Remove extra whitespace and convert to lowercase
        normalized = re.sub(r'\s+', ' ', text.strip().lower())
        # Remove punctuation
        normalized = re.sub(r'[^\w\s]', '', normalized)
        return normalized
    
    # Real implementations would be enabled by setting enable_real_metrics=True
    # These require additional dependencies:
    
    def _compute_real_bleu(self, reference: str, candidate: str) -> Dict[str, float]:
        """
        Real BLEU implementation using nltk or sacrebleu.
        Uncomment and install dependencies to use:
        
        from nltk.translate.bleu_score import sentence_bleu
        from nltk.tokenize import word_tokenize
        
        ref_tokens = [word_tokenize(reference.lower())]
        cand_tokens = word_tokenize(candidate.lower())
        
        bleu_1 = sentence_bleu(ref_tokens, cand_tokens, weights=(1, 0, 0, 0))
        bleu_2 = sentence_bleu(ref_tokens, cand_tokens, weights=(0.5, 0.5, 0, 0))
        bleu_4 = sentence_bleu(ref_tokens, cand_tokens, weights=(0.25, 0.25, 0.25, 0.25))
        
        return {
            'bleu_1': bleu_1,
            'bleu_2': bleu_2,
            'bleu_4': bleu_4
        }
        """
        pass
    
    def _compute_real_rouge(self, reference: str, candidate: str) -> Dict[str, float]:
        """
        Real ROUGE implementation using rouge-score.
        Uncomment and install dependencies to use:
        
        from rouge_score import rouge_scorer
        
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference, candidate)
        
        return {
            'rouge_1': scores['rouge1'].fmeasure,
            'rouge_2': scores['rouge2'].fmeasure,
            'rouge_l': scores['rougeL'].fmeasure
        }
        """
        pass
    
    def _compute_real_bert_score(self, reference: str, candidate: str) -> Dict[str, float]:
        """
        Real BERTScore implementation using bert-score.
        Uncomment and install dependencies to use:
        
        from bert_score import score
        
        P, R, F1 = score([candidate], [reference], lang='en', verbose=False)
        
        return {
            'bert_score_precision': P.item(),
            'bert_score_recall': R.item(),
            'bert_score_f1': F1.item()
        }
        """
        pass


def main():
    """Test the metrics calculator."""
    calc = MetricsCalculator()
    
    # Test examples
    reference = "The quick brown fox jumps over the lazy dog."
    candidate1 = "A quick brown fox leaps over a lazy dog."  # Similar
    candidate2 = "Hello world, this is completely different."  # Different
    candidate3 = "The quick brown fox jumps over the lazy dog."  # Exact
    
    test_cases = [
        ("Similar", reference, candidate1),
        ("Different", reference, candidate2),
        ("Exact", reference, candidate3)
    ]
    
    print("Metrics Calculator Test Results:")
    print("=" * 50)
    
    for name, ref, cand in test_cases:
        print(f"\n{name} Case:")
        print(f"Reference: {ref}")
        print(f"Candidate: {cand}")
        
        metrics = calc.compute_all_metrics(ref, cand)
        
        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value}")


if __name__ == "__main__":
    main()