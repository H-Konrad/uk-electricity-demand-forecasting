from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import TimeSeriesSplit

def split_dataset(dataset, train_size, validation_size):
    dataset = dataset.sort_values(["reference_time", "horizon"])
    reference_times = dataset["reference_time"].drop_duplicates().sort_values().reset_index(drop = True)
    reference_total = len(reference_times)

    train_end = int(reference_total * train_size)
    validation_end = int(reference_total * (train_size + validation_size))

    train_times = reference_times.iloc[:train_end]
    validation_times = reference_times.iloc[train_end:validation_end]
    test_times = reference_times.iloc[validation_end:]

    train_split = dataset[dataset["reference_time"].isin(train_times)].copy()
    validation_split = dataset[dataset["reference_time"].isin(validation_times)].copy()
    test_split = dataset[dataset["reference_time"].isin(test_times)].copy()

    return (
        train_split.reset_index(drop = True), 
        validation_split.reset_index(drop = True), 
        test_split.reset_index(drop = True)
    )

def split_features(splits):
    X_split = splits.drop(columns = [
        "reference_time",
        "target_time",
        "target_demand"
    ])

    y_split = splits["target_demand"]

    return X_split, y_split

def create_preprocessor(X_split):
    categorical_columns = ["season"]
    boolean_columns = ["is_weekend"]
    numeric_columns = [
        column for column in X_split.columns
        if column not in (categorical_columns + boolean_columns)
    ]

    preprocessor = ColumnTransformer(
        transformers = [
            (
                "numeric",
                StandardScaler(),
                numeric_columns
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown = "ignore"
                ),
                categorical_columns
            ),
            (
                "boolean",
                "passthrough",
                boolean_columns
            )
        ]
    )

    return preprocessor

def create_cv(splits, n_splits):
    splits = splits.sort_values(["reference_time", "horizon"])
    reference_times = splits["reference_time"].drop_duplicates().sort_values().reset_index(drop = True)
    time_split = TimeSeriesSplit(n_splits = n_splits)

    cv = []

    for train_index, validation_index in time_split.split(reference_times):
        train_times = reference_times.iloc[train_index]
        validation_times = reference_times.iloc[validation_index]

        train_rows = splits.index[splits["reference_time"].isin(train_times)].to_numpy()
        validation_rows = splits.index[splits["reference_time"].isin(validation_times)].to_numpy()

        cv.append((train_rows, validation_rows))

    return cv 