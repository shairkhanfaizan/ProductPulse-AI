from typing import Any, Optional
import re

# convert various value types of prices to float
def _clean_price(price_value: Any) -> Optional[float]:
    """
    Robustly extracts a float price.
    Handles: floats (10.99), strings ("$1,099.00"), and None.
    """
    
    # Handle None
    if price_value is None:
        return None 
    
    # Handle float and int
    if isinstance(price_value, (float, int)):
        return float(price_value)
    
    # Handle string
    if isinstance(price_value, str):
        clean_str = re.sub(r'[^\d.]', '', price_value)
        try:
            return float(clean_str)
        except ValueError:
            return None 
    
    # For any other type,    
    return None    
        

    