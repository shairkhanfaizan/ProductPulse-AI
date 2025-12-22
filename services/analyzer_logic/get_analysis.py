from schemas.analysis_schema import PriceEvaluation, BuyDecision, MarketAnalysis, BestOffer, Signals

# Helper function to structure analysis data
def get_analysis_data(fetched_product_info: dict, price_evaluation: PriceEvaluation, buy_decision: BuyDecision, market_analysis: MarketAnalysis, best_offer: BestOffer, risks_and_warnings: list, signals: Signals, confidence_score: float) -> dict:
    analysis_data = {
        "product_name": fetched_product_info.product_name,
        "price_evaluation": price_evaluation.model_dump(),
        "buy_decision": buy_decision.model_dump(),
        "market_analysis": market_analysis.model_dump(),
        "best_offer": best_offer.model_dump(),
        "risks_and_warnings": risks_and_warnings,
        "signals": signals.model_dump(),
        "confidence_score": confidence_score
    }
    return analysis_data
              