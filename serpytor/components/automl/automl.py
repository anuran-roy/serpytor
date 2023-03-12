from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, f1_score, mean_squared_error,
                             r2_score)
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


def get_best_model(
    features_df,
    labels_df,
    test_size=0.3,
    random_state=42,
    model_type: str = "classification",
    optimize_for: str = "balanced",
    get_all_models=False,
):
    """Get the best performing model for the given features and labels.
    Models are chosen from one of the following scikit-learn models:
    - For classification:
        - DecisionTreeClassifier
        - RandomForestClassifier
        - SupportVectorClassifier (or SVC)

    - For regression:
        - DecisionTreeRegressor
        - RandomForestRegressor
        - SupportVectorRegressor (or SVR)

    Important Flags:
        get_all_models (default: False): When turned on, returns all the models alongwith their metrics.
        **WARNING**: Can cause the function to slow down considerably.

    Example usage:

    ```python
    from serpytor.components.automl import get_best_model
    from sklearn.datasets import load_iris

    data = load_iris()
    features = data.data
    labels = data.target

    model = get_best_model(features, labels, test_size=0.3, model_type="classification")
    ```
    """

    model_glossary = {
        "classification": [DecisionTreeClassifier, RandomForestClassifier, SVC],
        "regression": [DecisionTreeRegressor, RandomForestRegressor, SVR],
    }

    X_train, X_test, Y_train, Y_test = train_test_split(
        features_df, labels_df, test_size=test_size, random_state=random_state
    )

    models = [model() for model in model_glossary[model_type]]

    for model_ in models:
        model = model_
        model.fit(X_train, Y_train)

    scores = {}
    Y_pred = model.predict(X_test)
    if model_type == "classification":
        scores = {
            model.__str__(): {
                "model": model,
                "scores": (
                    accuracy_score(Y_test, Y_pred),
                    f1_score(Y_test, Y_pred, average="micro"),
                ),
            }
            for model in models
        }
    elif model_type == "regression":
        scores = {
            model.__str__(): {
                "model": model,
                "scores": (
                    mean_squared_error(Y_test, Y_pred),
                    r2_score(Y_test, Y_pred),
                ),
            }
            for model in models
        }

    if optimize_for == "accuracy":
        return (
            (
                max(scores.items(), key=lambda x: x[1]["scores"][0]),
                scores.items(),
            )
            if get_all_models
            else max(scores.items(), key=lambda x: x[1]["scores"][0])
        )
    elif optimize_for == "balanced":
        return (
            (
                max(scores.items(), key=lambda x: x[1]["scores"][1]),
                scores.items(),
            )
            if get_all_models
            else max(scores.items(), key=lambda x: x[1]["scores"][1])
        )
