from services.analyzer_logic.confidence import compute_confidence_score
from services.analyzer_logic.price_analysis import get_price_evaluation
from services.analyzer_logic.market_analysis import generate_market_analysis
from services.analyzer_logic.risk_analysis import generate_risks_and_warnings
from services.analyzer_logic.signals import generate_signals
from services.analyzer_logic.buy_decision import get_buy_decision_info
from services.analyzer_logic.offer_selection import select_best_offer
from services.analyzer_logic.data_completeness import get_data_completeness_ratio
from services.analyzer_logic.get_analysis import get_analysis_data
from schemas.analysis_schema import Summary, AnalysisOutput
from schemas.fetcher_schema import FetcherOutput
from prompts.analyzer_prompts import system_prompt_template, summarize_prompt_template
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json
import traceback



# Define the argument schema for the tool
class AnalyzerArgs(BaseModel):
    fetched_product_info: FetcherOutput = Field(description="Structured product information (JSON) fetched from the web.")

# Define the Product Analyzer Tool
class Analyzer_Tool(BaseTool):
    name : str = "ProductAnalyzer" 
    description : str = "Analyzes structured product information (JSON) and provides insights such as price trends, demand forecasting, and competitive analysis based on historical and real-time data."
    args_schema : Type[BaseModel] = AnalyzerArgs 
    
    
    def _run(self, fetched_product_info: FetcherOutput) -> AnalysisOutput:
        """
        Analyzes market data and provides insights on pricing, competition, and buy recommendations.
        
        Args:
            fetched_product_info: Dictionary with fetched market data (prices, sellers, distribution)
            
        Returns:
            AnalysisOutput with summary, price evaluation, buy decision, best offer, market analysis, risks and warnings, signals and confidence score.
        """
        try:
            # Extract relevant fields from fetched_product_info
            current_price = fetched_product_info.current_price
            average_price = fetched_product_info.average_price
            lowest_price = fetched_product_info.lowest_price
            highest_price = fetched_product_info.highest_price
            seller_count = fetched_product_info.seller_count
            price_distribution = fetched_product_info.price_distribution

            
            # Get price evaluation
            price_evaluation = get_price_evaluation(current_price, average_price, lowest_price, highest_price, seller_count)
            
            # Get buy decision
            buy_decision = get_buy_decision_info(price_position=price_evaluation.price_position, price_gap_percent=price_evaluation.price_gap_percent, price_volatility=price_evaluation.price_volatility, seller_count=seller_count)
            
            # Select best offer
            best_offer = select_best_offer(price_distribution, average_price)
            
            # Generate market analysis
            market_analysis = generate_market_analysis(seller_count, lowest_price, highest_price, average_price)
            
            # Generate risks and warnings
            risks_and_warnings = generate_risks_and_warnings(seller_count, price_evaluation.price_volatility, current_price, average_price)
            
            # Generate market signals
            signals = generate_signals(price_evaluation.price_position, price_evaluation.price_volatility, seller_count)
            
            # get data completeness ratio for calculating confidence score
            data_completeness_ratio = get_data_completeness_ratio(current_price, average_price, lowest_price, highest_price, seller_count)
            
            # Compute confidence score        
            confidence_score = compute_confidence_score(seller_count, price_evaluation.price_position, price_evaluation.price_volatility, data_completeness_ratio)
            
            # Summarize analysis using LLM
            
            # initialize the LLM
            llm = ChatOllama(model="llama3.1:8b", temperature=0.5)
            
            # Get analysis data for the prompt
            analysis_data = get_analysis_data(fetched_product_info, price_evaluation, buy_decision, market_analysis, best_offer, risks_and_warnings, signals, confidence_score)
            
            # Define the prompt template 
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt_template),
                ("human", summarize_prompt_template + "\n\n{format_instructions}")
            ])
            
            parser = PydanticOutputParser(pydantic_object=Summary)
            
            # Create the LLM chain
            chain = prompt | llm | parser
                
            # generate the summary
            summary = chain.invoke({"analysis_data": json.dumps(analysis_data, indent=2), "format_instructions": parser.get_format_instructions()})
            
            print("✅ Analysis succeeded.")
            
            print(AnalysisOutput(
                summary = summary,
                price_evaluation = price_evaluation,
                buy_decision = buy_decision,
                best_offer = best_offer,
                market_analysis = market_analysis,
                risks_and_warnings = risks_and_warnings,
                signals = signals,
                confidence_score = confidence_score
            ))
            
            return AnalysisOutput(
                summary = summary,
                price_evaluation = price_evaluation,
                buy_decision = buy_decision,
                best_offer = best_offer,
                market_analysis = market_analysis,
                risks_and_warnings = risks_and_warnings,
                signals = signals,
                confidence_score = confidence_score
            )

        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            traceback.print_exc()
            raise