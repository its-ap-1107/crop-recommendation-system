from groq import Groq
import httpx
from typing import List, Dict, Any
from ..config import Config

class AIService:
    def __init__(self):
        """Initialize the Groq client with proper configuration"""
        self.client = Groq(
            api_key=Config.GROQ_API_KEY,
            http_client=httpx.Client(timeout=30.0)  # Set reasonable timeout
        )
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimates the number of tokens in a text string.
        This is a simple approximation - actual token count may vary.
        """
        # Simple estimation: ~4 characters per token on average
        return len(text) // 4
    
    def _truncate_text(self, text: str, max_tokens: int) -> str:
        """
        Truncates text to approximately fit within max_tokens.
        """
        estimated_chars = max_tokens * 4
        if len(text) > estimated_chars:
            return text[:estimated_chars] + "..."
        return text
    
    def generate_recommendation(self, user_data: Dict[str, Any], search_results: List[Dict[str, str]]) -> str:
        """
        Generates insurance recommendations using Groq's AI model.
        Uses the latest llama-3.3-70b-versatile model for better performance.
        Incorporates search results for more accurate recommendations.
        """
        try:
            # Convert numeric values to proper format
            age = str(user_data.get('age', ''))
            bmi = str(user_data.get('bmi', ''))
            blood_pressure = str(user_data.get('blood_pressure', ''))
            cholesterol = str(user_data.get('cholesterol', ''))
            
            # Prepare search context
            search_context = ""
            if search_results:
                search_context = "\n\nRelevant insurance information from trusted sources:\n"
                for idx, result in enumerate(search_results[:3], 1):  # Use top 3 results
                    search_context += f"\nSource {idx}:\n"
                    search_context += f"Title: {result.get('title', '')}\n"
                    search_context += f"Content Summary: {result.get('content', '')[:300]}...\n"  # Limit content length
                    search_context += f"URL: {result.get('url', '')}\n"
            
            # Create the full prompt
            prompt = f"""Based on the following patient profile and insurance market data, provide a detailed insurance recommendation:

Patient Profile:
- Age: {age}
- Gender: {user_data.get('gender', '')}
- BMI: {bmi}
- Blood Pressure: {blood_pressure}
- Cholesterol: {cholesterol}
- Smoker: {user_data.get('smoker', '')}
- Exercise Frequency: {user_data.get('exercise_frequency', '')}
- Family History: {user_data.get('family_history', '')}
- Previous Conditions: {user_data.get('previous_conditions', '')}

{search_context}

Please provide a comprehensive insurance recommendation including:
1. Risk Assessment Summary
2. Recommended Coverage Level (Basic, Standard, Premium) with justification
3. Specific Coverage Types and Benefits needed based on health profile
4. Estimated Monthly Premium Range
5. Key Considerations and Potential Exclusions
6. Tips for Getting Better Rates
7. Suggested Insurance Providers or Plans (based on search results)

Format the response in clear sections with bullet points for easy reading."""

            # Ensure prompt fits within model's context window
            max_prompt_tokens = Config.GROQ_MAX_TOKENS - Config.GROQ_RESPONSE_MAX_TOKENS
            truncated_prompt = self._truncate_text(prompt, max_prompt_tokens)
            
            print("Generating AI recommendation...")  # Debug log
            
            completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert insurance advisor with access to real-time market data. Provide clear, actionable recommendations based on the user's health data and current insurance market information."
                    },
                    {
                        "role": "user",
                        "content": truncated_prompt
                    }
                ],
                model=Config.GROQ_MODEL,
                temperature=Config.GROQ_TEMPERATURE,
                max_tokens=Config.GROQ_RESPONSE_MAX_TOKENS,
                top_p=0.9,
                stream=False
            )
            
            if not completion.choices:
                raise Exception("No response received from Groq API")
                
            recommendation = completion.choices[0].message.content
            print("AI recommendation generated successfully")  # Debug log
            return recommendation
            
        except httpx.HTTPError as e:
            error_msg = f"HTTP error occurred: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Failed to generate AI recommendation: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
            
    def __del__(self):
        """Cleanup method to ensure proper resource handling"""
        if hasattr(self, 'client') and hasattr(self.client, 'http_client'):
            self.client.http_client.close() 