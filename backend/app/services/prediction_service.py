"""Base class for prediction services."""

class BasePredictionService:
    def calculate_risk_score(self, user_data):
        """Calculate risk score based on user health data."""
        risk_score = 0.0
        
        # Age factor
        age = int(user_data.get('age', 0))
        if age >= 60:
            risk_score += 0.8
        elif age >= 45:
            risk_score += 0.6
        elif age >= 30:
            risk_score += 0.4
        else:
            risk_score += 0.2
            
        # BMI factor
        bmi = float(user_data.get('bmi', 0))
        if bmi >= 35:
            risk_score += 0.8
        elif bmi >= 30:
            risk_score += 0.6
        elif bmi >= 25:
            risk_score += 0.4
        else:
            risk_score += 0.2
            
        # Blood pressure factor
        bp = float(user_data.get('blood_pressure', 0))
        if bp >= 160:
            risk_score += 0.8
        elif bp >= 140:
            risk_score += 0.6
        elif bp >= 120:
            risk_score += 0.4
        else:
            risk_score += 0.2
            
        # Smoking factor
        if str(user_data.get('smoker', '')).lower() == 'yes':
            risk_score += 0.6
            
        # Exercise factor
        exercise = str(user_data.get('exercise_frequency', '')).lower()
        if exercise == 'low':
            risk_score += 0.6
        elif exercise == 'medium':
            risk_score += 0.3
            
        # Family history factor
        if user_data.get('family_history', 'none') != 'none':
            risk_score += 0.4
            
        # Normalize risk score
        risk_score = risk_score / 4.0  # Maximum possible score
        return min(risk_score, 1.0)

    def get_health_factors(self, user_data):
        """Extract health risk factors from user data."""
        health_factors = []
        try:
            bmi = float(user_data.get('bmi', 0))
            bp = float(user_data.get('blood_pressure', 0))
            chol = float(user_data.get('cholesterol', 0))
            
            if bmi > 30:
                health_factors.append("High BMI")
            if bp > 140:
                health_factors.append("High blood pressure")
            if str(user_data.get('smoker', '')).lower() == 'yes':
                health_factors.append("Smoker")
            if chol > 200:
                health_factors.append("High cholesterol")
            if str(user_data.get('exercise_frequency', '')).lower() == 'low':
                health_factors.append("Sedentary lifestyle")
            
            family_history = user_data.get('family_history', 'none')
            if family_history != 'none':
                condition_labels = {
                    'heart_disease': 'heart disease',
                    'diabetes': 'diabetes',
                    'cancer': 'cancer',
                    'asthma': 'asthma',
                    'hypertension': 'hypertension',
                    'stroke': 'stroke',
                    'fatty_liver': 'fatty liver disease',
                    'thyroid': 'thyroid disorders',
                    'arthritis': 'arthritis',
                    'obesity': 'obesity'
                }
                health_factors.append(f"Family history of {condition_labels.get(family_history, family_history)}")
        except (ValueError, TypeError) as e:
            print(f"Error processing health factors: {str(e)}")
        return health_factors

    def get_positive_factors(self, user_data):
        """Extract positive health factors from user data."""
        positive_factors = []
        try:
            if str(user_data.get('exercise_frequency', '')).lower() in ['high', 'medium']:
                positive_factors.append("Regular exercise routine")
            if str(user_data.get('smoker', '')).lower() == 'no':
                positive_factors.append("Non-smoker")
            if float(user_data.get('bmi', 0)) >= 18.5 and float(user_data.get('bmi', 0)) <= 24.9:
                positive_factors.append("Healthy BMI")
            if float(user_data.get('blood_pressure', 0)) < 120:
                positive_factors.append("Normal blood pressure")
            if float(user_data.get('cholesterol', 0)) < 200:
                positive_factors.append("Healthy cholesterol levels")
        except (ValueError, TypeError) as e:
            print(f"Error processing positive factors: {str(e)}")
        return positive_factors 