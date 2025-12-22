

# generate risks and warnings
def generate_risks_and_warnings(seller_count: int, price_volatility: str, current_price: float, average_price: float) -> list:
        risks = []

        if seller_count == 1:
            risks.append("Single seller detected — limited competition")

        if price_volatility == "high volatility":
            risks.append("High price volatility — prices may fluctuate rapidly")

        if current_price and average_price and current_price > average_price * 1.15:
            risks.append("Current listing is significantly overpriced")

        if not risks:
            risks.append("No significant risk indicators detected")

        return risks