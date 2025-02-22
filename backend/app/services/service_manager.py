from .ml_service import MLService
from .search_service import SearchService

class ServiceManager:
    def __init__(self):
        self.ml_service = MLService()
        self.search_service = SearchService()
    
    def analyze_health_data(self, user_data):
        """Analyze health data using both ML and search services."""
        try:
            # Get ML predictions
            ml_predictions = self.ml_service.predict(user_data)
            
            # Get search results
            search_results = self.search_service.search_insurance_info(user_data)
            
            # Combine the results
            combined_results = {
                'risk_assessment': {
                    'risk_level': ml_predictions['risk_level'],
                    'risk_score': ml_predictions['match_score'],
                    'risk_confidence': ml_predictions['risk_confidence'],
                    'risk_factors': search_results['risk_assessment']['risk_factors'],
                    'positive_factors': search_results['risk_assessment']['positive_factors'],
                    'risk_probabilities': ml_predictions['predictions']['risk_probabilities']
                },
                'recommendations': {
                    'recommended_plan_type': ml_predictions['recommended_plan'],
                    'matching_plans': []
                }
            }
            
            # Process each provider from search results
            for provider in search_results['providers']:
                plan_details = {
                    'provider': provider['name'],
                    'plan_name': provider['recommended_plan'],
                    'url': provider['plan_link'],
                    'premium_range': {
                        'min': int(provider['coverage_options'][0]['description'].split('₹')[1].split('-')[0].strip().replace(',', '')),
                        'max': int(provider['coverage_options'][0]['description'].split('₹')[2].strip().replace(',', ''))
                    },
                    'coverage_details': provider['features'],
                    'key_benefits': provider['features'],
                    'waiting_periods': ["30 days for general conditions", "2 years for specific diseases"],
                    'exclusions': ["Cosmetic treatments", "Self-inflicted injuries"],
                    'network_hospitals': "7000+ cashless hospitals across India",
                    'claim_process': "Simple 3-step digital claim process",
                    'features': provider['features'][:3],
                    'premium_info': {
                        'starting_from': f"₹{provider['coverage_options'][0]['description'].split('₹')[1].split('-')[0].strip()}",
                        'coverage_amount': "Up to ₹1 Crore"
                    },
                    'suitability_score': provider['match_score'] / 100
                }
                combined_results['recommendations']['matching_plans'].append(plan_details)
            
            # Add AI analysis if available
            if search_results.get('ai_analysis'):
                combined_results['ai_analysis'] = search_results['ai_analysis']
            
            # Add justification from search results
            combined_results['recommendations']['justification'] = search_results['risk_assessment']['recommendations']['justification']
            
            return combined_results
            
        except Exception as e:
            print(f"Error in analyze_health_data: {str(e)}")
            raise 