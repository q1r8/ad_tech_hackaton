from .model import get_catboost_model
from flask import request, render_template
import numpy as np
from app import app
import pandas as pd

model_path = 'classification_model/catboost_model_best.cbm'
model = get_catboost_model(model_path)


@app.route('/api/test', methods=['POST'])
def test():
    
    r = request.data.decode()
    data = pd.DataFrame(eval(r))

    predicts = model.predict(data)
    predicts = [elem[0] for elem in predicts]

    response = {
        'message' : 'alls fine',
        'predicts': str(predicts)
        }

    return response
