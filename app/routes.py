from .model import get_catboost_model
from .preprocess_input_data import preprocess_dataframe
from flask import request, render_template
import numpy as np
from app import app

model_path = 'classification_model/catboost_model.cbm'
model = get_catboost_model(model_path)

@app.route('/api/test', methods=['POST'])
def test():
    # r = request
    response = {
        'message' : 'alls fine'
                }

    return response
