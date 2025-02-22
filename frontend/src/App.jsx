import { useState, useEffect } from 'react'
import { Button } from './components/Button'
import { Input } from './components/Input'
import { Select } from './components/Select'
import { Card } from './components/Card'
import { Tabs, TabPanel } from './components/Tabs'

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

  useEffect(() => {
    // Fetch previous assessments when component mounts
    fetchAssessments()
  }, [])

  const fetchAssessments = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/assessments')
      const data = await response.json()
      setAssessments(data)
    } catch (error) {
      console.error('Error fetching assessments:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })
      
      const data = await response.json()
      setResult(data)
      // Refresh assessments list after new submission
      fetchAssessments()
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const viewAssessment = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/api/assessment/${id}`)
      const data = await response.json()
      setSelectedAssessment(data)
    } catch (error) {
      console.error('Error fetching assessment:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center">
          AI Health Insurance Assistant
        </h1>
        
        <Tabs defaultTab="new">
          <TabPanel value="new" label="New Assessment">
            <Card className="p-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block mb-2 font-medium">Age</label>
                    <Input
                      type="number"
                      value={userData.age}
                      onChange={(e) => setUserData({...userData, age: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block mb-2 font-medium">Gender</label>
                    <Select
                      value={userData.gender}
                      onChange={(e) => setUserData({...userData, gender: e.target.value})}
                    >
                      <option value="M">Male</option>
                      <option value="F">Female</option>
                    </Select>
                  </div>
                  
                  <div>
                    <label className="block mb-2 font-medium">BMI</label>
                    <Input
                      type="number"
                      step="0.1"
                      value={userData.bmi}
                      onChange={(e) => setUserData({...userData, bmi: e.target.value})}
                      required
                    />
                  </div>

                  <div>
                    <label className="block mb-2 font-medium">Blood Pressure</label>
                    <Input
                      type="number"
                      value={userData.blood_pressure}
                      onChange={(e) => setUserData({...userData, blood_pressure: e.target.value})}
                      required
                    />
                  </div>

                  <div>
                    <label className="block mb-2 font-medium">Cholesterol</label>
                    <Input
                      type="number"
                      value={userData.cholesterol}
                      onChange={(e) => setUserData({...userData, cholesterol: e.target.value})}
                      required
                    />
                  </div>

                  <div>
                    <label className="block mb-2 font-medium">Smoker</label>
                    <Select
                      value={userData.smoker}
                      onChange={(e) => setUserData({...userData, smoker: e.target.value})}
                    >
                      <option value="no">No</option>
                      <option value="yes">Yes</option>
                    </Select>
                  </div>

                  <div>
                    <label className="block mb-2 font-medium">Exercise Frequency</label>
                    <Select
                      value={userData.exercise_frequency}
                      onChange={(e) => setUserData({...userData, exercise_frequency: e.target.value})}
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </Select>
                  </div>

                  <div>
                    <label className="block mb-2 font-medium">Family History</label>
                    <Select
                      value={userData.family_history}
                      onChange={(e) => setUserData({...userData, family_history: e.target.value})}
                    >
                      <option value="no">No</option>
                      <option value="yes">Yes</option>
                    </Select>
                  </div>
                </div>

                <Button 
                  type="submit" 
                  className="w-full mt-6"
                  disabled={loading}
                >
                  {loading ? 'Analyzing...' : 'Get Insurance Recommendation'}
                </Button>
              </form>
            </Card>

            {result && (
              <Card className="mt-8 p-6">
                <h2 className="text-2xl font-semibold mb-4">Your Insurance Recommendation</h2>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium">Risk Score</h3>
                    <p className="text-lg">{(result.risk_score * 100).toFixed(1)}%</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium">Recommendation</h3>
                    <p className="whitespace-pre-line">{result.recommendation}</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium">Additional Information</h3>
                    <ul className="list-disc pl-5">
                      {result.relevant_info.map((info, index) => (
                        <li key={index}>{info.title}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            )}
          </TabPanel>
          
          <TabPanel value="history" label="Assessment History">
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">Previous Assessments</h2>
              <div className="space-y-4">
                {assessments.map((assessment) => (
                  <div 
                    key={assessment._id}
                    className="p-4 border rounded hover:bg-gray-50 cursor-pointer"
                    onClick={() => viewAssessment(assessment._id)}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">
                          Age: {assessment.user_data.age}, 
                          Risk Score: {(assessment.risk_score * 100).toFixed(1)}%
                        </p>
                        <p className="text-sm text-gray-500">
                          {new Date(assessment.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <Button variant="outline">
                        View Details
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {selectedAssessment && (
              <Card className="mt-8 p-6">
                <h2 className="text-2xl font-semibold mb-4">Assessment Details</h2>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium">Risk Score</h3>
                    <p className="text-lg">{(selectedAssessment.risk_score * 100).toFixed(1)}%</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium">Recommendation</h3>
                    <p className="whitespace-pre-line">{selectedAssessment.recommendation}</p>
                  </div>
                  
                  <div>
                    <h3 className="font-medium">Additional Information</h3>
                    <ul className="list-disc pl-5">
                      {selectedAssessment.relevant_info.map((info, index) => (
                        <li key={index}>{info.title}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            )}
          </TabPanel>
        </Tabs>
      </div>
    </div>
  )
}

export default App
