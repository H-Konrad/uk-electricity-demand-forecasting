from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def split_dataset(dataset, train_size, validation_size):
    dataset = dataset.sort_values(["reference_time", "horizon"])
    reference_times = dataset["reference_time"].drop_duplicates().sort_values()
    reference_total = len(reference_times)

    train_end = int(reference_total * train_size)
    validation_end = int(reference_total * (train_size + validation_size))

    train_times = reference_times.iloc[:train_end]
    validation_times = reference_times.iloc[train_end:validation_end]
    test_times = reference_times.iloc[validation_end:]

    train_split = dataset[dataset["reference_time"].isin(train_times)].copy()
    validation_split = dataset[dataset["reference_time"].isin(validation_times)].copy()
    test_split = dataset[dataset["reference_time"].isin(test_times)].copy()

    return train_split, validation_split, test_split

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
                    handle_unknown = "ingore"
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