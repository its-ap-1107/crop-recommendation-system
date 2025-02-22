import requests
from typing import List, Dict, Any
from ..config import Config

class SearchService:
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.groq_api_key = Config.GROQ_API_KEY
        self.base_url = "https://api.tavily.com/search"
        self.groq_url = "https://api.groq.com/v1/completions"
        self.insurance_plans = {
            'essential_care': {
                'name': 'Essential Care Plan',
                'provider': 'Niva Bupa Health Insurance',
                'website': 'https://www.nivabupa.com/health-insurance-plan/health-premia',
                'plan_link': 'https://www.nivabupa.com/health-insurance-plans/reassurev2-insurance.html',
                'monthly_premium_range': (5000, 8000),
                'coverage': {
                    'preventive_care': 100,
                    'primary_care': 80,
                    'specialist_visits': 70,
                    'emergency_care': 60,
                    'hospitalization': 60,
                    'prescription_drugs': 50
                },
                'features': [
                    'Telemedicine services 24/7',
                    'Wellness programs',
                    'Basic health coverage',
                    'Limited specialist visits'
                ],
                'best_for': ['young_healthy', 'budget_conscious', 'students']
            },
            'family_first': {
                'name': 'Family First Plan',
                'provider': 'Star Health Insurance',
                'website': 'https://www.starhealth.in/health-insurance/family-health-optima',
                'plan_link': 'https://www.starhealth.in/health-insurance/comprehensive',
                'monthly_premium_range': (8000, 12000),
                'coverage': {
                    'preventive_care': 100,
                    'primary_care': 90,
                    'specialist_visits': 85,
                    'emergency_care': 85,
                    'hospitalization': 80,
                    'prescription_drugs': 80
                },
                'features': [
                    'Family counseling services',
                    'Pediatric specialists',
                    'Maternity support',
                    'Comprehensive family coverage'
                ],
                'best_for': ['families', 'expecting_parents', 'children']
            },
            'chronic_care_plus': {
                'name': 'Chronic Care Plus',
                'provider': 'HDFC ERGO Health Insurance',
                'website': 'https://www.hdfcergo.com/health-insurance/optima-restore-individual-health-insurance-plan',
                'plan_link': 'https://www.hdfcergo.com/health-insurance/optima-restore-individual-health-insurance-plan',
                'monthly_premium_range': (12000, 18000),
                'coverage': {
                    'preventive_care': 100,
                    'primary_care': 100,
                    'specialist_visits': 95,
                    'emergency_care': 90,
                    'hospitalization': 95,
                    'prescription_drugs': 95
                },
                'features': [
                    'Care coordination',
                    'Specialist network access',
                    'Chronic disease support',
                    'Unlimited specialist visits'
                ],
                'best_for': ['chronic_conditions', 'frequent_care_needs', 'high_risk_patients']
            },
            'premium_health': {
                'name': 'Premium Health Elite',
                'provider': 'ICICI Lombard Health Insurance',
                'website': 'https://www.icicilombard.com/health-insurance/elevate-health-policy',
                'plan_link': 'https://www.icicilombard.com/health-insurance/elevate-health-policy',
                'monthly_premium_range': (15000, 25000),
                'coverage': {
                    'preventive_care': 100,
                    'primary_care': 100,
                    'specialist_visits': 100,
                    'emergency_care': 100,
                    'hospitalization': 100,
                    'prescription_drugs': 100
                },
                'features': [
                    'Concierge service',
                    'International coverage',
                    'Executive health program',
                    'Complete coverage'
                ],
                'best_for': ['premium_coverage', 'full_family_coverage', 'executives']
            }
        }
    
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

    def determine_recommended_plan(self, risk_score, user_data):
        """Determine the recommended insurance plan based on risk score and user data."""
        age = int(user_data.get('age', 0))
        
        if risk_score >= 0.7:  # High risk
            if age >= 60:
                return 'chronic_care_plus'
            else:
                return 'premium_health'
        elif risk_score >= 0.4:  # Medium risk
            if age >= 45:
                return 'chronic_care_plus'
            else:
                return 'family_first'
        else:  # Low risk
            if age < 30:
                return 'essential_care'
            else:
                return 'family_first'

    def get_groq_analysis(self, user_data, health_factors, positive_factors, risk_level):
        """Get comprehensive health analysis from Groq."""
        try:
            prompt = f"""Analyze the following health profile and provide a comprehensive insurance recommendation:

Patient Profile:
- Age: {user_data.get('age')}
- Gender: {user_data.get('gender')}
- BMI: {user_data.get('bmi')}
- Blood Pressure: {user_data.get('blood_pressure')}
- Cholesterol: {user_data.get('cholesterol')}
- Smoker: {user_data.get('smoker')}
- Exercise Frequency: {user_data.get('exercise_frequency')}
- Family History: {user_data.get('family_history')}

Risk Factors: {', '.join(health_factors) if health_factors else 'None'}
Positive Factors: {', '.join(positive_factors) if positive_factors else 'None'}
Overall Risk Level: {risk_level}

Please provide:
1. A detailed analysis of the patient's health status
2. Specific health risks and preventive measures
3. Recommended insurance coverage requirements
4. Long-term health management suggestions
5. Additional wellness recommendations"""

            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(self.groq_url, headers=headers, json=payload)
            response.raise_for_status()
            analysis = response.json()
            
            return analysis['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"Error getting Groq analysis: {str(e)}")
            return None

    def search_insurance_info(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Calculate risk score and determine factors
            risk_score = self.calculate_risk_score(user_data)
            risk_level = "high" if risk_score >= 0.7 else "moderate" if risk_score >= 0.4 else "low"
            
            # Process health factors and get recommended plan
            health_factors = self.get_health_factors(user_data)
            positive_factors = self.get_positive_factors(user_data)
            recommended_plan_key = self.determine_recommended_plan(risk_score, user_data)
            recommended_plan = self.insurance_plans[recommended_plan_key]
            
            # Get AI analysis from Groq
            ai_analysis = self.get_groq_analysis(user_data, health_factors, positive_factors, risk_level)
            
            # Prepare matched providers
            matched_providers = []
            for plan_key, plan in self.insurance_plans.items():
                match_score = 100 - (abs(risk_score - (list(self.insurance_plans.keys()).index(plan_key) / len(self.insurance_plans))) * 100)
                matched_providers.append({
                    'name': plan['provider'],
                    'website': plan['website'],
                    'plan_link': plan['plan_link'],
                    'plans': [plan['name']],
                    'features': plan['features'],
                    'match_score': match_score,
                    'recommended_plan': plan['name'],
                    'coverage_options': [
                        {
                            'title': f"{plan['name']} Coverage",
                            'description': f"Monthly premium range: ₹{plan['monthly_premium_range'][0]:,} - ₹{plan['monthly_premium_range'][1]:,}"
                        }
                    ]
                })
            
            # Sort providers by match score
            matched_providers.sort(key=lambda x: x['match_score'], reverse=True)
            
            return {
                'providers': matched_providers[:4],
                'risk_level': risk_level,
                'health_factors': health_factors,
                'search_results': [],
                'risk_score': risk_score,
                'ai_analysis': ai_analysis,
                'risk_assessment': {
                    'risk_level': risk_level,
                    'risk_factors': health_factors,
                    'positive_factors': positive_factors,
                    'recommendations': {
                        'coverage_level': recommended_plan['name'],
                        'premium_range': {
                            'min': recommended_plan['monthly_premium_range'][0],
                            'max': recommended_plan['monthly_premium_range'][1]
                        },
                        'coverage_types': [f"{k.replace('_', ' ').title()}: {v}%" for k, v in recommended_plan['coverage'].items()],
                        'justification': [
                            f"Risk level assessment: {risk_level.capitalize()}",
                            f"Based on identified health factors: {', '.join(health_factors) if health_factors else 'No significant health risks'}",
                            f"Positive health indicators: {', '.join(positive_factors) if positive_factors else 'None identified'}",
                            f"Best suited for: {', '.join(recommended_plan['best_for'])}"
                        ]
                    }
                }
            }
            
        except Exception as e:
            print(f"Error in search_insurance_info: {str(e)}")
            return {
                'providers': [],
                'risk_level': 'unknown',
                'health_factors': [],
                'search_results': [],
                'risk_score': 0.0,
                'ai_analysis': None,
                'risk_assessment': {
                    'risk_level': 'unknown',
                    'risk_factors': [],
                    'positive_factors': [],
                    'recommendations': {
                        'coverage_level': 'Standard',
                        'premium_range': {'min': 0, 'max': 0},
                        'coverage_types': [],
                        'justification': []
                    }
                }
            }

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