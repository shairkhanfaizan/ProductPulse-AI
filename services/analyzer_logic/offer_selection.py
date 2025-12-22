from schemas.analysis_schema import BestOffer


# Source rank score evaluation helper
def compute_rank_score(rank: int) -> float:
    if not rank:
        return 0.4
    return max(1 - (rank - 1) * 0.1, 0.2)


# price score evaluation helper        
def compute_price_score(price: float, lowest: float, average: float) -> float:
    if price <= lowest:
        return 1.0
    if price >= average:
        return 0.5
    return round(1 - ((price - lowest) / (average - lowest)) * 0.5, 3)
  

# Function to compute seller confidence score        
def compute_seller_confidence(seller: str, rating=None, reviews=None) -> float:
    seller = seller.lower()

    trusted_sellers = ["amazon", "walmart", "bestbuy", "flipkart"]
    refurb_sellers = ["reebelo", "cashify", "backmarket"]

    if any(name in seller for name in trusted_sellers):
        score = 0.9
    elif any(name in seller for name in refurb_sellers):
        score = 0.7
    else:
        score = 0.5

    if rating and rating >= 4.5:
        score += 0.1
    if reviews and reviews >= 1000:
        score += 0.1

    return min(score, 1.0)


# Select best offer from price distribution
def select_best_offer(price_distribution: list, average_price: float) -> BestOffer:
    best_offer = None
    best_score = -1

    prices = [p.price for p in price_distribution if p.price]
    lowest_price = min(prices) if prices else None

    for index, item in enumerate(price_distribution, start=1):
        price = item.price
        seller = item.seller

        if not price or not seller:
            continue

        # Filter overpriced offers
        if average_price and price > average_price * 1.3:
            continue

        price_score = compute_price_score(price, lowest_price, average_price)
        seller_confidence = compute_seller_confidence(seller)
        rank_score = compute_rank_score(index)

        final_score = (
            0.45 * price_score +
            0.35 * seller_confidence +
            0.20 * rank_score
        )

        if final_score > best_score:
            best_score = final_score
            best_offer = {
                "seller": seller,
                "price": price,
                "condition": "refurbished" if "refurb" in seller.lower() else "unknown",
                "seller_confidence": round(seller_confidence, 2),
                "source_rank": index
            }

    return BestOffer(
        seller=best_offer["seller"],
        price=best_offer["price"],
        condition=best_offer["condition"],
        seller_confidence=best_offer["seller_confidence"],
        source_rank=best_offer["source_rank"]
    )
