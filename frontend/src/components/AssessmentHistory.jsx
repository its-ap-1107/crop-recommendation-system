import { motion } from 'framer-motion';
import { Button } from './Button';
import PropTypes from 'prop-types';

const getRiskColor = (score) => {
  if (score < 0.3) return 'bg-green-500';
  if (score < 0.6) return 'bg-yellow-500';
  return 'bg-red-500';
};

const AssessmentCard = ({ assessment, onClick }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
    onClick={onClick}
  >
    <div className="flex justify-between items-center">
      <div>
        <div className="flex items-center mb-2">
          <span className={`inline-block w-3 h-3 rounded-full mr-2 ${getRiskColor(assessment.risk_score)}`}></span>
          <p className="font-semibold text-gray-900">
            Risk Score: {(assessment.risk_score * 100).toFixed(1)}%
          </p>
        </div>
        <p className="text-sm text-gray-600">
          Age: {assessment.user_data.age} | 
          BMI: {assessment.user_data.bmi} | 
          BP: {assessment.user_data.blood_pressure}
        </p>
        <p className="text-xs text-gray-500 mt-1">
          {new Date(assessment.timestamp).toLocaleString()}
        </p>
      </div>
      <Button variant="outline" className="flex items-center">
        View Details
        <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
        </svg>
      </Button>
    </div>
  </motion.div>
);

AssessmentCard.propTypes = {
  assessment: PropTypes.shape({
    risk_score: PropTypes.number.isRequired,
    timestamp: PropTypes.string.isRequired,
    user_data: PropTypes.shape({
      age: PropTypes.string.isRequired,
      bmi: PropTypes.string.isRequired,
      blood_pressure: PropTypes.string.isRequired
    }).isRequired
  }).isRequired,
  onClick: PropTypes.func.isRequired
};

const AssessmentHistory = ({ assessments, onViewAssessment }) => {
  return (
    <div className="space-y-4">
      {assessments.length === 0 ? (
        <p className="text-gray-500 text-center py-8">No previous assessments found.</p>
      ) : (
        assessments.map((assessment) => (
          <AssessmentCard
            key={assessment._id}
            assessment={assessment}
            onClick={() => onViewAssessment(assessment._id)}
          />
        ))
      )}
    </div>
  );
};

AssessmentHistory.propTypes = {
  assessments: PropTypes.arrayOf(
    PropTypes.shape({
      _id: PropTypes.string.isRequired,
      risk_score: PropTypes.number.isRequired,
      timestamp: PropTypes.string.isRequired,
      user_data: PropTypes.shape({
        age: PropTypes.string.isRequired,
        bmi: PropTypes.string.isRequired,
        blood_pressure: PropTypes.string.isRequired
      }).isRequired
    })
  ).isRequired,
  onViewAssessment: PropTypes.func.isRequired
};

export default AssessmentHistory;