from fastapi import FastAPI, HTTPException
import joblib
import shap
import pandas as pd

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

@app.get("/forecast/explanation/{horizon}")
def forecast_explanation(horizon: int):
    modelling = create_live_dataset(
        session_elexon = session_elexon,
        session_open_meteo = session_open_meteo
    )

    n_horizon = modelling[modelling["horizon"] == horizon].copy()

    X, _ = split_features(
        splits = n_horizon
    )

    try:
        prediction = model.predict(X)[0]
    except Exception as e:
        raise RuntimeError(
            "Model prediction failed."
        ) from e

    preprocessor = model.named_steps["preprocessor"]
    xgb_model = model.named_steps["model"]
    X_transformed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()

    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer(X_transformed)

    feature_effects = pd.DataFrame({
        "feature": feature_names,
        "shap_value": shap_values.values[0]
    })

    feature_effects["abs_shap"] = feature_effects["shap_value"].abs()
    feature_effects = feature_effects.sort_values(
        "abs_shap", 
        ascending = False
    ).head(10)

    n_horizon["target_time"] = pd.to_datetime(
        n_horizon["target_time"], 
        utc = True
    ).dt.tz_localize(None)

    target_time = n_horizon["target_time"].iloc[0]
    base_shap_value = shap_values.base_values[0]

    features = feature_effects[["feature", "shap_value"]].to_dict(
        orient = "records"
    )

    to_return = {
        "horizon": horizon,
        "target_time": target_time,
        "prediction": float(prediction),
        "base_shap_value": float(base_shap_value),
        "features": features
    }

    return to_return



if __name__ == "__main__":
    print(generate_forecast())