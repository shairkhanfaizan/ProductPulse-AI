from schemas.analysis_schema import Signals

# generate market signals
def generate_signals(price_position: str, price_volatility: str, seller_count: int) -> Signals:
    # Determine price signal
    if price_position == "below_market_average":
        price_signal = "bullish"
    elif price_position == "above_market_average":
        price_signal = "bearish"
    else:
        price_signal = "neutral"
    
    # Determine demand signal based on seller count
    demand_signal = "increasing" if seller_count >= 3 else "neutral"
    
    # Determine supply signal
    supply_signal = "healthy" if seller_count >= 3 else "low"
    
    # Determine momentum based on volatility
    if price_volatility == "low volatility":
        momentum = "stable"
    elif price_volatility == "high volatility":
        momentum = "volatile"
    else:
        momentum = "moderate"
    
    return Signals(
        price_signal=price_signal,
        demand_signal=demand_signal,
        supply_signal=supply_signal,
        momentum=momentum
    )
    
