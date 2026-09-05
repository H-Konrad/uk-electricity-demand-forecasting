from sklearn.model_selection import RandomizedSearchCV

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

    def optimise(self, X_train, y_train, params, scoring, cv, n_iter):
        self.search = RandomizedSearchCV(
            estimator = self.model,
            param_distributions = params,
            n_iter = n_iter,
            scoring = scoring,
            cv = cv,
            n_jobs = -1,
            random_state = 42,
            verbose = 2
        )

        self.search.fit(
            X_train,
            y_train
        )

        self.best_model = self.search.best_estimator_
        self.best_params = self.search.best_params_