import argparse

from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

import requests
from preprocessing_data.preprocess_input_data import preprocess_dataframe
import json 
import os

with open('preprocessing_data/city_coords.json', 'r') as f:
    cities_coords = json.load(f)

URL = 'http://10.10.67.145:5010/api/test'
headers = {'Content-type': 'application/json'}


def save_figures(serie_with_segment: pd.Series, report_path: str):
    """функция по созданию и сохранению графиков распределения в колонке

    Args:
        serie_with_segment (pd.Series, optional): серия для которой создать график распределения. Defaults to df['Segment'].
    """
    data = serie_with_segment.value_counts().reset_index()

    plt.figure(figsize=(10, 7))

    plt.bar(data['index'], data['Segment'])

    plt.title('Расппределение сегментов')
    plt.xlabel('Сегмент')
    plt.ylabel('Кол-во пользователей')
    
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    plt.savefig(f'{report_path}/segment_distribution.png')

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('Predict segments')
    parser.add_argument('--csv_input', '-ci', help='название csv для предсказывания сегментов')
    parser.add_argument('--csv_output', '-co', help='название csv с предсказанными сегментами')
    parser.add_argument('--path_for_reports', '-pfr', help='путь до папки, в которую сохранять отчеты')
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    csv_input_path = Path(args.csv_input)
    csv_output_path = Path(args.csv_output)
    reports_path = args.path_for_reports

    if (str(args.csv_input).endswith('.gz')) or (str(args.csv_input).endswith('.gzip')):
        df = pd.read_csv(csv_input_path)
    else:
        df = pd.read_csv(csv_input_path)
    df_for_predicts = preprocess_dataframe(df, cities_coords)

    r = requests.post(URL, data=json.dumps(df_for_predicts.to_dict()), headers=headers)

    df['Segment'] = eval(r.json()['predicts'])
    
    save_figures(df['Segment'], reports_path)
    df.to_csv(csv_output_path, index=False)

