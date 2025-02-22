import { motion } from 'framer-motion';
import { Button } from './Button';
import { Input } from './Input';
import { Select } from './Select';
import PropTypes from 'prop-types';

const FormField = ({ label, children, hint }) => (
  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
    <label className="block text-sm font-semibold text-gray-700">{label}</label>
    {children}
    {hint && <p className="text-xs text-gray-500">{hint}</p>}
  </motion.div>
);

FormField.propTypes = {
  label: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  hint: PropTypes.string
};

const FAMILY_HISTORY_OPTIONS = [
  { value: 'none', label: 'No history of conditions' },
  { value: 'heart_disease', label: 'Heart Disease' },
  { value: 'diabetes', label: 'Diabetes' },
  { value: 'cancer', label: 'Cancer' },
  { value: 'asthma', label: 'Asthma' },
  { value: 'hypertension', label: 'Hypertension' },
  { value: 'stroke', label: 'Stroke' },
  { value: 'fatty_liver', label: 'Fatty Liver Disease' },
  { value: 'thyroid', label: 'Thyroid Disorders' },
  { value: 'arthritis', label: 'Arthritis' },
  { value: 'obesity', label: 'Obesity' }
];

const HealthForm = ({ userData, setUserData, onSubmit, loading, error }) => {
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <FormField label="Age">
          <Input
            type="number"
            value={userData.age}
            onChange={(e) => setUserData({...userData, age: e.target.value})}
            required
            className="w-full"
            placeholder="Enter your age"
          />
        </FormField>
        
        <FormField label="Gender">
          <Select
            value={userData.gender}
            onChange={(e) => setUserData({...userData, gender: e.target.value})}
            className="w-full"
          >
            <option value="M">Male</option>
            <option value="F">Female</option>
            <option value="O">Other</option>
            <option value="P">Prefer not to say</option>
          </Select>
        </FormField>
        
        <FormField label="BMI" hint="Body Mass Index">
          <Input
            type="number"
            step="0.1"
            value={userData.bmi}
            onChange={(e) => setUserData({...userData, bmi: e.target.value})}
            required
            className="w-full"
            placeholder="Enter your BMI"
          />
        </FormField>

        <FormField label="Blood Pressure" hint="Systolic blood pressure in mmHg">
          <Input
            type="number"
            value={userData.blood_pressure}
            onChange={(e) => setUserData({...userData, blood_pressure: e.target.value})}
            required
            className="w-full"
            placeholder="Systolic BP (e.g., 120)"
          />
        </FormField>

        <FormField label="Cholesterol" hint="Total cholesterol in mg/dL">
          <Input
            type="number"
            value={userData.cholesterol}
            onChange={(e) => setUserData({...userData, cholesterol: e.target.value})}
            required
            className="w-full"
            placeholder="Total cholesterol"
          />
        </FormField>

        <FormField label="Smoker">
          <Select
            value={userData.smoker}
            onChange={(e) => setUserData({...userData, smoker: e.target.value})}
            className="w-full"
          >
            <option value="no">No</option>
            <option value="yes">Yes</option>
            <option value="former">Former Smoker</option>
            <option value="occasional">Occasional Smoker</option>
          </Select>
        </FormField>

        <FormField label="Exercise Frequency">
          <Select
            value={userData.exercise_frequency}
            onChange={(e) => setUserData({...userData, exercise_frequency: e.target.value})}
            className="w-full"
          >
            <option value="sedentary">Sedentary (No exercise)</option>
            <option value="low">Low (0-1 days/week)</option>
            <option value="medium">Medium (2-4 days/week)</option>
            <option value="high">High (5+ days/week)</option>
            <option value="athlete">Professional Athlete</option>
          </Select>
        </FormField>

        <FormField label="Family History" hint="Select the most severe condition">
          <Select
            value={userData.family_history}
            onChange={(e) => setUserData({...userData, family_history: e.target.value})}
            className="w-full"
          >
            {FAMILY_HISTORY_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </Select>
        </FormField>
      </div>

      <motion.div
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <Button 
          type="submit" 
          className="w-full max-w-md mx-auto py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-md flex items-center justify-center"
          disabled={loading}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Analyzing...
            </div>
          ) : (
            'Get Insurance Recommendation'
          )}
        </Button>
      </motion.div>
    </form>
  );
};

HealthForm.propTypes = {
  userData: PropTypes.shape({
    age: PropTypes.string.isRequired,
    gender: PropTypes.string.isRequired,
    bmi: PropTypes.string.isRequired,
    blood_pressure: PropTypes.string.isRequired,
    cholesterol: PropTypes.string.isRequired,
    smoker: PropTypes.string.isRequired,
    exercise_frequency: PropTypes.string.isRequired,
    family_history: PropTypes.string.isRequired
  }).isRequired,
  setUserData: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.string
};

export default HealthForm;