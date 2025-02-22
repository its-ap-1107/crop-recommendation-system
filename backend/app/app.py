from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

from .config import Config
from .services.risk_assessment import RiskAssessmentService
from .services.search_service import SearchService

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=Config.CORS_ORIGINS)

# Validate configuration
Config.validate_config()

# Initialize services
try:
    mongo_client = MongoClient(Config.MONGO_URI)
    mongo_client.server_info()  # Test connection
    
    search_service = SearchService()
    risk_service = RiskAssessmentService()
    
except Exception as e:
    print(f"Error initializing services: {str(e)}")
    raise

# Initialize database collections
db = mongo_client[Config.MONGO_DB_NAME]
assessments_collection = db[Config.ASSESSMENTS_COLLECTION]

@app.route('/api/analyze', methods=['POST'])
def analyze_insurance():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'bmi', 'blood_pressure', 'cholesterol', 
                         'smoker', 'exercise_frequency', 'family_history']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Calculate health risk
        risk_score = risk_service.analyze_health_risk(user_data)
        risk_level = risk_service.get_risk_level(risk_score)
        
        # Get relevant insurance information using search service
        search_data = search_service.search_insurance_info(user_data)
        
        # Process providers data
        providers = []
        for provider in search_data.get('providers', []):
            provider_data = {
                'name': provider.get('name', ''),
                'description': provider.get('description', ''),
                'rating': 4.5,  # Default rating
                'premium_range': {
                    'min': provider.get('monthly_premium_range', [5000, 8000])[0],
                    'max': provider.get('monthly_premium_range', [5000, 8000])[1]
                },
                'features': provider.get('features', []),
                'plan_types': [
                    {
                        'type': opt.get('title', ''),
                        'description': opt.get('description', '')
                    } for opt in provider.get('coverage_options', [])
                ],
                'links': {
                    'quote': provider.get('website', ''),
                    'details': provider.get('plan_link', '')
                }
            }
            providers.append(provider_data)
        
        # Store assessment
        assessment_data = {
            'user_data': user_data,
            'risk_score': risk_score,
            'search_results': search_data.get('search_results', []),
            'providers': providers,
            'risk_assessment': {
                'risk_level': risk_level,
                'risk_factors': search_data.get('health_factors', []),
                'positive_factors': search_data.get('positive_factors', []),
                'recommendations': {
                    'coverage_level': search_data.get('risk_assessment', {}).get('recommendations', {}).get('coverage_level', 'Standard'),
                    'premium_range': {
                        'min': 5000,
                        'max': 50000
                    },
                    'coverage_types': search_data.get('risk_assessment', {}).get('recommendations', {}).get('coverage_types', []),
                    'justification': search_data.get('risk_assessment', {}).get('recommendations', {}).get('justification', [])
                }
            },
            'ai_analysis': search_data.get('ai_analysis'),
            'timestamp': datetime.utcnow()
        }
        
        try:
            result = assessments_collection.insert_one(assessment_data)
            assessment_id = str(result.inserted_id)
        except Exception as e:
            print(f"Error storing in MongoDB: {str(e)}")
            assessment_id = None
        
        response_data = {
            'risk_score': risk_score,
            'providers': providers,
            'risk_assessment': assessment_data['risk_assessment'],
            'ai_analysis': search_data.get('ai_analysis'),
            'search_results': search_data.get('search_results', [])
        }
        
        if assessment_id:
            response_data['assessment_id'] = assessment_id
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in analyze_insurance: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request. Please try again.',
            'details': str(e)
        }), 500

@app.route('/api/assessments', methods=['GET'])
def get_assessments():
    try:
        assessments = list(assessments_collection.find(
            {}, 
            {
                'user_data': 1, 
                'risk_score': 1, 
                'timestamp': 1,
                'risk_assessment.risk_level': 1
            }
        ).sort('timestamp', -1).limit(10))
        
        for assessment in assessments:
            assessment['_id'] = str(assessment['_id'])
            assessment['timestamp'] = assessment['timestamp'].isoformat()
            
        return jsonify(assessments)
        
    except Exception as e:
        print(f"Error in get_assessments: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/<assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    try:
        assessment = assessments_collection.find_one({'_id': ObjectId(assessment_id)})
        if assessment:
            assessment['_id'] = str(assessment['_id'])
            assessment['timestamp'] = assessment['timestamp'].isoformat()
            
            # Ensure consistent data structure
            if 'risk_assessment' not in assessment:
                assessment['risk_assessment'] = {
                    'risk_level': 'unknown',
                    'risk_factors': [],
                    'positive_factors': [],
                    'recommendations': {
                        'coverage_level': 'Standard',
                        'premium_range': {'min': 5000, 'max': 50000},
                        'coverage_types': [],
                        'justification': []
                    }
                }
            
            if 'providers' in assessment:
                for provider in assessment['providers']:
                    if 'rating' not in provider:
                        provider['rating'] = 4.5
                    if 'premium_range' not in provider:
                        provider['premium_range'] = {'min': 5000, 'max': 8000}
                    if 'plan_types' not in provider:
                        provider['plan_types'] = [
                            {
                                'type': opt.get('title', ''),
                                'description': opt.get('description', '')
                            } for opt in provider.get('coverage_options', [])
                        ]
                    if 'links' not in provider:
                        provider['links'] = {
                            'quote': provider.get('website', ''),
                            'details': provider.get('plan_link', '')
                        }
            
            return jsonify(assessment)
        else:
            return jsonify({'error': 'Assessment not found'}), 404
            
    except Exception as e:
        print(f"Error in get_assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
