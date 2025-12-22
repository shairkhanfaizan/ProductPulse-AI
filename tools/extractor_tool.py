from langchain_core.tools import BaseTool 
from pydantic import BaseModel, Field 
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from schemas.product_schema import ProductSchema
from prompts.Extractor_prompt import extract_prompt_template
from typing import Type 
import traceback




# Define the argument schema for the tool
class ExtractorArgs(BaseModel):
    input_text: str = Field(description="The text to extract product information from.")
    
    
# Define the Product Extractor Tool
class Extractor_Tool(BaseTool):
    name : str = "ProductExtractor"
    description : str = "Extracts structured information from raw text. The input is a string, and the output is a dictionary containing the extracted fields"
    args_schema : Type[BaseModel] = ExtractorArgs
    
    def _run(self, input_text: str) -> dict:
        
        """
        Extracts product information from raw text using LLM.
        
        Args:
            input_text: Raw text containing product information
            
        Returns:
            Dictionary with extracted product information
            
        Raises:
            ValueError: If input is invalid
            RuntimeError: If extraction fails
        """
        try:
            # initialize the LLM
            llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)
            
            # Define the json parser
            json_parser = JsonOutputParser(schema = ProductSchema)
            
            # Define the prompt template 
            prompt = PromptTemplate(
                template=extract_prompt_template,
                input_variables= ["input_text"],
                partial_variables={'format_instructions': json_parser.get_format_instructions()}
            )
            
            # Format the prompt with user input
            formatted_prompt = prompt.format(input_text=input_text)
            
            # Get the response from the LLM
            response = llm.invoke(formatted_prompt)
            
            print("✅ Extraction succeeded.")
            
            # Parse and return the JSON response
            print(json_parser.parse(response.content))
            
            return json_parser.parse(response.content)
        
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            traceback.print_exc()
            raise
        
        