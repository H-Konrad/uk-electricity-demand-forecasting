from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.base import clone

def model_pipeline(model, preprocessor):
    pipeline = Pipeline([
        (
            "preprocessor",
            clone(preprocessor)
        ),
        (
            "model",
            model
        )
    ])

    return pipeline

def load_ridge(preprocessor):
    model = Ridge()
    return model_pipeline(model, preprocessor)

def load_random_forest(preprocessor):
    model = RandomForestRegressor(
        n_estimators = 200,
        max_depth = 10,
        random_state = 42,
        n_jobs = -1
    )
    return model_pipeline(model, preprocessor)

def load_xgboost(preprocessor):
    model = XGBRegressor(
        n_estimators = 200,
        max_depth = 6,
        learning_rate = 0.05,
        device = "cuda",
        tree_method = "hist",
        random_state = 42
    )
    return model_pipeline(model, preprocessor)