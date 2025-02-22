import { motion } from 'framer-motion';
import PropTypes from 'prop-types';
import { FaCheckCircle, FaExclamationTriangle, FaInfoCircle, FaShieldAlt } from 'react-icons/fa';

const HealthMetric = ({ label, value }) => (
  <div className="bg-gray-50 p-4 rounded-lg">
    <p className="text-sm text-gray-600">{label}</p>
    <p className="text-lg font-semibold">{value}</p>
  </div>
);

HealthMetric.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired
};

const RiskBadge = ({ level }) => {
  const getColorClasses = (level) => {
    switch (level?.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getColorClasses(level)}`}>
      {(level || 'Unknown').toUpperCase()}
    </span>
  );
};

RiskBadge.propTypes = {
  level: PropTypes.string
};

const ResourceCard = ({ resource }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow"
  >
    <h4 className="font-semibold text-indigo-700 mb-2">{resource.title}</h4>
    <p className="text-sm text-gray-600 mb-4 line-clamp-3">{resource.content}</p>
    <a 
      href={resource.url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="inline-flex items-center text-indigo-600 hover:text-indigo-800 text-sm font-medium"
    >
      Learn More
      <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
      </svg>
    </a>
  </motion.div>
);

ResourceCard.propTypes = {
  resource: PropTypes.shape({
    title: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired
  }).isRequired
};

const AssessmentDetails = ({ assessment }) => {
  if (!assessment) return null;

  const { user_data, risk_score, risk_assessment = {}, ai_analysis } = assessment;
  const {
    risk_level = 'unknown',
    risk_factors = [],
    positive_factors = [],
    recommendations = {
      coverage_level: 'Standard',
      premium_range: { min: 5000, max: 50000 },
      coverage_types: [],
      justification: []
    }
  } = risk_assessment;

  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Health Profile</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          <HealthMetric label="Age" value={user_data.age} />
          <HealthMetric label="Gender" value={user_data.gender} />
          <HealthMetric label="BMI" value={user_data.bmi} />
          <HealthMetric label="Blood Pressure" value={user_data.blood_pressure} />
          <HealthMetric label="Cholesterol" value={user_data.cholesterol} />
          <HealthMetric label="Exercise" value={user_data.exercise_frequency} />
        </div>
      </div>
      
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Risk Assessment</h3>
        <div className="bg-gray-100 p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <FaExclamationTriangle className={`text-${risk_level === 'high' ? 'red' : risk_level === 'moderate' ? 'yellow' : 'green'}-500`} />
              <span className="font-semibold">Risk Level:</span>
              <RiskBadge level={risk_level} />
            </div>
            <div className="text-2xl font-bold text-indigo-600">
              {(risk_score * 100).toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Health Factors</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {risk_factors.length > 0 && (
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h4 className="text-base font-semibold text-red-600 mb-3 flex items-center">
                <FaExclamationTriangle className="mr-2" />
                Risk Factors
              </h4>
              <ul className="space-y-2">
                {risk_factors.map((factor, index) => (
                  <li key={index} className="flex items-start">
                    <span className="inline-block w-2 h-2 rounded-full bg-red-400 mt-2 mr-3"></span>
                    <span className="text-gray-700">{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {positive_factors.length > 0 && (
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h4 className="text-base font-semibold text-green-600 mb-3 flex items-center">
                <FaCheckCircle className="mr-2" />
                Positive Factors
              </h4>
              <ul className="space-y-2">
                {positive_factors.map((factor, index) => (
                  <li key={index} className="flex items-start">
                    <span className="inline-block w-2 h-2 rounded-full bg-green-400 mt-2 mr-3"></span>
                    <span className="text-gray-700">{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {ai_analysis && (
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <FaInfoCircle className="mr-2 text-blue-500" />
            AI Analysis
          </h3>
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="prose max-w-none text-gray-700">
              {ai_analysis.split('\n').map((paragraph, index) => (
                <p key={index} className="mb-4">{paragraph}</p>
              ))}
            </div>
          </div>
        </div>
      )}
      
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <FaShieldAlt className="mr-2 text-indigo-600" />
          Coverage Recommendations
        </h3>
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="space-y-6">
            <div>
              <h4 className="text-base font-semibold text-indigo-600 mb-2">Recommended Level</h4>
              <p className="text-gray-700">{recommendations.coverage_level}</p>
            </div>
            
            <div>
              <h4 className="text-base font-semibold text-indigo-600 mb-2">Premium Range</h4>
              <p className="text-gray-700">
                ₹{recommendations.premium_range?.min?.toLocaleString()} - 
                ₹{recommendations.premium_range?.max?.toLocaleString()} per month
              </p>
            </div>

            {recommendations.coverage_types?.length > 0 && (
              <div>
                <h4 className="text-base font-semibold text-indigo-600 mb-2">Recommended Coverage</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {recommendations.coverage_types.map((type, index) => (
                    <div key={index} className="flex items-start bg-gray-50 p-3 rounded-lg">
                      <FaCheckCircle className="text-green-500 mt-1 mr-2 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{type}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {recommendations.justification?.length > 0 && (
              <div>
                <h4 className="text-base font-semibold text-indigo-600 mb-2">Justification</h4>
                <ul className="space-y-2">
                  {recommendations.justification.map((item, index) => (
                    <li key={index} className="flex items-start">
                      <span className="inline-block w-1.5 h-1.5 rounded-full bg-blue-400 mt-2 mr-3"></span>
                      <span className="text-sm text-gray-600">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

AssessmentDetails.propTypes = {
  assessment: PropTypes.shape({
    user_data: PropTypes.shape({
      age: PropTypes.string.isRequired,
      gender: PropTypes.string.isRequired,
      bmi: PropTypes.string.isRequired,
      blood_pressure: PropTypes.string.isRequired,
      cholesterol: PropTypes.string.isRequired,
      exercise_frequency: PropTypes.string.isRequired
    }).isRequired,
    risk_score: PropTypes.number.isRequired,
    risk_assessment: PropTypes.shape({
      risk_level: PropTypes.string,
      risk_factors: PropTypes.arrayOf(PropTypes.string),
      positive_factors: PropTypes.arrayOf(PropTypes.string),
      recommendations: PropTypes.shape({
        coverage_level: PropTypes.string,
        premium_range: PropTypes.shape({
          min: PropTypes.number,
          max: PropTypes.number
        }),
        coverage_types: PropTypes.arrayOf(PropTypes.string),
        justification: PropTypes.arrayOf(PropTypes.string)
      })
    }),
    ai_analysis: PropTypes.string
  }).isRequired
};

export default AssessmentDetails; 