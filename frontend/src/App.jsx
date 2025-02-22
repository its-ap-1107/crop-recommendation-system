import { useState, useEffect } from 'react'
import { Button } from './components/Button'
import { Input } from './components/Input'
import { Select } from './components/Select'
import { Card } from './components/Card'
import { Tabs, TabPanel } from './components/Tabs'
import { FaHeartbeat, FaRunning, FaUserMd, FaHistory, FaChartLine, FaShieldAlt, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa'
import { motion } from 'framer-motion'

function App() {
  const [userData, setUserData] = useState({
    age: '',
    gender: 'M',
    bmi: '',
    blood_pressure: '',
    cholesterol: '',
    smoker: 'no',
    exercise_frequency: 'medium',
    family_history: 'no',
    previous_conditions: 'none'
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [assessments, setAssessments] = useState([])
  const [selectedAssessment, setSelectedAssessment] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAssessments()
  }, [])

  const fetchAssessments = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/assessments`)
      const data = await response.json()
      setAssessments(data)
    } catch (error) {
      setError('Failed to fetch assessments. Please try again later.')
      console.error('Error fetching assessments:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })
      
      const data = await response.json()
      if (data.error) {
        throw new Error(data.error)
      }
      setResult(data)
      fetchAssessments()
    } catch (error) {
      setError(error.message || 'Failed to analyze. Please try again.')
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const viewAssessment = async (id) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/assessment/${id}`)
      const data = await response.json()
      setSelectedAssessment(data)
    } catch (error) {
      setError('Failed to fetch assessment details.')
      console.error('Error fetching assessment:', error)
    }
  }

  const getRiskColor = (score) => {
    if (score < 0.3) return 'bg-green-500'
    if (score < 0.6) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-indigo-900 mb-2">
          AI Sure
        </h1>
          <p className="text-gray-600 text-lg">
            Get personalized insurance recommendations based on your health profile
          </p>
        </motion.div>
        
        <Tabs defaultTab="new" className="bg-white rounded-xl shadow-lg">
          <TabPanel value="new" label="New Assessment" icon={<FaUserMd />}>
            <Card className="p-8">
              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                  {error}
                </div>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Age</label>
                    <Input
                      type="number"
                      value={userData.age}
                      onChange={(e) => setUserData({...userData, age: e.target.value})}
                      required
                      className="w-full"
                      placeholder="Enter your age"
                    />
                  </motion.div>
                  
                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Gender</label>
                    <Select
                      value={userData.gender}
                      onChange={(e) => setUserData({...userData, gender: e.target.value})}
                      className="w-full"
                    >
                      <option value="M">Male</option>
                      <option value="F">Female</option>
                    </Select>
                  </motion.div>
                  
                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">BMI</label>
                    <Input
                      type="number"
                      step="0.1"
                      value={userData.bmi}
                      onChange={(e) => setUserData({...userData, bmi: e.target.value})}
                      required
                      className="w-full"
                      placeholder="Enter your BMI"
                    />
                    <p className="text-xs text-gray-500">Body Mass Index</p>
                  </motion.div>

                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Blood Pressure</label>
                    <Input
                      type="number"
                      value={userData.blood_pressure}
                      onChange={(e) => setUserData({...userData, blood_pressure: e.target.value})}
                      required
                      className="w-full"
                      placeholder="Systolic BP (e.g., 120)"
                    />
                    <p className="text-xs text-gray-500">Systolic blood pressure in mmHg</p>
                  </motion.div>

                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Cholesterol</label>
                    <Input
                      type="number"
                      value={userData.cholesterol}
                      onChange={(e) => setUserData({...userData, cholesterol: e.target.value})}
                      required
                      className="w-full"
                      placeholder="Total cholesterol"
                    />
                    <p className="text-xs text-gray-500">Total cholesterol in mg/dL</p>
                  </motion.div>

                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Smoker</label>
                    <Select
                      value={userData.smoker}
                      onChange={(e) => setUserData({...userData, smoker: e.target.value})}
                      className="w-full"
                    >
                      <option value="no">No</option>
                      <option value="yes">Yes</option>
                    </Select>
                  </motion.div>

                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Exercise Frequency</label>
                    <Select
                      value={userData.exercise_frequency}
                      onChange={(e) => setUserData({...userData, exercise_frequency: e.target.value})}
                      className="w-full"
                    >
                      <option value="low">Low (0-1 days/week)</option>
                      <option value="medium">Medium (2-4 days/week)</option>
                      <option value="high">High (5+ days/week)</option>
                    </Select>
                  </motion.div>

                  <motion.div whileHover={{ scale: 1.02 }} className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700">Family History</label>
                    <Select
                      value={userData.family_history}
                      onChange={(e) => setUserData({...userData, family_history: e.target.value})}
                      className="w-full"
                    >
                      <option value="no">No history of conditions</option>
                      <option value="yes">Has family history</option>
                    </Select>
                  </motion.div>
                </div>

                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                <Button 
                  type="submit" 
                    className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-md"
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
            </Card>

            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <Card className="mt-8 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Insurance Recommendation</h2>
                  <div className="space-y-8">
                  <div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                        <FaChartLine className="mr-2" />
                        Risk Assessment
                      </h3>
                      <div className="bg-gray-100 p-6 rounded-lg">
                        <div className="flex items-center mb-2">
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <motion.div 
                              className={`h-3 rounded-full ${getRiskColor(result.risk_score)}`}
                              initial={{ width: 0 }}
                              animate={{ width: `${(result.risk_score * 100).toFixed(1)}%` }}
                              transition={{ duration: 1 }}
                            />
                          </div>
                          <span className="ml-4 font-semibold text-lg">
                            {(result.risk_score * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="flex justify-between text-sm text-gray-600">
                          <span>Low Risk</span>
                          <span>Moderate Risk</span>
                          <span>High Risk</span>
                        </div>
                        {result.health_factors && result.health_factors.length > 0 && (
                          <div className="mt-4">
                            <p className="text-sm font-medium text-gray-700 mb-2">Health Factors:</p>
                            <div className="flex flex-wrap gap-2">
                              {result.health_factors.map((factor, index) => (
                                <span
                                  key={index}
                                  className="px-3 py-1 bg-white rounded-full text-sm text-gray-700 border border-gray-200"
                                >
                                  {factor}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                  </div>
                  
                    {result.providers && result.providers.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                          <FaShieldAlt className="mr-2" />
                          Recommended Insurance Providers
                        </h3>
                        <div className="space-y-4">
                          {result.providers.map((provider, index) => (
                            <motion.div
                              key={index}
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ delay: index * 0.1 }}
                              className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all"
                            >
                              <div className="flex justify-between items-start mb-4">
                  <div>
                                  <h4 className="text-xl font-semibold text-indigo-700">{provider.name}</h4>
                                  <div className="flex items-center mt-1">
                                    <div className="flex items-center">
                                      <span className="text-sm font-medium text-gray-600">Match Score:</span>
                                      <span className="ml-2 text-sm font-semibold text-indigo-600">{provider.match_score}%</span>
                                    </div>
                                    <span className="mx-2 text-gray-300">|</span>
                                    <div className="flex items-center">
                                      <span className="text-sm font-medium text-gray-600">Recommended Plan:</span>
                                      <span className={`ml-2 text-sm font-semibold ${
                                        provider.recommended_plan === 'Premium' ? 'text-purple-600' :
                                        provider.recommended_plan === 'Standard' ? 'text-blue-600' :
                                        'text-green-600'
                                      }`}>
                                        {provider.recommended_plan}
                                      </span>
                                    </div>
                                  </div>
                                </div>
                                <div className="flex items-center">
                                  <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-lg text-sm font-medium hover:bg-indigo-100 transition-colors"
                                  >
                                    View Details
                                  </motion.button>
                                </div>
                  </div>
                  
                              {provider.features && provider.features.length > 0 && (
                                <div className="mt-4">
                                  <h5 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                                    <FaCheckCircle className="mr-2 text-green-500" />
                                    Key Features
                                  </h5>
                                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                    {provider.features.map((feature, idx) => (
                                      <li key={idx} className="flex items-start">
                                        <span className="inline-block w-1.5 h-1.5 rounded-full bg-indigo-400 mt-2 mr-2"></span>
                                        <span className="text-sm text-gray-600">{feature}</span>
                                      </li>
                      ))}
                    </ul>
                                </div>
                              )}

                              {provider.coverage_options && provider.coverage_options.length > 0 && (
                                <div className="mt-4">
                                  <h5 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                                    <FaExclamationTriangle className="mr-2 text-yellow-500" />
                                    Coverage Options
                                  </h5>
                                  <div className="space-y-2">
                                    {provider.coverage_options.map((option, idx) => (
                                      <div key={idx} className="bg-gray-50 p-3 rounded-lg">
                                        <p className="text-sm font-medium text-gray-700">{option.title}</p>
                                        <p className="text-sm text-gray-600 mt-1">{option.description}</p>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </motion.div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                        <FaHeartbeat className="mr-2" />
                        AI Recommendation
                      </h3>
                      <div className="bg-white border border-gray-200 rounded-lg p-6 prose max-w-none">
                        <p className="whitespace-pre-line text-gray-700">{result.recommendation}</p>
                      </div>
                    </div>
                    
                    {result.search_results && result.search_results.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                          <FaRunning className="mr-2" />
                          Relevant Resources
                        </h3>
                        <div className="grid gap-4 md:grid-cols-2">
                          {result.search_results.map((resource, index) => (
                            <motion.div
                              key={index}
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
                          ))}
                        </div>
                      </div>
                    )}
                </div>
              </Card>
              </motion.div>
            )}
          </TabPanel>
          
          <TabPanel value="history" label="Assessment History" icon={<FaHistory />}>
            <Card className="p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Previous Assessments</h2>
              <div className="space-y-4">
                {assessments.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">No previous assessments found.</p>
                ) : (
                  assessments.map((assessment) => (
                    <motion.div
                    key={assessment._id}
                      whileHover={{ scale: 1.02 }}
                      className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
                    onClick={() => viewAssessment(assessment._id)}
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
                  ))
                )}
              </div>
            </Card>

            {selectedAssessment && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <Card className="mt-8 p-8">
                  <div className="flex justify-between items-start mb-8">
                    <h2 className="text-2xl font-bold text-gray-900">Assessment Details</h2>
                    <p className="text-sm text-gray-500">
                      {new Date(selectedAssessment.timestamp).toLocaleString()}
                    </p>
                  </div>
                  
                  <div className="space-y-8">
                  <div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-4">Health Profile</h3>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm text-gray-600">Age</p>
                          <p className="text-lg font-semibold">{selectedAssessment.user_data.age}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm text-gray-600">Gender</p>
                          <p className="text-lg font-semibold">{selectedAssessment.user_data.gender}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm text-gray-600">BMI</p>
                          <p className="text-lg font-semibold">{selectedAssessment.user_data.bmi}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm text-gray-600">Blood Pressure</p>
                          <p className="text-lg font-semibold">{selectedAssessment.user_data.blood_pressure}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm text-gray-600">Cholesterol</p>
                          <p className="text-lg font-semibold">{selectedAssessment.user_data.cholesterol}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm text-gray-600">Exercise</p>
                          <p className="text-lg font-semibold">{selectedAssessment.user_data.exercise_frequency}</p>
                        </div>
                      </div>
                  </div>
                  
                  <div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-4">Risk Assessment</h3>
                      <div className="bg-gray-100 p-6 rounded-lg">
                        <div className="flex items-center mb-2">
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <motion.div 
                              className={`h-3 rounded-full ${getRiskColor(selectedAssessment.risk_score)}`}
                              initial={{ width: 0 }}
                              animate={{ width: `${(selectedAssessment.risk_score * 100).toFixed(1)}%` }}
                              transition={{ duration: 1 }}
                            />
                          </div>
                          <span className="ml-4 font-semibold text-lg">
                            {(selectedAssessment.risk_score * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    {selectedAssessment.recommendation && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Recommendation</h3>
                        <div className="bg-white border border-gray-200 rounded-lg p-6 prose max-w-none">
                          <p className="whitespace-pre-line text-gray-700">{selectedAssessment.recommendation}</p>
                        </div>
                      </div>
                    )}
                    
                    {selectedAssessment.search_results && selectedAssessment.search_results.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Relevant Resources</h3>
                        <div className="grid gap-4 md:grid-cols-2">
                          {selectedAssessment.search_results.map((resource, index) => (
                            <motion.div
                              key={index}
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
                          ))}
                        </div>
                      </div>
                    )}
                </div>
              </Card>
              </motion.div>
            )}
          </TabPanel>
        </Tabs>
      </div>
    </div>
  )
}

export default App
