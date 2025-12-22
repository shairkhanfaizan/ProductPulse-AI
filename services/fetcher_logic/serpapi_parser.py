from services.fetcher_logic.price_parser import _clean_price
from schemas.fetcher_schema import PriceDistribution 
from schemas.fetcher_schema import FetcherOutput
from datetime import datetime, timezone


# parse SerpAPI shopping results
def parse_serpapi_shopping_results(product_info: dict, serpapi_data: dict) -> FetcherOutput:
    """
    Parses SerpAPI shopping results and maps them to the FetcherOutput schema.
    """
    
    # Extract shopping results
    results= serpapi_data.get("shopping_results", [])
    
    # Process prices and build price distribution
    valid_prices = []
    price_distributions = []
    
    for item in results:
        
        # Extract seller/source name
        source = item.get("source") or item.get("seller") or "Unknown Seller" 
        
        # Extract and clean price
        raw_price = item.get("extracted_price") or item.get("price") or item.get("extracted_old_price") or None 
        final_price = _clean_price(raw_price)
        
        # Append to price distribution and valid prices if price is valid
        if final_price is not None:
            price_distributions.append(PriceDistribution(
                seller = source,
                price = final_price
            ))
            valid_prices.append(final_price) 
    
    # Calculate price statistics    
    count= len(valid_prices)
    if count>0:
        avg_price = sum(valid_prices) / count 
        lowest = min(valid_prices)
        highest = max(valid_prices) 
        curr_price = valid_prices[0] 
    else:
        lowest = highest = avg_price = curr_price = None 
    
    # Determine trend signals
    trend_signals = {} 
    if curr_price and avg_price:
        if curr_price < avg_price:
            trend_signals = {
                "signal" : "buy",
                "reason" : "below_market_average",
                "percentage_difference" : round(((avg_price - curr_price) / avg_price )* 100, 2)
            }
        elif curr_price > avg_price:
            trend_signals = {
                "signal" : "wait",
                "reason" : "above_market_average",
                "percentage_diffference" : round(((curr_price - avg_price) / avg_price) * 100, 2)
            }    
        else:
            trend_signals = { "signal" : "neutral", "reason" : "at_market_average"}    
    
    # Build and return the FetcherOutput 
    return FetcherOutput(
        product_name = product_info.get("product_name", "Unknown Product"),
        brand = product_info.get("brand"),
        model = product_info.get("model"),
        market_region = product_info.get("market_region"),
        currency = product_info.get("currency", "USD"),
        timestamp = datetime.now(timezone.utc).isoformat() + "Z",          # Coordinated Universal Time (UTC), eg: ISO 8601 format "2025-12-13 17:33:14.500000Z" Z: zulu time        
        current_price = curr_price,
        lowest_price = lowest,
        highest_price = highest,
        average_price = avg_price,
        seller_count = count,
        price_distribution = price_distributions,
        trend_signals = trend_signals
    )         