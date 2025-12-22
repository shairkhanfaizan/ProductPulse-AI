from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.predictor_prompt import generate_predictor_prompt
from schemas.analysis_schema import AnalysisOutput
from services.predictor_logic.buid_features import build_features
from services.predictor_logic.llm_reasoning import llm_reasoning
from dotenv import load_dotenv
import traceback
import joblib
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class PredictorArgs(BaseModel):
    analyzer_output: AnalysisOutput = Field(description="Final analyzed output from the Analyzer tool.")
    

class Predictor_Tool(BaseTool):
    name: str = "ProductPredictor"
    description: str = "Uses Logistic Regression for BUY/WAIT prediction and an LLM to validate and explain the decision."
    args_schema: Type[BaseModel] = PredictorArgs
    
    # Class constants
    MODEL_PATH: str = "models/logistic_predictor.joblib"
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_TEMPERATURE: float = 0.3
    
    # Internal attributes
    model: Optional[Any] = Field(default=None, exclude=True)
    llm: Optional[Any] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Check if model file exists
        if not os.path.exists(self.MODEL_PATH):
            raise FileNotFoundError(f"LogisticRegression model not found at {self.MODEL_PATH}")
        
        # Check if API key exists
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        try:
            # Load the trained Logistic Regression model
            object.__setattr__(self, 'model', joblib.load(self.MODEL_PATH))
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
        
        try:
            # Initialize the LLM
            object.__setattr__(self, 'llm', ChatGoogleGenerativeAI(
                model=self.LLM_MODEL,
                google_api_key=GOOGLE_API_KEY,
                temperature=self.LLM_TEMPERATURE
            ))
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")


    # Main execution method
    def _run(self, analyzer_output: AnalysisOutput) -> Dict[str, Any]:
        """
        Makes BUY/WAIT prediction using ML model and provides LLM-generated reasoning.
        
        Args:
            analyzer_output: Dictionary with analyzed market data and insights
            
        Returns:
            Dictionary containing:
                - final_decision (str): "BUY" or "WAIT"
                - confidence (float): Prediction confidence (0-1)
                - ml_decision (str): Raw ML model decision
                - llm_reasoning (list): Human-readable explanation bullets
                - feature_snapshot (dict): ML features used for prediction
        """
        try:
            # Extract features for ML model
            features = build_features(analyzer_output)

            # Get ML prediction
            probs = self.model.predict_proba([features])[0]
            pred = int(probs.argmax())
            confidence = float(probs[pred])

            ml_decision = "BUY" if pred == 1 else "WAIT"

            # Get LLM reasoning
            reasoning = llm_reasoning(self.llm, analyzer_output, ml_decision, confidence)
            
            print(f"✅ Prediction succeeded: {ml_decision} with confidence {confidence:.2f}")
            
            print({
                "final_decision": ml_decision,
                "confidence": round(confidence, 2),
                "ml_decision": ml_decision,
                "llm_reasoning": reasoning,
                "feature_snapshot": {
                    "price_gap_percent": features[0],
                    "price_spread_percent": features[1],
                    "seller_count": features[2],
                    "volatility_score": features[3],
                    "competition_score": features[4],
                    "confidence_score": features[5]
                }
            })
            
            return {
                "final_decision": ml_decision,
                "confidence": round(confidence, 2),
                "ml_decision": ml_decision,
                "llm_reasoning": reasoning,
                "feature_snapshot": {
                    "price_gap_percent": features[0],
                    "price_spread_percent": features[1],
                    "seller_count": features[2],
                    "volatility_score": features[3],
                    "competition_score": features[4],
                    "confidence_score": features[5]
                }
            }
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            traceback.print_exc()
            raise