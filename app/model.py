from catboost import CatBoostClassifier


def get_catboost_model():
    model = CatBoostClassifier()
    model.load_model('./classification_model/catboost_model.cbm')

    return model