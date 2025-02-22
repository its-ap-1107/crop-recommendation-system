# AI-Sure

A modern web application that helps users assess their health insurance risks and find suitable insurance providers using machine learning and AI-powered recommendations.

## Project Overview

This project consists of two main components:
- A React-based frontend for user interaction and data visualization
- A Flask-based backend with ML models for risk assessment and insurance recommendations

### Key Features

- Health risk assessment based on user inputs
- AI-powered insurance provider recommendations
- Historical assessment tracking
- Detailed risk analysis and recommendations
- Interactive and responsive UI

## Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Framer Motion for animations
- React Icons

### Backend
- Flask
- MongoDB
- Machine Learning models for risk assessment
- Provider search service

## Project Structure

```
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── styles/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
└── backend/
    ├── app/
    │   ├── models/
    │   ├── services/
    │   └── app.py
    ├── train_models.py
    └── requirements.txt
```

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file with:
   ```
   VITE_API_URL=http://localhost:5000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with required configurations:
   ```
   MONGO_URI=your_mongodb_uri
   DB_NAME=insurance_platform
   CORS_ORIGINS=http://localhost:5173
   ```

5. Start the Flask server:
   ```bash
   python -m flask run
   ```

## API Endpoints

### POST `/api/analyze`
Analyzes user health data and provides insurance recommendations.

### GET `/api/assessments`
Retrieves the history of risk assessments.

### GET `/api/assessment/<assessment_id>`
Retrieves detailed information about a specific assessment.

## Features in Detail

### Risk Assessment
- Analyzes user health data including age, BMI, blood pressure, etc.
- Provides a risk score and risk level assessment
- Identifies positive and negative health factors

### Insurance Recommendations
- Suggests suitable insurance providers
- Provides premium range estimates
- Lists available coverage options and plan types

### Assessment History
- Tracks all previous assessments
- Allows users to review past results
- Provides detailed assessment information

