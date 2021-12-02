import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
# from dash import dash_table
import requests
import json

import pandas as pd
import plotly.express as px

import base64
import io

from preprocessing_data.preprocess_input_data import preprocess_dataframe

with open('./dash/preprocessing_data/city_coords.json', 'r') as f:
    cities_coords = json.load(f)

URL = 'http://10.10.67.145:5010/api/test'
headers = {'Content-type': 'application/json'}

# df = pd.read_csv('asterank_exo.csv')

# fig = px.scatter(df, x='RPLANET', y='TPLANET')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Hello Dash!'),
    html.Div('Тестовый вывод графика'),
    # dcc.Graph(figure=fig)
])

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Перетащи сюда файл или ',
            html.A('выбери его')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Если юзер заливает CSV файл
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

            print('dataframe_is_processing')
            df = preprocess_dataframe(df, cities_coords, test_mode=True)

            r = requests.post(URL, data=json.dumps(df.to_dict()), headers=headers)
            df['Segment'] = eval(r.json()['predicts'])
            
        else:
            return html.Div([
                'Необходимо загрузить файл формата CSV.'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'Ошибка обработки файла!'
        ])

    return html.Div([
        html.H5('Имя файла: ' + filename),
        html.H5('Количество строк: ' + str(df.shape[0]))
        # А так же тут обновляем/выводим графики
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.run_server("0.0.0.0", 5011, debug=False)