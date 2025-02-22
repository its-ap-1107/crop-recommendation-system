import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import { FaBuilding, FaCheckCircle, FaExternalLinkAlt, FaShieldAlt } from 'react-icons/fa';

const PlanFeature = ({ feature }) => (
  <div className="flex items-center text-gray-700 mb-2">
    <FaCheckCircle className="text-green-500 mr-2" />
    <span>{feature}</span>
  </div>
);

PlanFeature.propTypes = {
  feature: PropTypes.string.isRequired
};

const PlanType = ({ type, description }) => (
  <div className="bg-gray-50 rounded-lg p-4 mb-4">
    <h4 className="text-sm font-semibold text-gray-800 mb-2 flex items-center">
      <FaShieldAlt className="mr-2 text-indigo-600" />
      {type}
    </h4>
    <p className="text-sm text-gray-600">{description}</p>
  </div>
);

PlanType.propTypes = {
  type: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired
};

const ProviderCard = ({ provider }) => {
  const {
    name,
    description,
    rating,
    features = [],
    plan_types = [],
    links = {}
  } = provider;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <FaBuilding className="text-2xl text-indigo-600 mr-3" />
          <div>
            <h3 className="text-xl font-semibold text-gray-900">{name}</h3>
            <div className="flex items-center mt-1">
              {Array.from({ length: Math.floor(rating) }).map((_, index) => (
                <span key={index} className="text-yellow-400">★</span>
              ))}
              <span className="text-sm text-gray-600 ml-2">({rating} / 5)</span>
            </div>
          </div>
        </div>
        {links.quote && (
          <a
            href={links.quote}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Get Quote
            <FaExternalLinkAlt className="ml-2 h-4 w-4" />
          </a>
        )}
      </div>

      <p className="text-gray-600 mb-4">{description}</p>

      <div className="space-y-4">
        {plan_types.map((plan, index) => (
          <PlanType key={index} {...plan} />
        ))}
      </div>

      <div className="mt-4">
        <h4 className="text-sm font-semibold text-gray-800 mb-3">Key Features</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {features.map((feature, index) => (
            <PlanFeature key={index} feature={feature} />
          ))}
        </div>
      </div>

      {links.details && (
        <div className="mt-6">
          <a
            href={links.details}
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-600 hover:text-indigo-800 flex items-center"
          >
            Learn More
            <FaExternalLinkAlt className="ml-1 h-4 w-4" />
          </a>
        </div>
      )}
    </motion.div>
  );
};

ProviderCard.propTypes = {
  provider: PropTypes.shape({
    name: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    rating: PropTypes.number.isRequired,
    features: PropTypes.arrayOf(PropTypes.string),
    plan_types: PropTypes.arrayOf(PropTypes.shape({
      type: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired
    })),
    links: PropTypes.shape({
      quote: PropTypes.string,
      details: PropTypes.string
    })
  }).isRequired
};

export default ProviderCard; 