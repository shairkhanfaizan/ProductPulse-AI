from schemas.analysis_schema import BuyDecision

# Recommended buy decision based on the analysis
def get_buy_decision_info(price_position: str, price_gap_percent: float, price_volatility: str, seller_count: int) -> BuyDecision:
     if price_position and price_gap_percent and price_volatility and seller_count is not None:
            if price_position == "below_market_average" and price_gap_percent <= -5 and price_volatility in ["low volatility", "moderate volatility"] and seller_count >=3:
                action = "Buy"
                urgency = "High"
                rationale = "The current price is significantly below the market average with multiple sellers available."
                rule_triggered = "BELOW_MARKET_STABLE_PRICE"  
            elif price_position == "below_market_average" and -2 < price_gap_percent < -5 and price_volatility == "low volatility":
                action = "Buy"
                urgency = "Medium"
                rationale = "The current price is moderately below the market average with low price volatility."
                rule_triggered = "SLIGHTLY_BELOW_MARKET_(LOW_VOLATILITY)" 
            elif price_position == "above_market_average" and price_gap_percent >= 3:
                action = "Wait"
                urgency = "Low"
                rationale = "The current price is above the market average; consider waiting for a better deal."
                rule_triggered = "ABOVE_MARKET_PRICE"        
            elif price_volatility == "high volatility":
                action = "Wait"
                urgency = "Medium"
                rationale = "High price volatility suggests waiting for a more stable price."
                rule_triggered = "HIGH_PRICE_VOLATILITY"
            elif (price_position == "at_market_average") or (price_position == "below_market_average" and seller_count == 1):
                action = "Neutral"
                urgency = "Low"
                rationale = "The current price is at the market average; no immediate action needed."
                rule_triggered = "MARKET_EQUILIBRIUM"     
            return BuyDecision(
                action = action,
                urgency = urgency,
                rationale = rationale,
                rule_triggered = rule_triggered
            )
       