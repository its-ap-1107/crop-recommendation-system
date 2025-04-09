from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import os
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier  # Change to use sklearn's implementation

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get the absolute path to the app directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'app', 'models')

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize variables
model = None
scaler = None
crop_labels = None

# Load the trained model and scaler
def load_models():
    global model, scaler, crop_labels
    try:
        print("Current working directory:", os.getcwd())
        print("Models directory:", MODELS_DIR)
        
        model_path = os.path.join(MODELS_DIR, 'crop_model.joblib')
        print(f"Checking if file exists: {os.path.exists(model_path)}")
        
        # Load all components from single file
        components = joblib.load(model_path)
        model = components['model']
        scaler = components['scaler']
        crop_labels = components['labels']
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure you've run train_models.py first")
        return False

# Load models when starting the application
models_loaded = load_models()

class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.get("/")
def read_root():
    if not models_loaded:
        return {"message": "Warning: Models not loaded. Please train the models first."}
    return {"message": "Crop Recommendation API is running"}

@app.post("/predict")
async def predict_crop(data: CropInput):
    if not models_loaded:
        raise HTTPException(
            status_code=500, 
            detail="Models not loaded. Please train the models first by running train_models.py"
        )
    
    try:
        # Add print statements for debugging
        print("Received input data:", data)
        
        input_data = np.array([[
            data.N,
            data.P,
            data.K,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall
        ]])
        
        if not isinstance(scaler, StandardScaler):
            raise HTTPException(
                status_code=500,
                detail="Scaler not properly initialized"
            )
            
        # Scale the input data
        try:
            input_scaled = scaler.transform(input_data)
            print("Scaled input:", input_scaled)
        except Exception as e:
            print("Error in scaling:", str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Error scaling input data: {str(e)}"
            )
        
        # Make prediction
        try:
            prediction = model.predict(input_scaled)
            print("Prediction:", prediction)
        except Exception as e:
            print("Error in prediction:", str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Error making prediction: {str(e)}"
            )
        
        return {
            "recommended_crop": prediction[0]
        }
    except Exception as e:
        print("Error in prediction endpoint:", str(e))
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        ) 