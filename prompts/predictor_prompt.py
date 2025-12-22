def generate_predictor_prompt(ml_decision: str, confidence: float, analyzer_output: dict) -> str:
    """
    Generates a prompt for the LLM to explain the ML prediction.
    
    Args:
        ml_decision: The ML model's decision (BUY or WAIT)
        confidence: Confidence score from the ML model
        analyzer_output: Full analysis data from the analyzer tool
        
    Returns:
        Formatted prompt string for the LLM
    """
    
    price_eval = getattr(analyzer_output, "price_evaluation", None)
    market_analysis = getattr(analyzer_output, "market_analysis", None)
    buy_decision = getattr(analyzer_output, "buy_decision", None)
    
    prompt = f"""You are an expert product analyst. The ML model has made a prediction. Provide clear, actionable reasoning.

        **ML PREDICTION:**
        - Decision: {ml_decision}
        - Confidence: {confidence:.1%}

        **MARKET DATA:**
        - Current Price Position: {price_eval.price_position if price_eval else 'N/A'}
        - Price Gap: {price_eval.price_gap_percent if price_eval else 0:.1f}%
        - Price Volatility: {price_eval.price_volatility if price_eval else 'N/A'}
        - Seller Count: {market_analysis.seller_count if market_analysis else 0}
        - Competition Level: {market_analysis.competition_level if market_analysis else 'N/A'}
        - Price Spread: {market_analysis.price_spread_percent if market_analysis else 0:.1f}%

        **ANALYZER RECOMMENDATION:**
        - Action: {buy_decision.action if buy_decision else 'N/A'}
        - Urgency: {buy_decision.urgency if buy_decision else 'N/A'}
        - Rule Triggered: {buy_decision.rule_triggered if buy_decision else 'N/A'}

        **TASK:**
        Provide 3-5 clear, concise bullet points explaining why the {ml_decision} decision makes sense (or doesn't). Consider:
        1. Price positioning and value
        2. Market stability and risk factors
        3. Competition and supply dynamics
        4. Timing and urgency considerations

        Format as bullet points starting with '-'. Be specific and actionable."""
            
    return prompt