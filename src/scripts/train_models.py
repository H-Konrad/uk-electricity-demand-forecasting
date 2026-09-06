import pandas as pd
import joblib

from src.training.baselines import get_baseline_predictions
from src.training.evaluation import evaluate_baseline, evaluate_models
from src.training.models import load_random_forest, load_ridge, load_xgboost
from src.training.trainer import ModelTrainer
from src.training.data import (
    split_dataset, split_features, create_preprocessor, create_cv
)

data_path = "data/dataset/modelling_dataset.parquet"
save_path = "data/results/training_results.parquet"

def main():
    dataset = pd.read_parquet(data_path)

    train_split, validation_split, _ = split_dataset(
        dataset = dataset,
        train_size = 0.7,
        validation_size = 0.15
    )

    cv = create_cv(
        splits = train_split,
        n_splits = 2
    )

    X_train, y_train = split_features(
        splits = train_split
    )

    X_validation, y_validation = split_features(
        splits = validation_split
    )

    preprocessor = create_preprocessor(
        X_split = X_train
    )

    models = {
        "ridge": {
            "model": load_ridge(
                preprocessor = preprocessor
            ),
            "params": {
                "model__alpha": [0.001, 0.01, 0.1, 1, 10, 100]
            }
        },
        "random_forest": {
            "model": load_random_forest(
                preprocessor = preprocessor
            ),
            "params": {
                "model__n_estimators": [100, 200, 400, 600],
                "model__max_depth": [4, 8, 12, 16],
                "model__max_features": ["sqrt", 0.25, 0.5, 0.75]
            }
        },
        "xgboost": {
            "model": load_xgboost(
                preprocessor = preprocessor
            ),
            "params": {
                "model__n_estimators": [100, 200, 400, 600],
                "model__max_depth": [3, 6, 9, 12],
                "model__learning_rate": [0.01, 0.05, 0.1, 0.2]
            }
        }
    }

    results = []
    for model_name, model_setup in models.items():
        model_class = ModelTrainer(model = model_setup["model"])
        print("TRAINING")
        model_class.train(
            X_train = X_train,
            y_train = y_train
        )

        initial_metrics = evaluate_models(
            model = model_class.best_model,
            X_test = X_validation,
            y_test = y_validation
        )

        results.append({
            "model": model_name,
            "version": "initial",
            "mae": initial_metrics["mae"],
            "rmse": initial_metrics["rmse"]
        })

        print(f"MAE: {initial_metrics["mae"]:.2f} ||||| RMSE: {initial_metrics["rmse"]:.2f}")

        joblib.dump(
            value = model_class.best_model,
            filename = f"models/initial_{model_name}.joblib"
        )

        print("OPTIMISE")

        model_class.optimise(
            X_train = X_train,
            y_train = y_train,
            params = model_setup["params"],
            scoring = "neg_mean_absolute_error",
            cv = cv,
            n_iter = 3
        )

        optimised_metrics = evaluate_models(
            model = model_class.best_model,
            X_test = X_validation,
            y_test = y_validation
        )

        results.append({
            "model": model_name,
            "version": "optimised",
            "mae": optimised_metrics["mae"],
            "rmse": optimised_metrics["rmse"]
        })

        print(f"BEST PARAMETERS\n{model_class.best_params}")
        print(f"MAE: {optimised_metrics["mae"]:.2f} ||||| RMSE: {optimised_metrics["rmse"]:.2f}")

        joblib.dump(
            value = model_class.best_model,
            filename = f"models/optimised_{model_name}.joblib"
        )

        print()

    model_results_df = pd.DataFrame(results)

    baseline_predictions = get_baseline_predictions(dataset)
    baseline_columns = [
        "baseline_30m",
        "baseline_24h",
        "baseline_7d",
    ]

    results = []
    for baseline in baseline_columns:
        results.append(evaluate_baseline(baseline_predictions, baseline))

    baseline_results_df = pd.DataFrame(results)

    print("BASELINE METRICS")
    print(baseline_results_df)

    results_to_save = pd.concat(
        [model_results_df, baseline_results_df],
        ignore_index = True
    )

    results_to_save.to_parquet(
        path = save_path, 
        index = False, 
        engine = "pyarrow"
    )

if __name__ == "__main__":
    main()