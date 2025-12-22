from pydantic import BaseModel, Field
from typing import List


# Detailed price evaluation of the product
class PriceEvaluation(BaseModel):
    current_price: float = Field(description="The current price of the product.")
    average_price: float = Field(description="The average market price of the product.")
    lowest_price: float = Field(description="The lowest recorded price of the product.")
    highest_price: float = Field(description="The highest recorded price of the product.")
    price_position: str = Field(description="Indicates if the current price is above, below, or at the average market price.")
    price_gap_percent: float = Field(description="The percentage difference between the current price and the average price.")
    price_volatility: str = Field(description="Indicates the price volatility level: low, moderate, or high.")
        
        
# Recommended buy decision based on the analysis
class BuyDecision(BaseModel):
    action : str = Field(description="Recommended action: buy, wait, or neutral.")
    urgency : str = Field(description="Urgency level for the action: high, medium, low.")
    rationale : str = Field(description="Rationale behind the recommended action.")
    rule_triggered : str = Field(description="The specific rule that triggered this decision.")        
    
    
# Details of the best offer available in the market  
class BestOffer(BaseModel):
    seller: str = Field(description="The name of the seller offering the best price.")
    price: float = Field(description="The best offer price.")
    condition: str = Field(description="The condition of the product (e.g., new, used).")
    seller_confidence: float = Field(description="Confidence score of the seller's reliability.")
    source_rank: int = Field(description="Rank of the source in search results.")    
    

# Comprehensive market analysis for the product 
class MarketAnalysis(BaseModel):
    seller_count: int = Field(description="Number of unique sellers offering the product.")
    competition_level: str = Field(description="Level of competition among sellers: low, moderate, high.")
    pricing_health: str = Field(description="Health of pricing in the market: stable, moderate_variation, fragmented.")
    price_spread_percent: float = Field(description="Percentage spread between highest and lowest prices.")

    
# Market signals derived from the analysis  
class Signals(BaseModel):
    price_signal: str = Field(description="Indicates the price trend: bullish, bearish, neutral.")
    demand_signal: str = Field(description="Indicates the demand trend: increasing, decreasing, neutral.")
    supply_signal: str = Field(description="Indicates the supply status: healthy, low, excess.")
    momentum: str = Field(description="Indicates the market momentum: rising, falling, stable.") 
    
    
# Concise summary of the analysis
class Summary(BaseModel):
    headline: str = Field(description="A concise headline summarizing the analysis.")
    key_points: List[str] = Field(description="A list of key points highlighting the main findings.")
    short_explanation: str = Field(description="A brief explanation supporting the headline.")            


# Overall analysis output schema
class AnalysisOutput(BaseModel):
    summary : Summary = Field(description="Concise summary of the analysis.")
    price_evaluation: PriceEvaluation = Field(description="Detailed evaluation of the product's pricing.")
    buy_decision: BuyDecision = Field(description="Recommended buy decision based on the analysis.")
    best_offer : BestOffer = Field(description="Details of the best offer available in the market.")
    market_analysis: MarketAnalysis = Field(description="Comprehensive market analysis for the product.")
    risks_and_warnings : list = Field(description="List of identified risks and warnings.")
    signals: Signals = Field(description="Market signals derived from the analysis.")
    confidence_score: float = Field(description="Overall confidence score of the analysis.")  
    
