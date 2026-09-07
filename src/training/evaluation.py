from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_absolute_percentage_error

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
        "version": "baseline",
        "mae": mae,
        "rmse": rmse
    }

def evaluate_models(y_test, X_test = None, model = None, predictions = None, mape = False):
    if predictions is None:
        predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_true = y_test,
        y_pred = predictions
    )

    rmse = root_mean_squared_error(
        y_true = y_test,
        y_pred = predictions
    )

    if mape:
        value = mean_absolute_percentage_error(
            y_true = y_test,
            y_pred = predictions
        ) * 100

        return {
            "mae": mae,
            "rmse": rmse,
            "mape": value
        }

    return {
        "mae": mae,
        "rmse": rmse
    }