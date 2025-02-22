from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
import numpy as np
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Initialize database
db = mongo_client.insurance_assistant
users_collection = db.users
assessments_collection = db.assessments

def analyze_health_risk(user_data):
    # Calculate risk score based on user data
    risk_score = 0
    
    # Age factor
    age = float(user_data['age'])
    risk_score += age / 100
    
    # BMI factor
    bmi = float(user_data['bmi'])
    if bmi < 18.5 or bmi > 30:
        risk_score += 0.2
    
    # Blood pressure factor
    bp = float(user_data['blood_pressure'])
    if bp > 140:
        risk_score += 0.3
        
    # Other factors
    if user_data['smoker'] == 'yes':
        risk_score += 0.4
    if user_data['family_history'] == 'yes':
        risk_score += 0.2
    if user_data['previous_conditions'] != 'none':
        risk_score += 0.3
        
    return min(risk_score, 1.0)

@app.route('/api/analyze', methods=['POST'])
def analyze_insurance():
    user_data = request.json
    
    try:
        # Calculate health risk
        risk_score = analyze_health_risk(user_data)
        
        # Generate insurance recommendation using Groq
        prompt = f"""
        Given the following patient data:
        - Age: {user_data['age']}
        - Gender: {user_data['gender']}
        - BMI: {user_data['bmi']:.1f}
        - Blood Pressure: {user_data['blood_pressure']}
        - Cholesterol: {user_data['cholesterol']}
        - Smoker: {user_data['smoker']}
        - Exercise Frequency: {user_data['exercise_frequency']}
        - Family History: {user_data['family_history']}
        - Previous Conditions: {user_data['previous_conditions']}
        - Calculated Risk Score: {risk_score:.2f}

        Provide a detailed health insurance recommendation including:
        1. Recommended coverage level (Basic, Standard, Premium)
        2. Key benefits to look for
        3. Estimated monthly premium range
        4. Special considerations based on their health profile
        """
        
        completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.7,
        )
        
        # Get relevant insurance information using Tavily
        search_result = tavily_client.search(
            query=f"health insurance plans for {user_data['age']} year old with {user_data['previous_conditions']} condition",
            search_depth="advanced"
        )
        
        # Store the assessment in MongoDB
        assessment_data = {
            'user_data': user_data,
            'risk_score': risk_score,
            'recommendation': completion.choices[0].message.content,
            'relevant_info': search_result,
            'timestamp': datetime.utcnow()
        }
        
        result = assessments_collection.insert_one(assessment_data)
        
        return jsonify({
            'assessment_id': str(result.inserted_id),
            'risk_score': risk_score,
            'recommendation': completion.choices[0].message.content,
            'relevant_info': search_result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessments', methods=['GET'])
def get_assessments():
    try:
        # Get the latest 10 assessments
        assessments = list(assessments_collection.find(
            {}, 
            {'user_data': 1, 'risk_score': 1, 'timestamp': 1}
        ).sort('timestamp', -1).limit(10))
        
        # Convert ObjectId to string for JSON serialization
        for assessment in assessments:
            assessment['_id'] = str(assessment['_id'])
            assessment['timestamp'] = assessment['timestamp'].isoformat()
            
        return jsonify(assessments)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/<assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    try:
        from bson.objectid import ObjectId
        
        assessment = assessments_collection.find_one({'_id': ObjectId(assessment_id)})
        if assessment:
            assessment['_id'] = str(assessment['_id'])
            assessment['timestamp'] = assessment['timestamp'].isoformat()
            return jsonify(assessment)
        else:
            return jsonify({'error': 'Assessment not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
