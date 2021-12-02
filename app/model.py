from catboost import CatBoostClassifier


def get_catboost_model(path: str):
    model = CatBoostClassifier()
    model.load_model(path)

    return model