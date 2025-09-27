# main.py
import uvicorn
import pandas as pd
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Obesity Level Prediction API",
    description="API for predicting obesity levels based on lifestyle and habits using a trained XGBoost model."
)

# --- Load the trained model and label encoder ---
try:
    with open('xgboost_model.pkl', 'rb') as model_file:
        model_pipeline = pickle.load(model_file)
    with open('label_encoder.pkl', 'rb') as le_file:
        label_encoder = pickle.load(le_file)
except FileNotFoundError as e:
    raise RuntimeError(f"Required file not found: {e}.")
except Exception as e:
    raise RuntimeError(f"Error loading model or label encoder: {e}")

# --- Input Data Schema ---
class ObesityPredictionInput(BaseModel):
    Gender: str
    Age: float
    Height: float
    Weight: float
    family_history_with_overweight: str
    FAVC: str
    FCVC: float
    NCP: float
    CAEC: str
    SMOKE: str
    CH2O: float
    SCC: str
    FAF: float
    TUE: float
    CALC: str
    MTRANS: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Obesity Level Prediction API!"}

@app.post("/predict_obesity")
async def predict_obesity(input_data: ObesityPredictionInput):
    try:
        input_df = pd.DataFrame([input_data.dict()])

        # Normalize categorical inputs
        categorical_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC',
                            'SMOKE', 'SCC', 'CALC', 'MTRANS']
        for col in categorical_cols:
            input_df[col] = input_df[col].str.lower().str.strip()

        prediction_encoded = model_pipeline.predict(input_df)[0]
        predicted_label = label_encoder.inverse_transform([prediction_encoded])[0]

        return {
            "prediction": predicted_label,
            "input_data": input_data.dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)