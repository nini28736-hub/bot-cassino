from abc import ABC, abstractmethod
from typing import List, Dict, Any

class StrategyResult:
    def __init__(self, name: str, vote: str, confidence: float, weight: float):
        self.name = name
        self.vote = vote          # Ex: "RED", "BLACK", "NONE"
        self.confidence = confidence  # 0.0 a 1.0
        self.weight = weight        # Peso na votacao

class BaseStrategy(ABC):
    @abstractmethod
    async def analyze(self, history: List[Dict[str, Any]]) -> StrategyResult:
        pass

class ColorPatternStrategy(BaseStrategy):
    """Busca sequencias repetitivas de cores."""
    async def analyze(self, history: List[Dict[str, Any]]) -> StrategyResult:
        if len(history) < 5:
            return StrategyResult("PadraoCores", "NONE", 0.0, 1.0)

        recent_colors = [item.get("color") for item in history[-4:]]
        
        # Exemplo: Se saíram 4 vermelhos seguidos
        if recent_colors == ["RED", "RED", "RED", "RED"]:
            return StrategyResult("PadraoCores", "RED", 0.85, 1.5)
        elif recent_colors == ["BLACK", "BLACK", "BLACK", "BLACK"]:
            return StrategyResult("PadraoCores", "BLACK", 0.85, 1.5)

        return StrategyResult("PadraoCores", "NONE", 0.0, 1.0)

class SequenceBreakStrategy(BaseStrategy):
    """Aposta na inversao apos longa sequencia da mesma cor."""
    async def analyze(self, history: List[Dict[str, Any]]) -> StrategyResult:
        if len(history) < 6:
            return StrategyResult("QuebraSequencia", "NONE", 0.0, 1.0)

        recent_colors = [item.get("color") for item in history[-6:]]
        
        if all(c == "RED" for c in recent_colors):
            return StrategyResult("QuebraSequencia", "BLACK", 0.75, 1.2)
        elif all(c == "BLACK" for c in recent_colors):
            return StrategyResult("QuebraSequencia", "RED", 0.75, 1.2)

        return StrategyResult("QuebraSequencia", "NONE", 0.0, 1.0)