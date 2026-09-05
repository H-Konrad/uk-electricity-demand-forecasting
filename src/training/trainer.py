from sklearn.model_selection import GridSearchCV

class ModelTrainer:
    def __init__(self, model):
        self.model = model
        self.best_model = None
        self.best_params = None
        self.search = None

    def train(self, X_train, y_train):
        self.model.fit(
            X_train,
            y_train
        )

        self.best_model = self.model

    def optimise(self, X_train, y_train, params, scoring, cv):
        self.search = GridSearchCV(
            estimator = self.model,
            param_grid = params,
            scoring = scoring,
            cv = cv,
            n_jobs = -1
        )

        self.search.fit(
            X_train,
            y_train
        )

        self.best_model = self.search.best_estimator_
        self.best_params = self.search.best_params_