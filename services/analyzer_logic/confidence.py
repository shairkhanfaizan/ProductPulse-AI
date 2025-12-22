
# calculate confidence score
def compute_confidence_score(seller_count: int, price_volatility: str, price_position: str, data_completeness_ratio: float) -> float:
        score = 0.0

        # Seller confidence with max value 0.3
        if seller_count >= 5:
            score += 0.3
        elif seller_count >= 3:
            score += 0.2
        elif seller_count == 2:
            score += 0.1

        # Volatility confidence with max value 0.3
        if price_volatility == "low volatility":
            score += 0.3
        elif price_volatility == "moderate volatility":
            score += 0.2
        else:
            score += 0.05

        # Price clarity with max value 0.2
        if price_position in ["below_market_average", "above_market_average"]:
            score += 0.2
        else:
            score += 0.1

        # Data completeness with max value 0.2
        score += round(min(data_completeness_ratio, 1.0) * 0.2, 2)

        return round(min(score, 1.0), 2)