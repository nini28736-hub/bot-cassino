import asyncio
from typing import List, Dict, Any
from engine.strategies import BaseStrategy, StrategyResult

class DecisionEngine:
    def __init__(self, strategies: List[BaseStrategy], consensus_threshold: float = 70.0):
        self.strategies = strategies
        self.threshold = consensus_threshold

    async def evaluate(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        tasks = [strat.analyze(history) for strat in self.strategies]
        results: List[StrategyResult] = await asyncio.gather(*tasks)

        scores: Dict[str, float] = {}
        total_weight = 0.0

        for res in results:
            if res.vote == "NONE":
                continue
            weighted_score = res.confidence * res.weight
            scores[res.vote] = scores.get(res.vote, 0.0) + weighted_score
            total_weight += res.weight

        if total_weight == 0.0:
            return {"signal": None, "consensus": 0.0}

        best_vote = max(scores, key=scores.get)
        consensus = (scores[best_vote] / total_weight) * 100.0

        if consensus >= self.threshold:
            return {"signal": best_vote, "consensus": consensus}

        return {"signal": None, "consensus": consensus}