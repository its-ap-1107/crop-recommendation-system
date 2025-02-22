import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import { FaChartLine, FaShieldAlt, FaInfoCircle, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';

const RiskBadge = ({ level }) => {
  const getColorClasses = (level) => {
    switch (level.toLowerCase()) {
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
      {level.toUpperCase()}
    </span>
  );
};

RiskBadge.propTypes = {
  level: PropTypes.string.isRequired
};

const ProgressBar = ({ score }) => {
  const getColor = (score) => {
    if (score < 0.3) return 'bg-green-500';
    if (score < 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="relative pt-1 w-full">
      <div className="flex items-center justify-between mb-2">
        <div>
          <span className="text-xs font-semibold inline-block text-gray-600">
            Risk Score
          </span>
        </div>
        <div>
          <span className="text-xs font-semibold inline-block text-gray-600">
            {(score * 100).toFixed(1)}%
          </span>
        </div>
      </div>
      <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${(score * 100).toFixed(1)}%` }}
          transition={{ duration: 1 }}
          className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${getColor(score)}`}
        />
      </div>
      <div className="flex justify-between text-xs text-gray-600 mt-1">
        <span>Low Risk</span>
        <span>Moderate Risk</span>
        <span>High Risk</span>
      </div>
    </div>
  );
};

ProgressBar.propTypes = {
  score: PropTypes.number.isRequired
};

const HealthFactors = ({ factors }) => (
  <div className="mt-6">
    <h4 className="text-sm font-semibold text-gray-700 mb-3">Health Factors</h4>
    <div className="flex flex-wrap gap-2">
      {factors.map((factor, index) => (
        <span
          key={index}
          className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
        >
          {factor}
        </span>
      ))}
    </div>
  </div>
);

HealthFactors.propTypes = {
  factors: PropTypes.arrayOf(PropTypes.string).isRequired
};

const RiskFactors = ({ factors }) => (
  <div className="mt-6">
    <h4 className="text-base font-semibold text-gray-800 flex items-center mb-3">
      <FaExclamationTriangle className="mr-2 text-yellow-500" />
      Risk Factors Analysis
    </h4>
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <ul className="space-y-2">
        {factors.map((factor, index) => (
          <li key={index} className="flex items-start">
            <span className="inline-block w-2 h-2 rounded-full bg-red-400 mt-2 mr-3"></span>
            <span className="text-gray-700">{factor}</span>
          </li>
        ))}
      </ul>
    </div>
  </div>
);

RiskFactors.propTypes = {
  factors: PropTypes.arrayOf(PropTypes.string).isRequired
};

const PositiveFactors = ({ factors }) => (
  <div className="mt-6">
    <h4 className="text-base font-semibold text-gray-800 flex items-center mb-3">
      <FaCheckCircle className="mr-2 text-green-500" />
      Positive Health Factors
    </h4>
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <ul className="space-y-2">
        {factors.map((factor, index) => (
          <li key={index} className="flex items-start">
            <span className="inline-block w-2 h-2 rounded-full bg-green-400 mt-2 mr-3"></span>
            <span className="text-gray-700">{factor}</span>
          </li>
        ))}
      </ul>
    </div>
  </div>
);

PositiveFactors.propTypes = {
  factors: PropTypes.arrayOf(PropTypes.string).isRequired
};

const CoverageRecommendation = ({ recommendations }) => (
  <div className="mt-6">
    <h4 className="text-base font-semibold text-gray-800 flex items-center mb-3">
      <FaShieldAlt className="mr-2 text-indigo-500" />
      Coverage Recommendations
    </h4>
    <div className="space-y-4">
      <div className="bg-indigo-50 p-4 rounded-lg">
        <p className="text-sm font-medium text-gray-800">
          Recommended Level: <span className="text-indigo-600 font-semibold">{recommendations.coverage_level}</span>
        </p>
        <p className="text-sm text-gray-600 mt-2">
          Monthly Premium Range: <span className="font-semibold">₹{recommendations.premium_range?.min.toLocaleString()} - ₹{recommendations.premium_range?.max.toLocaleString()}</span>
        </p>
      </div>
      
      {recommendations.coverage_types && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h5 className="text-sm font-medium text-gray-700 mb-3">Recommended Coverage Types</h5>
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

      {recommendations.justification.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h5 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <FaInfoCircle className="mr-2 text-blue-500" />
            Justification
          </h5>
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
);

CoverageRecommendation.propTypes = {
  recommendations: PropTypes.shape({
    coverage_level: PropTypes.string.isRequired,
    premium_range: PropTypes.shape({
      min: PropTypes.number.isRequired,
      max: PropTypes.number.isRequired
    }),
    coverage_types: PropTypes.arrayOf(PropTypes.string),
    justification: PropTypes.arrayOf(PropTypes.string).isRequired
  }).isRequired
};

const AIAnalysis = ({ analysis }) => {
  if (!analysis) return null;

  return (
    <div className="mt-6">
      <h4 className="text-base font-semibold text-gray-800 mb-3">
        AI Health Analysis
      </h4>
      <div className="grid grid-cols-1 gap-4">
        {analysis.split('\n\n').map((section, index) => {
          if (!section.trim()) return null;
          const [title, ...content] = section.split('\n');
          return (
            <div key={index} className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow">
              {title && (
                <h5 className="text-sm font-medium text-gray-800 mb-2">
                  {title}
                </h5>
              )}
              <div className="text-sm text-gray-600">
                {content.map((paragraph, pIndex) => (
                  <p key={pIndex} className="mb-2 last:mb-0">
                    {paragraph.replace(/^- /, '')}
                  </p>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

AIAnalysis.propTypes = {
  analysis: PropTypes.string
};

const RiskAssessment = ({ data }) => {
  if (!data) return null;

  const { risk_score = 0, risk_assessment = {}, ai_analysis } = data;
  const {
    risk_level = 'unknown',
    risk_factors = [],
    positive_factors = [],
    recommendations = {
      coverage_level: 'Standard',
      premium_range: { min: 0, max: 0 },
      coverage_types: [],
      justification: []
    }
  } = risk_assessment;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-lg p-6 space-y-6"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-gray-900 flex items-center">
          <FaChartLine className="mr-2 text-indigo-600" />
          Risk Assessment Summary
        </h3>
        <RiskBadge level={risk_level} />
      </div>

      <ProgressBar score={risk_score} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          {risk_factors.length > 0 && (
            <RiskFactors factors={risk_factors} />
          )}
        </div>
        <div>
          {positive_factors.length > 0 && (
            <PositiveFactors factors={positive_factors} />
          )}
        </div>
      </div>

      <AIAnalysis analysis={ai_analysis} />

      <CoverageRecommendation recommendations={recommendations} />
    </motion.div>
  );
};

RiskAssessment.propTypes = {
  data: PropTypes.shape({
    risk_score: PropTypes.number.isRequired,
    ai_analysis: PropTypes.string,
    risk_assessment: PropTypes.shape({
      risk_level: PropTypes.string.isRequired,
      risk_factors: PropTypes.arrayOf(PropTypes.string).isRequired,
      positive_factors: PropTypes.arrayOf(PropTypes.string).isRequired,
      recommendations: PropTypes.shape({
        coverage_level: PropTypes.string.isRequired,
        premium_range: PropTypes.shape({
          min: PropTypes.number.isRequired,
          max: PropTypes.number.isRequired
        }),
        coverage_types: PropTypes.arrayOf(PropTypes.string),
        justification: PropTypes.arrayOf(PropTypes.string).isRequired
      }).isRequired
    }).isRequired
  }).isRequired
};

export default RiskAssessment; 