import requests
from typing import List, Dict, Any
from ..config import Config
from .prediction_service import BasePredictionService

class SearchService(BasePredictionService):
    def __init__(self):
        super().__init__()
        self.api_key = Config.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"
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

    def generate_health_analysis(self, user_data, health_factors, positive_factors, risk_level):
        """Generate a comprehensive health analysis based on user data."""
        age = int(user_data.get('age', 0))
        bmi = float(user_data.get('bmi', 0))
        bp = float(user_data.get('blood_pressure', 0))
        chol = float(user_data.get('cholesterol', 0))
        
        analysis = []
        
        # Health Status Analysis
        analysis.append("Health Status Analysis")
        if risk_level == 'high':
            analysis.append("Your health profile indicates several areas requiring attention and proactive management.")
        elif risk_level == 'moderate':
            analysis.append("Your health profile shows some risk factors that would benefit from lifestyle modifications.")
        else:
            analysis.append("Your health profile generally indicates good health with some areas for optimization.")
            
        # Age-specific Recommendations
        analysis.append("\nAge-specific Considerations")
        if age >= 60:
            analysis.append("- Regular health check-ups recommended every 6 months")
            analysis.append("- Focus on preventive care and early intervention")
            analysis.append("- Consider comprehensive coverage for age-related conditions")
        elif age >= 45:
            analysis.append("- Annual health check-ups recommended")
            analysis.append("- Preventive screenings for common mid-life conditions")
            analysis.append("- Balance between coverage and cost-effectiveness")
        else:
            analysis.append("- Regular health check-ups recommended annually")
            analysis.append("- Focus on preventive care and healthy lifestyle")
            analysis.append("- Consider basic coverage with wellness benefits")
            
        # Risk Factor Analysis
        if health_factors:
            analysis.append("\nKey Health Risks")
            for factor in health_factors:
                analysis.append(f"- {factor}")
                
        # Positive Factor Analysis
        if positive_factors:
            analysis.append("\nPositive Health Indicators")
            for factor in positive_factors:
                analysis.append(f"- {factor}")
                
        # Insurance Recommendations
        analysis.append("\nInsurance Coverage Recommendations")
        if risk_level == 'high':
            analysis.append("- Comprehensive coverage with low deductibles")
            analysis.append("- Extensive network of specialists")
            analysis.append("- Coverage for pre-existing conditions")
            analysis.append("- Preventive care benefits")
        elif risk_level == 'moderate':
            analysis.append("- Balanced coverage with moderate deductibles")
            analysis.append("- Good network of providers")
            analysis.append("- Wellness program benefits")
        else:
            analysis.append("- Basic coverage with preventive care benefits")
            analysis.append("- Higher deductible options for lower premiums")
            analysis.append("- Wellness program incentives")
            
        return "\n".join(analysis)

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

    def get_health_factors(self, user_data):
        """Extract health risk factors from user data."""
        health_factors = []
        try:
            bmi = float(user_data.get('bmi', 0))
            bp = float(user_data.get('blood_pressure', 0))
            chol = float(user_data.get('cholesterol', 0))
            
            if bmi > 30:
                health_factors.append("high_bmi")
            if bp > 140:
                health_factors.append("high_bp")
            if str(user_data.get('smoker', '')).lower() == 'yes':
                health_factors.append("smoker")
            if chol > 200:
                health_factors.append("high_cholesterol")
            if str(user_data.get('exercise_frequency', '')).lower() == 'low':
                health_factors.append("sedentary_lifestyle")
            
            if user_data.get('previous_conditions', 'none') != 'none':
                health_factors.append(user_data['previous_conditions'])
            
            if user_data.get('family_history', 'none') != 'none':
                health_factors.append('family_history')
            
            if int(user_data.get('age', 0)) >= 60:
                health_factors.append('senior')
            elif int(user_data.get('age', 0)) >= 45:
                health_factors.append('middle_age')
                
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

    def calculate_premium(self, user_data, base_premium_range):
        """Calculate personalized premium based on user health data."""
        min_premium, max_premium = base_premium_range
        risk_score = self.calculate_risk_score(user_data)
        age = int(user_data.get('age', 0))
        
        # Age factor
        if age >= 60:
            age_multiplier = 1.4
        elif age >= 45:
            age_multiplier = 1.2
        elif age >= 30:
            age_multiplier = 1.1
        else:
            age_multiplier = 1.0
            
        # Risk score factor
        risk_multiplier = 1.0 + (risk_score * 0.5)  # Max 50% increase based on risk
        
        # Calculate adjusted premiums
        adjusted_min = int(min_premium * age_multiplier * risk_multiplier)
        adjusted_max = int(max_premium * age_multiplier * risk_multiplier)
        
        return (adjusted_min, adjusted_max)

    def calculate_match_score(self, user_data, plan):
        """Calculate how well a plan matches user needs."""
        score = 0
        age = int(user_data.get('age', 0))
        
        # Age-based matching (30%)
        if age >= 60 and any(tag in ['chronic_conditions', 'high_risk_patients'] for tag in plan['best_for']):
            score += 30
        elif 30 <= age < 60 and 'families' in plan['best_for']:
            score += 30
        elif age < 30 and 'young_healthy' in plan['best_for']:
            score += 30
        
        # Risk level matching (30%)
        risk_score = self.calculate_risk_score(user_data)
        if risk_score >= 0.7 and any(tag in ['chronic_conditions', 'high_risk_patients'] for tag in plan['best_for']):
            score += 30
        elif 0.4 <= risk_score < 0.7 and 'families' in plan['best_for']:
            score += 30
        elif risk_score < 0.4 and 'young_healthy' in plan['best_for']:
            score += 30
        
        # Coverage matching based on health factors (40%)
        health_factors = self.get_health_factors(user_data)
        coverage_score = 0
        if health_factors:
            if plan['coverage']['specialist_visits'] >= 85:
                coverage_score += 10
            if plan['coverage']['emergency_care'] >= 85:
                coverage_score += 10
            if plan['coverage']['hospitalization'] >= 85:
                coverage_score += 10
            if plan['coverage']['prescription_drugs'] >= 85:
                coverage_score += 10
        else:
            # If no health factors, give points for basic coverage
            coverage_score = 40
        
        score += coverage_score
        return score  # Already capped at 100 by the components

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
            
            # Calculate personalized premium and match score
            adjusted_premium_range = self.calculate_premium(user_data, recommended_plan['monthly_premium_range'])
            match_score = self.calculate_match_score(user_data, recommended_plan)
            
            # Generate health analysis
            analysis = self.generate_health_analysis(user_data, health_factors, positive_factors, risk_level)
            
            # Prepare matched providers with insurance links and match scores
            matched_providers = []
            for plan_key, plan in self.insurance_plans.items():
                plan_match_score = self.calculate_match_score(user_data, plan)
                premium_range = self.calculate_premium(user_data, plan['monthly_premium_range'])
                matched_providers.append({
                    'name': plan['provider'],
                    'website': plan['website'],
                    'plan_link': plan['plan_link'],
                    'plans': [plan['name']],
                    'features': plan['features'],
                    'match_score': plan_match_score,
                    'recommended_plan': plan['name'],
                    'insurance_links': {
                        'website': plan['website'],
                        'plan_details': plan['plan_link']
                    },
                    'coverage_options': [
                        {
                            'title': f"{plan['name']} Coverage",
                            'description': f"Monthly premium range: ₹{premium_range[0]:,} - ₹{premium_range[1]:,}",
                            'link': plan['plan_link']
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
                'ai_analysis': analysis,
                'risk_assessment': {
                    'risk_level': risk_level,
                    'risk_factors': health_factors,
                    'positive_factors': positive_factors,
                    'recommendations': {
                        'coverage_level': recommended_plan['name'],
                        'premium_range': {
                            'min': adjusted_premium_range[0],
                            'max': adjusted_premium_range[1]
                        },
                        'coverage_types': [f"{k.replace('_', ' ').title()}: {v}%" for k, v in recommended_plan['coverage'].items()],
                        'justification': [
                            f"Risk level assessment: {risk_level.capitalize()}",
                            f"Based on identified health factors: {', '.join(health_factors) if health_factors else 'No significant health risks'}",
                            f"Positive health indicators: {', '.join(positive_factors) if positive_factors else 'None identified'}",
                            f"Best suited for: {', '.join(recommended_plan['best_for'])}",
                            f"Plan match score: {match_score}%"
                        ],
                        'insurance_link': recommended_plan['plan_link'],
                        'provider_website': recommended_plan['website'],
                        'match_score': match_score
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
                        'justification': [],
                        'insurance_link': '',
                        'provider_website': '',
                        'match_score': 0
                    }
                }
            }