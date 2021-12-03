from .model import get_catboost_model
from flask import request, render_template
import numpy as np
from app import app
import pandas as pd
# from preprocessing_data.preprocess_input_data import preprocess_dataframe

# with open('./preprocessing_data/city_coords.json', 'r') as f:
#     cities_coords = json.load(f)

model_path = 'classification_model/catboost_model.cbm'
model = get_catboost_model(model_path)



@app.route('/api/test', methods=['POST'])
def test():
    render_template('index.html')
    r = request.data.decode()
    data = pd.DataFrame(eval(r))
    # data = preprocess_dataframe(data, cities_coords, test_mode=True)

    predicts = model.predict(data)
    predicts = [elem[0] for elem in predicts]

    response = {
        'message' : 'alls fine',
        'predicts': str(predicts)
        }

    return response
