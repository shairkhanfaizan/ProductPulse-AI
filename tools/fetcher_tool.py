from langchain.tools import BaseTool 
from pydantic import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
from services.fetcher_logic.query_builder  import flatten_value
from services.fetcher_logic.serpapi_parser import parse_serpapi_shopping_results
from schemas.fetcher_schema import FetcherOutput
import requests
import traceback
import os


load_dotenv()
# Load environment variables
SERPAPI_KEY = os.getenv('SERPAPI_KEY')


# Define the argument schema for the tool
class FetcherArgs(BaseModel):
    product_info: dict = Field(description="JSON containing product details to search for.")

# Define the Product Fetcher Tool
class Fetcher_Tool(BaseTool):
    name : str = "ProductFetcher"
    description : str = "Takes structured product information (JSON) extracted from text and searches the web for matching products. Uses the provided fields such as product name, brand, RAM, storage, condition, and location to fetch real-time product details like price, availability, specifications, and seller information."
    args_schema : Type[BaseModel] = FetcherArgs 

    def _run(self, product_info: dict) -> FetcherOutput:
        
        """
        Fetches real-time product prices and availability from Google Shopping.
        
        Args:
            product_info: Dictionary with product details (name, brand, specs, region)
            
        Returns:
            FetcherOutput with prices, sellers, and market data
        """
        try:
            # Build the search query from product_info
            important_fields = {
                "product_name",
                "brand",
                "model",
                "category",
                "attributes",
                "condition",  
                "market_region", 
                "additional_context",
                "search_keywords",
                "input_confidence"
            }
            
            # Construct the search query
            query = ""
            for field in important_fields:
                parts = []
                if field not in product_info:
                    raise ValueError(f"Missing required field: {field}")
                else:
                    value = product_info.get(field)
                    parts.extend(flatten_value(value))
                    query = " ".join(parts)
                    query = " ".join(query.split())
                    
            # parameters for SerpAPI request        
            params = {
                "engine" : "google_shopping", 
                "q": query,
                "api_key": SERPAPI_KEY,
                "hl": "en",                                   #host language
                "gl": product_info.get("market_region"),      #geolocation
                "num": 5                                      #number of results

            }        
                    
            # url for SerpAPI request
            url = "https://serpapi.com/search"
            
            # Make the request to SerpAPI
            result = requests.get(url, params=params)
            data = result.json()
            
            # Parse and clean the SerpAPI shopping results
            clean_data = parse_serpapi_shopping_results(product_info, data)
            
            print("✅ Fetching succeeded.")
            print(clean_data)
            
            return clean_data
    
        except Exception as e:
            print(f"❌ Fetching failed: {e}")
            traceback.print_exc()
            raise
            
        