from typing import Dict, Any
from ..config import Config

class RiskAssessmentService:
    # Risk weights for different conditions
    HIGH_RISK_CONDITIONS = {
        'heart_disease', 'cancer', 'stroke'
    }
    
    MODERATE_RISK_CONDITIONS = {
        'diabetes', 'hypertension', 'fatty_liver', 'thyroid',
        'arthritis', 'obesity', 'asthma'
    }
    
    @staticmethod
    def analyze_health_risk(user_data: Dict[str, Any]) -> float:
        """
        Analyzes health risk based on user data and returns a risk score between 0 and 1.
        """
        try:
            risk_score = 0.0
            weights = Config.RISK_WEIGHTS
            
            # Age factor (0.1 per decade starting from 20)
            age = float(user_data['age'])
            risk_score += min((age - 20) / 10 * 0.1, 0.3) if age > 20 else 0
            
            # BMI factor
            bmi = float(user_data['bmi'])
            if bmi > 30:  # Obese
                risk_score += 0.2
            elif bmi > 25:  # Overweight
                risk_score += 0.1
            elif bmi < 18.5:  # Underweight
                risk_score += 0.1
            
            # Blood pressure factor
            bp = float(user_data['blood_pressure'])
            if bp >= 160:  # Stage 2 hypertension
                risk_score += 0.3
            elif bp >= 140:  # Stage 1 hypertension
                risk_score += 0.2
            elif bp >= 120:  # Elevated
                risk_score += 0.1
                
            # Cholesterol factor
            cholesterol = float(user_data['cholesterol'])
            if cholesterol >= 240:  # High
                risk_score += 0.2
            elif cholesterol >= 200:  # Borderline high
                risk_score += 0.1
                
            # Smoking factor
            if user_data['smoker'].lower() == 'yes':
                risk_score += 0.2
            elif user_data['smoker'].lower() == 'occasional':
                risk_score += 0.1
                
            # Exercise factor
            exercise = user_data['exercise_frequency'].lower()
            if exercise == 'sedentary':
                risk_score += 0.2
            elif exercise == 'low':
                risk_score += 0.1
                
            # Family history factor
            family_history = user_data['family_history']
            if family_history != 'none':
                if family_history in RiskAssessmentService.HIGH_RISK_CONDITIONS:
                    risk_score += 0.3
                elif family_history in RiskAssessmentService.MODERATE_RISK_CONDITIONS:
                    risk_score += 0.2
            
            # Normalize and cap the risk score
            return min(risk_score, 1.0)
            
        except Exception as e:
            raise ValueError(f"Error calculating risk score: {str(e)}")
    
    @staticmethod
    def get_risk_level(risk_score: float) -> str:
        """
        Converts a risk score to a risk level string.
        """
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "moderate"
        else:
            return "low"
    
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