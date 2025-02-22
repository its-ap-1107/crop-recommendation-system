import { useState, useEffect } from 'react'
import { Card } from './components/Card'
import { Tabs, TabPanel } from './components/Tabs'
import { FaUserMd, FaHistory } from 'react-icons/fa'
import { motion } from 'framer-motion'
import RiskAssessment from './components/RiskAssessment'
import ProviderCard from './components/ProviderCard'
import Header from './components/Header'
import HealthForm from './components/HealthForm'
import AssessmentHistory from './components/AssessmentHistory'
import AssessmentDetails from './components/AssessmentDetails'

function App() {
  const [userData, setUserData] = useState({
    age: '',
    gender: 'M',
    bmi: '',
    blood_pressure: '',
    cholesterol: '',
    smoker: 'no',
    exercise_frequency: 'medium',
    family_history: 'none'
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Header />
        
        <Tabs defaultTab="new" className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <TabPanel 
            value="new" 
            label="New Assessment" 
            icon={<FaUserMd className="text-indigo-600" />}
            className="p-6 sm:p-8"
          >
            <Card className="bg-white rounded-xl shadow-sm p-6 sm:p-8">
              <HealthForm
                userData={userData}
                setUserData={setUserData}
                onSubmit={handleSubmit}
                loading={loading}
                error={error}
              />
            </Card>

            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="mt-8 space-y-8"
              >
                <RiskAssessment data={result} />

                {result.providers && result.providers.length > 0 && (
                  <div className="space-y-6">
                    <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                      <span className="gradient-bg text-white p-2 rounded-lg mr-3">
                        <FaUserMd className="h-6 w-6" />
                      </span>
                      Recommended Insurance Providers
                    </h2>
                    <div className="grid gap-6">
                      {result.providers.map((provider, index) => (
                        <ProviderCard key={index} provider={provider} />
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </TabPanel>
          
          <TabPanel 
            value="history" 
            label="Assessment History" 
            icon={<FaHistory className="text-indigo-600" />}
            className="p-6 sm:p-8"
          >
            <Card className="bg-white rounded-xl shadow-sm p-6 sm:p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <span className="gradient-bg text-white p-2 rounded-lg mr-3">
                  <FaHistory className="h-6 w-6" />
                </span>
                Previous Assessments
              </h2>
              <AssessmentHistory
                assessments={assessments}
                onViewAssessment={viewAssessment}
              />
            </Card>

            {selectedAssessment && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <Card className="mt-8 bg-white rounded-xl shadow-sm p-6 sm:p-8">
                  <div className="flex justify-between items-start mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                      <span className="gradient-bg text-white p-2 rounded-lg mr-3">
                        <FaUserMd className="h-6 w-6" />
                      </span>
                      Assessment Details
                    </h2>
                    <p className="text-sm text-gray-500">
                      {new Date(selectedAssessment.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <AssessmentDetails assessment={selectedAssessment} />
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
