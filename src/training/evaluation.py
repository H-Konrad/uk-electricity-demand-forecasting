from sklearn.metrics import mean_absolute_error, root_mean_squared_error

def evaluate_baseline(df, prediction_column):
    mae = mean_absolute_error(
        y_true = df["target_demand"],
        y_pred = df[prediction_column]
    )

    rmse = root_mean_squared_error(
        y_true = df["target_demand"],
        y_pred = df[prediction_column]
    )

    return {
        "model": prediction_column,
        "mae": mae,
        "rmse": rmse
    }