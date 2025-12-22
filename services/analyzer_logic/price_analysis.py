from schemas.analysis_schema import PriceEvaluation



# get price position helper
def get_price_position(current_price: float, average_price: float, seller_count: int) -> str:
    
    
        if current_price and average_price:
            percentage_diff = round((abs(current_price - average_price) / average_price) * 100, 2)
            if seller_count and seller_count ==1:
                price_position = "at_market_average"
            if percentage_diff > -2:
                price_position = "below_market_average"
            elif percentage_diff <= 2:
                price_position = "at_market_average"   
            else:
                price_position = "above_market_average"
        else:
            price_position = "Unknown"  
            
        return price_position  
 

# get price volatility helper    
def get_price_volatility(highest_price: float, lowest_price: float, average_price: float) -> str:
    try:
        if highest_price and lowest_price and average_price:
            percentage_diff = round(((highest_price - lowest_price) / average_price) * 100, 2)    
            if percentage_diff <=5:
                price_volatility = "low volatility"
            elif 5 < percentage_diff <=15:    
                price_volatility = "moderate volatility"
            else:
                price_volatility = "high volatility"              
                
        return price_volatility     
    except Exception as e:
        return ({"error": str(e)})


   
# price evaluation aggregation helper    
def get_price_evaluation(current_price: float, average_price: float, lowest_price: float, highest_price: float, seller_count: int) -> PriceEvaluation:
        
        price_position = get_price_position(current_price, average_price, seller_count)
        price_volatility = get_price_volatility(highest_price, lowest_price, average_price)
        print("Price Position:", price_position)
        print("Price Volatility:", price_volatility)
        print("Current Price:", current_price)
        print("Average Price:", average_price)
        print("Lowest Price:", lowest_price)
        print("Highest Price:", highest_price)
        price_gap_percent = round((current_price - average_price) / average_price * 100, 2)
        print("Price Gap Percent:", price_gap_percent)
        
        return PriceEvaluation(
            current_price = current_price,
            average_price = average_price,
            lowest_price = lowest_price,
            highest_price = highest_price,
            price_position = price_position,
            price_gap_percent = price_gap_percent,
            price_volatility = price_volatility
        )    
    