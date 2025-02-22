import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import { FaChartLine, FaCheckCircle, FaExclamationTriangle, FaShieldAlt, FaChartBar } from 'react-icons/fa';

const RiskBadge = ({ level }) => {
  const getColorClasses = (level) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border border-red-200';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border border-gray-200';
    }
  };

  return (
    <span className={`px-4 py-1.5 rounded-full text-sm font-semibold ${getColorClasses(level)} shadow-sm`}>
      {level.toUpperCase()}
    </span>
  );
};

RiskBadge.propTypes = {
  level: PropTypes.string.isRequired
};

const ProgressBar = ({ score }) => {
  const getColor = (score) => {
    if (score < 0.3) return 'from-green-400 to-green-500';
    if (score < 0.6) return 'from-yellow-400 to-yellow-500';
    return 'from-red-400 to-red-500';
  };

  return (
    <div className="relative pt-1 w-full">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          <FaChartBar className="text-gray-500 mr-2" />
          <span className="text-sm font-medium text-gray-700">
            Risk Score
          </span>
        </div>
        <div>
          <span className="text-sm font-bold text-gray-700">
            {(score * 100).toFixed(1)}%
          </span>
        </div>
      </div>
      <div className="h-3 bg-gray-100 rounded-full overflow-hidden shadow-inner">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${(score * 100).toFixed(1)}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full bg-gradient-to-r ${getColor(score)}`}
        />
      </div>
      <div className="flex justify-between text-xs text-gray-500 mt-2 font-medium">
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

const FactorCard = ({ icon: Icon, title, factors, type }) => {
  const getColors = () => {
    switch (type) {
      case 'risk':
        return {
          bg: 'bg-red-50',
          border: 'border-red-100',
          icon: 'text-red-500',
          dot: 'bg-red-400'
        };
      case 'positive':
        return {
          bg: 'bg-green-50',
          border: 'border-green-100',
          icon: 'text-green-500',
          dot: 'bg-green-400'
        };
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-100',
          icon: 'text-gray-500',
          dot: 'bg-gray-400'
        };
    }
  };

  const colors = getColors();

  return (
    <div className={`rounded-xl ${colors.bg} border ${colors.border} p-5 h-full`}>
      <h4 className="text-base font-semibold text-gray-800 flex items-center mb-4">
        <Icon className={`mr-2 ${colors.icon}`} />
        {title}
      </h4>
      <ul className="space-y-3">
        {factors.map((factor, index) => (
          <li key={index} className="flex items-start">
            <span className={`inline-block w-2 h-2 rounded-full ${colors.dot} mt-2 mr-3`}></span>
            <span className="text-gray-700">
              {factor.replace(/_/g, ' ')}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

FactorCard.propTypes = {
  icon: PropTypes.elementType.isRequired,
  title: PropTypes.string.isRequired,
  factors: PropTypes.arrayOf(PropTypes.string).isRequired,
  type: PropTypes.oneOf(['risk', 'positive', 'default']).isRequired
};

const CoverageRecommendation = ({ recommendations }) => (
  <div className="mt-8">
    <h4 className="text-lg font-semibold text-gray-800 flex items-center mb-4">
      <FaShieldAlt className="mr-3 text-indigo-500" />
      Coverage Recommendations
    </h4>
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl p-6 border border-indigo-100 shadow-sm">
        <div className="mb-4">
          <p className="text-xl font-semibold text-gray-800">
            Recommended Plan: <span className="text-indigo-600">{recommendations.coverage_level}</span>
          </p>
          <p className="text-base text-gray-600 mt-2">
            Monthly Premium Range: <span className="font-semibold">₹5,000 - ₹10,000</span>
          </p>
        </div>
      </div>
      
      {recommendations.coverage_types && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h5 className="text-base font-semibold text-gray-800 mb-4">Coverage Types</h5>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.coverage_types.map((type, index) => (
              <div key={index} className="flex items-center bg-gray-50 p-4 rounded-lg border border-gray-100">
                <FaCheckCircle className="text-green-500 mr-3 flex-shrink-0" />
                <span className="text-sm text-gray-700">{type}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {recommendations.justification.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h5 className="text-base font-semibold text-gray-800 mb-4">
            Why This Plan?
          </h5>
          <ul className="space-y-3">
            {recommendations.justification.map((item, index) => (
              <li key={index} className="flex items-start">
                <span className="inline-block w-2 h-2 rounded-full bg-indigo-400 mt-2 mr-3"></span>
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
    justification: PropTypes.arrayOf(PropTypes.string).isRequired,
    insurance_link: PropTypes.string.isRequired,
    provider_website: PropTypes.string.isRequired
  }).isRequired
};

const AIAnalysis = ({ analysis }) => {
  if (!analysis) return null;

  return (
    <div className="mt-8">
      <h4 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <FaChartLine className="mr-3 text-blue-500" />
        AI Health Analysis
      </h4>
      <div className="grid grid-cols-1 gap-4">
        {analysis.split('\n\n').map((section, index) => {
          if (!section.trim()) return null;
          const [title, ...content] = section.split('\n');
          return (
            <div key={index} className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
              {title && (
                <h5 className="text-base font-medium text-gray-800 mb-3">
                  {title}
                </h5>
              )}
              <div className="text-sm text-gray-600 space-y-2">
                {content.map((paragraph, pIndex) => (
                  <p key={pIndex}>
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
      justification: [],
      provider_website: '',
      insurance_link: ''
    }
  } = risk_assessment;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-lg p-8"
    >
      <div className="flex items-center justify-between mb-8">
        <h3 className="text-2xl font-bold text-gray-900 flex items-center">
          <div className="bg-indigo-100 p-2 rounded-lg mr-3">
            <FaChartLine className="text-indigo-600 text-xl" />
          </div>
          Risk Assessment Summary
        </h3>
        <RiskBadge level={risk_level} />
      </div>

      <div className="bg-gray-50 rounded-xl p-6 mb-8">
        <ProgressBar score={risk_score} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {risk_factors.length > 0 && (
          <FactorCard
            icon={FaExclamationTriangle}
            title="Risk Factors"
            factors={risk_factors}
            type="risk"
          />
        )}
        {positive_factors.length > 0 && (
          <FactorCard
            icon={FaCheckCircle}
            title="Positive Health Factors"
            factors={positive_factors}
            type="positive"
          />
        )}
      </div>

      <AIAnalysis analysis={ai_analysis} />

      <CoverageRecommendation recommendations={{
        ...recommendations,
        provider_website: recommendations.provider_website || '',
        insurance_link: recommendations.insurance_link || ''
      }} />
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
        justification: PropTypes.arrayOf(PropTypes.string).isRequired,
        provider_website: PropTypes.string.isRequired,
        insurance_link: PropTypes.string.isRequired
      }).isRequired
    }).isRequired
  }).isRequired
};

export default RiskAssessment; 