from .model import get_catboost_model
from flask import request, render_template
import numpy as np
from app import app

model_path = 'classification_model/catboost_model.cbm'
model = get_catboost_model(model_path)

@app.route('/api/test', methods=['POST'])
def test():
    r = request.data.decode()
    print(r)
    response = {
        'message' : 'alls fine'
                }

    return response
