from typing import Dict, Any, List
from prompts.predictor_prompt import generate_predictor_prompt
from schemas.analysis_schema import AnalysisOutput


def llm_reasoning(llm, analyzer_output: AnalysisOutput, ml_decision: str, confidence: float) -> List[str]:
        """
        Uses LLM to generate human-readable reasoning for the ML decision.
        """
        try:
            prompt = generate_predictor_prompt(
                ml_decision=ml_decision, 
                confidence=confidence, 
                analyzer_output=analyzer_output
            )
            response = llm.invoke(prompt)
            
            # Parse reasoning into bullet points
            reasoning = [
                line.strip("- ").strip() 
                for line in response.content.split("\n") 
                if line.strip()
            ]
            
            return reasoning if reasoning else ["Decision based on ML model analysis"]
            
        except Exception as e:
            return [f"LLM reasoning failed: {str(e)}", "Decision based solely on ML model"]