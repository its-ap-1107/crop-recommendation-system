from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

from .config import Config
from .services.risk_assessment import RiskAssessmentService
from .services.ai_service import AIService
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
    ai_service = AIService()
    
except Exception as e:
    print(f"Error initializing services: {str(e)}")
    raise

# Initialize database collections
db = mongo_client[Config.MONGO_DB_NAME]
users_collection = db[Config.USERS_COLLECTION]
assessments_collection = db[Config.ASSESSMENTS_COLLECTION]

@app.route('/api/analyze', methods=['POST'])
def analyze_insurance():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'bmi', 'blood_pressure', 'cholesterol', 
                         'smoker', 'exercise_frequency', 'family_history', 'previous_conditions']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Calculate health risk
        risk_score = RiskAssessmentService.analyze_health_risk(user_data)
        
        # Get relevant insurance information using Tavily
        search_results = search_service.search_insurance_info(user_data)
        
        # Generate AI recommendation using both user data and search results
        recommendation = ai_service.generate_recommendation(user_data, search_results)
        
        # Store assessment
        assessment_data = {
            'user_data': user_data,
            'risk_score': risk_score,
            'recommendation': recommendation,
            'search_results': search_results,
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
            'recommendation': recommendation,
            'search_results': search_results[:3]  # Send top 3 most relevant results
        }
        
        if assessment_id:
            response_data['assessment_id'] = assessment_id
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in analyze_insurance: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessments', methods=['GET'])
def get_assessments():
    try:
        assessments = list(assessments_collection.find(
            {}, 
            {'user_data': 1, 'risk_score': 1, 'timestamp': 1}
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
            return jsonify(assessment)
        else:
            return jsonify({'error': 'Assessment not found'}), 404
            
    except Exception as e:
        print(f"Error in get_assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
