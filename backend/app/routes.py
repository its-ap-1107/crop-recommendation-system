from flask import Blueprint, request, jsonify
from .services.service_manager import ServiceManager

api = Blueprint('api', __name__)
service_manager = ServiceManager()

@api.route('/analyze', methods=['POST'])
def analyze_health():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate required fields
        required_fields = ['age', 'gender', 'bmi', 'blood_pressure', 'cholesterol', 
                         'smoker', 'exercise_frequency', 'family_history']
        missing_fields = [field for field in required_fields if field not in user_data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
            
        # Get combined predictions from ML and search services
        results = service_manager.analyze_health_data(user_data)
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Error in analyze_health: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}) 