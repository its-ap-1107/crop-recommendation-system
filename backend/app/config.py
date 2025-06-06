from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys and Credentials
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    
    # Risk Assessment Weights
    RISK_WEIGHTS: Dict[str, float] = {
        "age": 0.01,  # per year
        "bmi_abnormal": 0.2,
        "high_blood_pressure": 0.3,
        "smoker": 0.4,
        "family_history": 0.2,
        "previous_conditions": 0.3
    }
    
    # MongoDB Collections
    MONGO_DB_NAME = "insurance_assistant"
    USERS_COLLECTION = "users"
    ASSESSMENTS_COLLECTION = "assessments"
    
    # API Configuration
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]  # Add your frontend URLs
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True
    
    @staticmethod
    def validate_config() -> None:
        required_vars = ["TAVILY_API_KEY", "MONGO_URI"]
        missing = [var for var in required_vars if not getattr(Config, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}") 