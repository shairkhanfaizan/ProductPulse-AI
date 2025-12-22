from typing import List, Dict, Any
from schemas.analysis_schema import AnalysisOutput

# Feature Extraction for ML Model
def build_features(analyzer_output: AnalysisOutput) -> List[float]:
    """
    Extracts 6 features from analyzer output for ML prediction.
    
    Features:
    1. price_gap_percent
    2. price_spread_percent
    3. seller_count
    4. volatility_score (0=low, 1=medium, 2=high)
    5. competition_score (0=low, 1=medium, 2=high)
    6. confidence_score
    """
    price_eval = analyzer_output.price_evaluation or {}
    market = analyzer_output.market_analysis or {}

    volatility_map = {
        "low volatility": 0,
        "medium volatility": 1,
        "moderate volatility": 1,
        "high volatility": 2
    }

    competition_map = {
        "low": 0,
        "medium": 1,
        "moderate": 1,
        "high": 2
    }

    return [
        price_eval.price_gap_percent or 0.0,
        market.price_spread_percent or 0.0,
        market.seller_count or 0,
        volatility_map.get((price_eval.price_volatility or "").lower(), 1),
        competition_map.get((market.competition_level or "").lower(), 1),
        analyzer_output.confidence_score or 0.5
    ]