from typing import Dict, Any
from ..config import Config

class RiskAssessmentService:
    @staticmethod
    def analyze_health_risk(user_data: Dict[str, Any]) -> float:
        """
        Analyzes health risk based on user data and returns a risk score between 0 and 1.
        """
        try:
            risk_score = 0.0
            weights = Config.RISK_WEIGHTS
            
            # Age factor
            age = float(user_data['age'])
            risk_score += age * weights['age']
            
            # BMI factor
            bmi = float(user_data['bmi'])
            if bmi < 18.5 or bmi > 30:
                risk_score += weights['bmi_abnormal']
            
            # Blood pressure factor
            bp = float(user_data['blood_pressure'])
            if bp > 140:
                risk_score += weights['high_blood_pressure']
                
            # Other factors
            if user_data['smoker'].lower() == 'yes':
                risk_score += weights['smoker']
            if user_data['family_history'].lower() == 'yes':
                risk_score += weights['family_history']
            if user_data['previous_conditions'].lower() != 'none':
                risk_score += weights['previous_conditions']
                
            return min(risk_score, 1.0)
            
        except Exception as e:
            raise ValueError(f"Error calculating risk score: {str(e)}")
    
    @staticmethod
    def generate_recommendation_prompt(user_data: Dict[str, Any], risk_score: float) -> str:
        """
        Generates a prompt for the AI model based on user data and risk score.
        """
        return f"""
        Given the following patient data:
        - Age: {user_data['age']}
        - Gender: {user_data['gender']}
        - BMI: {user_data['bmi']:.1f}
        - Blood Pressure: {user_data['blood_pressure']}
        - Cholesterol: {user_data['cholesterol']}
        - Smoker: {user_data['smoker']}
        - Exercise Frequency: {user_data['exercise_frequency']}
        - Family History: {user_data['family_history']}
        - Previous Conditions: {user_data['previous_conditions']}
        - Calculated Risk Score: {risk_score:.2f}

        Provide a detailed health insurance recommendation including:
        1. Recommended coverage level (Basic, Standard, Premium)
        2. Key benefits to look for
        3. Estimated monthly premium range
        4. Special considerations based on their health profile
        
        Format the response in clear sections with bullet points for easy reading.
        """ 