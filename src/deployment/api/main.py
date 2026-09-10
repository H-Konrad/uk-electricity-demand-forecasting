from fastapi import FastAPI, HTTPException
import joblib

from src.deployment.live.features import create_live_dataset
from src.utils.sessions import elexon_session, weather_data_session
from src.training.data import split_features

model_path = "models/optimised_xgboost.joblib"

model_info_dict = {
    "model": "XGBoost",
    "mae": 1280,
    "rmse": 1721,
    "forecast_horizons": 48,
    "forecast_window_hours": 24
}

app = FastAPI()

model = joblib.load(
    filename = model_path
)

session_elexon = elexon_session()
session_open_meteo = weather_data_session()

def generate_forecast():
    modelling = create_live_dataset(
        session_elexon = session_elexon,
        session_open_meteo = session_open_meteo
    )

    X, _ = split_features(
        splits = modelling
    )

    try:
        predictions = model.predict(X)
    except Exception as e:
        raise RuntimeError(
            "Model prediction failed."
        ) from e

    forecast = modelling[[
        "reference_time",
        "target_time",
        "horizon"
    ]].copy()

    forecast["predicted_demand"] = predictions

    return forecast

@app.get("/forecast")
def forecast():
    try:
        forecast_df = generate_forecast()

        return forecast_df.to_dict(
            orient = "records"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code = 503,
            detail = str(e)
        )

@app.get("/model-info")
def model_info():
    return model_info_dict


if __name__ == "__main__":
    print(generate_forecast())