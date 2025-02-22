import numpy as np
import pandas as pd
import joblib
import os
from .prediction_service import BasePredictionService

class MLService(BasePredictionService):
    def __init__(self):
        super().__init__()
        self.risk_model = None
        self.plan_model = None
        self.score_model = None
        self.label_encoders = {}
        self.scaler = None
        self.features = None
        self.models_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        self.load_models()

    def load_models(self):
        """Load trained models from joblib file."""
        try:
            model_file = os.path.join(self.models_path, 'insurance_models.joblib')
            if not os.path.exists(model_file):
                raise FileNotFoundError(f"Model file not found. Please run train_models.py first.")
            
            print("Loading ML models...")
            models = joblib.load(model_file)
            self.risk_model = models['risk_model']
            self.plan_model = models['plan_model']
            self.score_model = models['score_model']
            self.label_encoders = models['label_encoders']
            self.scaler = models['scaler']
            self.features = models['feature_names']
            print("Models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            raise

    def predict(self, user_data):
        """Make predictions using trained models."""
        try:
            # Create DataFrame with correct column names
            input_data = pd.DataFrame([{
                'Age': user_data['age'],
                'Gender': user_data['gender'],
                'BMI': user_data['bmi'],
                'Blood Pressure': user_data['blood_pressure'],
                'Cholesterol': user_data['cholesterol'],
                'Smoker': user_data['smoker'],
                'Exercise Frequency': user_data['exercise_frequency'],
                'Family History': user_data['family_history'],
                'Previous Conditions': user_data.get('previous_conditions', 'none')
            }])
            
            # Create categorical features
            input_data['age_group'] = pd.cut(input_data['Age'], 
                                           bins=[0, 30, 45, 60, 100],
                                           labels=['young', 'middle', 'senior', 'elderly'])
            
            input_data['bmi_category'] = pd.cut(input_data['BMI'],
                                              bins=[0, 18.5, 25, 30, 35, 100],
                                              labels=['underweight', 'normal', 'overweight', 'obese', 'severely_obese'])
            
            input_data['bp_category'] = pd.cut(input_data['Blood Pressure'],
                                             bins=[0, 120, 140, 160, 200],
                                             labels=['normal', 'prehypertension', 'stage1', 'stage2'])
            
            # Encode categorical variables
            for col, le in self.label_encoders.items():
                if col in input_data.columns:
                    input_data[col] = le.transform(input_data[col])
            
            # Scale numerical features
            numerical_features = ['Age', 'BMI', 'Blood Pressure', 'Cholesterol']
            input_data[numerical_features] = self.scaler.transform(input_data[numerical_features])
            
            # Make predictions
            risk_level = self.risk_model.predict(input_data[self.features])[0]
            recommended_plan = self.plan_model.predict(input_data[self.features])[0]
            match_score = float(self.score_model.predict(input_data[self.features])[0])
            
            # Get prediction probabilities for risk level
            risk_probs = self.risk_model.predict_proba(input_data[self.features])[0]
            risk_confidence = float(max(risk_probs) * 100)
            
            return {
                'risk_level': risk_level,
                'recommended_plan': recommended_plan,
                'match_score': match_score,
                'risk_confidence': risk_confidence,
                'predictions': {
                    'risk_probabilities': {
                        'low': float(risk_probs[0] * 100),
                        'moderate': float(risk_probs[1] * 100),
                        'high': float(risk_probs[2] * 100)
                    }
                }
            }
            
        except Exception as e:
            print(f"Error making predictions: {str(e)}")
            raise 