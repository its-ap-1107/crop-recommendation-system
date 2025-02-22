import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

const insuranceService = {
    analyzeHealth: async (userData) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/api/analyze`, userData);
            return response.data;
        } catch (error) {
            console.error('Error analyzing health data:', error);
            throw error;
        }
    },

    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    },

    getRiskLevelColor: (level) => {
        switch (level.toLowerCase()) {
            case 'low':
                return 'success';
            case 'moderate':
                return 'warning';
            case 'high':
                return 'error';
            default:
                return 'info';
        }
    },

    processAnalysisResults: (data) => {
        return {
            riskAssessment: {
                level: data.risk_assessment.risk_level,
                score: data.risk_assessment.risk_score * 100,
                confidence: data.risk_assessment.risk_confidence,
                factors: {
                    risk: data.risk_assessment.risk_factors,
                    positive: data.risk_assessment.positive_factors
                },
                probabilities: data.risk_assessment.risk_probabilities
            },
            recommendations: {
                planType: data.recommendations.recommended_plan_type,
                plans: data.recommendations.matching_plans.map(plan => ({
                    ...plan,
                    formattedPremium: {
                        min: insuranceService.formatCurrency(plan.premium_range.min),
                        max: insuranceService.formatCurrency(plan.premium_range.max)
                    }
                })),
                justification: data.recommendations.justification
            },
            aiAnalysis: data.ai_analysis
        };
    },

    async getAssessments() {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/assessments`);
            return response.data;
        } catch (error) {
            console.error('Error fetching assessments:', error);
            throw error;
        }
    },

    async getAssessment(assessmentId) {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/assessment/${assessmentId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching assessment:', error);
            throw error;
        }
    }
};

export default insuranceService; 