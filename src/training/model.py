from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def load_ridge():
    return Ridge()

def load_random_forest():
    return RandomForestRegressor(
        random_state = 42,
        n_jobs = -1
    )

def load_xgboost():
    return XGBRegressor(
        random_state = 42,
        n_jobs = -1
    )