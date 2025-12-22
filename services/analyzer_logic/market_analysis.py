from schemas.analysis_schema import MarketAnalysis

# generate market analysis
def generate_market_analysis(seller_count: int, lowest_price: float, highest_price: float, average_price: float) -> MarketAnalysis:
        if not all([seller_count, lowest_price, highest_price, average_price]):
            return {"market_status": "insufficient_data"}

        spread_percent = round(((highest_price - lowest_price) / average_price) * 100, 2)

        if seller_count >= 5:
            competition = "high"
        elif 2 <= seller_count < 5:
            competition = "moderate"
        else:
            competition = "low"

        if spread_percent <= 10:
            pricing_health = "stable"
        elif spread_percent <= 20:
            pricing_health = "moderate_variation"
        else:
            pricing_health = "fragmented"

        return MarketAnalysis(
            seller_count = seller_count,
            competition_level = competition,
            pricing_health = pricing_health,
            price_spread_percent = spread_percent,
        )