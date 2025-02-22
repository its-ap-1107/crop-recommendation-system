import requests
from typing import List, Dict, Any
from ..config import Config

class SearchService:
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"
        self.insurance_providers = [
            "Tata AIG Health Insurance",
            "SBI Health Insurance",
            "Reliance Health Insurance",
            "Future Generali India Insurance",
            "New India Assurance",
            "ManipalCigna Health Insurance",
            "HDFC ERGO Health Insurance",
            "Care Health Insurance",
            "Aditya Birla Health Insurance",
            "ICICI Lombard General Insurance"
        ]
    
    def search_insurance_info(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for relevant insurance information based on user data.
        Returns insurance recommendations and provider information.
        """
        try:
            # Create a targeted search query based on user profile
            conditions = str(user_data.get('previous_conditions', 'none'))
            age = str(user_data.get('age', ''))
            health_factors = []
            risk_level = "low"
            
            try:
                bmi = float(user_data.get('bmi', 0))
                bp = float(user_data.get('blood_pressure', 0))
                chol = float(user_data.get('cholesterol', 0))
                
                if bmi > 30:
                    health_factors.append("high BMI")
                    risk_level = "high"
                if bp > 140:
                    health_factors.append("high blood pressure")
                    risk_level = "high"
                if str(user_data.get('smoker', '')).lower() == 'yes':
                    health_factors.append("smoker")
                    risk_level = "high"
                if chol > 200:
                    health_factors.append("high cholesterol")
                    risk_level = "moderate"
                if str(user_data.get('exercise_frequency', '')).lower() == 'low':
                    health_factors.append("sedentary lifestyle")
                    risk_level = "moderate"
                if str(user_data.get('family_history', '')).lower() == 'yes':
                    health_factors.append("family history")
                    risk_level = "moderate"
            except (ValueError, TypeError) as e:
                print(f"Error processing health factors: {str(e)}")
                
            health_factors_str = " and ".join(health_factors) if health_factors else "general health"
            
            # Construct search queries for different aspects
            queries = [
                f"health insurance plans for {age} year old with {health_factors_str} in India",
                f"{risk_level} risk health insurance coverage benefits and exclusions",
                "health insurance premium calculation factors and typical rates India"
            ]
            
            all_results = []
            provider_info = {}
            
            for provider in self.insurance_providers:
                provider_info[provider] = {
                    "name": provider,
                    "match_score": 0,
                    "features": [],
                    "coverage_options": [],
                    "premium_range": {"min": 0, "max": 0}
                }
            
            for query in queries:
                try:
                    # Perform search using direct API call
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                    
                    payload = {
                        "query": query,
                        "search_depth": "advanced",
                        "max_results": 10,
                        "include_answer": True,
                        "include_raw_content": True,
                        "include_images": False,
                        "search_type": "news",
                        "include_domains": [
                            "tataaig.com",
                            "sbilife.co.in",
                            "reliancegeneral.co.in",
                            "futuregenerali.in",
                            "newindia.co.in",
                            "manipalcigna.com",
                            "hdfcergo.com",
                            "careinsurance.com",
                            "adityabirlacapital.com",
                            "icicilombard.com"
                        ]
                    }
                    
                    response = requests.post(self.base_url, headers=headers, json=payload)
                    response.raise_for_status()
                    search_result = response.json()
                    
                    if isinstance(search_result, dict) and 'results' in search_result:
                        results = search_result.get('results', [])
                        if results:
                            all_results.extend(results)
                            
                            # Process results to update provider information
                            for result in results:
                                for provider in self.insurance_providers:
                                    if provider.lower() in result.get('title', '').lower() or provider.lower() in result.get('content', '').lower():
                                        provider_info[provider]['match_score'] += result.get('score', 0)
                                        content = result.get('content', '').lower()
                                        
                                        # Extract features and coverage options
                                        if 'coverage' in content or 'benefit' in content:
                                            provider_info[provider]['features'].append(result.get('title', ''))
                                        if 'premium' in content or 'price' in content:
                                            provider_info[provider]['coverage_options'].append({
                                                'title': result.get('title', ''),
                                                'description': result.get('content', '')[:200]
                                            })
                except requests.exceptions.RequestException as e:
                    print(f"Error in search query: {str(e)}")
                    continue
            
            # Calculate final match scores and sort providers
            matched_providers = []
            for provider, info in provider_info.items():
                if info['match_score'] > 0:
                    # Normalize score based on health factors
                    base_score = info['match_score']
                    if risk_level == "high" and "comprehensive" in str(info).lower():
                        base_score *= 1.2
                    elif risk_level == "low" and "basic" in str(info).lower():
                        base_score *= 1.1
                    
                    matched_providers.append({
                        'name': info['name'],
                        'match_score': round(base_score * 100, 2),
                        'features': list(set(info['features']))[:3] if info['features'] else [],
                        'coverage_options': info['coverage_options'][:2] if info['coverage_options'] else [],
                        'recommended_plan': 'Premium' if risk_level == "high" else 'Standard' if risk_level == "moderate" else 'Basic'
                    })
            
            # Sort providers by match score
            matched_providers.sort(key=lambda x: x['match_score'], reverse=True)
            
            # Prepare search results
            formatted_results = []
            for result in all_results[:3]:  # Take top 3 results
                formatted_results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', '')[:500] if result.get('content') else '',
                    'score': result.get('score', 0)
                })
            
            return {
                'providers': matched_providers[:5] if matched_providers else [],
                'risk_level': risk_level,
                'health_factors': health_factors,
                'search_results': formatted_results
            }
            
        except Exception as e:
            print(f"Error in search_insurance_info: {str(e)}")
            return {
                'providers': [],
                'risk_level': 'unknown',
                'health_factors': [],
                'search_results': []
            }