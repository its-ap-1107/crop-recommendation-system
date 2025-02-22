import requests
from typing import List, Dict, Any
from ..config import Config

class SearchService:
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"
    
    def search_insurance_info(self, user_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Search for relevant insurance information based on user data.
        Returns a list of relevant articles and their content.
        """
        try:
            # Create a targeted search query based on user profile
            conditions = str(user_data.get('previous_conditions', 'none'))
            age = str(user_data.get('age', ''))
            health_factors = []
            
            try:
                if float(user_data.get('bmi', 0)) > 30:
                    health_factors.append("high BMI")
                if float(user_data.get('blood_pressure', 0)) > 140:
                    health_factors.append("high blood pressure")
                if str(user_data.get('smoker', '')).lower() == 'yes':
                    health_factors.append("smoker")
                if float(user_data.get('cholesterol', 0)) > 200:
                    health_factors.append("high cholesterol")
                if str(user_data.get('exercise_frequency', '')).lower() == 'low':
                    health_factors.append("sedentary lifestyle")
            except (ValueError, TypeError) as e:
                print(f"Error processing health factors: {str(e)}")
                
            health_factors_str = " and ".join(health_factors) if health_factors else "general health"
            
            # Construct search query
            search_query = "health insurance recommendations and coverage options for {} year old with {} condition and {}".format(
                age, conditions, health_factors_str
            )
            
            # Perform search using direct API call
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "query": search_query,
                "search_depth": "advanced",
                "max_results": 10,
                "include_answer": True,
                "include_raw_content": True,
                "include_images": False,
                "include_domains": [
                    "healthcare.gov",
                    "cms.gov",
                    "bcbs.com",
                    "uhc.com",
                    "cigna.com",
                    "aetna.com",
                    "humana.com",
                    "anthem.com",
                    "healthline.com",
                    "webmd.com"
                ]
            }
            
            print(f"Searching with query: {search_query}")  # Debug log
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            search_result = response.json()
            
            # Extract relevant information
            processed_results = []
            if isinstance(search_result, dict) and 'results' in search_result:
                for result in search_result['results']:
                    processed_results.append({
                        'title': result.get('title', ''),
                        'url': result.get('url', ''),
                        'content': result.get('content', '')[:500],  # Limit content length
                        'score': result.get('score', 0)
                    })
            
            print(f"Found {len(processed_results)} search results")  # Debug log
            return processed_results[:5]  # Return top 5 most relevant results
            
        except requests.exceptions.RequestException as e:
            print(f"Tavily API request error: {str(e)}")
            return []
        except Exception as e:
            print(f"Error in search_insurance_info: {str(e)}")
            return []